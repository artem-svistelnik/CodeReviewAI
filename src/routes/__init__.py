from routes.health import health_router
from routes.review import review_router


def include_routes(app):
    app.include_router(health_router)
    app.include_router(review_router)
