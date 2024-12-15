from fastapi import FastAPI, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="CRUD Application")


templates = Jinja2Templates(directory="./app/templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    posts = crud.get_posts(db)
    return templates.TemplateResponse("index.html", {"request": request, "users": users, "posts": posts})


@app.post("/users/create")
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = schemas.UserCreate(username=username, email=email, password=password)
    crud.create_user(db, user)
    return RedirectResponse(url="/", status_code=303)


@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users/edit.html", {"request": request, "user": user})


@app.post("/users/edit/{user_id}")
def edit_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.email = email
    crud.update_user(db, user)
    return RedirectResponse(url="/", status_code=303)

@app.post("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/posts/create")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    post = schemas.PostCreate(title=title, content=content, user_id=user_id)
    crud.create_post(db, post)
    return RedirectResponse(url="/", status_code=303)


@app.get("/posts/edit/{post_id}", response_class=HTMLResponse)
def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("posts/edit.html", {"request": request, "post": post})

@app.post("/posts/edit/{post_id}")
def edit_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = title
    post.content = content
    crud.update_post(db, post)
    return RedirectResponse(url="/", status_code=303)

@app.post("/posts/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    crud.delete_post(db, post_id)
    return RedirectResponse(url="/", status_code=303)
