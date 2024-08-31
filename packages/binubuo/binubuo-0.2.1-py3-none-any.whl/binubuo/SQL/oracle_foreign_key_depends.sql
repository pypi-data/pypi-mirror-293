with pur as (
            select 
                a.owner
                , a.constraint_name
                , a.constraint_type
                , a.table_name
                , a.r_owner
                , a.r_constraint_name
                , b.column_name local_col
            from 
                all_constraints a, all_cons_columns b
            where 
                a.constraint_type in('P','U','R')
            and 
                a.owner = user
            and
                a.owner = b.owner
            and
                a.constraint_name = b.constraint_name
        )
        , relations as (
            select 
                a.owner
                , a.table_name
                , a.r_owner
                , b.table_name r_table_name
                , b.constraint_type r_constraint_type
                , a.local_col
                , b.local_col remote_col
            from 
                pur a 
            join 
                pur b on (a.r_owner, a.r_constraint_name) = ((b.owner, b.constraint_name))
        )
select
    r_table_name
    , remote_col
    , local_col
from relations
where
    table_name = :tabname