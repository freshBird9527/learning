import gdb
from common import ngxtypes

class NginxStrPrettyPrinter(object):
    def __init__(self, val):
        self.val = val

    def to_string(self):
        len = self.val['len']
        data = self.val['data'].string(length=len)  # char* to python string
        return '{len = ' + str(len) + ', data = ' + data + '}'


class NginxTableEltPrettyPrinter(object):
    def __init__(self, val):
        self.val = val

    def to_string(self):
        key = self.val['key'].address.cast(ngxtypes.ngx_str_pointer_type)      # &key
        value = self.val['value'].address.cast(ngxtypes.ngx_str_pointer_type)  # &value
        lowcase_key = self.val['lowcase_key'].cast(ngxtypes.ngx_void_pointer_type)
        res = '{hash = ' + str(self.val['hash']) + ', key = ' +  str(key) + \
            ', value = ' + str(value) + ', lowcase_key = ' + str(lowcase_key) + '}'
        return res


class NginxPrettyPrinterLocator(gdb.printing.PrettyPrinter):
    def __init__(self):
        super(NginxPrettyPrinterLocator, self).__init__(
            'nginx_pretty_printers', []
        )

    def __call__(self, val):
        if val.type == ngxtypes.ngx_str_pointer_type:
            return NginxStrPrettyPrinter(val)
        if val.type == ngxtypes.ngx_table_elt_pointer_type:
            return NginxTableEltPrettyPrinter(val)


gdb.printing.register_pretty_printer(None, NginxPrettyPrinterLocator(), replace=True)
