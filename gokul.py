import mydb
d = mydb.mydb('myfile.db')
d['hello'] = 17          # able to use string or int or float as key
d[183] = [12, 14, 24]    # able to store lists as values (will probably internally jsonify it?)
d.flush()                # easy to flush on disk 




from sqlitedict import SqliteDict

mydict = SqliteDict('./my_db.sqlite', autocommit=True)
mydict['some_key'] = any_picklable_object
print(mydict['some_key'])
for key, value in mydict.items():
    print(key, value)
print(len(mydict))
mydict.close()




import os
import random
from contextlib import closing

import lipsum
from sqlitedict import SqliteDict

def main():
    with closing(SqliteDict('./my_db.sqlite', autocommit=True)) as d:
        for _ in range(100000):
            v = lipsum.generate_paragraphs(2)[0:random.randint(200, 1000)]
            d[os.urandom(10)] = v

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    import json

from wiredtiger import wiredtiger_open


WT_NOT_FOUND = -31803


class WTDict:
    """Create a wiredtiger backed dictionary"""

    def __init__(self, path, config='create'):
        self._cnx = wiredtiger_open(path, config)
        self._session = self._cnx.open_session()
        # define key value table
        self._session.create('table:keyvalue', 'key_format=S,value_format=S')
        self._keyvalue = self._session.open_cursor('table:keyvalue')

    def __enter__(self):
        return self

    def close(self):
        self._cnx.close()

    def __exit__(self, *args, **kwargs):
        self.close()

    def _loads(self, value):
        return json.loads(value)

    def _dumps(self, value):
        return json.dumps(value)

    def __getitem__(self, key):
        self._session.begin_transaction()
        self._keyvalue.set_key(key)
        if self._keyvalue.search() == WT_NOT_FOUND:
            raise KeyError()
        out = self._loads(self._keyvalue.get_value())
        self._session.commit_transaction()
        return out

    def __setitem__(self, key, value):
        self._session.begin_transaction()
        self._keyvalue.set_key(key)
        self._keyvalue.set_value(self._dumps(value))
        self._keyvalue.insert()
        self._session.commit_transaction()
        
        
        
        
        
        #!/usr/bin/env python3

import os
import random

import lipsum
from wtdict import WTDict


def main():
    with WTDict('wt') as wt:
        for _ in range(100000):
            v = lipsum.generate_paragraphs(2)[0:random.randint(200, 1000)]
            wt[os.urandom(10)] = v

if __name__ == '__main__':
    main()




import pysos
t = time.time()
import time
N = 100 * 1000
db = pysos.Dict("test.db")
for i in range(N):
    db["key_" + str(i)] = {"some": "object_" + str(i)}
db.close()

print('PYSOS time:', time.time() - t)
# => PYSOS time: 3.424309253692627




import json
from lmdbm import Lmdb

class JsonLmdb(Lmdb):
  def _pre_key(self, value):
    return value.encode("utf-8")
  def _post_key(self, value):
    return value.decode("utf-8")
  def _pre_value(self, value):
    return json.dumps(value).encode("utf-8")
  def _post_value(self, value):
    return json.loads(value.decode("utf-8"))

with JsonLmdb.open("test.db", "c") as db:
  db["key"] = {"some": "object"}
  obj = db["key"]
  print(obj["some"])  # prints "object"
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 