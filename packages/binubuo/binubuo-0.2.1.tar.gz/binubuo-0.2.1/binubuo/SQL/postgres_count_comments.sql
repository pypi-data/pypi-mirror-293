SELECT
                    count(
                    (
                        SELECT
                            pg_catalog.col_description(c.oid, cols.ordinal_position::int)
                        FROM pg_catalog.pg_class c
                        WHERE
                            c.oid     = (SELECT cols.table_name::regclass::oid) AND
                            c.relname = cols.table_name
                    ))

                FROM information_schema.columns cols
                WHERE
                    cols.table_name = %s