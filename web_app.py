from aiohttp import web
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "webapp_static")


async def index_handler(request):
    return web.FileResponse(os.path.join(STATIC_DIR, "index.html"))


def create_app():
    app = web.Application()
    app.router.add_get("/", index_handler)
    app.router.add_static("/static/", path=STATIC_DIR, name="static")
    return app
