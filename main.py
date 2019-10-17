import os
import time
import threading

from sanic.log import logger

from app import create_app


def run_workers_for_existent_urls():
    from app.database.models import Website
    from app.database.connector import scoped_session
    from app.endpoints.crud import worker_routine
    with scoped_session() as session:
        existent_websites = [{'id': website.id, 'url': website.url, 'interval': website.interval}
                             for website in session.query(Website).all()]
    for website in existent_websites:
        t = threading.Thread(target=worker_routine,
                             args=[website],
                             daemon=True)
        t.start()


def run():
    time.sleep(3)  # Making sure the database has time to properly set up
    os.system('alembic revision --autogenerate')
    os.system('alembic upgrade head')
    run_workers_for_existent_urls()
    create_app()


if __name__ == '__main__':
    run()
