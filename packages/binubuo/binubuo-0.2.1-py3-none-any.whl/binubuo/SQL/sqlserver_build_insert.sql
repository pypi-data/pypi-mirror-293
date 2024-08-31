with base_col_cast as (
select
	cols.table_name
	, concat('[', cols.column_name, ']') as column_name
	, cols.ordinal_position
	, case
		when cols.DATA_TYPE in ('datetime', 'datetime2') then 'convert(datetime, cast(d_d_s_r as datetime2))'
		when cols.DATA_TYPE = 'date' then 'convert(date, cast(d_d_s_r as datetime2))'
		else 'd_d_s_r'
	end col_cast
from
	INFORMATION_SCHEMA.COLUMNS cols
where
	cols.TABLE_NAME = ?
), agrr_cols as (
select 
	bcc.table_name
    , string_agg(bcc.column_name, ',') within group (order by bcc.ordinal_position) as l1
	, string_agg(bcc.col_cast, ',') within group (order by bcc.ordinal_position) as l2
from 
	base_col_cast bcc
group by
	bcc.table_name)
select
	concat('(', l1, ') values (', l2, ')')
from
	agrr_cols;