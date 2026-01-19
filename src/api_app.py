from fastapi import FastAPI, Depends, status, HTTPException, Query, Path
from src.library import Library
from src.storage.sql_storage import SqlLibraryStorage
from src.config import DB_PATH, API_KEY
from src.schemas import BookOut, BookSearchResult, BookUpdate, BookStatsOut
from src.google_api_client import GoogleBooksClient
from src.exceptions import BookNotFoundError

app = FastAPI()


def sql_library():
    return Library(SqlLibraryStorage(DB_PATH))


def google_client():
    return GoogleBooksClient(API_KEY)



@app.get("/")
def home():
    return {
        "status": "running",
        "docs": "/docs",
    }


@app.get("/books", response_model=list[BookOut], status_code=status.HTTP_200_OK)
def read_books(q: str | None = None, library: Library = Depends(sql_library)):
    if isinstance(library.storage, SqlLibraryStorage):
        if q is None or q == "":
            bookout_list = []

            for item in library.books:
                full_item = library.storage.get_with_metadata(item)
                bookout_item = BookOut.from_metadata(full_item)

                bookout_list.append(bookout_item)

            return bookout_list
        elif q:
            meta_books = library.storage.search(q=q)

            return [BookOut.from_metadata(item) for item in meta_books]


@app.get("/books/random", response_model=BookOut, status_code=status.HTTP_200_OK)
def get_random(library: Library = Depends(sql_library)):
    if library.is_empty():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library is empty."
        )

    if isinstance(library.storage, SqlLibraryStorage):
        chosen_book = library.storage.get_random_book()

        if chosen_book:
            return BookOut.from_metadata(chosen_book)


@app.get("/books/stats", response_model=BookStatsOut, status_code=200)
def get_stats(library: Library = Depends(sql_library)):
    if isinstance(library.storage, SqlLibraryStorage):
        book_stats = library.storage.get_stats()

        return BookStatsOut(**book_stats)


@app.get("/books/{sql_index}", response_model=BookOut)
def get_book(sql_index: int, library: Library = Depends(sql_library)):
    if isinstance(library.storage, SqlLibraryStorage):
        fetched_book = library.storage.get_by_sql_index(sql_index)

        if not fetched_book:
            raise HTTPException(404, detail="Book does not exist.")

        return BookOut.from_metadata(fetched_book)


@app.delete("/books/{sql_index}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(sql_index: int, library: Library = Depends(sql_library)):

    if not library.remove_by_sql_index(sql_index):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found."
        )


@app.get("/search/google", response_model=list[BookSearchResult])
def show_results(
    q: str = Query(min_length=1),
    results: int = Query(default=10, le=20, ge=1),
    client: GoogleBooksClient = Depends(google_client),
):
    book_list = client.search_books(q, results)

    if not book_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No books found"
        )

    return [
        BookSearchResult(
            title=book.title,
            author=book.author,
            date_published=book.date_published,
            book_id=book.book_id,
            isbn=book.isbn,
        )
        for book in book_list
    ]


@app.post(
    "/books/from-google/{book_id}",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
)
def post_book(
    book_id: str,
    library: Library = Depends(sql_library),
    client: GoogleBooksClient = Depends(google_client),
):
    try:
        book = client.get_book_by_id(book_id)
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found.")

    if library.check_book_exists(book.book_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Book already in library."
        )

    library.add(book)

    if isinstance(library.storage, SqlLibraryStorage):
        meta_book = library.storage.get_with_metadata(book)

        return BookOut.from_metadata(meta_book)


@app.put("/books/{sql_index}", response_model=BookOut, status_code=status.HTTP_200_OK)
def update_book(
    sql_index: int, updated_book: BookUpdate, library: Library = Depends(sql_library)
):
    if isinstance(library.storage, SqlLibraryStorage):
        updates = updated_book.model_dump(exclude_none=True, exclude_unset=True)

        if not updates:
            raise HTTPException(status_code=400, detail="No fields provided to update.")

        new_book = library.storage.update_book(sql_index, updates)

        if not new_book:
            raise HTTPException(status_code=404, detail="Book not found.")

        return BookOut.from_metadata(new_book)
