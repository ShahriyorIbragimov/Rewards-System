from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import uvicorn
from router import router

from users.models import Users
from admin.models import AdminProfiles
from groups.models import Groups, GroupMemberships
from notifications.models import Notifications
from orders.models import Orders, OrderItems
from products.models import Products
from rewards.models import Rewards
from students.models import StudentProfiles
from teachers.models import TeacherProfiles
from transactions.models import Transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
