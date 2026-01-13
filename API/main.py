from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
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

app = FastAPI(title="Rewards System API", description="API for managing rewards, users, and more")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Rewards System API", "version": "1.0.0"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
