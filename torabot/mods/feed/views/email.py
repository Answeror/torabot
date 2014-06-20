from .. import Feed as Mod


def format_notice_body(notice):
    return Mod.instance.jinja2_env.get_template(
        template_name(Mod.instance, notice)
    ).render(
        notice=notice,
        mod=Mod.instance
    )


def template_name(mod, notice):
    return '%s/notice/%s.txt' % (mod.display_name, notice.change.kind)
