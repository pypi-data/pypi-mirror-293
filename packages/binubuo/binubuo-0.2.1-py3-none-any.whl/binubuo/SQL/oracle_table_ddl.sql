select dbms_metadata.get_ddl('TABLE', :tabname)
            from dual