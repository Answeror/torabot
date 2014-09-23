function changes(query, result){
    var a = [];
    for (var i in result.arts) {
        var found = false;
        for (var j in query.result.arts) {
            if (query.result.arts[j].id == result.arts[i].id) {
                found = true;
                break;
            }
        }
        if (!found) {
            a.push(result.arts[i]);
        }
    }
    return a;
}
