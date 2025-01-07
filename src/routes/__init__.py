from routes.health import health_router


def include_routes(app):
    app.include_router(health_router)
