from linqex.utils import *
from linqex.tools.iterlisttool import EnumerableListTool

from typing import Dict, List, Callable, Union, NoReturn, Optional, Tuple, Type, Generic
import itertools

class EnumerableItemTool(EnumerableListTool, Generic[_TV]):
        
    def __init__(self, iterable:Optional[List[_TV]]=None):
        super().__init__(iterable)

    def Get(self, *key:int) -> Union[List[_TV],_TV]:
        return super().Get(*key)
    
    def GetKey(self, value:_TV) -> int:
        return super().GetKey(value)
    
    def GetKeys(self) -> List[int]:
        return super().GetKeys()
    
    def GetValues(self) -> List[_TV]:
        return super().GetValues()
    
    def GetItems(self) -> List[Tuple[int,_TV]]:
        return super().GetItems()
    
    def Copy(self) -> List[_TV]:
        return super().Copy()



    def Take(self, count:int) -> List[_TV]:
        return super().Take(count)
    
    def TakeLast(self, count:int) -> List[_TV]:
        return super().TakeLast(count)
    
    def Skip(self, count:int) -> List[_TV]:
        return super().Skip(count)
    
    def SkipLast(self, count:int) -> List[_TV]:
        return super().SkipLast(count)

    def Select(self, selectFunc:Callable[[int,_TV],_TFV]=lambda key, value: value) -> List[_TFV]:
        return list(map(selectFunc, self.GetKeys(), self.GetValues()))
    
    def Distinct(self, distinctFunc:Callable[[int,_TV],_TFV]=lambda key, value: value) -> List[_TV]:
        newIterable = self.Copy()
        indexStep = 0
        for key, value in self.GetItems():
            if EnumerableItemTool(EnumerableItemTool(newIterable).Select(distinctFunc)).Count(distinctFunc(key, value)) > 1:
                EnumerableItemTool(newIterable).Delete(key-indexStep)
                indexStep += 1
        return newIterable
    
    def Except(self, *value:_TV) -> List[_TV]:
        return list(zip(*self.Where(lambda i, v: not v in value)))[1] 

    def InnerJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[int,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[int,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[int,_TV,int,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue)
    ) -> List[_TFV2]:
        newIterable:EnumerableItemTool[_TFV2] = EnumerableItemTool()
        for inKey, inValue in EnumerableItemTool(self.Get()).GetItems():
            outer = EnumerableItemTool(iterable).Where(lambda outKey, outValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
            EnumerableItemTool(outer).Loop(lambda key, outItem:newIterable.Add(joinFunc(inKey, inValue, outItem[0], outItem[1])))
        return newIterable.Get()

    def LeftJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[int,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[int,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[int,_TV,int,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue)
    ) -> List[_TFV2]:
        newIterable:EnumerableItemTool[_TFV2] = EnumerableItemTool()
        for inKey, inValue in EnumerableItemTool(self.Get()).GetItems():
            outer = EnumerableItemTool(iterable).Where(lambda outKey, outValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
            if outer == []: newIterable.Add(joinFunc(inKey, inValue, None, None))
            else: EnumerableItemTool(outer).Loop(lambda key, outItem: newIterable.Add(joinFunc(inKey, inValue, [0], outItem[1])))
        return newIterable.Get()

    def RightJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[int,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[int,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[int,_TV,int,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue)
    ) -> List[_TFV2]:
        newIterable:EnumerableItemTool[_TFV2] = EnumerableItemTool()
        for outKey, outValue in EnumerableItemTool(iterable).GetItems():
            inner = EnumerableItemTool(self.Get()).Where(lambda inKey, inValue: outerFunc(outKey, outValue) == innerFunc(inKey, inValue))
            if inner == []: newIterable.Add(joinFunc(None, None, outKey, outValue))
            else: EnumerableItemTool(inner).Loop(lambda key, inItem: newIterable.Add(joinFunc(inItem[0], inItem[1], outKey, outValue)))
        return newIterable.Get() 
      
    def OrderBy(self, *orderByFunc:Tuple[Callable[[int,_TV],Union[Tuple[_TFV],_TFV]],_Desc]) -> List[_TV]:
        if orderByFunc == ():
            orderByFunc = ((lambda key, value: value))
        iterable = self.GetItems()
        orderByFunc = list(reversed(orderByFunc))
        for func, desc in orderByFunc:
            iterable = sorted(iterable, key=lambda x: func(x[0], x[1]), reverse=desc)
        return list(zip(*iterable))[1]
        
    def GroupBy(self, groupByFunc:Callable[[int,_TV],Union[Tuple[_TFV],_TFV]]=lambda value: value) -> List[Tuple[Union[Tuple[_TFV],_TFV], List[_TV]]]:
        iterable = EnumerableItemTool(self.OrderBy((groupByFunc, False))).GetItems()
        iterable = itertools.groupby(iterable, lambda items: groupByFunc(items[0], items[1]))
        return [(keys, list(zip(*list(group)))[1]) for keys, group in iterable]
    
    def Reverse(self) -> List[_TV]:
        return super().Reverse()
          
    def Zip(self, iterable:List[_TV2], zipFunc:Callable[[int,_TV,int,_TV2],_TFV]=lambda inKey, inValue, outKey, outValue: (inValue, outValue)) -> List[_TFV]:
        newIterable = EnumerableItemTool(list(zip(self.GetValues(), EnumerableItemTool(iterable).GetKeys(), EnumerableItemTool(iterable).GetValues())))
        return newIterable.Select(lambda key, value: zipFunc(key, value[0], value[1], value[2]))



    def Where(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> List[Tuple[int,_TV]]:
        result = list()
        for index, value in self.GetItems():
            if conditionFunc(index, value):
                result.append((index, value))
        return result
    
    def OfType(self, *type:Type) -> List[Tuple[int,_TV]]:
        return self.Where(lambda key, value: isinstance(value,type))
    
    def First(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional[Tuple[int,_TV]]:
        for index, value in self.GetItems():
            if conditionFunc(index, value):
                return (index,value)
        return None
    
    def Last(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) == 0:
            return None
        else:
            return result[-1]
        
    def Single(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: True) -> Optional[Tuple[int,_TV]]:
        result = self.Where(conditionFunc)
        if len(result) != 1:
            return None
        else:
            return result[0]



    def Any(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: value) -> bool:
        result = False
        for key, value in self.GetItems():
            if conditionFunc(key, value):
                result = True
                break
        return result
    
    def All(self, conditionFunc:Callable[[int,_TV],bool]=lambda key, value: value) -> bool:
        result = True
        for key, value in self.GetItems():
            if not conditionFunc(key, value):
                result = False
                break
        return result
 
    def SequenceEqual(self, iterable:List[_TV2]) -> bool:
        return super().SequenceEqual(iterable)



    def Accumulate(self, accumulateFunc:Callable[[_TV,int,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> List[_TFV]:
        firstTemp:bool = True
        def FirstTemp(temp):
            nonlocal firstTemp
            if firstTemp:
                firstTemp = False
                return temp[1]
            else:
                return temp
        if not self.IsEmpty():
            result = [self.GetValues()[0]]
            result.extend(list(itertools.accumulate(self.GetItems(), lambda temp, next: accumulateFunc(FirstTemp(temp), next[0], next[1])))[1:])
            return result
        else:
            return []

    def Aggregate(self, accumulateFunc:Callable[[_TV,int,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> _TFV:
        return self.Accumulate(accumulateFunc)[-1]



    def Count(self, value:_TV) -> int:
        return super().Count(value)
        
    def Lenght(self) -> int:
        return super().Lenght()
    
    def Sum(self) -> Optional[_TV]:
        return super().Sum()
        
    def Avg(self) -> Optional[_TV]:
        return super().Avg()
        
    def Max(self) -> Optional[_TV]:
        return super().Max()
        
    def Min(self) -> Optional[_TV]:
        return super().Min()



    def Add(self, value:_Value):
        super().Add(value)

    def Prepend(self, value:_Value):
        super().Prepend(value)

    def Insert(self, key:_Key, value:_Value):
        super().Insert(key, value)

    def Update(self, key:int, value:_Value):
        super().Update(key, value)

    def Concat(self, *iterable:List[_Value]):
        super().Concat(*iterable)

    def Union(self, *iterable:List[_Value]):
        super().Union(*iterable)

    def Delete(self, *key:int):
        super().Delete(*key)

    def Remove(self, *value:_TV):
        super().Remove(*value)

    def RemoveAll(self, *value:_TV):
        super().RemoveAll(*value)

    def Clear(self):
        super().Clear()



    def Loop(self, loopFunc:Callable[[int,_TV],NoReturn]=lambda value: print(value)):
        for key, value in self.GetItems():
            loopFunc(key, value)



    def ToDict(self) -> Dict[int,_TV]:
        return super().ToDict()

    def ToList(self) -> List[_TV]:
        return self.GetValues()

    def ToItem(self) -> List[Tuple[int,_TV]]:
        return list(enumerate(self.iterable))



    def IsEmpty(self) -> bool:
        return super().IsEmpty()

    def ContainsByKey(self, *key:int) -> bool:
        return super().ContainsByKey(*key)

    def Contains(self, *value:_TV) -> bool:
        return super().Contains(*value)



    @staticmethod
    def Range(start:int, stop:int, step:int=1) -> List[int]:
        return EnumerableListTool.Range(start, stop, step)
    
    @staticmethod
    def Repeat(value:_TV, count:int) -> List[_TV]:
        return EnumerableListTool.Repeat(value, count)




__all__ = ["EnumerableItemTool"]
