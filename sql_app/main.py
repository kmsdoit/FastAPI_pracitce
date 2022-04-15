
from fastapi import FastAPI,Query,Depends,HTTPException # fastAPI를 사용하기 위한 패키지, Query는 쿼리파라미터를 다루는 클래스이다.
import uvicorn # uvicorn 사용을 위한 패키지
from typing import Optional # 특정 파라미터를 선택적으로 사용하고 싶을때 사용
from pydantic import BaseModel # Validation,Config 관리를 위해서 사용한다 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
import sqlalchemy.orm.session
import sql_app.model
import sql_app.database
import sql_app.schemas
import sql_app.crud



sql_app.models.Base.metadata.create_all(bind=sql_app.database.engine)


app = FastAPI() # app 이라는 변수를 이용해서 fastAPI 사용

# Dependency
def get_db():
    db = sql_app.database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:8080",
] #
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserModel(BaseModel):
    userid : int
    name : str
    age : int
    company : Optional[str] = None



# app.get 예제
@app.get("/user/query/{userid}")
def queryClassTest(userid:Optional[str] = Query(None,min_length=3,max_length=20)):
    results = {"users": [{"userid": "Foo"}, {"userid": "Bar"}]}
    if userid:
        results.update({"userid": userid})
    return results

@app.get('/user/{userid}') # userid를 pathParameter를 통해 조회
def getUserId1(userid : str, option:Optional[str] = None): # optional 패키지를 통해 선택적으로 값을 받을 수 있다
    if option: # option 쿼리 스트링 값이 있을경우
        return {userid : option}
    return {userid:userid+" and option is None"} # option 쿼리 스트링 값이 없을 경우

@app.get('/user/test/{userid}')
def getUserId3(userid:int): # int때문에 숫자형 자료만 들어올 수 있음
    return {"userid":userid}

@app.get('/user/{userid}')
def getUserId2(userid):
    return {"userid":userid}

@app.get('/hello')
def hello():
    return "hello world"



# app.post 에제
@app.post('/user/{userid}')
def postUserid(usermodel : UserModel):
    usermodel_dict = usermodel.dict()
    if usermodel.company:
        usermodel_dict.update({"company" : usermodel.company + "이라는 회사에 다니고 있습니다"})    
    return usermodel_dict


@app.post("/users",response_model=sql_app.schemas.User)
def create_user2(user:sql_app.schemas.UserCreate, db: Session = Depends(get_db)): # 무조건 typing을 해줘야 에러가 발생하지 않음
    db_user = sql_app.crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return sql_app.crud.create_user(db=db, user=user)



if __name__ == '__main__': # uvicorn 환경설정
    uvicorn.run(app,host="0.0.0.0",port="8000",reload=True) # http://localhost:8000 사용 

