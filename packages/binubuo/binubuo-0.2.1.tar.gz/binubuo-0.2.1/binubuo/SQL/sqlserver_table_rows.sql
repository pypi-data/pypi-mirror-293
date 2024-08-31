SELECT
   Total_Rows= SUM(st.row_count)
FROM
   sys.dm_db_partition_stats st
WHERE
    object_name(object_id) = ? AND (index_id < 2)