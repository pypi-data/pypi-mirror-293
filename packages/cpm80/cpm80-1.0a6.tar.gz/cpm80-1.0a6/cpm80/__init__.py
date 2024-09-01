#!/usr/bin/env python3

import appdirs
import argparse
import importlib.resources
import pathlib
import sys
import termios
import tty
import z80

SECTOR_SIZE = 128


class Error(BaseException):
    pass


class DiskFormat(object):
    def __init__(self, *, sectors_per_track=40, num_reserved_tracks=0,
                 block_size=2048, num_blocks=400, num_dir_entries=128):
        def _div_ceil(a, b):
            return -(a // -b)

        if block_size not in (1024, 2048, 4096, 8192, 16384):
            raise Error(f'invalid block size ({block_size})')

        if block_size == 1024 and num_blocks > 0x100:
            raise Error('block size 1024 is not valid for disks with '
                        'more than 0x100 blocks')

        self.sectors_per_track = sectors_per_track
        self.num_reserved_tracks = num_reserved_tracks
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.num_dir_entries = num_dir_entries
        self.skew_factor = 0  # No translation.
        self.removable = True

        # CP/M Disk Parameter Block Fields.
        self.bls_block_size = self.block_size
        self.spt_sectors_per_track = self.sectors_per_track
        self.bsh_block_shift_factor = self.block_size.bit_length() - 8
        self.blm_allocation_block_mask = 2**self.bsh_block_shift_factor - 1
        self.dsm_disk_size_max = self.num_blocks - 1
        self.exm_extent_mask = (self.blm_allocation_block_mask >> 3
                                if self.dsm_disk_size_max < 0x100
                                else self.blm_allocation_block_mask >> 4)
        self.drm_max_dir_entry = self.num_dir_entries - 1
        self.cks_directory_check_size = (self.num_dir_entries // 4
                                         if self.removable else 0)
        self.off_system_tracks_offset = self.num_reserved_tracks

        DIR_ENTRY_SIZE = 32
        num_dir_blocks = _div_ceil(self.num_dir_entries * DIR_ENTRY_SIZE,
                                   self.block_size)
        dir_alloc_mask = (0xffff >> num_dir_blocks) ^ 0xffff
        self.al0_allocation_mask = (dir_alloc_mask >> 8) & 0xff
        self.al1_allocation_mask = (dir_alloc_mask >> 0) & 0xff

        num_reserved_blocks = _div_ceil((self.num_reserved_tracks *
                                         self.sectors_per_track * SECTOR_SIZE),
                                        self.block_size)
        total_num_blocks = num_reserved_blocks + self.num_blocks
        self.disk_size = total_num_blocks * self.block_size

    def translate_sector(self, logical_sector):
        # TODO: Support arbitrary skew factors.
        assert self.skew_factor == 0
        physical_sector = logical_sector
        return physical_sector


DISK_FORMATS = {
    'default': DiskFormat(),

    # Also used on Orion 128 machines. The number of blocks is
    # one less than it could be, likely due to a mistake, so the
    # last block is never used.
    'korvet': DiskFormat(num_reserved_tracks=4, num_blocks=389),
}


class DiskImage(object):
    def __init__(self, format=None):
        if format is None:
            format = DiskFormat()

        self.format = format

        size = format.disk_size
        self.data = bytearray(size)
        self.data[:] = b'\xe5' * size

    def get_sector(self, sector, track):
        sector_index = sector + track * self.format.spt_sectors_per_track
        offset = sector_index * SECTOR_SIZE
        return memoryview(self.data)[offset:offset + SECTOR_SIZE]

    def translate_sector(self, logical_sector):
        return self.format.translate_sector(logical_sector)


class DiskDrive(object):
    def __init__(self, image=None):
        if image is None:
            image = DiskImage()

        self.image = image
        self.current_sector = 0
        self.current_track = 0

    @property
    def format(self):
        return self.image.format

    def translate_sector(self, logical_sector):
        return self.image.translate_sector(logical_sector)

    def read_sector(self):
        sector = self.image.get_sector(self.current_sector, self.current_track)
        return bytes(sector)

    def write_sector(self, data):
        assert len(data) == SECTOR_SIZE
        sector = self.image.get_sector(self.current_sector, self.current_track)
        sector[:] = data


class KeyboardDevice(object):
    def __init__(self):
        self.__ctrl_c_count = 0

    def input(self):
        # Borrowed from:
        # https://stackoverflow.com/questions/510357/how-to-read-a-single-character-from-the-user
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = ord(sys.stdin.read(1))
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # Catch Ctrl+C.
        if ch == 3:
            self.__ctrl_c_count += 1
            if self.__ctrl_c_count >= 3:
                return None
        else:
            self.__ctrl_c_count = 0

        # Translate backspace.
        if ch == 127:
            ch = 8

        return ch


class StringKeyboard(object):
    def __init__(self, *commands):
        self.__input = '\n'.join(commands) + '\n'
        self.__i = 0

    def input(self):
        if self.__i >= len(self.__input):
            return None

        c = self.__input[self.__i]
        self.__i += 1
        return ord(c)


class DisplayDevice(object):
    def output(self, c):
        sys.stdout.write(chr(c))
        sys.stdout.flush()


class StringDisplay(object):
    def __init__(self):
        self.__output = []

    def output(self, c):
        self.__output.append(c)

    @property
    def string(self):
        return ''.join(chr(c) for c in self.__output)


class CPMMachineMixin(object):
    __REBOOT = 0x0000
    __DEFAULT_FCB = 0x005c
    __TPA = 0x0100

    BDOS_ENTRY = 0x0005
    C_WRITESTR = 9
    S_BDOSVER = 0xc
    F_OPEN = 0xf
    F_CLOSE = 0x10
    F_READ = 0x14
    F_WRITE = 0x15
    F_MAKE = 0x16
    F_RENAME = 0x17
    F_DMAOFF = 0x1a

    __CCP_BASE = 0x9400
    __CCP_READ_COMMAND = __CCP_BASE + 0x1aa
    __CCP_GET_COMMAND = __CCP_BASE + 0x385
    __CCP_RUN_COMMAND = __CCP_BASE + 0x398

    __BIOS_BASE = 0xaa00
    __BIOS_DISK_TABLES_HEAP_BASE = __BIOS_BASE + 0x80

    def __init__(self, *, drive=None, console_reader=None,
                 console_writer=None):
        self.__drive = drive or DiskDrive()
        self.__console_reader = console_reader or KeyboardDevice()
        self.__console_writer = console_writer or DisplayDevice()
        self.__done = False

        self.__breakpoints = {
            self.__CCP_READ_COMMAND: self.on_read_ccp_command,
            self.__CCP_GET_COMMAND: None,
            self.__CCP_RUN_COMMAND: self.on_ccp_command,
        }

        BIOS_VECTORS = (
            self.on_boot,
            self.on_wboot,
            self.on_const,
            self.on_conin,
            self.on_conout,
            self.on_list,
            self.on_punch,
            self.on_reader,
            self.on_home,
            self.on_seldsk,
            self.on_settrk,
            self.on_setsec,
            self.on_setdma,
            self.on_read,
            self.on_write,
            self.on_listst,
            self.on_sectran)

        self.__bios_vectors = {}
        for i, handler in enumerate(BIOS_VECTORS):
            addr = self.__BIOS_BASE + i * 3

            assert addr not in self.__bios_vectors
            self.__bios_vectors[addr] = handler

            assert addr not in self.__breakpoints
            self.__breakpoints[addr] = handler

        for addr in self.__breakpoints:
            self.set_breakpoint(addr)

        self.__ccp_command_line = None

        self.on_boot()

    def __allocate_disk_table_block(self, image):
        addr = self.__disk_tables_heap
        self.__disk_tables_heap += len(image)
        self.set_memory_block(addr, image)
        return addr

    def __set_up_disk_tables(self):
        f = self.__drive.format

        # Shared by all identical drives.
        dpb_disk_param_block = self.__allocate_disk_table_block(
            f.spt_sectors_per_track.to_bytes(2, 'little') +
            f.bsh_block_shift_factor.to_bytes(1, 'little') +
            f.blm_allocation_block_mask.to_bytes(1, 'little') +
            f.exm_extent_mask.to_bytes(1, 'little') +
            f.dsm_disk_size_max.to_bytes(2, 'little') +
            f.drm_max_dir_entry.to_bytes(2, 'little') +
            f.al0_allocation_mask.to_bytes(1, 'little') +
            f.al1_allocation_mask.to_bytes(1, 'little') +
            f.cks_directory_check_size.to_bytes(2, 'little') +
            f.off_system_tracks_offset.to_bytes(2, 'little'))

        # Shared by all drives.
        dirbuf_scratch_pad = self.__allocate_disk_table_block(b'\x00' * 128)

        xlt_sector_translation_vector = 0x0000
        bdos_scratch_pad1 = 0x0000
        bdos_scratch_pad2 = 0x0000
        bdos_scratch_pad3 = 0x0000
        cks = (f.drm_max_dir_entry + 1) // 4 if f.removable else 0
        csv_scratch_pad = self.__allocate_disk_table_block(b'\x00' * cks)
        alv_scratch_pad = self.__allocate_disk_table_block(
            b'\x00' * (f.dsm_disk_size_max // 8 + 1))

        self.__disk_header_table = self.__allocate_disk_table_block(
            xlt_sector_translation_vector.to_bytes(2, 'little') +
            bdos_scratch_pad1.to_bytes(2, 'little') +
            bdos_scratch_pad2.to_bytes(2, 'little') +
            bdos_scratch_pad3.to_bytes(2, 'little') +
            dirbuf_scratch_pad.to_bytes(2, 'little') +
            dpb_disk_param_block.to_bytes(2, 'little') +
            csv_scratch_pad.to_bytes(2, 'little') +
            alv_scratch_pad.to_bytes(2, 'little'))

    @staticmethod
    def __load_data(path):
        return importlib.resources.files('cpm80').joinpath(path).read_bytes()

    def on_boot(self):
        BDOS_BASE = 0x9c00
        self.set_memory_block(BDOS_BASE, self.__load_data('bdos.bin'))

        JMP = b'\xc3'
        JMP_BIOS = JMP + self.__BIOS_BASE.to_bytes(2, 'little')
        self.set_memory_block(self.__REBOOT, JMP_BIOS)

        for addr in self.__bios_vectors:
            RET = b'\xc9'
            self.set_memory_block(addr, RET)

        self.__disk_tables_heap = self.__BIOS_DISK_TABLES_HEAP_BASE
        self.__set_up_disk_tables()

        self.sp = 0x100

        self.__dma_addr = 0x80

        BDOS_ENTRY = BDOS_BASE + 0x11
        JMP_BDOS = JMP + BDOS_ENTRY.to_bytes(2, 'little')
        self.set_memory_block(self.BDOS_ENTRY, JMP_BDOS)

        CURRENT_DISK = 0
        CURRENT_DISK_ADDR = 0x0004
        self.set_memory_block(CURRENT_DISK_ADDR,
                              CURRENT_DISK.to_bytes(1, 'little'))

        self.c = CURRENT_DISK
        self.on_wboot()

    def on_wboot(self):
        self.set_memory_block(self.__CCP_BASE, self.__load_data('ccp.bin'))
        self.pc = self.__CCP_BASE

    def on_const(self):
        # TODO
        self.a = 0

    def on_conin(self):
        c = self.__console_reader.input()
        if c is None:
            self.__done = True
            return

        self.a = c

    def on_conout(self):
        self.__console_writer.output(self.c)

    def on_list(self):
        assert 0  # TODO

    def on_punch(self):
        assert 0  # TODO

    def on_reader(self):
        assert 0  # TODO

    def on_home(self):
        self.__drive.current_track = 0

    def on_seldsk(self):
        DISK_A = 0
        if self.c == DISK_A:
            self.hl = self.__disk_header_table
            return

        self.hl = 0

    def on_settrk(self):
        self.__drive.current_track = self.bc

    def on_setsec(self):
        self.__drive.current_sector = self.bc

    def on_setdma(self):
        self.__dma = self.bc

    def on_read(self):
        self.set_memory_block(self.__dma, self.__drive.read_sector())
        self.a = 0  # Read OK.

    def on_write(self):
        data = self.memory[self.__dma:self.__dma + SECTOR_SIZE]
        self.__drive.write_sector(data)
        self.a = 0  # Write OK.

    def on_listst(self):
        assert 0  # TODO

    def on_sectran(self):
        self.hl = self.__drive.translate_sector(self.bc)

    def on_breakpoint(self):
        handler = self.__breakpoints.get(self.pc)
        if handler:
            handler()

    # TODO: Should be implemented in the CPU package.
    def __push(self, nn):
        self.sp = (self.sp - 1) & 0xffff
        self.memory[self.sp] = (nn >> 8) & 0xff
        self.sp = (self.sp - 1) & 0xffff
        self.memory[self.sp] = (nn >> 0) & 0xff

    def __reach_ccp_command_processing(self):
        while self.pc != self.__CCP_GET_COMMAND:
            events = super().run()
            if events & self._BREAKPOINT_HIT:
                self.on_breakpoint()

    def bdos_call(self, entry, *, de=None):
        # Make sure CCP got control and initialised the system.
        self.__reach_ccp_command_processing()

        self.c = entry
        if de is not None:
            self.de = de
        self.__push(self.__CCP_GET_COMMAND)
        self.pc = self.BDOS_ENTRY

        # Execute the call.
        self.__reach_ccp_command_processing()

    def write_str(self, s, *, addr=None):
        if addr is None:
            addr = self.__TPA
        s = s.encode('ascii') + b'$'
        self.set_memory_block(addr, s)
        self.bdos_call(self.C_WRITESTR, de=addr)

    def get_bdos_version(self):
        self.bdos_call(self.S_BDOSVER)
        system_type = self.b
        cpm_version = self.a

        cpm_type = (system_type >> 0) & 0xf
        machine_type = (system_type >> 4) & 0xf

        return cpm_version, cpm_type, machine_type

    def __make_fcb(self, filename):
        filename, type = filename.split('.', maxsplit=1)

        DEFAULT_DRIVE = 0
        drive = DEFAULT_DRIVE

        filename = filename.upper().encode('ascii')
        filename += b' ' * (8 - len(filename))
        assert len(filename) == 8

        type = type.upper().encode('ascii')
        type += b' ' * (3 - len(type))
        assert len(type) == 3

        extent = 0

        s1_reserved = b'\x00'
        s2_reserved = b'\x00'

        rc_record_count = 0
        d_reserved = b'\x00' * 16
        cr_current_record = 0

        r0 = b'\x00'
        r1 = b'\x00'
        r2 = b'\x00'

        return (drive.to_bytes(1, 'little') +
                filename +
                type +
                extent.to_bytes(1, 'little') +
                s1_reserved +
                s2_reserved +
                rc_record_count.to_bytes(1, 'little') +
                d_reserved +
                cr_current_record.to_bytes(1, 'little') +
                r0 + r1 + r2)

    # TODO: Support custom FCB addresses, explicit drive
    # specification, file attributes, etc.
    # TODO: Seems to support wildcards?
    def open_file(self, filename):
        FCB = self.__DEFAULT_FCB
        self.set_memory_block(FCB, self.__make_fcb(filename))

        self.bdos_call(self.F_OPEN, de=FCB)

        dir_code = self.a
        if dir_code == 0xff:
            raise Error(f'cannot open file: F_OPEN returned {dir_code}: '
                        'file not found')

        return dir_code

    # TODO: Support custom FCB addresses.
    def close_file(self):
        self.bdos_call(self.F_CLOSE, de=self.__DEFAULT_FCB)
        dir_code = self.a
        if dir_code == 0xff:
            # TODO: The filename cannot be found in the directory.
            assert 0

        return dir_code

    # TODO: Support custom FCB and DMA addresses.
    def read_file(self, num_sectors=1):
        DMA = self.__TPA
        self.set_dma(DMA)

        sectors = []
        while len(sectors) < num_sectors:
            self.bdos_call(self.F_READ, de=self.__DEFAULT_FCB)

            if self.a != 0:
                break

            sectors.append(self.memory[DMA:DMA + SECTOR_SIZE])

        return b''.join(sectors)

    # TODO: Support custom FCB and DMA addresses.
    def write_file(self, data):
        DMA = self.__TPA
        self.set_dma(DMA)

        while data:
            chunk = data[0:128]
            data = data[128:]

            chunk += b'\x1a' * (SECTOR_SIZE - len(chunk))
            self.set_memory_block(DMA, chunk)

            self.bdos_call(self.F_WRITE, de=self.__DEFAULT_FCB)
            if self.a != 0:
                raise Error(f'cannot write file: F_WRITE returned {self.a}')

    # TODO: Support custom FCB addresses, explicit drive
    # specification, file attributes, etc.
    # TODO: Throw cpm80 exceptions on problematic input.
    # TODO: Prohibit wildcards.
    # TODO: Delete existing files before creating new ones.
    def make_file(self, filename):
        FCB = self.__DEFAULT_FCB
        self.set_memory_block(FCB, self.__make_fcb(filename))

        # TODO: Before calling this, make sure the file doesn't exist.
        self.bdos_call(self.F_MAKE, de=FCB)

        dir_code = self.a
        if dir_code == 0xff:
            # TODO: No more directory space is available.
            assert 0

        return dir_code

    # TODO: Support custom FCB addresses, explicit drive
    # specification, file attributes, etc.
    # TODO: Prohibit wildcards?
    def rename_file(self, old, new):
        FCB = self.__DEFAULT_FCB
        self.set_memory_block(FCB, (self.__make_fcb(old)[:16] +
                                    self.__make_fcb(new)[:16]))

        self.bdos_call(self.F_RENAME, de=FCB)

        dir_code = self.a
        if dir_code == 0xff:
            raise Error(f'cannot open file: F_RENAME returned {dir_code}: '
                        'file not found')

        return dir_code

    def set_dma(self, dma):
        self.bdos_call(self.F_DMAOFF, de=dma)

    def on_read_ccp_command(self):
        assert self.pc == self.__CCP_READ_COMMAND

        COMMAND_SIZE_ADDR = self.__CCP_BASE + 7
        size = self.memory[COMMAND_SIZE_ADDR]

        COMMAND_BUFF = COMMAND_SIZE_ADDR + 1
        b = bytes(self.memory[COMMAND_BUFF:COMMAND_BUFF + size])
        self.__ccp_command_line = b.decode('ascii')

    def on_ccp_command(self):
        assert self.pc == self.__CCP_RUN_COMMAND
        command, *args = self.__ccp_command_line.split()
        if command == 'exit':
            self.__done = True

    def run(self):
        while not self.__done:
            events = super().run()
            if events & self._BREAKPOINT_HIT:
                self.on_breakpoint()


class I8080CPMMachine(CPMMachineMixin, z80.I8080Machine):
    def __init__(self, *, drive=None, console_reader=None,
                 console_writer=None):
        z80.I8080Machine.__init__(self)
        CPMMachineMixin.__init__(self, drive=drive,
                                 console_reader=console_reader,
                                 console_writer=console_writer)


def main(args=None):
    parser = argparse.ArgumentParser(description='CP/M-80 2.2 emulator.')
    parser.add_argument('--temp-disk', action='store_true',
                        help='do not load the default disk image')
    parser.add_argument('commands', metavar='command', type=str, nargs='*',
                        help='A CP/M or internal emulator command to execute.')
    args = parser.parse_args(args)

    console_reader = None
    if args.commands is not None:
        console_reader = StringKeyboard(*args.commands)

    app_dirs = appdirs.AppDirs('cpm80')
    data_dir = pathlib.Path(app_dirs.user_data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    disk_path = data_dir / 'disk.img'
    image = DiskImage()
    if not args.temp_disk:
        try:
            image.data[:] = disk_path.read_bytes()
        except FileNotFoundError:
            pass

    drive = DiskDrive(image)

    try:
        m = I8080CPMMachine(drive=drive, console_reader=console_reader)
        m.run()
    except Error as e:
        sys.exit(f'cpm80: {e}')

    if not args.temp_disk:
        disk_path.write_bytes(image.data)


if __name__ == '__main__':
    main()
