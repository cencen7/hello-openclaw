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
