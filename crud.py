import models
from logger import logger
from authentication.auth import hash_password, verify_password
from models import User, RefreshToken

#CREATE
def create_log(db, log,current_user):
    logger.info(f"Creating log for food: {log.food}")
    db_log = models.Log(
        food=log.food,
        calories=log.calories,
        protein=log.protein,
        fiber=log.fiber,
        date=log.date,
        user_id=current_user.id
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    logger.info(f"Created log with ID: {db_log.id}")
    return db_log

#SELECT *
def get_logs(db,current_user, skip, limit,food,min_calories,max_calories,sort,start_date, end_date):
    logger.info(f"Fetching all logs for user: {current_user.id}")
    query = db.query(models.Log).filter(models.Log.user_id == current_user.id)
    if min_calories is not None:
        query = query.filter(models.Log.calories >= min_calories)
    if max_calories is not None:
        query = query.filter(models.Log.calories <= max_calories)
    if food:
        query = query.filter(models.Log.food.ilike(f"%{food}%"))
    if start_date:
        query = query.filter(models.Log.date >= start_date)
    if end_date:
        query = query.filter(models.Log.date <= end_date)
    if sort == "asc":
        query = query.order_by(models.Log.date.asc())
    else:
        query = query.order_by(models.Log.date.desc())
    return query.offset(skip).limit(limit).all()

#SELECT * from WHERE id=id
def get_log(db, id: int, current_user):
    logger.info(f"Fetching log with ID: {id}")
    return db.query(models.Log).filter(models.Log.id == id, models.Log.user_id == current_user.id).first()

#DELETE
def delete_log(db, id: int, current_user):
    logger.info(f"Deleting log with ID: {id}")
    log = db.query(models.Log).filter(models.Log.id == id, models.Log.user_id == current_user.id).first()
    if log:
        db.delete(log)
        db.commit()
        logger.info(f"Deleted log with ID: {log.id}")
    else:
        logger.warning(f"No log with ID: {id}")
    return log

#UPDATE
def update_log(db, id:int, updated_log,current_user):
    log = db.query(models.Log).filter(models.Log.id == id,models.Log.user_id == current_user.id).first()

    if not log:
        return None

    log.food = updated_log.food
    log.calories = updated_log.calories
    log.protein = updated_log.protein
    log.fiber = updated_log.fiber
    log.date = updated_log.date

    db.commit()
    db.refresh(log)
    return log

def patch_log(db, id: int, updated_log,current_user):
    logger.info(f"Patching log with ID: {id}")
    log = db.query(models.Log).filter(models.Log.id == id, models.Log.user_id == current_user.id).first()

    if not log:
        logger.warning(f"No log with ID: {id}")
        return None
    update_data = updated_log.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    logger.info(f"Updated log with ID: {id}")
    return log

def create_user(db,user):
    hashed_pw = hash_password(user.password)
    db_user = User(
        email = user.email,
        hashed_password = hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db, email:str, password:str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_email(db, email:str):
    return db.query(User).filter(User.email == email).first()

def save_refresh_token(db,token, user_id):
    refresh_token = RefreshToken(token = token, user_id = user_id)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token

def get_refresh_token(db, token):
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()

def revoke_refresh_token(db, token):
    db_token = get_refresh_token(db, token)
    if db_token:
        db_token.revoked = True
        db.commit()