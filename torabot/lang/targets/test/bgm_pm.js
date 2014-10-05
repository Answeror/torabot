function main(chii_auth) {
    return {
        "@all": [
            {
                "@json_decode[headers]": {
                    "@jinja2": {
                        "template": { "text<": "headers.json" },
                        "kargs": { "chii_auth": chii_auth }
                    }
                }
            },
            {
                "@request": {
                    "uri": "http://bgm.tv",
                    "headers": { "&": "headers" }
                }
            },
            {
                "@xslt": {
                    "html_encoded": {
                        "[body]": {
                            "@request": {
                                "uri": "http://bgm.tv/pm",
                                "headers": { "&": "headers" }
                            }
                        }
                    },
                    "xslt": { "text<": "bgm_pm.xslt" }
                }
            }
        ]
    };
}
