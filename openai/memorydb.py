from collections import defaultdict

class DB:
   class Table:
       def __init__(self):
           self.col_map = {} # col name to col index
           self.rows = []
      
       def insert(self, dic):
           if len(self.col_map) == 0:
               for ind, name in enumerate(dic.keys()):
                   self.col_map[name] = ind
           row = [dic[key] for key in self.col_map.keys()]
           self.rows.append(row)
      
       def query(self, col_names, conds, order_by_col, reverse):
           result =[]
           for row in self.rows:
               satisfy = True
               for cond in conds:
                   col, op, val = cond
                   ind = self.col_map[col]
                   if op == ">":
                       if row[ind] <= val:
                           satisfy = False
                           break
                   if op == "<":
                       if row[ind] >= val:
                           satisfy = False
                           break
                   if op == "=":
                       if row[ind] != val:
                           satisfy = False
                           break
               if not satisfy:
                   continue
               result.append(row)

           # sort
           if len(order_by_col):
               ind = self.col_map[order_by_col]
               result = sorted(result, key = lambda item : item[ind], reverse=reverse)

           # filter
           res = []
           for row in result:
               item = {}
               for col in col_names:
                   ind = self.col_map[col]
                   item[col] = row[ind]
               res.append(item)
           return res

   def __init__(self):
       self.tables = {} # table name to Table
  
   def insert(self, name, dic):
       if name not in self.tables:
           new_table = self.Table()
           self.tables[name] = new_table
       self.tables[name].insert(dic)

   # assume all condtions are AND
   def query(self, table_name, col_names, conds = [], order_by_col = "", reverse = False):
       table = self.tables[table_name]
       return table.query(col_names, conds, order_by_col, reverse)




db = DB()
db.insert("users", {"id": "1", "name": "Ada", "birthday": "1815-12-10"})
db.insert("users", {"birthday": "1791-12-26", "id": "2", "name": "Charles"})
db.insert("users", {"id": "3", "name": "Ben", "birthday": "1715-12-11"})
assert db.query("users", ["name"]) == [{"name": "Ada",}, {"name": "Charles"}, {"name": "Ben"}]
assert db.query("users", ["name", "birthday"]) == [{"name": "Ada", "birthday": "1815-12-10"}, {"name": "Charles", "birthday": "1791-12-26"}, {"name": "Ben", "birthday": "1715-12-11"}]
# should return [{"name": "Ada",}, {"name": "Charles"}]

assert db.query("users", ["name"], [["birthday", ">", "1800-01-01"]]) == [{"name": "Ada"}]

assert db.query("users", ["name"], [["birthday", "<", "1800-01-01"]], "birthday") == [{'name': 'Ben'}, {'name': 'Charles'}]
assert db.query("users", ["name"], [["birthday", "<", "1800-01-01"]], "birthday", True) == [{'name': 'Charles'}, {'name': 'Ben'}]