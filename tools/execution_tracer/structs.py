"""
S2E Selective Symbolic Execution Framework

Copyright (c) 2016, Dependable Systems Laboratory, EPFL
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Dependable Systems Laboratory, EPFL nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE DEPENDABLE SYSTEMS LABORATORY, EPFL BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import struct


class TraceEntryType(object):
    """
    The different types of trace entries that can be written to the log.
    """
    TRACE_MOD_LOAD = 0
    TRACE_MOD_UNLOAD = 1
    TRACE_PROC_UNLOAD = 2
    TRACE_CALL = 3
    TRACE_RET = 4
    TRACE_TB_START = 5
    TRACE_TB_END = 6
    TRACE_MODULE_DESC = 7
    TRACE_FORK = 8
    TRACE_CACHESIM = 9
    TRACE_TESTCASE = 10
    TRACE_BRANCHCOV = 11
    TRACE_MEMORY = 12
    TRACE_PAGEFAULT = 13
    TRACE_TLBMISS = 14
    TRACE_ICOUNT = 15
    TRACE_MEM_CHECKER = 16
    TRACE_EXCEPTION = 17
    TRACE_STATE_SWITCH = 18
    TRACE_TB_START_X64 = 19
    TRACE_TB_END_X64 = 20
    TRACE_BLOCK = 21
    TRACE_MAX = 22


class TraceEntry(object):
    """
    Abstract trace entry class.

    Defines how a particular trace entry is serialized to the log.
    """

    FORMAT = None

    def __init__(self, fmt=''):
        self._struct = struct.Struct(fmt)

    def __len__(self):
        return self._struct.size

    def serialize(self):
        raise NotImplementedError()

    def as_dict(self):
        raise NotImplementedError()

    @classmethod
    def static_size(cls):
        if cls.FORMAT:
            return struct.calcsize(cls.FORMAT)
        else:
            raise ValueError('Cannot statically determine the size of %s' % cls)


class TraceItemHeader(TraceEntry):
    """
    The header for a trace entry.
    """

    FORMAT = '<QIBIQ'

    def __init__(self, timestamp, size, type_, state_id, pid):
        super(TraceItemHeader, self).__init__(TraceItemHeader.FORMAT)
        self._timestamp = timestamp
        self._size = size
        self._type = type_
        self._state_id = state_id
        self._pid = pid

    def serialize(self):
        return self._struct.pack(self._timestamp,
                                 self._size,
                                 self._type,
                                 self._state_id,
                                 self._pid)

    def as_dict(self):
        return {
            'timestamp': self._timestamp,
            'size': self._size,
            'type': self._type,
            'stateId': self._state_id,
            'pid': self._pid,
        }

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def size(self):
        return self._size

    @property
    def type(self):
        return self._type

    @property
    def state_id(self):
        return self._state_id

    @property
    def pid(self):
        return self._pid


class TraceModuleLoad(TraceEntry):
    """
    Serialize a module load event.
    """

    FORMAT = '<32s256sQQQQQ'

    def __init__(self, name, path, load_base, native_base, size, address_space,
                 pid):
        super(TraceModuleLoad, self).__init__(TraceModuleLoad.FORMAT)
        self._name = name
        self._path = path
        self._load_base = load_base
        self._native_base = native_base
        self._size = size
        self._address_space = address_space
        self._pid = pid

    def serialize(self):
        return self._struct.pack(self._name,
                                 self._path,
                                 self._load_base,
                                 self._native_base,
                                 self._size,
                                 self._address_space,
                                 self._pid)

    def as_dict(self):
        return {
            'name': self.name,
            'path': self.path,
            'loadBase': self.load_base,
            'nativeBase': self.native_base,
            'size': self.size,
            'addressSpace': self.address_space,
            'pid': self.pid,
        }

    @property
    def name(self):
        return self._name.rstrip('\0')

    @property
    def path(self):
        return self._path.rstrip('\0')

    @property
    def load_base(self):
        return self._load_base

    @property
    def native_base(self):
        return self._native_base

    @property
    def size(self):
        return self._size

    @property
    def address_space(self):
        return self._address_space

    @property
    def pid(self):
        return self._pid


class TraceModuleUnload(TraceEntry):
    """
    Serialize a module unload event.
    """

    FORMAT = '<Q'

    def __init__(self, load_base):
        super(TraceModuleUnload, self).__init__(TraceModuleUnload.FORMAT)
        self._load_base = load_base

    def serialize(self):
        return self._struct.pack(self._load_base)

    def as_dict(self):
        return {
            'loadBase': self.load_base,
        }

    @property
    def load_base(self):
        return self._load_base


class TraceProcessUnload(TraceEntry):
    """
    Serialize a process unload event.
    """

    FORMAT = '<'

    def serialize(self):
        return ''

    def as_dict(self):
        return {}


class TraceCall(TraceEntry):
    """
    Serialize a function call event.
    """

    FORMAT = '<QQ'

    def __init__(self, source, target):
        super(TraceCall, self).__init__(TraceCall.FORMAT)
        self._source = source
        self._target = target

    def serialize(self):
        return self._struct.pack(self._source, self._target)

    def as_dict(self):
        return {
            'source': self.source,
            'target': self.target,
        }

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target


class TraceReturn(TraceEntry):
    """
    Serialize a function return event.
    """

    FORMAT = '<QQ'

    def __init__(self, source, target):
        super(TraceReturn, self).__init__(TraceReturn.FORMAT)
        self._source = source
        self._target = target

    def serialize(self):
        return self._struct.pack(self._source, self._target)

    def as_dict(self):
        return {
            'source': self.source,
            'target': self.target,
        }

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target


class TraceFork(TraceEntry):
    """
    Serialize a process fork event.
    """

    def __init__(self, pc, state_ids):
        super(TraceFork, self).__init__('QI%dI' % len(state_ids))
        self._pc = pc
        self._state_ids = state_ids

    def serialize(self):
        return self._struct.pack(self._pc,
                                 len(self._state_ids),
                                 *self._state_ids)

    def as_dict(self):
        return {
            'pc': self.pc,
            'stateIds': self.state_ids,
        }

    @property
    def pc(self):
        return self._pc

    @property
    def state_ids(self):
        return self._state_ids


class TraceBranchCoverage(TraceEntry):
    """
    Serialize a branch event.
    """

    FORMAT = '<QQ'

    def __init__(self, pc, dest_pc):
        super(TraceBranchCoverage, self).__init__(TraceBranchCoverage.FORMAT)
        self._pc = pc
        self._dest_pc = dest_pc

    def serialize(self):
        return self._struct.pack(self._pc, self._dest_pc)

    def as_dict(self):
        return {
            'pc': self.pc,
            'destPc': self.dest_pc,
        }

    @property
    def pc(self):
        return self._pc

    @property
    def dest_pc(self):
        return self._dest_pc


class TraceCacheSimType(object):
    """
    Types of cache events.
    """
    CACHE_PARAMS = 0
    CACHE_NAME = 1
    CACHE_ENTRY = 2


class TraceCacheSimParams(TraceEntry):
    FORMAT = '<BIIIII'

    def __init__(self, type_, cache_id, size, line_size, associativity,
                 upper_cache_id):
        super(TraceCacheSimParams, self).__init__(TraceCacheSimParams.FORMAT)
        self._type = type_
        self._cache_id = cache_id
        self._size = size
        self._line_size = line_size
        self._associativity = associativity
        self._upper_cache_id = upper_cache_id

    def serialize(self):
        return self._struct.pack(self._type,
                                 self._cache_id,
                                 self._size,
                                 self._line_size,
                                 self._associativity,
                                 self._upper_cache_id)

    def as_dict(self):
        return {
            'type': self.type,
            'cacheId': self.cache_id,
            'size': self.size,
            'lineSize': self.line_size,
            'associativity': self.associativity,
            'upperCacheId': self.upper_cache_id,
        }

    @property
    def type(self):
        return self._type

    @property
    def cache_id(self):
        return self._cache_id

    @property
    def size(self):
        return self._size

    @property
    def line_size(self):
        return self._line_size

    @property
    def associativity(self):
        return self._associativity

    @property
    def upper_cache_id(self):
        return self._upper_cache_id


class TraceCacheSimName(TraceEntry):
    FORMAT = '<BIIs'

    def __init__(self, type_, id_, length, name):
        super(TraceCacheSimName, self).__init__(TraceCacheSimName.FORMAT)
        self._type = type_
        self._id = id_
        self._length = length
        self._name = name

    def serialize(self):
        return self._struct.pack(self._type,
                                 self._id,
                                 self._length,
                                 self._name)

    def as_dict(self):
        return {
            'type': self.type,
            'id': self.id,
            'length': self.length,
            'name': self.name,
        }

    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

    @property
    def length(self):
        return self._length

    @property
    def name(self):
        return self._name


class TraceCacheSimEntry(TraceEntry):
    FORMAT = '<BBQQBBBB'

    def __init__(self, type_, cache_id, pc, address, size, is_write, is_code,
                 miss_count):
        super(TraceCacheSimEntry, self).__init__(TraceCacheSimEntry.FORMAT)
        self._type = type_
        self._cache_id = cache_id
        self._pc = pc
        self._address = address
        self._size = size
        self._is_write = is_write
        self._is_code = is_code
        self._miss_count = miss_count

    def serialize(self):
        return self._struct.pack(self._type,
                                 self._cache_id,
                                 self._pc,
                                 self._address,
                                 self._size,
                                 self._is_write,
                                 self._is_code,
                                 self._miss_count)

    def as_dict(self):
        return {
            'type': self.type,
            'cacheId': self.cache_id,
            'pc': self.pc,
            'address': self.address,
            'size': self.size,
            'isWrite': self.is_write,
            'isCode': self.is_code,
            'missCount': self.miss_count,
        }

    @property
    def type(self):
        return self._type

    @property
    def cache_id(self):
        return self._cache_id

    @property
    def pc(self):
        return self._pc

    @property
    def address(self):
        return self._address

    @property
    def size(self):
        return self._size

    @property
    def is_write(self):
        return self._is_write

    @property
    def is_code(self):
        return self._is_code

    @property
    def miss_count(self):
        return self._miss_count


class TraceMemChecker(TraceEntry):
    class Flags(object):
        GRANT = 1
        REVOKE = 2
        READ = 4
        WRITE = 8
        EXECUTE = 16
        RESOURCE = 32

    FORMAT = '<QIIIs'

    def __init__(self, start, size, flags, name):
        super(TraceMemChecker, self).__init__(TraceMemChecker.FORMAT)
        self._start = start
        self._size = size
        self._flags = flags
        self._name = name

    def serialize(self):
        return self._struct.pack(self._start,
                                 self._size,
                                 self._flags,
                                 len(self._name),
                                 self._name)

    def as_dict(self):
        return {
            'start': self.start,
            'size': self.size,
            'flags': self.flags,
            'name': self.name,
        }

    @property
    def start(self):
        return self._start

    @property
    def size(self):
        return self._size

    @property
    def flags(self):
        return self._flags

    @property
    def name(self):
        return self._name


class TraceTestCase(TraceEntry):
    # TODO
    pass


class TraceMemory(TraceEntry):
    """
    Serialize a memory access event.
    """

    FORMAT = '<QQQBBQQ'

    def __init__(self, pc, address, value, size, flags, host_address,
                 concrete_buffer):
        super(TraceMemory, self).__init__(TraceMemory.FORMAT)
        self._pc = pc
        self._address = address
        self._value = value
        self._size = size
        self._flags = flags
        self._host_address = host_address
        self._concrete_buffer = concrete_buffer

    def serialize(self):
        return self._struct.pack(self._pc,
                                 self._address,
                                 self._value,
                                 self._size,
                                 self._flags,
                                 self._host_address,
                                 self._concrete_buffer)

    def as_dict(self):
        return {
            'pc': self.pc,
            'address': self.address,
            'value': self.value,
            'size': self.size,
            'flags': self.flags,
            'hostAddress': self.host_address,
            'concreteBuffer': self.concrete_buffer,
        }

    @property
    def pc(self):
        return self._pc

    @property
    def address(self):
        return self._address

    @property
    def value(self):
        return self._value

    @property
    def size(self):
        return self._size

    @property
    def flags(self):
        return self._flags

    @property
    def host_address(self):
        return self._host_address

    @property
    def concrete_buffer(self):
        return self._concrete_buffer


class TracePageFault(TraceEntry):
    """
    Serialize a page fault event.
    """

    FORMAT = '<QQB'

    def __init__(self, pc, address, is_write):
        super(TracePageFault, self).__init__(TracePageFault.FORMAT)
        self._pc = pc
        self._address = address
        self._is_write = is_write

    def serialize(self):
        return self._struct.pack(self._pc, self._address, self._is_write)

    def as_dict(self):
        return {
            'pc': self.pc,
            'address': self.address,
            'isWrite': self.is_write,
        }

    @property
    def pc(self):
        return self._pc

    @property
    def address(self):
        return self._address

    @property
    def is_write(self):
        return self._is_write


class TraceTLBMiss(TraceEntry):
    """
    Serialize a TLB miss event.
    """

    FORMAT = '<QQB'

    def __init__(self, pc, address, is_write):
        super(TraceTLBMiss, self).__init__(TraceTLBMiss.FORMAT)
        self._pc = pc
        self._address = address
        self._is_write = is_write

    def serialize(self):
        return self._struct.pack(self._pc, self._address, self._is_write)

    def as_dict(self):
        return {
            'pc': self.pc,
            'address': self.address,
            'isWrite': self.is_write,
        }

    @property
    def pc(self):
        return self._pc

    @property
    def address(self):
        return self._address

    @property
    def is_write(self):
        return self._is_write


class TraceICount(TraceEntry):
    """
    Serialize an instruction count event.
    """

    FORMAT = '<Q'

    def __init__(self, count):
        super(TraceICount, self).__init__(TraceICount.FORMAT)
        self._count = count

    def serialize(self):
        return self._struct.pack(self._count)

    def as_dict(self):
        return {
            'count': self.count,
        }

    @property
    def count(self):
        return self._count


class TraceTranslationBlock(TraceEntry):
    """
    Serialize a translation block event.
    """
    class TranslationBlockType(object):
        TB_DEFAULT = 0
        TB_JMP = 1
        TB_JMP_IND = 2
        TB_COND_JMP = 3
        TB_COND_JMP_IND = 4
        TB_CALL = 5
        TB_CALL_IND = 6
        TB_REP = 7
        TB_RET = 8

    class X86Registers(object):
        EAX = 0
        ECX = 1
        EDX = 2
        EBX = 3
        ESP = 4
        EBP = 5
        ESI = 6
        EDI = 7

    FORMAT = '<QQIBB8Q'

    def __init__(self, pc, target_pc, size, tb_size, tb_type, symb_mask,
                 registers):
        super(TraceTranslationBlock, self).__init__(TraceTranslationBlock.FORMAT)
        self._pc = pc
        self._target_pc = target_pc
        self._size = size
        self._tb_size = tb_size
        self._tb_type = tb_type
        self._symb_mask = symb_mask
        self._registers = registers

    def serialize(self):
        return self._struct.pack(self._pc,
                                 self._target_pc,
                                 self._size,
                                 self._tb_type,
                                 self._symb_mask,
                                 *self._registers)

    def as_dict(self):
        return {
            'pc': self.pc,
            'targetPc': self.target_pc,
            'size': self.size,
            'tbSize': self.tb_size,
            'tbType': self.tb_type,
            'symbMask': self.symb_mask,
            'registers': self.registers,
        }

    @property
    def pc(self):
        return self._pc

    @property
    def target_pc(self):
        return self._target_pc

    @property
    def size(self):
        return self._size

    @property
    def tb_size(self):
        return self._tb_size

    @property
    def tb_type(self):
        return self._tb_type

    @property
    def symb_mask(self):
        return self._symb_mask

    @property
    def registers(self):
        return self._registers


class TraceBlock(TraceEntry):
    """
    Serialize a basic block event.
    """

    FORMAT = '<QQB'

    def __init__(self, start_pc, end_pc, tb_type):
        super(TraceBlock, self).__init__(TraceBlock.FORMAT)
        self._start_pc = start_pc
        self._end_pc = end_pc
        self._tb_type = tb_type

    def serialize(self):
        return self._struct.pack(self._start_pc, self._end_pc, self._tb_type)

    def as_dict(self):
        return {
            'startPc': self.start_pc,
            'endPc': self.end_pc,
            'tbType': self.tb_type,
        }

    @property
    def start_pc(self):
        return self._start_pc

    @property
    def end_pc(self):
        return self._end_pc

    @property
    def tb_type(self):
        return self._tb_type


class TraceTranslationBlock64(TraceEntry):
    """
    Serialize a 64-bit translation block event.
    """

    FORMAT = '<SB8Q'

    def __init__(self, base, symb_mask, extended_registers):
        super(TraceTranslationBlock64, self).__init__(TraceTranslationBlock64.FORMAT)
        self._base = base
        self._symb_mask = symb_mask
        self._extended_registers = extended_registers

    def serialize(self):
        return self._struct.pack(self._base.serialize(),
                                 self._symb_mask,
                                 *self._extended_registers)

    def as_dict(self):
        return {
            'base': self.base,
            'symbMask': self.symb_mask,
            'extendedRegisters': self.extended_registers,
        }

    @property
    def base(self):
        return self._base

    @property
    def symb_mask(self):
        return self._symb_mask

    @property
    def extended_registers(self):
        return self._extended_registers


class TraceException(TraceEntry):
    """
    Serialize an exception event.
    """

    FORMAT = '<QI'

    def __init__(self, pc, vector):
        super(TraceException, self).__init__(TraceException.FORMAT)
        self._pc = pc
        self._vector = vector

    def serialize(self):
        return self._struct.pack(self._pc, self._vector)

    def as_dict(self):
        return {
            'pc': self.pc,
            'vector': self.vector,
        }

    @property
    def pc(self):
        return self._pc

    @property
    def vector(self):
        return self._vector


class TraceStateSwitch(TraceEntry):
    """
    Serialize a state switch event.
    """

    FORMAT = '<I'

    def __init__(self, new_state_id):
        super(TraceStateSwitch, self).__init__(TraceStateSwitch.FORMAT)
        self._new_state_id = new_state_id

    def serialize(self):
        return self._struct.pack(self._new_state_id)

    def as_dict(self):
        return {
            'newStateId': self.new_state_id,
        }

    @property
    def new_state_id(self):
        return self._new_state_id
