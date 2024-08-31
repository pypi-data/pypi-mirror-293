select
                        cols.column_name
                        , case cols.data_type
                            when 'integer' then 'number'
                            when 'numeric' then 'number'
                            when 'double precision' then 'number'
                            when 'character varying' then 'string'
                            when 'character' then 'string'
                            when 'text' then 'text'
                            when 'money' then 'number'
                            when 'date' then 'date'
                            when 'timestamp without time zone' then 'time'
                            when 'timestamp with time zone' then 'time'
                            when 'time without time zone' then 'time'
                            when 'time with time zone' then 'time'
                            when 'bigint' then 'number'
                            when 'real' then 'number'
                            when 'smallint' then 'number'
                            else 'string'
                        end column_data_type
                        , case
                            when cols.data_type = 'integer' and cstats.n_distinct between 1 and 2 then 'numeric_on_off'
                            when cols.data_type = 'integer' then 'small_number'
                            when cols.data_type = 'numeric' and cols.numeric_precision < 5 then 'small_amount'
                            when cols.data_type = 'numeric' and cols.numeric_precision > 4 then 'medium_amount'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 10 and cstats.n_distinct between 1 and 5 then 'flow_status'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 30 and (case when cstats.n_distinct <= -.9 then sut.n_live_tup else cstats.n_distinct end) > round(sut.n_live_tup*0.7) then 'full_name'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width < 10 then 'medium_word'
                            when cols.data_type in ('character varying', 'character') and cstats.avg_width > 20 then 'large_word'
                            when cols.data_type = 'money' then 'medium_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width < 4 then 'small_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width < 6 then 'medium_amount'
                            when cols.data_type = 'double precision' and cstats.avg_width > 5 then 'large_amount'
                            when cols.data_type = 'date' then 'date'
                            when cols.data_type in ('timestamp without time zone', 'timestamp with time zone') then 'timestamp'
                            when cols.data_type in ('time without time zone', 'time with time zone') then 'time'
                            when cols.data_type in ('bigint', 'real', 'smallint') then 'small_number'
                            when cols.data_type = 'boolean' then 'boolean'
                            else 'word'
                        end column_def_generator
                        , (
                            select
                                pg_catalog.col_description(c.oid, cols.ordinal_position::int)
                            from 
                                pg_catalog.pg_class c
                            where
                                c.oid = (select cols.table_name::regclass::oid) 
                            and
                                c.relname = cols.table_name
                        ) as column_comment
                        , sut.n_live_tup as num_rows
                        , case
                            when cstats.null_frac > 0 then greatest(round(sut.n_live_tup*cstats.null_frac), 1)
                            else 0
                        end num_nulls
                        , case
                            when cstats.n_distinct <= -.9 then sut.n_live_tup
                            when cstats.n_distinct < 0 and cstats.n_distinct > -.9 then round(sut.n_live_tup*0.9)
                            else cstats.n_distinct
                        end num_distinct
                        , cols.is_nullable
                        , cstats.avg_width
                    from
                        information_schema.columns cols
                        inner join pg_stat_user_tables sut on sut.relname = cols.table_name
                        left outer join pg_stats cstats on cstats.attname = cols.column_name and cstats.tablename = cols.table_name
                    where
                        cols.table_name = %s
                    order by
                        cols.ordinal_position asc;