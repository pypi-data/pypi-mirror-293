select
	cols.column_name
	, case cols.data_type
		when 'varchar' then 'string'
		when 'int' then 'number'
        when 'bigint' then 'number'
        when 'decimal' then 'number'
        when 'money' then 'number'
        when 'numeric' then 'number'
        when 'smallint' then 'number'
        when 'smallmoney' then 'number'
        when 'tinyint' then 'number'
        when 'float' then 'number'
        when 'real' then 'number'
        when 'char' then 'string'
        when 'text' then 'text'
        when 'nchar' then 'string'
        when 'nvarchar' then 'string'
        when 'ntext' then 'text'
        when 'date' then 'date'
        when 'smalldatetime' then 'date'
        when 'datetime' then 'time'
        when 'datetime2' then 'time'
        when 'time' then 'time'
		else 'string'
	end column_data_type
	, case
        when cols.data_type = 'money' then 'medium_amount'
        when cols.data_type = 'smallmoney' then 'small_amount'
        when cols.data_type in ('bigint', 'int', 'decimal', 'numeric') then 'medium_number'
        when cols.data_type in ('smallint', 'tinyint') then 'small_number'
        when cols.data_type in ('date', 'smalldatetime') then 'near_date'
        when cols.data_type in ('datetime', 'datetime2') then 'near_time'
        else 'word'
    end column_def_generator
	, cast(exp.value as nvarchar(100)) as column_comment
	, (SELECT SUM(sPTN.Rows)
            FROM 
                  sys.objects AS sOBJ
                  INNER JOIN sys.partitions AS sPTN
                        ON sOBJ.object_id = sPTN.object_id
            WHERE
                  sOBJ.name = ?
                  AND sOBJ.type = 'U'
                  AND sOBJ.is_ms_shipped = 0x0
                  AND index_id < 2 -- 0:Heap, 1:Clustered
            ) as num_rows
	, '0' as num_nulls
	, '0' as num_distinct
	, cols.is_nullable as nullable
	, case
            when cols.character_maximum_length is not null then cols.character_maximum_length
            when cols.character_maximum_length is null and cols.numeric_precision is not null then cols.numeric_precision
            else 25
      end avg_col_len
from
	INFORMATION_SCHEMA.COLUMNS cols
	left outer join sys.extended_properties exp on object_id(cols.table_name) = exp.major_id and cols.ordinal_position = exp.minor_id and exp.class_desc = 'OBJECT_OR_COLUMN' and exp.name = 'MS_DESCRIPTION'
where
	cols.table_name = ?
order by
	cols.ORDINAL_POSITION asc