import quart.flask_patch  # noqa
from flask_wtf.csrf import CSRFProtect
from quart import Quart
from quart_rate_limiter import RateLimiter

from app import http
from app.config import config

csrf = CSRFProtect()
rate_limiter = RateLimiter()


def init_website():
    server = Quart(__name__)
    server.config["SECRET_KEY"] = config.SECRET_KEY

    http.client.init()
    csrf.init_app(server)
    rate_limiter.init_app(server)

    from app.api.views import api
    from app.website.errors import errors
    from app.website.views import website

    server.register_blueprint(errors)
    server.register_blueprint(website)
    server.register_blueprint(api)

    return server
