function main(query, result){
    return {
        "@js": {
            "code": {"text<": "pixiv_changes.js"},
            "args": ["changes", query, result]
        }
    }
}
