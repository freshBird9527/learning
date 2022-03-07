import gdb
from common import gdbutils

class NginxListDump(gdb.Command):
    def __init__(self):
        super(NginxListDump, self).__init__(
            "ngx_list_dump", gdb.COMMAND_USER
        )
    
    def _range_all(self, ptr, val_type):
        res_list = []
        # {last = 0x55cd9244f710, part = {elts = 0x55cd92444570, nelts = 6, 
        # next = 0x0}, size = 48, nalloc = 20, pool = 0x55cd9244f650}
        res_list.append(str(ptr.dereference()))

        pi = 0
        part = ptr['part']
        while True:
            elt = part['elts'].cast(val_type.pointer())
            for i in range(part['nelts']):
                res_list.append('\n[%d][%d]: %s' %(pi, i, str(elt)))
                elt = elt + 1
            if part['next'] == gdbutils.null():
                break
            pi += 1
            part = part['next']

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
        
        ptr = gdbutils.parse_ptr(argv[0], 'ngx_list_t')
        if not ptr:
            gdbutils.err("Expected pointer argument of type (ngx_list_t *)")
            return

        try:
            val_type = gdb.lookup_type(argv[1])
        except:
            gdbutils.err('No type named "%s"' %(argv[1]))
            return
        gdbutils.out(self._range_all(ptr, val_type))


NginxListDump()
