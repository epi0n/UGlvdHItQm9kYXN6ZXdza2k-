import os

from sanic import Sanic

DB_URL = 'postgresql://docker:docker@postgres_db:5432/docker'
megabyte = 10e6


def create_app():
    app = Sanic(__name__)
    from app.endpoints.crud import ResponseFetcher, WebsiteFetcher
    app.add_route(WebsiteFetcher.as_view(), '/api/fetcher')
    app.add_route(WebsiteFetcher.as_view(), '/api/fetcher/<website_id:int>')
    app.add_route(ResponseFetcher.as_view(), '/api/fetcher/<website_id:int>/history')
    app.go_fast(debug=True, workers=os.cpu_count(), host='0.0.0.0', port=8080)
