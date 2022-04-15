from sqlalchemy.orm import Session
from . import models, schemas
import database


# import sql_app.models # 절대경로로 불러오는방법
# import sql_app.schemas # 절대경로로 불러오는방법

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    