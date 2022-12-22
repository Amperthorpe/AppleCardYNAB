from _private import APPLE_CARD_ID, PAYEE_ID, PAYEE_NAME
from datetime import datetime, timedelta
import json


class YNABTransaction:
    def __init__(
        self,
        memo=None,
        date=None,
        category=None,
    ) -> None:
        self.memo = memo
        self.local_date: datetime = date
        self.category = category

        self.amount = 0

    def set_outflow(self, outflow_str: str) -> bool:  # $1.23 -> -1230
        # Validate input
        if "$" not in outflow_str or "." not in outflow_str:
            return False
        outflow_str = outflow_str.removeprefix("$").replace(".", "")
        outflow_str = outflow_str + "0"
        amount = -int(outflow_str)
        self.amount = amount
        return True

    def print(self):
        print(f"{self.memo}: {self.outflow}, {self.local_date}")

    def trans_dict(self) -> dict:
        date_utc = self.local_date - timedelta(hours=8)
        # Timezones are hard. Hardcoded here for PST
        base_dict = {
            "account_id": APPLE_CARD_ID,
            "date": date_utc.strftime(r"%Y-%m-%d"),
            "amount": self.amount,
            "payee_id": PAYEE_ID,
            "payee_name": PAYEE_NAME,
            "category_id": None,
            "memo": self.memo,
            "cleared": "uncleared",
            "approved": True,
            "flag_color": None,
            "import_id": None,
        }
        return base_dict

    @staticmethod
    def json_list(trans_list) -> dict:
        final_dict = {"transactions": []}
        for t in trans_list:
            t: YNABTransaction
            final_dict["transactions"].append(t.trans_dict())
        return final_dict
