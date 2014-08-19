drop trigger if exists update_query_mtime on query;
create trigger update_query_mtime
    before update of result on query
    for each row
    execute procedure update_query_mtime();
