from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.get(
    "/authors/",
    response_model=list[schemas.Author]
)
def read_authors(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get(
    "/authors/{author_id}/",
    response_model=schemas.Author
)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/books", response_model=schemas.Book)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author doesn't exist")
    return crud.create_book(author_id=author_id, db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    author_id: int | None = None,
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100)
):
    db_books = crud.get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )

    return db_books
