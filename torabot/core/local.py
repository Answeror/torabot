def get_current_conf():
    try:
        from flask import current_app
        return current_app.config
    except:
        try:
            from celery import current_app
            return current_app.conf
        except:
            return {}
