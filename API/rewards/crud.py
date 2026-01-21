from sqlalchemy.orm import Session
from . import schemas as s
from . import models as m
from fastapi import HTTPException, status
import uuid

def create_reward(db: Session, data: s.RewardCreate):
    try:
        reward_data = data.model_dump()
        reward = m.Rewards(**reward_data)
        db.add(reward)
        db.commit()
        db.refresh(reward)
        return reward
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_rewards(group_id: uuid.UUID, db: Session):
    try:
        return db.query(m.Rewards).filter(m.Rewards.group_id == group_id).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_reward(db: Session, id: uuid.UUID):
    try:
        reward = db.query(m.Rewards).filter(m.Rewards.id == id).first()
        if not reward:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reward is not found."
            )
        return reward
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def delete_reward(db: Session, id: uuid.UUID):
    try:
        reward = get_reward(db=db, id=id)
        db.delete(reward)
        db.commit()
        return reward
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )