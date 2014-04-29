import mimeparse
from uuid import uuid4
from logbook import Logger
from flask import (
    jsonify,
    render_template,
    current_app,
    request,
    redirect,
    url_for,
)
from .. import db
from .errors import AuthError
from .response import make_response_content


log = Logger(__name__)


def make(app):
    from . import main
    main.make(app)
    from . import admin
    admin.make(app)

    app.context_processor(inject_locals)
    app.errorhandler(AuthError)(auth_error_guard)
    app.errorhandler(db.error.InvalidArgumentError)(invalid_argument_error_guard)
    app.errorhandler(db.error.UniqueConstraintError)(unique_constraint_error_guard)
    app.errorhandler(Exception)(general_error_guard)


def invalid_argument_error_guard(e):
    text = '无效值'
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
    }), 400


def unique_constraint_error_guard(e):
    text = '重复值错误'
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
    }), 400


def inject_locals():
    from ..core.mod import mod, mods
    from ..core.local import is_user, is_admin, current_user_id
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
        mods=mods(),
        is_user=is_user,
        is_admin=is_admin,
        current_user_id=current_user_id,
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
