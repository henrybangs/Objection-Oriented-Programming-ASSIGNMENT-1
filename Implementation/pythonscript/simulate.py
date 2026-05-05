import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def borrow(user, book):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/borrow", json={
            "user_id": user,
            "book_id": book
        })
        print(f"BORROW RESPONSE ({user}):", res.json())

async def return_book(user, book):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/return", json={
            "user_id": user,
            "book_id": book
        })
        print(f"RETURN RESPONSE ({user}):", res.json())

async def simulate_multiple_users():
    # 3 students acting at the same time
    await asyncio.gather(
        borrow("STU-001", "BK-301"),
        borrow("STU-002", "BK-301"),
        borrow("STU-003", "BK-301")
    )

    await asyncio.gather(
        return_book("STU-001", "BK-301"),
        return_book("STU-002", "BK-301")
    )

asyncio.run(simulate_multiple_users())
