class hasinfo(type):
    def __new__(metaclass, classname, baseclasses, classdict):
        if len(baseclasses) and not '__info__' in classdict:
            raise TypeError('does not have __info__')
        return type.__new__(metaclass, classname, baseclasses, classdict)

class withinfo(metaclass=hasinfo):
    pass

class correct(withinfo):
    def __info__(self): pass

class incorrect(withinfo):
    pass
