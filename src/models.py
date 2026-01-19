from __future__ import annotations

class Book:
    def __init__(
        self,
        title: str,
        book_id: str,
        author: str,
        page_count: int | str,
        description: str,
        categories: str,
        date_published: str,
        isbn: str,
    ):
        self.title = title
        self.book_id = book_id
        self.author = author
        self.page_count = page_count
        self.description = description
        self.categories = categories
        self.date_published = date_published
        self.isbn = isbn

    @classmethod
    def from_api(cls, item: dict) -> Book:
        volume_info = item.get("volumeInfo", {})
        sample = volume_info.get("industryIdentifiers", {})
        identifier = next(
            (value for value in sample if value.get("type") == "ISBN_13"), {}
        )

        book_title = volume_info.get("title", "Unknown")
        book_id = item.get("id", "")
        book_author = ", ".join(volume_info.get("authors", ["Unknown author"]))
        book_published_date = volume_info.get("publishedDate", "Unknown")
        book_page_count = volume_info.get("pageCount", "Unknown")
        book_description = volume_info.get("description", "No book description")
        book_category = ", ".join(volume_info.get("categories", ["Unknown category"]))
        book_isbn = identifier.get("identifier", "Unknown ISBN")

        return cls(
            title=book_title,
            author=book_author,
            date_published=book_published_date,
            page_count=book_page_count,
            description=book_description,
            categories=book_category,
            book_id=book_id,
            isbn=book_isbn,
        )

    @classmethod
    def from_dict(cls, data: dict) -> Book:
        book_title = data.get("Title", "Unknown")
        book_id = data.get("ID", "")
        book_author = data.get("Authors", ["Unknown author"])
        book_published_date = data.get("Date Published", "Unknown")
        book_page_count = data.get("Page Count", "Unknown")
        book_description = data.get("Description", "No book description")
        book_category = data.get("Categories", ["Unknown category"])
        book_isbn = data.get("isbn", "Unknown ISBN")

        return cls(
            title=book_title,
            author=book_author,
            date_published=book_published_date,
            page_count=book_page_count,
            description=book_description,
            categories=book_category,
            book_id=book_id,
            isbn=book_isbn,
        )

    def to_dict(self) -> dict:
        return {
            "Title": self.title,
            "ID": self.book_id,
            "Authors": self.author,
            "Date Published": self.date_published,
            "Page Count": self.page_count,
            "Description": self.description,
            "Categories": self.categories,
            "isbn": self.isbn,
        }

    def short_line(self) -> str:
        return f"{self.title} -- {self.author} ({self.date_published})"

    def detailed_text(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"ID: {self.book_id}\n"
            f"Authors: {self.author}\n"
            f"Description: {self.description}\n"
            f"Date Published: {self.date_published}\n"
            f"Page count: {self.page_count}\n"
            f"Categories: {self.categories}\n"
            f"isbn: {self.isbn}\n"
        )


class BookWithMetadata:
    def __init__(self, raw_book: Book, sql_index: int, created_at: str) -> None:
        self.raw_book = raw_book
        self.sql_index = sql_index
        self.created_at = created_at

    @classmethod
    def from_row(cls, row: tuple, book: Book) -> BookWithMetadata:
        book_sql_index = row[0]
        book_created_at = row[9]

        return cls(
            raw_book=book,
            sql_index=book_sql_index,
            created_at=book_created_at,
        )

    def detailed_text(self) -> str:
        return (
            f"sql index: {self.sql_index}\n"
            f"{self.raw_book.detailed_text()}"
            f"created at: {self.created_at}\n"
        )
