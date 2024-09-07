from fastapi import APIRouter, Depends, HTTPException, Request
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database_files import get_db
from app.database_files.models import User

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Проверяем, есть ли идентификатор пользователя в сессии
    user_id = request.session.get("user")
    if not user_id:
        raise HTTPException(status_code=401, detail="Необходимо авторизоваться")

    # Получаем пользователя из базы данных по user_id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@auth_router.post("/register")
async def register_user(email: str, password: str, db: Session = Depends(get_db)):
    try:
        user = User(email=email, hashed_password=get_password_hash(password))
        db.add(user)
        db.commit()
        return {"message": "Вы успешно зарегистрированы"}
    except Exception as e:
        raise e


@auth_router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Logged in successfully"}


@auth_router.get("/profile/{user_id}")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@auth_router.put("/profile/{user_id}")
async def update_profile(user_id: int, email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = email
    user.hashed_password = get_password_hash(password)
    db.commit()
    return {"message": "Profile updated"}


@auth_router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
