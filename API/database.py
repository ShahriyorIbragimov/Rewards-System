from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

engine = create_engine(
    url=settings.DATABASE_URL,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

from groups import models as group_models
from notifications import models as notification_models
from orders import models as order_models
from products import models as product_models
from rewards import models as reward_models
from students import models as student_models
from transactions import models as transaction_models
from users import models as user_models
