from __future__ import annotations
from pydantic import BaseModel
from src.models import BookWithMetadata


class BookOut(BaseModel):
    sql_index: int
    title: str
    author: str | None
    description: str | None
    categories: str | None
    page_count: int | str
    date_published: str | None
    book_id: str
    isbn: str | None
    created_at: str

    @classmethod
    def from_metadata(cls, book: BookWithMetadata) -> BookOut:
        return cls(
            sql_index=book.sql_index,
            title=book.raw_book.title,
            author=book.raw_book.author,
            description=book.raw_book.description,
            categories=book.raw_book.categories,
            page_count=book.raw_book.page_count,
            date_published=book.raw_book.date_published,
            book_id=book.raw_book.book_id,
            isbn=book.raw_book.isbn,
            created_at=book.created_at,
        )


class BookSearchResult(BaseModel):
    title: str
    author: str | None
    date_published: str | None
    book_id: str
    isbn: str | None


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    categories: str | None = None
    page_count: int | None = None
    date_published: str | None = None
    isbn: str | None = None


class PageCountStats(BaseModel):
    min_pages: int | None
    max_pages: int | None
    avg_pages: float | None


class BookAddedInfo(BaseModel):
    sql_index: int
    title: str
    created_at: str


class BookStatsOut(BaseModel):
    total_books: int
    unique_authors: int
    page_count: PageCountStats | None = None
    earliest_added: BookAddedInfo | None = None
    latest_added: BookAddedInfo | None = None
