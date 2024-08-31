with base_histograms as (select
                                    json_object(
                                        key 'hkv' value {ref_col_name} 
                                        , key 'fcnt' value fcnt
                                        , key 'low_cnt' value first_value(fcnt) ignore nulls over (order by fcnt)
                                        , key 'high_cnt' value last_value(fcnt) ignore nulls over (order by fcnt rows between unbounded preceding and unbounded following)
                                    ) jsobj
                                from (
                                    select
                                    ora_hash(a.{ref_col_name}) {ref_col_name}
                                    , count(b.{col_name}) fcnt
                                    from {ref_tab_name} a
                                    , {tab_name} b
                                    where
                                    a.{ref_col_name} = b.{col_name}
                                    and
                                    a.{ref_col_name} in (
                                        select 
                                        {ref_col_name}
                                        from
                                        {ref_tab_name} sample({ref_sample})
                                    )
                                    group by
                                    a.{ref_col_name}
                                ))
                            select
                                json_arrayagg(jsobj returning clob)
                            from
                                base_histograms