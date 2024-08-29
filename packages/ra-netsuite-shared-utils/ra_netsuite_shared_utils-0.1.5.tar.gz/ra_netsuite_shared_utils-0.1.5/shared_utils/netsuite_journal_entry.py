class NetsuiteJournalItem:
    def __init__(self, account_id, amount, department, class_id, location, memo):
        self.account_id = account_id
        self.amount = abs(float(amount))
        self.department = department
        self.class_id = class_id
        self.location = location
        self.memo = memo
        self.is_debit = float(amount) >= 0
        self.custcol4 = 2 if "CGST" in memo or "SGST" in memo or "IGST" in memo else 1


    def to_dict(self):
        entry_type = "debit" if self.is_debit else "credit"
        return {
            "account": {
                "id": str(self.account_id)
            },
            entry_type: self.amount,
            "department": self.department,
            "class": self.class_id,
            "location": self.location,
            "memo": self.memo,
            "custcol4": self.custcol4
        }
