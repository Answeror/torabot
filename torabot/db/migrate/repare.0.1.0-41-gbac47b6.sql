delete from notice where notice.change_id in (select change.id from change inner join query on change.query_id = query.id and query.kind = 'bilibili');
delete from change where change.id in (select change.id from change inner join query on change.query_id = query.id and query.kind = 'bilibili');
