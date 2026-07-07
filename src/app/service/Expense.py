from typing import Optional
from pydantic import BaseModel, Field

class Expense(BaseModel):
    """Information about a transaction made on any Card"""

    amount: Optional[str] = Field(title="expense", description="Expense made on the transaction")
    merchant: Optional[str] = Field(title="merchant", description="Merchant name whom the transaction has been made")
    currency: Optional[str] = Field(title="currency", description="Currency of the transaction")
    user_id: Optional[str] = Field(default=None, title="user_id", description="ID of the user who made the transaction")

    def serialize(self):
        return {
            "amount": self.amount,
            "merchant": self.merchant,
            "currency": self.currency,
            "user_id": self.user_id
        }
    