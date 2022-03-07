import gdb
from common import gdbutils

class NginxArrayDump(gdb.Command):
    def __init__(self):
        super(NginxArrayDump, self).__init__(
            "ngx_array_dump", gdb.COMMAND_USER
        )
    
    def _range_all(self, ptr, val_type):
        res_list = []
        # {elts = 0x555555673538, nelts = 1, size = 16, nalloc = 10, pool = 0x555555671510}
        res_list.append(str(ptr.dereference()))

        val_ptr = ptr['elts'].cast(val_type.pointer())
        for i in range(ptr['nelts']):
            res_list.append('\n[%d]: %s' %(i, str(val_ptr)))  # call NginxStrPrettyPrinter.to_string
            val_ptr = val_ptr + 1

        res_list.append('\n')
        return ''.join(res_list)

    def complete(self, text, word):
        return gdb.COMPLETE_SYMBOL

    # example: val ngx_str_t
    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) != 2:
            gdbutils.err('Expected fmt "ptr val_type)"')
            return
        
        ptr = gdbutils.parse_ptr(argv[0], 'ngx_array_t')
        if not ptr:
            gdbutils.err("Expected pointer argument of type (ngx_array_t *)")
            return

        try:
            val_type = gdb.lookup_type(argv[1])
        except:
            gdbutils.err('No type named "%s"' %(argv[1]))
            return
        gdbutils.out(self._range_all(ptr, val_type))


NginxArrayDump()
