import mimeparse
from uuid import uuid4
from logbook import Logger
from flask import jsonify, render_template, current_app, request
from .momentjs import momentjs
from ..core.mod import mod, mods


log = Logger(__name__)


def make(app):
    from . import main
    main.make(app)
    from . import admin
    admin.make(app)

    app.context_processor(inject_locals)
    app.errorhandler(Exception)(general_error_guard)


def inject_locals():
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
    )


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
