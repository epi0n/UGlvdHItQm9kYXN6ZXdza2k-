import requests
import time
import threading

from sanic.log import logger
from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy import Sequence
from sqlalchemy.dialects.postgresql import insert

from app import megabyte
from app.database.connector import scoped_session
from app.database.models import Response, Website


def worker_routine(website):
    while True:
        created_at = time.time()
        try:
            response = requests.get(website['url'], timeout=5)
            duration = time.time() - created_at
            if response.content:
                response = response.content.decode()
                logger.info(f' Received response for URL {website["url"]} (ID {website["id"]}).')
        except requests.exceptions.Timeout as e:
            duration = time.time() - created_at
            logger.error(f' Error occured while fetching URL {website["url"]} (ID {website["id"]}):\n{e.response}')
            response = None
        with scoped_session() as session:
            insert_dict = {'id': session.execute(Sequence('response_id_seq')), 'website_id': website['id'],
                           'response': response, 'duration': duration, 'created_at': created_at}
            session.execute(insert(Response).values(insert_dict))
        time.sleep(website['interval'])


class WebsiteFetcher(HTTPMethodView):
    async def get(self, request):
        with scoped_session() as session:
            return json({'id': res.id, 'url': res.url, 'interval': res.interval}
                        for res in session.query(Website).all())

    async def delete(self, request, website_id):
        with scoped_session() as session:
            exists = session.query(Website).filter(Website.id == website_id).scalar()
            if not exists:
                return json('Not Found.', status=404)
            session.query(Website).filter(Website.id == website_id).delete()
            return json(f'Successfully deleted url {exists.url}.')

    async def post(self, request):
        url, interval = request.json.get('url'), request.json.get('interval')
        if url and interval:
            with scoped_session() as session:
                if not session.query(Website).filter(Website.url == url).scalar():
                    if len(requests.get(url).content) > megabyte:
                        return json('Request Entity Too Large.', status=413)
                    website = Website(id=session.execute(Sequence('website_id_seq')), url=url, interval=interval)
                    session.add(website)
                    t = threading.Thread(target=worker_routine,
                                         args=[{'id': website.id, 'url': website.url, 'interval': website.interval}],
                                         daemon=True)
                    t.start()
                    return json({'id': website.id})
                return json('URL already exists.', status=418)
        return json({'message': 'Bad request.'}, status=400)


class ResponseFetcher(HTTPMethodView):
    async def get(self, request, website_id):
        with scoped_session() as session:
            exists = session.query(Response).filter(Response.website_id == website_id).all()
            response = json({'response': res.response, 'duration': res.duration, 'created_at': res.created_at}
                            for res in exists) if exists else json({'msg': 'Not found.'}, 404)
            return response
