from fga.db import db
import flask_migrate
from fga.db.fixtures import seed_db


def init_cli(app, manager):
    if app.debug:

        @app.cli.command("seed", help="Seed DB with test data")
        def seed_db_cmd():
            seed_db()

        manager.add_command(seed_db_cmd)

        # init-db
        @app.cli.command(
            "init-db", help="Reinitialize database from scratch (deletes all data)"
        )
        def init_db_cmd():
            print(f"Initializing {db.engine.url}")
            db.drop_all(app=app)
            db.create_all(app=app)
            print("Initialized DB")

        manager.add_command(init_db_cmd)

        @app.cli.command("drop-db", help="Drop every table in the database")
        def drop_db_cmd():
            print(f"Dropping all tables in {db.engine.url}")
            db.reflect(app=app)
            db.drop_all(app=app)
            print("Success")

        manager.add_command(drop_db_cmd)

        # config check
        @app.cli.command("config", help="View configuration")
        def config_cmd():
            import pprint

            pprint.pprint(app.config)

        manager.add_command(config_cmd)


def migrate_handler(event, context):
    from app import app

    with app.app_context():
        flask_migrate.upgrade()
    return "Migrated"


def seed_handler(event, context):
    """Lambda entry point."""
    from app import app

    with app.app_context():
        seed_db()

    return "Seeded DB."


def init_handler(event, context):
    from app import app

    with app.app_context():
        # drop_all_tables(app=app)
        db.create_all(app=app)
    return "DB initialized."
