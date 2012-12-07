from collections import OrderedDict
from threading import Lock

class Cache:
    def __init__(self,size=100):
        if int(size)<1 : raise AttributeError('size < 1 or not a number')
        self.size = size
        self.dict = OrderedDict()
        self.lock = Lock()

    def __getitem__(self,key):
        with self.lock:
            return self.dict[key]

    def __setitem__(self,key,value):
        with self.lock:
            print(len(self.dict))
            while len(self.dict) >= self.size:
                self.dict.popitem(last=False)
            self.dict[key]=value

    def __delitem__(self,key):
        with self.lock:
            del self.dict[key]

if __name__ == "__main__":

    c=Cache(size=3)
    c[1]=100
    c[2]=200
    c[3]=300
    c[4]=400
    print(c[1])

    