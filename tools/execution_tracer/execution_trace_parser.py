#!/usr/bin/env python

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

from __future__ import print_function

"""
Parses an S2E binary execution trace file and outputs the result as
pretty-printed JSON.
"""

import argparse
import json
import struct

from structs import *


class S2ETraceParserException(Exception):
    pass


class S2ETraceParser(object):
    """Parses an S2E execution trace file."""

    ENTRY_CLASSES = {
        TraceEntryType.TRACE_MOD_LOAD: TraceModuleLoad,
        TraceEntryType.TRACE_MOD_UNLOAD: TraceModuleUnload,
        TraceEntryType.TRACE_PROC_UNLOAD: TraceProcessUnload,
        TraceEntryType.TRACE_CALL: TraceCall,
        TraceEntryType.TRACE_RET: TraceReturn,
        TraceEntryType.TRACE_TB_START: None,
        TraceEntryType.TRACE_TB_END: None,
        TraceEntryType.TRACE_MODULE_DESC: None,
        TraceEntryType.TRACE_FORK: TraceFork,
        TraceEntryType.TRACE_CACHESIM: None,
        TraceEntryType.TRACE_TESTCASE: TraceTestCase,
        TraceEntryType.TRACE_BRANCHCOV: TraceBranchCoverage,
        TraceEntryType.TRACE_MEMORY: TraceMemory,
        TraceEntryType.TRACE_PAGEFAULT: TracePageFault,
        TraceEntryType.TRACE_TLBMISS: TraceTLBMiss,
        TraceEntryType.TRACE_ICOUNT: TraceICount,
        TraceEntryType.TRACE_MEM_CHECKER: TraceMemChecker,
        TraceEntryType.TRACE_EXCEPTION: TraceException,
        TraceEntryType.TRACE_STATE_SWITCH: TraceStateSwitch,
        TraceEntryType.TRACE_TB_START_X64: None,
        TraceEntryType.TRACE_TB_END_X64: None,
        TraceEntryType.TRACE_BLOCK: TraceBlock,
    }

    def __init__(self, filename):
        """
        Creates a new S2E execution trace parser based on the given trace file.
        """
        self._file = open(filename, 'rb')

    def __del__(self):
        self._file.close()

    def read(self):
        """
        Parses the S2E binary execution trace file and returns a list of
        `(trace entry header, trace entry)` tuples.
        """
        results = []

        while True:
            raw_header = self._file.read(TraceItemHeader.static_size())

            # An empty header signifies EOF
            if not raw_header:
                break

            unpacked_header = struct.unpack(TraceItemHeader.FORMAT, raw_header)
            header = TraceItemHeader(*unpacked_header)

            # Determine what the next blob of data is from the header's type
            data_type = header.type
            entry_cls = S2ETraceParser.ENTRY_CLASSES.get(data_type)
            if not entry_cls:
                raise S2ETraceParserException('The header type %d does not '
                                              'have a corresponding entry '
                                              'class' % data_type)
            raw_data = self._file.read(header.size)
            if entry_cls.FORMAT is not None:
                # The struct format can be determined statically
                unpacked_data = struct.unpack(entry_cls.FORMAT, raw_data)
                data = entry_cls(*unpacked_data)
                results.append((header, data))
            else:
                # TODO The struct format needs to be determined dynamically
                pass

        return results

def _merge_dicts(a, b):
    """Merge two dictionaries."""
    c = a.copy()
    c.update(b)

    return c


def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description='Parse S2E execution trace '
                                                 'log files')
    parser.add_argument('log_file', metavar='FILE', action='store',
                        help='Path to log file')

    return parser.parse_args()
    

def main(argument):
    """The main function."""

    entry_classes = {
        TraceEntryType.TRACE_MOD_LOAD: 'moduleLoad',
        TraceEntryType.TRACE_MOD_UNLOAD: 'moduleUnload',
        TraceEntryType.TRACE_PROC_UNLOAD: 'processUnload',
        TraceEntryType.TRACE_CALL: 'call',
        TraceEntryType.TRACE_RET: 'return',
        TraceEntryType.TRACE_TB_START: '',
        TraceEntryType.TRACE_TB_END: '',
        TraceEntryType.TRACE_MODULE_DESC: '',
        TraceEntryType.TRACE_FORK: 'fork',
        TraceEntryType.TRACE_CACHESIM: '',
        TraceEntryType.TRACE_TESTCASE: 'testCase',
        TraceEntryType.TRACE_BRANCHCOV: 'branchCoverage',
        TraceEntryType.TRACE_MEMORY: 'memory',
        TraceEntryType.TRACE_PAGEFAULT: 'pageFault',
        TraceEntryType.TRACE_TLBMISS: 'tlbMiss',
        TraceEntryType.TRACE_ICOUNT: 'iCount',
        TraceEntryType.TRACE_MEM_CHECKER: 'memChecker',
        TraceEntryType.TRACE_EXCEPTION: 'exception',
        TraceEntryType.TRACE_STATE_SWITCH: 'stateSwitch',
        TraceEntryType.TRACE_TB_START_X64: '',
        TraceEntryType.TRACE_TB_END_X64: '',
        TraceEntryType.TRACE_BLOCK: 'block',
    }
    
    args = argparse.Namespace(log_file=argument)

    try:
        log_reader = S2ETraceParser(args.log_file)
        results = log_reader.read()
        json_results = [{entry_classes[h.type]: _merge_dicts(h.as_dict(), d.as_dict())} for h, d in results]

        return json_results
    except S2ETraceParserException as e:
        print('ERROR: %s' % e)


if __name__ == '__main__':
    main()
