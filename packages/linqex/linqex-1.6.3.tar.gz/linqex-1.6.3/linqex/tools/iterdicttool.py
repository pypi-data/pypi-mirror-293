from linqex.utils import *

from typing import Dict, List, Callable, Union, NoReturn, Optional, Tuple, Type, Generic
from numbers import Number
from collections import OrderedDict
import itertools

class EnumerableDictTool(Generic[_TK,_TV]):
    
    def __init__(self, iterable:Optional[Dict[_TK,_TV]]=None):
        if iterable is None:
            iterable:Dict[_TK,_TV] = dict()
        if isinstance(iterable, dict):
            self.iterable:Dict[_TK,_TV] = iterable
        elif isinstance(iterable, list):
            self.iterable:Dict[_TK,_TV] = dict(iterable)
        else:
            raise TypeError("Must be dict, not {}".format(str(type(iterable))[8,-2]))

    def Get(self, *key:_TK) -> Union[Dict[_TK,_TV],_TV]:
        iterable = self.iterable
        for k in key:
            if  k in EnumerableDictTool(iterable).GetKeys():
                iterable = iterable[k]
            else:
                raise KeyError(k)
        return iterable
    
    def GetKey(self, value:_TV) -> _TK:
        return {v: k for k, v in self.GetItems()}[value]
    
    def GetKeys(self) -> List[_TK]:
        return list(self.Get().keys())
    
    def GetValues(self) -> List[_TV]:
        return list(self.Get().values())
    
    def GetItems(self) -> List[Tuple[_TK,_TV]]:
        return list(self.Get().items())
    
    def Copy(self) -> Dict[_TK,_TV]:
        return self.Get().copy()



    def Take(self, count:int) -> Dict[_TK,_TV]:
        return dict(self.GetItems()[:count])
    
    def TakeLast(self, count:int) -> Dict[_TK,_TV]:
        return self.Skip(self.Lenght()-count)
    
    def Skip(self, count:int) -> Dict[_TK,_TV]:
        return dict(self.GetItems()[count:])
    
    def SkipLast(self, count:int) -> Dict[_TK,_TV]:
        return self.Take(self.Lenght()-count)
    
    def Select(self, 
        selectFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        selectFuncByKey:Callable[[_TK,_TV],_TFK]=lambda key, value: key
    ) -> Dict[_TFK,_TFV]:
        return dict(list(map(lambda key, value: (selectFuncByKey(key,value), selectFunc(key,value)), self.GetKeys(), self.GetValues())))
    
    def Distinct(self, distinctFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value) -> Dict[_TK,_TV]:
        newIterable = self.Copy()
        for key, value in self.GetItems():
            if EnumerableDictTool(EnumerableDictTool(newIterable).Select(distinctFunc)).Count(distinctFunc(key, value)) > 1:
                EnumerableDictTool(newIterable).Delete(key)
        return newIterable
    
    def Except(self, *value:_TV) -> Dict[_TK,_TV]:
        return self.Where(lambda k, v: not v in value)
    
    def ExceptByKey(self, *key:_TK) -> Dict[_TK,_TV]:
        return self.Where(lambda k, v: not k in key)

    def InnerJoin(self, iterable: Dict[_TK2,_TV2], 
        innerFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[_TK2,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK2]=lambda inKey, inValue, outKey, outValue: inKey
    ) -> Dict[_TFK2,_TFV2]:
        newValueIterable:List[_TFV2] = []
        newKeyIterable: List[_TFK2] = []
        def JoinFunc(inKey:_TK, inValue:_TV, outKey:_TK2, outValue:_TV2):
            nonlocal newKeyIterable, newValueIterable
            newKeyIterable.append(joinFuncByKey(inKey, inValue, outKey, outValue))
            newValueIterable.append(joinFunc(inKey, inValue, outKey, outValue))
        for inKey, inValue in EnumerableDictTool(self.Get()).GetItems():
            outer = EnumerableDictTool(iterable).Where(lambda outKey, outValue: outerFunc(outKey,outValue) == innerFunc(inKey, inValue))
            EnumerableDictTool(outer).Loop(lambda outKey, outValue: JoinFunc(inKey, inValue, outKey, outValue))
        return dict(zip(newKeyIterable, newValueIterable))

    def LeftJoin(self, iterable: Dict[_TK2,_TV2], 
        innerFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[_TK2,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK2]=lambda inKey, inValue, outKey, outValue: inKey,
    ) -> Dict[_TFK2,_TFV2]:
        newValueIterable:List[_TFV2] = []
        newKeyIterable: List[_TFK2] = []
        def JoinFunc(inKey:_TK, inValue:_TV, outKey:_TK2, outValue:_TV2):
            nonlocal newKeyIterable, newValueIterable
            newKeyIterable.append(joinFuncByKey(inKey, inValue, outKey, outValue))
            newValueIterable.append(joinFunc(inKey, inValue, outKey, outValue))
        for inKey, inValue in EnumerableDictTool(self.Get()).GetItems():
            outer = EnumerableDictTool(iterable).Where(lambda outKey, outValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
            if outer == []: 
                newKeyIterable.append(joinFuncByKey(inKey, inValue, None, None))
                newValueIterable.append(joinFunc(inKey, inValue, None, None))
            else:
                EnumerableDictTool(outer).Loop(lambda outKey, outValue: JoinFunc(inKey, inValue, outKey, outValue))
        return dict(zip(newKeyIterable, newValueIterable))

    def RightJoin(self, iterable: Dict[_TK2,_TV2], 
        innerFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[_TK2,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK2]=lambda inKey, inValue, outKey, outValue: inKey
    ) -> Dict[_TFK2,_TFV2]:
        newValueIterable:List[_TFV2] = []
        newKeyIterable: List[_TFK2] = []
        def JoinFunc(inKey:_TK, inValue:_TV, outKey:_TK2, outValue:_TV2):
            nonlocal newKeyIterable, newValueIterable
            newKeyIterable.append(joinFuncByKey(inKey, inValue, outKey, outValue))
            newValueIterable.append(joinFunc(inKey, inValue, outKey, outValue))
        for outKey, outValue in EnumerableDictTool(iterable).GetItems():
            inner = EnumerableDictTool(self.Get()).Where(lambda inKey, inValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
            if inner is None:
                newKeyIterable.append(joinFuncByKey(None, None, outKey, outValue))
                newValueIterable.append(joinFunc(None, None, outKey, outValue))
            else:
                EnumerableDictTool(inner).Loop(lambda inKey, inValue: JoinFunc(inKey, inValue, outKey, outValue))
        return dict(zip(newKeyIterable, newValueIterable))
      
    def OrderBy(self, *orderByFunc:Tuple[Callable[[_TK,_TV],Union[Tuple[_TFV],_TFV]],_Desc]) -> Dict[_TK,_TV]:
        if orderByFunc == ():
            orderByFunc = ((lambda key, value: value, False))
        iterable = self.GetItems()
        orderByFunc = list(reversed(orderByFunc))
        for func, desc in orderByFunc:
            iterable = sorted(iterable, key=lambda x: func(x[0], x[1]), reverse=desc)
        return OrderedDict(iterable)
        
    def GroupBy(self, groupByFunc:Callable[[_TK,_TV],Union[Tuple[_TFV],_TFV]]=lambda key, value: value) -> Dict[Union[Tuple[_TFV],_TFV], Dict[_TK,_TV]]:
        iterable = EnumerableDictTool(self.OrderBy((groupByFunc, False))).GetItems()
        iterable = itertools.groupby(iterable, lambda items: groupByFunc(items[0], items[1]))
        return {keys : dict(group) for keys, group in iterable}

    def Reverse(self) -> Dict[_TK,_TV]:
            return dict(zip(reversed(self.GetKeys()),reversed(self.GetValues())))
        
    def Zip(self, iterable:Dict[_TK2,_TV2], 
        zipFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        zipFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK]=lambda inKey, inValue, outKey, outValue: inKey
    ) -> Dict[_TFK,_TFV]:
        newIterable = EnumerableDictTool(dict(zip(self.GetKeys(),list(zip(self.GetValues(), EnumerableDictTool(iterable).GetItems())))))
        return newIterable.Select(lambda key, value: zipFunc(key, value[0], value[1][0], value[1][1]), lambda key, value: zipFuncByKey(key, value[0], value[1][0], value[1][1]))



    def Where(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> Dict[_TK,_TV]:
        result = dict()
        for key, value in self.GetItems():
            if conditionFunc(key, value):
                result[key] = value
        return result
    
    def OfType(self, *type:Type) -> List[Tuple[_TK,_TV]]:
        return EnumerableDictTool(self.Where(lambda key, value: isinstance(value,type))).GetItems()
    
    def OfTypeByKey(self, *type:Type) -> List[Tuple[_TK,_TV]]:
        return EnumerableDictTool(self.Where(lambda key, value: isinstance(key,type))).GetItems()
    
    def First(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> Optional[Tuple[_TK,_TV]]:
        for key, value in self.GetItems():
            if conditionFunc(key, value):
                return (key,value)
        return None
    
    def Last(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> Optional[Tuple[_TK,_TV]]:
        result = EnumerableDictTool(self.Where(conditionFunc)).GetItems()
        if len(result) == 0:
            return None
        else:
            return result[-1]
        
    def Single(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> Optional[Tuple[_TK,_TV]]:
        result = EnumerableDictTool(self.Where(conditionFunc)).GetItems()
        if len(result) != 1:
            return None
        else:
            return result[0]



    def Any(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: value) -> bool:
        result = False
        for key, value in self.GetItems():
            if conditionFunc(key, value):
                result = True
                break
        return result
    
    def All(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: value) -> bool:
        result = True
        for key, value in self.GetItems():
            if not conditionFunc(key, value):
                result = False
                break
        return result
    
    def SequenceEqual(self, iterable:Dict[_TK2,_TV2]) -> bool:
        if self.Lenght() != len(iterable):
            return False
        for key, value in self.GetItems():
            if key in iterable.keys():
                if not iterable[key] == value:
                    return False
            else:
                return False
        return True



    def Accumulate(self, accumulateFunc:Callable[[_TV,_TK,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> Dict[_TK,_TFV]:
        firstTemp:bool = True
        def FirstTemp(temp):
            nonlocal firstTemp
            if firstTemp:
                firstTemp = False
                return temp[1]
            else:
                return temp
        if not self.IsEmpty():
            result = dict([self.GetItems()[0]])
            result.update(dict(zip(self.GetKeys()[1:], list(itertools.accumulate(self.GetItems(), lambda temp, next: accumulateFunc(FirstTemp(temp), next[0], next[1])))[1:])))
            return result
        else:
            return {}
        
    def Aggregate(self, accumulateFunc:Callable[[_TV,_TK,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> _TFV:
        return EnumerableDictTool(self.Accumulate(accumulateFunc)).GetValues()[-1]



    def Count(self, value:_TV) -> int:
        return self.GetValues().count(value)
        
    def Lenght(self) -> int:
        return len(self.Get())
    
    def Sum(self) -> Optional[_TV]:
        if self.OfType(Number):
            return sum(self.GetValues())
        else:
            return None
        
    def Avg(self) -> Optional[_TV]:
        if self.OfType(Number):
            return sum(self.GetValues()) / self.Lenght()
        else:
            return None
        
    def Max(self) -> Optional[_TV]:
        if self.OfType(Number):
            return max(self.GetValues())
        else:
            return None
        
    def Min(self) -> Optional[_TV]:
        if self.OfType(Number):
            return min(self.GetValues())
        else:
            return None




    def Add(self, key:_Key, value:_Value):
        self.Get()[key] = value

    def Update(self, key:_TK, value:_Value):
        if key in self.GetKeys():
            self.Get()[key] = value
        else:
            raise KeyError(key)

    def Concat(self, *iterable:Dict[_TK2,_TV2]):
        for i in iterable:
            self.Get().update(i)

    def Union(self, *iterable:Dict[_TK2,_TV2]):
        if not iterable in [(),[]]:
            iterable:list = list(iterable)
            newIterable = EnumerableDictTool()
            filter = self.Where(lambda k, v: v in iterable[0].values() and k in iterable[0].keys())
            EnumerableDictTool(filter).Loop(lambda k, v: newIterable.Add(k, v))
            iterable.pop(0)
            self.Clear()
            self.Concat(newIterable.Get())
            self.Union(*iterable)

    def Delete(self, *key:_TK):
        for k in key:
            self.Get().pop(k)

    def Remove(self, *value:_TV):
        for v in value:
            self.Get().pop(self.First(lambda k, val: val == v)[0])

    def RemoveAll(self, *value:_TV):
        for v in value:
            while True:
                if self.Contains(v):
                    self.Remove(v)
                else:
                    break

    def Clear(self):
        self.Get().clear()



    def Loop(self, loopFunc:Callable[[_TK,_TV],NoReturn]=lambda key, value: print(key,value)):
        for key, value in self.GetItems():
            loopFunc(key, value)



    def ToDict(self) -> Dict[_TK,_TV]:
        return self.Get()

    def ToList(self) -> List[_TV]:
        return self.GetValues()
    
    def ToItem(self) -> List[Tuple[int,_TV]]:
        return list(enumerate(self.GetValues()))



    def IsEmpty(self) -> bool:
        return self.Get() in [[],{}]
    
    def ContainsByKey(self, *key:_TK) -> bool:
        iterable = self.GetKeys()
        for k in key:
            if not k in iterable:
                return False
        return True
    
    def Contains(self, *value:_TV) -> bool:
        iterable = self.GetValues()
        for v in value:
            if not v in iterable:
                return False
        return True


__all__ = ["EnumerableDictTool"]
