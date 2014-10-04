from logbook import Logger


log = Logger(__name__)


def init_conf(conf, mod):
    conf.from_object('torabot.conf')
    try:
        conf.from_object(mod)
    except:
        log.info('No toraconf.py provided. Use default config.')
