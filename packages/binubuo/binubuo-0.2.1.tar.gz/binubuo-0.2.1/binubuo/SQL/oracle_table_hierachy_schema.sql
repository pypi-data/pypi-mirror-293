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
        , with_parents as (
            select 
                * 
            from 
                relations
            union
            select 
                r_owner
                , r_table_name
                , null
                , null
                , null
                , null
                , null
            from 
                relations 
            where 
                (r_owner, r_table_name) not in (
                    select 
                        owner
                        , table_name
                    from 
                        relations
                    where 
                        (owner, table_name) != ((r_owner, r_table_name))
                )
        ), all_data as (
        select 
            * 
        from (
            select 
                level lvl
                , owner
                , table_name
                , r_owner
                , r_table_name
                , r_constraint_type
                , local_col
                , remote_col
                , connect_by_iscycle is_cycle
            from 
                with_parents
            start with 
                r_owner is null
            connect by 
                nocycle (r_owner, r_table_name) = ((prior owner, prior table_name))
            order siblings by 
                owner, table_name
        ))
select
    distinct ad1.table_name
    , ad1.owner
    , ad1.lvl
from
    all_data ad1
where
    ad1.lvl = (select max(ad2.lvl) from all_data ad2 where ad2.owner = ad1.owner and ad2.table_name = ad1.table_name)
order by
    ad1.lvl asc