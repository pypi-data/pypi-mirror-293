with foreign_references as (
                        select a.table_name, a.column_name, a.constraint_name, c.owner, 
                        -- referenced pk
                        c.r_owner, c_pk.table_name r_table_name, c2.column_name r_column_name
                        from user_cons_columns a
                        join user_constraints c on a.constraint_name = c.constraint_name
                        join user_constraints c_pk on c.r_constraint_name = c_pk.constraint_name
                        join user_cons_columns c2 on c_pk.constraint_name = c2.constraint_name
                        where c.constraint_type = 'R'
                        and a.table_name = :tabname
                    ),
unique_references as (
                        select :tabname as jcon_tab, b.column_name as jcon_col, count(a.table_name) jcon_is_uniq
                        from user_constraints a
                        join user_cons_columns b on a.table_name = b.table_name and a.constraint_name = b.constraint_name
                        where a.constraint_type in ('P', 'U')
                        and a.table_name = upper(:tabname)
                        group by :tabname, b.column_name
)
                    select utc.column_name, json_object(
                        key 'column_name' value utc.column_name
                        , key 'table_name' value ut.table_name
                        , key 'column_datatype' value case utc.data_type
                            when 'CLOB' then 'text'
                            when 'NUMBER' then 'number'
                            when 'VARCHAR2' then 'string'
                            when 'VARCHAR' then 'string'
                            when 'NVARCHAR2' then 'string'
                            when 'CHAR' then 'string'
                            when 'DATE' then 'date'
                            when 'TIMESTAMP(6)' then 'time'
                            when 'TIMESTAMP' then 'time'
                            else 'string'
                        end 
                        , key 'table_level_rowcount' value nvl(ut.num_rows, 0) 
                        , key 'table_level_avg_row_length' value nvl(ut.avg_row_len, 0)
                        , key 'column_level_avg_col_length' value nvl(utc.avg_col_len, 0)
                        , key 'column_data_length' value utc.data_length
                        , key 'column_number_precision' value utc.data_precision
                        , key 'column_number_decimals' value utc.data_scale
                        , key 'column_is_unique' value case
                            when ur.jcon_is_uniq = 1 then 'yes'
                            else 'no'
                        end
                        , key 'column_nullable' value utc.nullable
                        , key 'column_nulls' value utc.num_nulls
                        , key 'column_distinct_count' value utc.num_distinct
                        , key 'column_low_value' value 'Not given'
                        , key 'column_high_value' value 'Not given'
                        , key 'column_is_reference' value case
                            when fr.column_name is not null then 1
                            else 0
                        end
                        , key 'reference_table' value fr.r_table_name
                        , key 'reference_column' value fr.r_column_name
                         absent on null) col_infer_meta
                    from
                        user_tab_cols utc
                        inner join user_tables ut on ut.table_name = utc.table_name
                        left outer join foreign_references fr on fr.table_name = utc.table_name and fr.column_name = utc.column_name
                        left outer join unique_references ur on ur.jcon_tab = utc.table_name and ur.jcon_col = utc.column_name
                    where
                        utc.table_name = :tabname
                    order by 
                        utc.column_id asc