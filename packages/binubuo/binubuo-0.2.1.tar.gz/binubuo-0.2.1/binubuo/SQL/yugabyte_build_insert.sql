select 
                table_name
                , '(' || string_agg(column_name, ',' ORDER BY ordinal_position) || ') values (' || string_agg('d_d_s_r', ',' ORDER BY ordinal_position) || ')' as ins_stmt
            from information_schema.columns 
            where table_name = %s
            group by table_name