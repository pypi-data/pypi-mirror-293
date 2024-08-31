select
                    utc.column_name
                    , case utc.data_type
                        when 'NUMBER' then 'number'
                        when 'VARCHAR2' then 'string'
                        when 'NVARCHAR2' then 'string'
                        when 'DATE' then 'date'
                        when 'TIMESTAMP' then 'time'
                        when 'TIMESTAMP(6)' then 'time'
                        else 'string'
                    end as column_data_type
                    , case
                        when utc.data_type = 'NUMBER' and utc.avg_col_len = 3 and utc.num_distinct <=2 then 'numeric_on_off'
                        when utc.data_type = 'NUMBER' and utc.avg_col_len < 4 then 'small_number'
                        when utc.data_type = 'NUMBER' and utc.avg_col_len < 6 then 'medium_number'
                        when utc.data_type = 'NUMBER' and utc.avg_col_len > 5 then 'large_number'
                        when utc.data_type = 'FLOAT' and utc.avg_col_len < 4 then 'small_amount'
                        when utc.data_type = 'FLOAT' and utc.avg_col_len < 6 then 'medium_amount'
                        when utc.data_type = 'FLOAT' and utc.avg_col_len > 5 then 'large_amount'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 10 and utc.num_distinct <=5 then 'flow_status'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 30 and utc.num_distinct > round(ut.num_rows*0.7) then 'full_name'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len < 10 then 'medium_word'
                        when utc.data_type in ('VARCHAR2', 'NVARCHAR2', 'CHAR') and utc.avg_col_len > 20 then 'large_word'
                        when utc.data_type = 'DATE' then 'date'
                        when utc.data_type = 'TIMESTAMP' then 'timestamp'
                        when utc.data_type = 'TIMESTAMP(6)' then 'timestamp'
                        else 'word'
                    end as column_def_generator
                    , ucc.comments 
                    , ut.num_rows
                    , utc.num_nulls
                    , utc.num_distinct
                    , utc.nullable
                    , utc.avg_col_len
                from
                    user_tab_columns utc
                    inner join user_tables ut on ut.table_name = utc.table_name
                    left outer join user_col_comments ucc on utc.table_name = ucc.table_name and utc.column_name = ucc.column_name 
                where
                    utc.table_name = :tabname
                order by 
                    utc.column_id asc