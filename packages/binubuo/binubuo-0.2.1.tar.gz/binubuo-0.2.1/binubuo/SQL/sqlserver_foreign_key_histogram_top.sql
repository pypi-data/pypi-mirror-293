with base_data as (select top 50
    CONVERT(NVARCHAR(32),HashBytes('MD5', cast(a.[{ref_col_name}] as varchar(200))),2) [{col_name}]
    , count(b.[{col_name}]) fcnt
    from {ref_schema_name}.{ref_tab_name} a
    , {schema_name}.{tab_name} b
    where
    a.[{ref_col_name}] = b.[{col_name}]
    and
    a.[{ref_col_name}] in (
        select 
        [{ref_col_name}]
        from
        {ref_schema_name}.{ref_tab_name}
    )
    group by
		a.[{ref_col_name}]
)
select
    {col_name} as hkv
    , fcnt
	, first_value(fcnt) over (order by fcnt) low_cnt
	, last_value(fcnt) over (order by fcnt rows between unbounded preceding and unbounded following) high_cnt
from
    base_data
order by
    fcnt asc
for json auto