import mimeparse
from uuid import uuid4
from logbook import Logger
from functools import partial
from flask import (
    jsonify,
    render_template,
    current_app,
    request,
    redirect,
    url_for,
)
from .. import db
from .errors import AuthError, BusyError
from .response import make_response_content


log = Logger(__name__)


def make(app):
    from . import main
    main.make(app)
    from . import admin
    admin.make(app)
    from . import api
    api.make(app)

    app.context_processor(inject_locals)
    register_error_handlers(app)


def register_error_handlers(app):
    app.errorhandler(AuthError)(auth_error_guard)
    app.errorhandler(db.error.InvalidArgumentError)(partial(simple_error_guard, text='无效值.', status_code=400))
    app.errorhandler(db.error.InvalidEmailError)(partial(simple_error_guard, text='无效邮箱.', status_code=400))
    app.errorhandler(db.error.UniqueConstraintError)(partial(simple_error_guard, text='重复值错误.', status_code=400))
    app.errorhandler(db.error.DeleteEmailInUseError)(partial(simple_error_guard, text='请退订相关订阅后再删除该邮箱.', status_code=400))
    app.errorhandler(BusyError)(partial(simple_error_guard, text='更新姬反应不过来了... 请稍后重新查询 >_<', status_code=500))
    app.errorhandler(Exception)(general_error_guard)


def simple_error_guard(e, text, status_code):
    return make_response_content({
        'application/json': lambda: jsonify(dict(
            ok=False,
            message=dict(text=text, html=text)
        )),
        'text/html': lambda: render_template(
            'message.html',
            ok=False,
            message=text
        )
    }), status_code


def inject_locals():
    from ..core.mod import mod, frontend_mods
    from ..core.local import (
        is_user,
        is_admin,
        current_user_id,
        intro,
        current_username,
        is_user_activated,
        current_user,
    )
    from .momentjs import momentjs
    return dict(
        min=min,
        max=max,
        len=len,
        str=str,
        isinstance=isinstance,
        momentjs=momentjs,
        mod=mod,
        default_mod=current_app.config['TORABOT_DEFAULT_MOD'],
        mods=[m for m in frontend_mods() if m.public or is_user],
        is_user=is_user,
        is_admin=is_admin,
        current_user_id=current_user_id,
        current_username=current_username,
        intro=intro,
        is_user_activated=is_user_activated,
        current_user=current_user,
        debug=current_app.config['TORABOT_DEBUG'],
    )


def auth_error_guard(e):
    return redirect(url_for('main.index'))


def general_error_guard(e):
    name = str(uuid4())
    log.exception(name)
    template = '出错了. 错误编号 %s . 你可以提交该编号给 %s , 协助改进torabot.'

    def format_json():
        return jsonify(dict(
            message=dict(
                text=template % (
                    name,
                    current_app.config.get('TORABOT_REPORT_EMAIL', '')
                ),
                html=template % (
                    name,
                    "<a href='mailto:{0}' target=_blank>{0}</a>".format(
                        current_app.config.get('TORABOT_REPORT_EMAIL', '')
                    )
                )
            )
        ))

    def format_html():
        return render_template(
            'message.html',
            ok=False,
            message=template % (
                name,
                current_app.config.get('TORABOT_REPORT_EMAIL', '')
            ),
        )

    formats = {
        'application/json': format_json,
        'text/html': format_html,
    }
    return formats[mimeparse.best_match(formats, request.headers['accept'])](), 400
