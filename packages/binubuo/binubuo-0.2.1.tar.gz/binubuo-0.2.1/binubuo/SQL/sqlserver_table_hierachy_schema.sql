WITH dependencies -- Get object with FK dependencies
AS (
    SELECT FK.TABLE_NAME AS Obj
        , PK.TABLE_NAME AS Depends
    FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS C
    INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS FK
        ON C.CONSTRAINT_NAME = FK.CONSTRAINT_NAME
    INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS PK
        ON C.UNIQUE_CONSTRAINT_NAME = PK.CONSTRAINT_NAME
    ), 
no_dependencies -- The first level are objects with no dependencies 
AS (
    SELECT 
        o_tab.name AS Obj
    FROM sys.objects o_tab
    WHERE o_tab.name NOT IN (SELECT obj FROM dependencies) --we remove objects with dependencies from first CTE
    AND o_tab.type = 'U' -- Just tables
    ), 
recursiv -- recursive CTE to get dependencies
AS (
    SELECT Obj AS [Table]
        , CAST('' AS VARCHAR(max)) AS DependsON
        , 0 AS LVL -- Level 0 indicate tables with no dependencies
    FROM no_dependencies
 
    UNION ALL
 
    SELECT d.Obj AS [Table]
        , CAST(IIF(LVL > 0, r.DependsON + ' > ', '') + d.Depends AS VARCHAR(max)) -- visually reflects hierarchy
        , R.lvl + 1 AS LVL
    FROM dependencies d
    INNER JOIN recursiv r
        ON d.Depends = r.[Table]
    )
-- The final result, with some extra fields for more information
SELECT DISTINCT SCHEMA_NAME(O.schema_id) AS [TableSchema]
    , R.[Table]
    , R.DependsON
    , R.LVL
FROM recursiv R
INNER JOIN sys.objects O
    ON R.[Table] = O.name
where
	R.lvl = (select max(R2.lvl) from recursiv r2 where r2.[Table] = r.[Table])
and
	SCHEMA_NAME(O.schema_id) != 'dbo'
ORDER BY R.LVL
    , R.[Table]