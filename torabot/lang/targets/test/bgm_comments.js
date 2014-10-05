function main(path) {
    return {
        "@all": [
            {
                "@jinja2[template]": {
                    "template": { "text<": "bgm_comments.xslt" },
                    "kargs": { "id": "bgm.tv{{ path }}" }
                }
            },
            {
                "@xslt": {
                    "html_encoded": {
                        "[body]": {
                            "@request": "http://bgm.tv" + path
                        }
                    },
                    "xslt": { "&": "template" }
                }
            }
        ]
    };
}
