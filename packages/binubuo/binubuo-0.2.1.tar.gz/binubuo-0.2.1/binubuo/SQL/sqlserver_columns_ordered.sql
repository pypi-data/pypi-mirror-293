select 
                column_name
            from information_schema.columns 
            where table_name = ?
            ORDER BY ordinal_position