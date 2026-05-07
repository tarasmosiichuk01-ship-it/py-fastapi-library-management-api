from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    authors = select(models.DBAuthor).offset(skip).limit(limit)
    return db.scalars(authors).all()


def get_author_by_name(db: Session, name: str):
    statement = select(models.DBAuthor).where(models.DBAuthor.name == name)
    return db.scalar(statement)


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(
        select(models.DBAuthor).where(
            models.DBAuthor.id == author_id
        )
    )


def create_book(author_id: int, db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_books(
    author_id: int | None,
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    books = select(models.DBBook)

    if author_id:
        books = books.where(models.DBBook.author_id == author_id)

    books = books.offset(skip).limit(limit)

    return db.scalars(books).all()
