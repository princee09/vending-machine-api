# Vending Machine API


This project contains **a number of hidden bugs**. Your task is to **debug and fix them**. The goal is to solve as many as you can—it’s okay if you don’t find all of them.

**Reference:** The correct API behaviour is defined in [api-specifications.md](api-specifications.md). Use it as the source of truth.

**Workflow:** Fork this repository and do all your work (and commits) in your fork.

**Code quality:** Read and understand the existing code and your own changes. Don’t apply fixes without understanding what the code does and why you’re changing it.

**AI tools:** You may use AI tools. If you do, you **must share the relevant chat history with us during the interview**.

### Mandatory for the interview

- Bring your laptop.
- Ensure the project is set up on your machine before you come.
- If you used AI, have the chat history ready to share.

---

FastAPI-based REST API for a vending machine system. See [api-specifications.md](api-specifications.md) for full specifications.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration

Set environment variables (optional; defaults shown):

- `MAX_SLOTS` – maximum number of slots (default: `10`)
- `MAX_ITEMS_PER_SLOT` – optional per-slot item limit
- `DATABASE_URL` – database URL (default: `sqlite:///./vending.db`)

Example:

```bash
export MAX_SLOTS=20
```

## Run

```bash
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

## Endpoints

- `POST /slots` – create slot
- `GET /slots` – list slots
- `GET /slots/full-view` – slots with nested items
- `DELETE /slots/{slot_id}` – remove slot
- `POST /slots/{slot_id}/items` – add item to slot
- `POST /slots/{slot_id}/items/bulk` – bulk add items
- `GET /slots/{slot_id}/items` – list items in slot
- `GET /items/{item_id}` – get single item
- `PATCH /items/{item_id}/price` – update item price
- `DELETE /slots/{slot_id}/items/{item_id}` – remove item or quantity
- `DELETE /slots/{slot_id}/items` – clear slot or remove specific items
- `POST /purchase` – purchase item
- `GET /purchase/change-breakdown?change=<amount>` – change denomination breakdown
- `GET /health` – health check
