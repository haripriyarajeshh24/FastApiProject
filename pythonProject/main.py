
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Users(BaseModel):
    signup: str
    login: str


class Posts(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description:  str = Field(min_length=1)


@app.post("/post/")
async def create_post(post: Posts, db: Session = Depends(get_db)):
    post_model = models.Posts()
    post_model.name = post.name
    post_model.description = post.description

    db.add(post_model)
    db.commit()
    return post


@app.get("/post/")
async def get_post(db: Session = Depends(get_db)):
    return db.query(models.Posts).all()


@app.put("/{post_id}")
async def update_book(post_id: int, post: Posts, db: Session = Depends(get_db)):
    post_model = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if post_model is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post_model.name = post.name
    post_model.description = post.description

    db.add(post_model)
    db.commit()

    return post


@app.delete("/{post_id}")
async def delete_book(post_id: int, post: Posts, db: Session = Depends(get_db)):
    post_model = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if post_model is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.query(models.Posts).filter(models.Posts.id == post_id).delete()
    db.commit()
    return post

# Run the FastAPI application using Uvicorn if this script is the main program
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application on the specified host and port
    uvicorn.run(app, host="127.0.0.1", port=8000)
