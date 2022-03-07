import gdb

ngx_void_pointer_type = gdb.lookup_type('void').pointer()
ngx_str_pointer_type = gdb.lookup_type('ngx_str_t').pointer()
ngx_array_pointer_type = gdb.lookup_type('ngx_array_t').pointer()
ngx_table_elt_pointer_type = gdb.lookup_type('ngx_table_elt_t').pointer()