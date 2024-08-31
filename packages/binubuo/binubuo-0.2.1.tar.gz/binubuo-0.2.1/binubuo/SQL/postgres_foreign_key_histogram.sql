with base_histograms as (select
                                    json_strip_nulls(json_build_object(
                                        'hashed_key'
                                        , {ref_col_name}
                                        , 'fcnt'
                                        , fcnt
                                        , 'low_cnt'
                                        , first_value(fcnt) over (order by fcnt)
                                        , 'high_cnt'
                                        , last_value(fcnt) over (order by fcnt rows between unbounded preceding and unbounded following)
                                    )) jsobj
                                  from (
                                    select
                                      md5(cast(a.{ref_col_name} as text)) {ref_col_name}
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
                                          {ref_tab_name} tablesample system ({ref_sample})
                                      )
                                    group by
                                      a.{ref_col_name}
                                    limit 50
                                  ) sq2
                                )
                                select
                                    json_agg(jsobj)
                                from
                                    base_histograms;