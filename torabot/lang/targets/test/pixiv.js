function main(username, password){
    return {
        "@all": [
            {
                "@": "echo",
                "name": "user_agent",
                "args": [ "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0" ]
            },
            {
                "@request": [{
                    "uri": "http://www.pixiv.net/login.php",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": { "&": "user_agent" }
                    },
                    "body": {
                        "@base64_encode": [ "mode=login&pixiv_id=" + username + "&pass=" + password + "&skip=1" ]
                    }
                }]
            },
            {
                "@json_compress": {
                    "@xslt": {
                        "html_encoded": {
                            "[]": [
                                {
                                    "@request": [{
                                        "uri": "http://www.pixiv.net/bookmark_new_illust.php",
                                        "headers": {
                                            "User-Agent": { "&": "user_agent" }
                                        }
                                    }]
                                },
                                "body"
                            ]
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
