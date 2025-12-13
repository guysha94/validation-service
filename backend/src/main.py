from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from python_sdk.application.api import API

from .conf import settings
from .router import router

api = API(
    name="Validation Service",
    version="0.0.1",
    debug=True,
    init_postgres=True,
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/", response_class=RedirectResponse, summary="Redirect to Docs", status_code=302)
async def root():
    return RedirectResponse(url="/docs")


api.include_router(router)


def main():

    api.run(
        app_path=f"{__name__}:api",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.debug,
        log_level=settings.log_level,
    )
