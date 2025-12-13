from fastapi import APIRouter

from .auth.api import router as auth_router
from .health import router as health_router
from .rules.api import router as rules_router
from .users.api import router as users_router
from .validations.api import router as validations_router


router = APIRouter()

router.include_router(health_router)
router.include_router(rules_router)
router.include_router(validations_router)
router.include_router(auth_router)
router.include_router(users_router)
