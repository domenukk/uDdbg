from tabulate import tabulate
from unicorn import *

import utils
from modules.unicorndbgmodule import AbstractUnicornDbgModule


class Mappings(AbstractUnicornDbgModule):
    def __init__(self, core_instance):
        AbstractUnicornDbgModule.__init__(self, core_instance)
        self.mappings = []
        self.context_name = "mappings_module"
        self.command_map = {
            'map': {
                'help': 'Mappings',
                'usage': 'map [list|add|remove] [...]',
                'sub_commands': {
                    'l': {
                        'ref': "list",
                    },
                    'm': {
                        'ref': "map",
                    },
                    'u': {
                        'ref': "unmap",
                    },
                    'list': {
                        'short': 'l',
                        'usage': 'list',
                        'help': 'List mappings',
                        'function': {
                            "context": "mappings_module",
                            "f": "list"
                        }
                    },
                    'map': {
                        'usage': 'map [address] [length]',
                        'help': 'Map *length at *address',
                        'function': {
                            "context": "mappings_module",
                            "f": "add"
                        }
                    },
                    'unmap': {
                        'usage': 'unmap [address] [length]',
                        'help': 'Unmap *length at *address',
                        'function': {
                            "context": "mappings_module",
                            "f": "remove"
                        }
                    }
                }
            }
        }

    def list(self, func_name, *args):
        h = [utils.green_bold('PATH'),
             utils.green_bold('ADDRESS'),
             utils.green_bold('LENGTH')]
        print(tabulate(self.mappings, h, tablefmt="rst"))

    def map(self, func_name, *args):
        off = utils.input_to_offset(args[0])
        lent = utils.input_to_offset(args[1])

        if off < 1024:
            off += 1024 - (off % 1024)

        if lent % 1024 is not 0:
            lent += 1024 - (lent % 1024)

        self.core_instance.get_emu_instance().mem_map(off, lent)
        print('Mapped ' + str(lent) + ' at ' + hex(off))

    def unmap(self, func_name, *args):
        off = utils.input_to_offset(args[0])
        lent = utils.input_to_offset(args[1])

        if off < 1024:
            off += 1024 - (off % 1024)

        if lent % 1024 is not 0:
            lent += 1024 - (lent % 1024)

        self.core_instance.get_emu_instance().mem_unmap(off, lent)
        print('Unmapped ' + str(lent) + ' at ' + hex(off))

    def internal_add(self, address, length, path=None):
        self.mappings.append([path, hex(address), length])

    def init(self):
        pass

    def delete(self):
        pass