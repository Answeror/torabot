from flask import Flask


app = Flask(__name__)
app.config.from_object('toraconf')


from . import views
assert views
