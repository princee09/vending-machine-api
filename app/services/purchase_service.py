import time
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Item


def purchase(db: Session, item_id: str, cash_inserted: int) -> dict:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise ValueError("item_not_found")
    #Bug found 9.
#  Validate cash_inserted can be composed of supported denominations
    if not can_make_amount(cash_inserted, settings.SUPPORTED_DENOMINATIONS):
        raise ValueError("invalid_denomination")
    # time.sleep(0.05)  # demo: widens race window for concurrent purchase/restock
 #bug found 8. purchase function has a race condition due to the delay between checking quantity and decrementing it.
    if item.quantity <= 0:
        raise ValueError("out_of_stock")
    if cash_inserted < item.price:
        raise ValueError("insufficient_cash", item.price, cash_inserted)
    # No validation that cash_inserted or change use SUPPORTED_DENOMINATIONS
    change = cash_inserted - item.price
#Validate change can be returned with supported denominations
    if not can_make_amount(change, settings.SUPPORTED_DENOMINATIONS):
        raise ValueError("cannot_make_change")
    item.quantity -= 1
    item.slot.current_item_count -= 1
    db.commit()
    db.refresh(item)
    return {
        "item": item.name,
        "price": item.price,
        "cash_inserted": cash_inserted,
        "change_returned": change,
        "remaining_quantity": item.quantity,
        "message": "Purchase successful",
    }


def change_breakdown(change: int) -> dict:
    denominations = sorted(settings.SUPPORTED_DENOMINATIONS, reverse=True)
    result: dict[str, int] = {}
    remaining = change
    for d in denominations:
        if remaining <= 0:
            break
        count = remaining // d
        if count > 0:
            result[str(d)] = count
            remaining -= count * d
    return {"change": change, "denominations": result}

#add validation to ensure cash_inserted can be composed of supported denominations:

def can_make_amount(amount: int, denominations: list[int]) -> bool:
    """Check if amount can be composed using given denominations (greedy check)"""
    if amount == 0:
        return True
    remaining = amount
    for d in sorted(denominations, reverse=True):
        remaining = remaining % d
    return remaining == 0