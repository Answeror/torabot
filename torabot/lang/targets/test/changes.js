function changes(query, result){
    var a = [];
    for (var i in result.arts) {
        if (query.result.arts.indexOf(result.arts[i]) < 0) {
            a.push(result.arts[i]);
        }
    }
    return a;
}
