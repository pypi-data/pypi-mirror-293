select top 1 table_schema
from INFORMATION_SCHEMA.TABLES
where TABLE_NAME = ?
order by table_schema;