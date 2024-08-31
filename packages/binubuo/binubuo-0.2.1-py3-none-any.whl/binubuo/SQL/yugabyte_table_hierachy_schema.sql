with recursive recursiv as (
    select
        obj as Tab
        , '' as DependsOn
        , 0 as Lvl
    from no_dependencies
    
    union all
    
    select
        d.obj as Tab
        , 'depends' as DependsOn
        , r.lvl + 1 as Lvl
    from
        dependencies d
        inner join recursiv r on d.depends = r.Tab
), dependencies as (         
select kcu.table_name as obj,
       rel_tco.table_name as depends,
       kcu.table_schema as owner
from information_schema.table_constraints tco
join information_schema.key_column_usage kcu
          on tco.constraint_schema = kcu.constraint_schema
          and tco.constraint_name = kcu.constraint_name
join information_schema.referential_constraints rco
          on tco.constraint_schema = rco.constraint_schema
          and tco.constraint_name = rco.constraint_name
join information_schema.table_constraints rel_tco
          on rco.unique_constraint_schema = rel_tco.constraint_schema
          and rco.unique_constraint_name = rel_tco.constraint_name
where tco.constraint_type = 'FOREIGN KEY'
and kcu.table_schema = %s
group by kcu.table_schema,
         kcu.table_name,
         rel_tco.table_name,
         rel_tco.table_schema,
         kcu.constraint_name
order by kcu.table_schema,
         kcu.table_name
), no_dependencies as (
select 
    bt.table_name as obj
from 
    information_schema.tables bt
where 
    bt.table_name not in (select obj from dependencies)
and
    bt.table_type = 'BASE TABLE'
and
    bt.table_schema = %s)
select distinct
    r.Tab
    , r.DependsOn
    , r.Lvl
from
    recursiv r
where
    r.Lvl = (select max(r2.Lvl) from recursiv r2 where r2.Tab = r.Tab)
order by
    r.Lvl
;