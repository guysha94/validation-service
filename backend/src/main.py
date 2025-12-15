from typing import Optional, Union

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from python_sdk.application.api import API
from python_sdk.conf import configure_logger
from python_sdk.utils.optimizations import optimize_gc

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


def main(
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
        reload: Optional[bool] = None,
        workers: int = 1,
        log_level: Optional[Union[str, int]] = None,

):

    optimize_gc()
    configure_logger(enqueue=True)

    api.run(
        app_path=f"{__name__}:api",
        host=host or settings.api.host,
        port=port or settings.api.port,
        reload=reload if reload is not None else settings.debug,
        log_level=log_level or settings.log_level,
        workers=workers,
    )
