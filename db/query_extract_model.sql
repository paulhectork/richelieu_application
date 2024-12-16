select information_schema.columns.table_name,
       information_schema.columns.column_name,
       information_schema.columns.data_type,
       information_schema.columns.is_nullable
from information_schema.columns
where information_schema.columns.table_schema = 'public'
order by information_schema.columns.table_name, 
         information_schema.columns.column_name 
         asc;