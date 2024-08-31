with foreign_references as (SELECT
                            tc.table_schema,
                            tc.constraint_name,
                            tc.table_name,
                            kcu.column_name,
                            ccu.table_schema AS foreign_table_schema,
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name
                        FROM
                            information_schema.table_constraints AS tc     
                            JOIN information_schema.key_column_usage AS kcu      ON tc.constraint_name = kcu.constraint_name      AND tc.table_schema = kcu.table_schema    
                            JOIN information_schema.constraint_column_usage AS ccu      ON ccu.constraint_name = tc.constraint_name      AND ccu.table_schema = tc.table_schema
                        WHERE tc.constraint_type = 'FOREIGN KEY' 
                        AND tc.table_name = %s
                        )
                    select
                        cols.column_name
                        , json_strip_nulls(json_build_object(
                            'column_name'
                            , cols.column_name
                            , 'table_name'
                            , cols.table_name
                            , 'column_datatype'
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
                                when 'xml' then 'text'
                                else 'string'
                            end
                            , 'table_level_rowcount'
                            , coalesce(sut.n_live_tup, 0)
                            , 'table_level_avg_row_length'
                            , 0
                            , 'column_level_avg_col_length'
                            , coalesce(cstats.avg_width, 0)
                            , 'column_data_length'
                            , case
                                when cols.character_maximum_length is not null then cols.character_maximum_length
                                else null
                            end 
                            , 'column_number_precision'
                            , cols.numeric_precision 
                            , 'column_number_decimals'
                            , cols.numeric_scale 
                            , 'column_nullable'
                            , cols.is_nullable
                            , 'column_nulls'
                            , case
                                when cstats.null_frac > 0 then greatest(round(sut.n_live_tup*cstats.null_frac), 1)
                                else 0
                            end
                            , 'column_distinct_count'
                            , case
                                when cstats.n_distinct <= -.9 then sut.n_live_tup
                                when cstats.n_distinct < 0 and cstats.n_distinct > -.9 then round(sut.n_live_tup*0.9)
                                else cstats.n_distinct
                            end
                            , 'column_low_value'
                            , 'Not extractable'
                            , 'column_high_value'
                            , 'Not extractable'
                            , 'column_is_reference'
                            , case
                                when fr.column_name is not null then 1
                                else 0
                            end
                            , 'reference_table'
                            , fr.foreign_table_name
                            , 'reference_column'
                            , fr.foreign_column_name
                        ))
                    from
                        information_schema.columns cols
                        inner join pg_stat_user_tables sut on sut.relname = cols.table_name
                        left outer join pg_stats cstats on cstats.attname = cols.column_name and cstats.tablename = cols.table_name
                        left outer join foreign_references fr on fr.table_name = cols.table_name and fr.column_name = cols.column_name
                    where
                        cols.table_name = %s
                    order by
                        cols.ordinal_position asc