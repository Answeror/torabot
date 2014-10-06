function main(username, password, download){
    return {
        "@all": [
            {
                "@request[login]": {
                    "context": "pixiv",
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
                "@eval": {
                    "@js": [
                        { "text<": "pixiv_download_top_10.js" },
                        download,
                        [
                            {
                                "[contents]": {
                                    "@json_decode": {
                                        "@base64_decode": [{
                                            "[body]": {
                                                "@request/login": {
                                                    "context": "pixiv",
                                                    "uri": "http://www.pixiv.net/ranking.php?format=json&mode=daily&p=1d"
                                                }
                                            }
                                        }]
                                    }
                                }
                            }
                        ]
                    ]
                }
            }
        ]
    };
}

function download_arts_parallel(arts){
    downloads = [];
    for (var i = 0; i < Math.min(10, arts.length); ++i) {
        var art = arts[i];
        downloads.push({
            "id": art.illust_id,
            "title": art.title,
            "preview_uri": art.url,
            "image_data": {
                "[body]": {
                    "@request": {
                        "context": "pixiv",
                        "uri": "http://www.pixiv.net/member_illust.php?mode=big&illust_id=" + art.illust_id,
                        "headers": { "referer": "http://www.pixiv.net/" }
                    }
                }
            }
        });
    }
    return downloads;
}

function download_arts_sequence(arts){
    downloads = [];
    for (var i = 0; i < Math.min(10, arts.length); ++i) {
        var art = arts[i];
        if (i == 0) {
            var suffix = '';
        } else {
            var suffix = '/d' + (i - 1);
        }
        var request = "@request[d" + i + "]" + suffix;
        var download = {
            "id": art.illust_id,
            "title": art.title,
            "preview_uri": art.url,
            "image_data": { "[body]": { } }
        };
        download.image_data["[body]"][request] = {
            "context": "pixiv",
            "uri": "http://www.pixiv.net/member_illust.php?mode=big&illust_id=" + art.illust_id,
            "headers": { "referer": "http://www.pixiv.net/" }
        };
        downloads.push(download);
    }
    return downloads;
}
