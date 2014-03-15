def appengine():
    from flask import current_app, g
    engine = getattr(g, 'torabot_engine', None)
    if engine is None:
        from sqlalchemy import create_engine
        engine = create_engine(current_app.config['TORABOT_CONNECTION_STRING'])
        g.torabot_engine = engine
    return engine
