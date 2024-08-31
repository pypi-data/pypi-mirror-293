select 
                    '(' || listagg(column_name, ',') within group (order by column_id asc) || ') values (' || listagg(':c' ||rownum, ',') within group (order by column_id asc) || ')'
                from user_tab_cols
                where table_name = :tabname
                order by
                    column_id