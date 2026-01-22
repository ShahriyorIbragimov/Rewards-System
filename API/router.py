from fastapi import APIRouter
from auth.router import router as auth_router
from users.router import router as users_router
from students.router import router as students_router
from groups.router import router as groups_router
from products.router import router as products_router
from rewards.router import router as rewards_router

router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(students_router, prefix="/students", tags=["Student Profiles"])
router.include_router(groups_router, prefix="/groups", tags=["Groups"])
router.include_router(products_router, prefix="/products", tags=["Products"])
router.include_router(rewards_router, prefix="/rewards", tags=["Rewards"])