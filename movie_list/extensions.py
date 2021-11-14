from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True
        return options


db = SQLAlchemy()
mm = Marshmallow()


def init_extensions(app):

    # sqlalchecmy
    db.app = app
    db.init_app(app)

    # marshmallow
    mm.init_app(app)

    # # migration
    Migrate(app, db, render_as_batch=False)

    CORS(app)
