function main(username, password){
    return {
        "@all": [
            {
                "@request": {
                    "uri": "http://www.pixiv.net/login.php",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    "body": {
                        "@base64_encode": [ "mode=login&pixiv_id=" + username + "&pass=" + password + "&skip=1" ]
                    }
                }
            },
            {
                "@json_compress": {
                    "@xslt": {
                        "html_encoded": {
                            "[body]": {
                                "@request": {
                                    "uri": "http://www.pixiv.net/bookmark_new_illust.php"
                                }
                            }
                        },
                        "xslt": {
                            "text<": "pixiv_json.xml"
                        }
                    }
                }
            }
        ]
    }
}
