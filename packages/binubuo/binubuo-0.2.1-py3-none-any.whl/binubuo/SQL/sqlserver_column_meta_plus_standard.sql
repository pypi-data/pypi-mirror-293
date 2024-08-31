with foreign_references as (
    select  object_name(a.parent_object_id) l_table_name
		, a.name
        , c.name l_column_name
		, object_name(b.referenced_object_id) r_table_name
		, d.name r_column_name
from    sys.foreign_keys a
        join sys.foreign_key_columns b
                  on a.object_id=b.constraint_object_id
        join sys.columns c
                  on b.parent_column_id = c.column_id
             and a.parent_object_id=c.object_id
        join sys.columns d
                  on b.referenced_column_id = d.column_id
            and a.referenced_object_id = d.object_id
where   object_name(a.parent_object_id) = ?
)
select
        cols.column_name as column_name
        , cols.table_name as table_name
        , cols.table_schema as table_schema
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
        end column_datatype
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
                ) as table_level_rowcount
        , '0' as column_nulls
        , '0' as column_distinct_count
        , cols.is_nullable as column_nullable
        , case
                when cols.character_maximum_length is not null then cols.character_maximum_length
                when cols.character_maximum_length is null and cols.numeric_precision is not null then cols.numeric_precision
                else 25
        end column_level_avg_col_length
        , 'Not given' as column_low_value
        , 'Not given' as column_high_value
        , case
            when fr.r_column_name is not null then 1
            else 0
        end column_is_reference
        , fr.r_table_name as reference_table
        , fr.r_column_name as reference_column
from
	INFORMATION_SCHEMA.COLUMNS cols
	left outer join sys.extended_properties exp on object_id(cols.table_name) = exp.major_id and cols.ordinal_position = exp.minor_id and exp.class_desc = 'OBJECT_OR_COLUMN' and exp.name = 'MS_DESCRIPTION'
    left outer join foreign_references fr on cols.table_name = fr.l_table_name and cols.column_name = fr.l_column_name
where
	cols.table_name = ?
order by
	cols.ORDINAL_POSITION asc
for json path;