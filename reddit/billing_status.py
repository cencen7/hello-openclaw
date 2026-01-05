"""
纯手写parsing json


We accidentally dropped the database where we store the current billing status for our advertisers. Fortunately, we still have the logs for all the transactions they did, and we can use this to recreate the dropped data.
Part 1
You are asked to process the financial transactions from the old system to build up a BillingStatus per user to be stored in our new system.
You should create a class called BillingStatus, which will represent an account state. Each financial transaction represents a modification to a BillingStatus. A BillingStatus should be able to ingest new transactions that are generated in our own systems.
Given a collection of financial transactions, we want to generate a BillingStatus instance for each user. This can be represented as a dict:
{ user_id: BillingStatus(), user_id2: BillingStatus()}
Our BillingStatus class should start with two monetary columns:
'ad_delivery_pennies': 0, 'payment_pennies': 0
Each transaction can have multiple monetary columns. Upon processing a transaction, the values in the monetary columns should be added to the current value in the BillingStatus.
Given this input:
monetary_columns = ('ad_delivery_pennies','payment_pennies')
transactions = {
'ff8bc1c2-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000001},
'ff8bc2e4-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000002},
'ff8bc4ec-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'payment_pennies': 500, 'transaction_timestamp': 1500000003},
'fv24z4ec-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'payment_pennies': 500, 'transaction_timestamp': 1500000004}
}
JSON
{"ff8bc1c2-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000001}, "ff8bc2e4-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000002}, "ff8bc4ec-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "payment_pennies": 500, "transaction_timestamp": 1500000003}, "fv24z4ec-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "payment_pennies": 500, "transaction_timestamp": 1500000004}}
Expected Output (format however you want):
{1: BillingStatus(‘ad_delivery_pennies’=3000, ‘payment_pennies’=1000)}

Part 2
Now let's add a concept of an "overwrite transaction" where the transaction can indicate whether it should overwrite the current BillingStatus monetary value with the monetary value in the transaction.
monetary_columns = ('ad_delivery_pennies','payment_pennies')
transactions = {
'ff8ba98a-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000001,'overwrite': False},
'ff8bad4a-8d45-11e9-bc42-526af7764f64': {'user_id': 2, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000004},
'ff8baea8-8d45-11e9-bc42-526af7764f64': {'user_id': 2, 'payment_pennies': 600, 'transaction_timestamp': 1500000007,'overwrite': False},
'ff8bb4ac-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000002,'overwrite': False},
'ff8bb600-8d45-11e9-bc42-526af7764f64': {'user_id': 2, 'ad_delivery_pennies': 1000, 'payment_pennies': 500, 'transaction_timestamp': 1500000003,'overwrite': False},
'ff8bb89e-8d45-11e9-bc42-526af7764f64': {'user_id': 2, 'payment_pennies': 2000, 'transaction_timestamp': 1500000005,'overwrite': True},
'ff8bb9c0-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'payment_pennies': 500, 'transaction_timestamp': 1500000003, 'overwrite': False},
'ff8bbf74-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'payment_pennies': 500, 'transaction_timestamp': 1500000004, 'overwrite': True},
'ff8bc0a0-8d45-11e9-bc42-526af7764f64': {'user_id': 2, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000001},
'ff8bc1c2-8d45-11e9-bc42-526af7764f64': {'user_id': 2, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000002},
'ff923488-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'payment_pennies': 100, 'transaction_timestamp': 1500000013},
}
output = {
1: BillingStatus('ad_delivery_pennies'=1000, 'payment_pennies'=600),
2: BillingStatus('ad_delivery_pennies'=4000, 'payment_pennies'=2600),
}
JSON
{"ff8ba98a-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000001, "overwrite": false}, "ff8bad4a-8d45-11e9-bc42-526af7764f64": {"user_id": 2, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000004}, "ff8baea8-8d45-11e9-bc42-526af7764f64": {"user_id": 2, "payment_pennies": 600, "transaction_timestamp": 1500000007, "overwrite": false}, "ff8bb4ac-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000002, "overwrite": false}, "ff8bb600-8d45-11e9-bc42-526af7764f64": {"user_id": 2, "ad_delivery_pennies": 1000, "payment_pennies": 500, "transaction_timestamp": 1500000003, "overwrite": false}, "ff8bb89e-8d45-11e9-bc42-526af7764f64": {"user_id": 2, "payment_pennies": 2000, "transaction_timestamp": 1500000005, "overwrite": true}, "ff8bb9c0-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "payment_pennies": 500, "transaction_timestamp": 1500000003, "overwrite": false}, "ff8bbf74-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "payment_pennies": 500, "transaction_timestamp": 1500000004, "overwrite": true}, "ff8bc0a0-8d45-11e9-bc42-526af7764f64": {"user_id": 2, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000001}, "ff8bc1c2-8d45-11e9-bc42-526af7764f64": {"user_id": 2, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000002}, "ff923488-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "payment_pennies": 100, "transaction_timestamp": 1500000013}}

Part 3
Now we want to add an additional concept of 'undo_last' and 'redo_last'. When 'undo_last' is set to True, it will undo a regular transaction before it, where
regular transaction is one of: a transaction without any options ('overwrite', 'undo_last' or 'redo_last') or a transaction with only 'overwrite'. When 'redo_last'
is set to True, it will redo a previously undone transaction, if non transactions were reverted then this operation can discarded.
monetary_columns = ('ad_delivery_pennies','payment_pennies')
transactions = {
'ff8bc1c2-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000001},
'ff8bc2e4-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'undo_last': True, 'transaction_timestamp': 1500000002},
'ff8bc4ec-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'payment_pennies': 500, 'transaction_timestamp': 1500000003},
'fv24z4ec-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'payment_pennies': 500, 'transaction_timestamp': 1500000004}
}
output = {
1: BillingStatus('ad_delivery_pennies'=1000, 'payment_pennies'=1000),
}
JSON
{"ff8bc1c2-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000001}, "ff8bc2e4-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "undo_last": true, "transaction_timestamp": 1500000002}, "ff8bc4ec-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "payment_pennies": 500, "transaction_timestamp": 1500000003}, "fv24z4ec-8d45-11e9-bc42-526af7764f64": {"user_id": 1, "ad_delivery_pennies": 1000, "payment_pennies": 500, "transaction_timestamp": 1500000004}}



代码


################ level 2 ########################
class BillingStatus:
def __init__(self):
self.ad_delivery_pennies = 0
self.payment_pennies = 0

def ingest_transaction(self, transaction):
for key in ('ad_delivery_pennies', 'payment_pennies'):
if key in transaction:
if transaction.get('overwrite', False):
setattr(self, key, transaction[key])
else:
setattr(self, key, getattr(self, key) + transaction[key])

def __repr__(self):
return f"BillingStatus(ad_delivery_pennies={self.ad_delivery_pennies}, payment_pennies={self.payment_pennies})"

def process_transactions(transactions):
user_billing_status = {}

for transaction in transactions.values():
user_id = transaction['user_id']
if user_id not in user_billing_status:
user_billing_status[user_id] = BillingStatus()
user_billing_status[user_id].ingest_transaction(transaction)

return user_billing_status

第一问问了很多edge case，需要按时间排序吗，monetary columns会变吗，为了考虑这些因素稍微耽误了点时间
第二问加了overwrite后output不对，那个log又臭又长很难检查，加上时间不够有点紧张，最后面试官提示是第一问没有implement的一个点，想到是时间排序最后写对了。
第三问只有五分钟了，就讲了下思路。。不过面试官一直在给予肯定
"""

monetary_columns = ('ad_delivery_pennies','payment_pennies')
transactions = {
'ff8bc1c2-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000001},
'ff8bc2e4-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'transaction_timestamp': 1500000002},
'ff8bc4ec-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'payment_pennies': 500, 'transaction_timestamp': 1500000003},
'fv24z4ec-8d45-11e9-bc42-526af7764f64': {'user_id': 1, 'ad_delivery_pennies': 1000, 'payment_pennies': 500, 'transaction_timestamp': 1500000004}
}


from typing import Dict, Iterable, Any, Tuple, List


class BillingStatus:
    """Running billing status for a single user."""
    def __init__(self) -> None:
        self.values = {}
        # transations have done and took effect
        self.appied_stack: List[Dict[str, Any]] = []
        # transations have undone, could be redo
        self.undone_stack: List[Dict[str, Any]] = []

    @classmethod
    def with_columns(cls, monetary_columns: Iterable[str]) -> 'BillingStatus':
        """Create a BillingStatus with specified monetary columns initialized to 0."""
        bs = cls()
        for col in monetary_columns:
            bs.values[col] = 0
        return bs
    
    def reserve_effects(self, effects: Dict[str, Any]) -> None:
        for col, e in effects.items():
            if e["op"] == "add":
                self.values[col] -= e["delta"]
            elif e["op"] == "set":
                self.values[col] = e["prev"]
            else:
                raise ValueError(f"Unknown operation {e['op']} for column {col}")
            
    def apply_effects(self, effects: Dict[str, Any]) -> None:
        for col, e in effects.items():
            if e["op"] == "add":
                self.values[col] += e["val"]
            elif e["op"] == "set":
                self.values[col] -= e["new"]
            else:
                raise ValueError(f"Unknown operation {e['op']} for column {col}")
    
    def reverse_transaction(self, tx: Dict[str, Any], monetary_columns:Iterable[str]) -> None:
        """Reverse a single transaction by subtracting its monetary column from the current totals"""
        overwrite = tx.get('overwrite', False)
        for col in monetary_columns:
            if col in tx:
                if overwrite:
                    self.values[col] = tx.get('val_before_overwrite', 0)
                else:
                    self.values[col] -= int(tx[col])
    
    def ingest_transaction(self, tx: Dict[str, Any], monetary_columns:Iterable[str]) -> None:
        """Apply a single transaction by adding its monerary column to the current totals"""
        overwrite = tx.get('overwrite', False)
        redo_last = tx.get('redo_last', False)
        undo_last = tx.get('undo_last', False)
        if undo_last:
            if not self.applied_stack:
                return
            rec = self.applied_stack.pop()
            self.reserve_effects(rec)
            self.undone_stack.append(rec)
            return
        
        if redo_last:
            if not self.undone_stack:
                return
            rec = self.undone_stack.pop()
            self.apply_effects(rec)
            self.applied_stack.append(rec)
            return
        
        effects: Dict[str, Any] = {}
        for col in monetary_columns:
            if col in tx:
                if overwrite:
                    prev = self.values[col]
                    self.values[col] = int(tx[col])
                    effects[col] = {
                        "op": "set",
                        "prev": prev,
                        "new": int(tx[col]),
                    }
                else:
                    self.values[col] += int(tx[col])
                    effects[col] = {
                        "op": "add",
                        "delta": int(tx[col]),
                        "val": int(tx[col])
                    }
        if effects:
            self.applied_stack.append(effects)
            self.undone_stack.clear()

    def __repr__(self) -> str:
        cols = ", ".join(f"'{k}'={v}" for k, v in self.values.items())
        return f"BillingStatus({cols})"
    

def build_billing_status_by_user(
        transactions: Dict[str, Dict[str, Any]],
        monetary_columns: Tuple[str, ...]) -> Dict[int, BillingStatus]:
    """
    Build {user_id: BillingStatus} from transation logs.
    Only additive updates; overwrite transactions.

    Time complexity: sorting dominates → O(n log n) for n transactions;
    ingest is O(n * m) where m=len(monetary_columns).
    """
    ordered: List[Tuple[str, Dict[str, Any]]] = sorted(
        transactions.items(),
        key=lambda item: item[1]['transaction_timestamp']
    )
    result: Dict[int, BillingStatus] = {}
    for _, tx in ordered:
        user_id = tx['user_id']
        if user_id not in result:
            result[user_id] = BillingStatus.with_columns(monetary_columns)
        result[user_id].ingest_transaction(tx, monetary_columns)
    return result





if __name__ == "__main__":
    monetary_columns = ("ad_delivery_pennies", "payment_pennies")
    transactions = {
        "ff8bc1c2-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000001
        },
        "ff8bc2e4-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1, "ad_delivery_pennies": 1000, "transaction_timestamp": 1500000002
        },
        "ff8bc4ec-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1, "payment_pennies": 500, "transaction_timestamp": 1500000003
        },
        "fv24z4ec-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1, "ad_delivery_pennies": 1000, "payment_pennies": 500, "transaction_timestamp": 1500000004
        },
    }

    out = build_billing_status_by_user(transactions, monetary_columns)
    print(out)

    transactions2 = {
        "ff8ba98a-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1,
            "ad_delivery_pennies": 1000,
            "transaction_timestamp": 1500000001,
            "overwrite": False,
        },
        "ff8bad4a-8d45-11e9-bc42-526af7764f64": {
            "user_id": 2,
            "ad_delivery_pennies": 1000,
            "transaction_timestamp": 1500000004,
        },
        "ff8baea8-8d45-11e9-bc42-526af7764f64": {
            "user_id": 2,
            "payment_pennies": 600,
            "transaction_timestamp": 1500000007,
            "overwrite": False,
        },
        "ff8bb4ac-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1,
            "ad_delivery_pennies": 1000,
            "transaction_timestamp": 1500000002,
            "overwrite": False,
        },
        "ff8bb600-8d45-11e9-bc42-526af7764f64": {
            "user_id": 2,
            "ad_delivery_pennies": 1000,
            "payment_pennies": 500,
            "transaction_timestamp": 1500000003,
            "overwrite": False,
        },
        "ff8bb89e-8d45-11e9-bc42-526af7764f64": {
            "user_id": 2,
            "payment_pennies": 2000,
            "transaction_timestamp": 1500000005,
            "overwrite": True,
        },
        "ff8bb9c0-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1,
            "payment_pennies": 500,
            "transaction_timestamp": 1500000003,
            "overwrite": False,
        },
        "ff8bbf74-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1,
            "ad_delivery_pennies": 1000,
            "payment_pennies": 500,
            "transaction_timestamp": 1500000004,
            "overwrite": True,
        },
        "ff8bc0a0-8d45-11e9-bc42-526af7764f64": {
            "user_id": 2,
            "ad_delivery_pennies": 1000,
            "transaction_timestamp": 1500000001,
        },
        "ff8bc1c2-8d45-11e9-bc42-526af7764f64": {
            "user_id": 2,
            "ad_delivery_pennies": 1000,
            "transaction_timestamp": 1500000002,
        },
        "ff923488-8d45-11e9-bc42-526af7764f64": {
            "user_id": 1,
            "payment_pennies": 100,
            "transaction_timestamp": 1500000013,
        },
    }

    out2 = build_billing_status_by_user(transactions2, monetary_columns)
    print(out2)
