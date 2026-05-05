from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()

# -----------------------------
# In-memory "database"
# -----------------------------
books = {
    "BK-301": {"title": "Database Systems (Limkokwing Edition)", "available": 2},
    "BK-102": {"title": "Network Security Basics", "available": 1}
}

# active loans storage
loans = {}

# -----------------------------
# Request Models
# -----------------------------
class BorrowRequest(BaseModel):
    user_id: str
    book_id: str

class ReturnRequest(BaseModel):
    user_id: str
    book_id: str


# -----------------------------
# BORROW ENDPOINT
# -----------------------------
@app.post("/borrow")
async def borrow_book(request: BorrowRequest):
    # simulate processing delay (real-world API behavior)
    await asyncio.sleep(1)

    book = books.get(request.book_id)

    # check if book exists
    if not book:
        return {"status": "error", "message": "Book not found in Limkokwing library system"}

    # check availability
    if book["available"] <= 0:
        return {"status": "failed", "message": "No copies available right now"}

    # reduce available copies
    book["available"] -= 1

    # store loan record
    loans.setdefault(request.user_id, []).append(request.book_id)

    return {
        "status": "success",
        "message": f"{request.user_id} borrowed {book['title']}",
        "remaining_copies": book["available"]
    }


# -----------------------------
# RETURN ENDPOINT
# -----------------------------
@app.post("/return")
async def return_book(request: ReturnRequest):
    await asyncio.sleep(1)

    book = books.get(request.book_id)

    if not book:
        return {"status": "error", "message": "Invalid book ID"}

    # check if user actually borrowed it
    user_loans = loans.get(request.user_id, [])

    if request.book_id not in user_loans:
        return {"status": "failed", "message": "This user did not borrow this book"}

    # remove from user loans
    user_loans.remove(request.book_id)

    # increase available copies
    book["available"] += 1

    return {
        "status": "success",
        "message": f"{request.user_id} returned {book['title']}",
        "available_copies": book["available"]
    }
