select 
                    column_name
                from user_tab_cols
                where table_name = :tabname
                order by
                    column_id