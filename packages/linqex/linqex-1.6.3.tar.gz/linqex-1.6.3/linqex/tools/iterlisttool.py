from linqex.utils import *

from typing import Dict, List, Callable, Union, NoReturn, Optional, Tuple, Type, Generic
from numbers import Number
import itertools

class EnumerableListTool(Generic[_TV]):
    
    def __init__(self, iterable:Optional[List[_TV]]=None):
        if iterable is None:
            iterable:List[_TV] = list()
        if isinstance(iterable, list):
            self.iterable:List[_TV] = iterable
        elif isinstance(iterable, (tuple, set)):
            self.iterable:List[_TV] = list(iterable)
        else:
            raise TypeError("Must be tuple, set and list, not {}".format(str(type(iterable))[8,-2]))

    def Get(self, *key:int) -> Union[List[_TV],_TV]:
        iterable = self.iterable
        for k in key:
            if  k < len(iterable):
                iterable = iterable[k]
            else:
                raise IndexError(k)
        return iterable
    
    def GetKey(self, value:_TV) -> int:
        return self.iterable.index(value)
    
    def GetKeys(self) -> List[int]:
        return list(range(len(self.Get())))
    
    def GetValues(self) -> List[_TV]:
        return self.Get()
    
    def GetItems(self) -> List[Tuple[int,_TV]]:
        return list(enumerate(self.Get()))
    
    def Copy(self) -> List[_TV]:
        return self.Get().copy()



    def Take(self, count:int) -> List[_TV]:
        return self.Get()[:count]
    
    def TakeLast(self, count:int) -> List[_TV]:
        return self.Skip(self.Lenght()-count)
    
    def Skip(self, count:int) -> List[_TV]:
        return self.Get()[count:]
    
    def SkipLast(self, count:int) -> List[_TV]:
        return self.Take(self.Lenght()-count)
    
    def Select(self, selectFunc:Callable[[_TV],_TFV]=lambda value: value) -> List[_TFV]:
        return list(map(selectFunc,self.Get()))
    
    def Distinct(self, distinctFunc:Callable[[_TV],_TFV]=lambda value: value) -> List[_TV]:
        newIterable = self.Copy()
        indexStep = 0
        for key, value in self.GetItems():
            if EnumerableListTool(EnumerableListTool(newIterable).Select(distinctFunc)).Count(distinctFunc(value)) > 1:
                EnumerableListTool(newIterable).Delete(key-indexStep)
                indexStep += 1
        return newIterable
    
    def Except(self, *value:_TV) -> List[_TV]:
        return list(zip(*self.Where(lambda v: not v in value)))[1]  
      
    def InnerJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue)
    ) -> List[_TFV2]:
        newIterable:EnumerableListTool[_TFK2] = EnumerableListTool()
        for inValue in self.Get():
            outer = EnumerableListTool(iterable).Where(lambda outValue: outerFunc(outValue) == innerFunc(inValue))
            EnumerableListTool(outer).Loop(lambda outItem: newIterable.Add(joinFunc(inValue, outItem[1])))
        return newIterable.Get()
        
    def LeftJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue)
    ) -> List[_TFV2]:
        newIterable:EnumerableListTool[_TFK2] = EnumerableListTool()
        for inValue in self.Get():
            outer = EnumerableListTool(iterable).Where(lambda outValue: outerFunc(outValue) == innerFunc(inValue))
            if outer == []: newIterable.Add(joinFunc(inValue, None))
            else: EnumerableListTool(outer).Loop(lambda outItem: newIterable.Add(joinFunc(inValue, outItem[1])))
        return newIterable.Get()

    def RightJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue)
    ) -> List[_TFV2]:
        newIterable:EnumerableListTool[_TFK2] = EnumerableListTool()
        for outValue in iterable:
            inner = EnumerableListTool(self.Get()).Where(lambda inValue: outerFunc(outValue) == innerFunc(inValue))
            if inner == []: newIterable.Add(joinFunc(None, outValue))
            else: EnumerableListTool(inner).Loop(lambda inItem: newIterable.Add(joinFunc(inItem[1], outValue)))
        return newIterable.Get()

    def OrderBy(self, *orderByFunc:Tuple[Callable[[_TV],Union[Tuple[_TFV],_TFV]],_Desc]) -> List[_TV]:
        if orderByFunc == ():
            orderByFunc = ((lambda value: value, False))
        iterable = self.Get()
        orderByFunc:list = list(reversed(orderByFunc))
        for func, desc in orderByFunc:
            iterable = sorted(iterable, key=func, reverse=desc)
        return list(iterable)
        
    def GroupBy(self, groupByFunc:Callable[[_TV],Union[Tuple[_TFV],_TFV]]=lambda value: value) -> List[Tuple[Union[Tuple[_TFV],_TFV], List[_TV]]]:
        iterable = self.OrderBy((groupByFunc, False))
        iterable = itertools.groupby(iterable, groupByFunc)
        return [(keys, list(group)) for keys, group in iterable]

    def Reverse(self) -> List[_TV]:
        return list(reversed(self.Get()))
        
    def Zip(self, iterable:List[_TV2], zipFunc:Callable[[_TV,_TV2],_TFV]=lambda inValue, outValue: (inValue, outValue)) -> List[_TFV]:
        newIterable = EnumerableListTool(list(zip(self.GetValues(), EnumerableListTool(iterable).GetValues())))
        return newIterable.Select(lambda value: zipFunc(value[0], value[1]))



    def Where(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> List[Tuple[int,_TV]]:
        result = list()
        for index, value in self.GetItems():
            if conditionFunc(value):
                result.append((index, value))
        return result
    
    def OfType(self, *type:Type) -> List[Tuple[int,_TV]]:
        return self.Where(lambda value: isinstance(value,type))
    
    def First(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional[Tuple[int,_TV]]:
        for index, value in self.GetItems():
            if conditionFunc(value):
                return (index,value)
        return None
    
    def Last(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) == 0:
            return None
        else:
            return result[-1]
        
    def Single(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) != 1:
            return None
        else:
            return result[0]



    def Any(self, conditionFunc:Callable[[_TV],bool]=lambda value: value) -> bool:
        result = False
        for value in self.Get():
            if conditionFunc(value):
                result = True
                break
        return result
    
    def All(self, conditionFunc:Callable[[_TV],bool]=lambda value: value) -> bool:
        result = True
        for value in self.Get():
            if not conditionFunc(value):
                result = False
                break
        return result
    
    def SequenceEqual(self, iterable:List[_TV2]) -> bool:
        if self.Lenght() != len(iterable):
            return False
        for value in self.Get():
            if not value in iterable:
                return False
        return True



    def Accumulate(self, accumulateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> List[_TFV]:
        return list(itertools.accumulate(self.Get(), lambda temp, next: accumulateFunc(temp, next)))

    def Aggregate(self, accumulateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> _TFV:
        return self.Accumulate(accumulateFunc)[-1]




    def Count(self, value:_TV) -> int:
        return self.GetValues().count(value)
        
    def Lenght(self) -> int:
        return len(self.Get())
    
    def Sum(self) -> Optional[_TV]:
        if self.OfType(Number):
            return sum(self.Get())
        else:
            return None
        
    def Avg(self) -> Optional[_TV]:
        if self.OfType(Number):
            return sum(self.Get()) / self.Lenght()
        else:
            return None
        
    def Max(self) -> Optional[_TV]:
        if self.OfType(Number):
            return max(self.Get())
        else:
            return None
        
    def Min(self) -> Optional[_TV]:
        iterable = self.GetValues()
        if self.OfType(Number):
            return min(iterable)
        else:
            return None



    def Add(self, value:_Value):
        self.Get().append(value)

    def Prepend(self, value:_Value):
        self.Insert(0, value)

    def Insert(self, key:_Key, value:_Value):
        self.Get().insert(key, value)

    def Update(self, key:int, value:_Value):
        self.Get()[key] = value

    def Concat(self, *iterable:List[_Value]):
        for i in iterable:
            self.Get().extend(i)

    def Union(self, *iterable:List[_Value]):
        if not iterable in [(),[]]:
            iterable:list = list(iterable)
            newIterable = EnumerableListTool()
            filter = dict(self.Where(lambda v: v in iterable[0]))
            EnumerableListTool(filter).Loop(lambda v: newIterable.Add(v))
            iterable.pop(0)
            self.Clear()
            self.Concat(newIterable.Get())
            self.Union(*iterable)

    def Delete(self, *key:int):
        i = 0
        for k in sorted(key):
            k -= i
            self.Get().pop(k)
            i += 1

    def Remove(self, *value:_TV):
        for v in value:
            self.Get().remove(v)

    def RemoveAll(self, *value:_TV):
        for v in value:
            while True:
                if self.Contains(v):
                    self.Remove(v)
                else:
                    break

    def Clear(self):
        self.Get().clear()



    def Loop(self, loopFunc:Callable[[_TV],NoReturn]=lambda value: print(value)):
        for value in self.Get():
            loopFunc(value)



    def ToDict(self) -> Dict[int,_TV]:
        return dict(self.GetItems())

    def ToList(self) -> List[_TV]:
        return self.Get()
    
    def ToItem(self) -> List[Tuple[int,_TV]]:
        return list(enumerate(self.iterable))
    



    def IsEmpty(self) -> bool:
        return self.Get() in [[],{}]

    def ContainsByKey(self, *key:int) -> bool:
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



    @staticmethod
    def Range(start:int, stop:int, step:int=1) -> List[int]:
        return list(range(start,stop,step))
    @staticmethod
    def Repeat(value:_TV, count:int) -> List[_TV]:
        return list(itertools.repeat(value, count))



__all__ = ["EnumerableListTool"]
