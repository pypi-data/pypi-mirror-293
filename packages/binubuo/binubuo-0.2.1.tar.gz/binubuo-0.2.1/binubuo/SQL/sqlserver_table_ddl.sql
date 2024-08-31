with base_cols as (
select
	case
		when CHARACTER_MAXIMUM_LENGTH is not null then
			concat('[', COLUMN_NAME, ']',' ', '[', data_type, ']','(',CHARACTER_MAXIMUM_LENGTH,')')
		else
			concat('[', COLUMN_NAME, ']',' ', '[', data_type, ']')
	end ctab
	, ORDINAL_POSITION
	, table_schema
	, table_name
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = ?)
select
	concat('create table ', lower(table_schema), '.', lower(table_name), ' (', string_agg(ctab, ',') within group (order by ordinal_position), ')') as ddl_str
from
	base_cols
group by
	TABLE_SCHEMA, TABLE_NAME