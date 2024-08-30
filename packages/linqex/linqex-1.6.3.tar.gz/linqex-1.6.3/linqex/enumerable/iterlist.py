from linqex.utils import *
from linqex.tools.iterlisttool import EnumerableListTool

from typing import Dict, List, Callable, Union, NoReturn, Optional, Tuple, Type, Generic, overload, Self
from collections.abc import Iterator

def EnumerableListCatch(enumerableList:"EnumerableList", iterable:Optional[List[_TV]], *keyHistoryAdd:_Key, oneValue:bool=False) -> Optional["EnumerableList[_TV]"]:
    if iterable is None:
        return None
    else:
        newEnumerableList = EnumerableList(iterable)
        newEnumerableList._main = enumerableList._main
        newEnumerableList._orderby = enumerableList._orderby
        newEnumerableList.keyHistory = enumerableList.keyHistory.copy()
        if keyHistoryAdd != ():
            if isinstance(keyHistoryAdd[0], (list, tuple)) and len(enumerableList.keyHistory) != 0:
                if isinstance(enumerableList.keyHistory[-1], (list, tuple)):
                    newEnumerableList.keyHistory[-1].extend(keyHistoryAdd[0])
                else:
                    newEnumerableList.keyHistory.extend(keyHistoryAdd)
            else:
                newEnumerableList.keyHistory.extend(keyHistoryAdd)
        newEnumerableList._oneValue = oneValue
        return newEnumerableList

def EnumerableListToValue(enumerableListOrValue:Union["EnumerableList[_TV2]",_TV]) -> _TV:
    if isinstance(enumerableListOrValue, EnumerableList):
        return enumerableListOrValue.ToValue
    else:
        return enumerableListOrValue

class EnumerableList(Iterator[_TV], Generic[_TV]):
    
    def __init__(self, iterable:List[_TV]=None):
        self.iterable:List[_TV] = EnumerableListToValue(iterable)
        self.keyHistory:list = list()
        self._main:EnumerableList = self
        self._orderby:list = list()
        self._oneValue:bool = False

    def __call__(self, iterable:List[_TV]=None):
        self.__init__(iterable)

    def Get(self, *key:int) -> Union["EnumerableList[_TV]",_TV]:
        iterable = EnumerableListTool(self.iterable).Get(*key)
        if isinstance(iterable,list):
            return EnumerableListCatch(self, iterable, key)
        else:
            return iterable
    
    def GetKey(self, value:_TV) -> int:
        return EnumerableListTool(self.iterable).GetKey(EnumerableListToValue(value))
    
    def GetKeys(self) -> "EnumerableList[int]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).GetKeys())
    
    def GetValues(self) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).GetValues())
    
    def GetItems(self) -> "EnumerableList[Tuple[int,_TV]]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).GetItems())
    
    def Copy(self) -> "EnumerableList[_TV]":
        return EnumerableList(EnumerableListTool(self.iterable).Copy())



    def Take(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).Take(count))
    
    def TakeLast(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).TakeLast(count))
    
    def Skip(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).Skip(count))
    
    def SkipLast(self, count:int) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).SkipLast(count))
    
    def Select(self, selectFunc:Callable[[_TV],_TFV]=lambda value: value) -> "EnumerableList[_TFV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).Select(selectFunc))
    
    def Distinct(self, distinctFunc:Callable[[_TV],_TFV]=lambda value: value) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).Distinct(distinctFunc))
    
    def Except(self, exceptFunc:Callable[[_TV],_TFV]=lambda value: value, *value:_TV) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).Except(exceptFunc, *map(EnumerableListToValue, value)))

    def Join(self, iterable: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue),
        joinType:JoinType=JoinType.INNER
    ) -> "EnumerableList[_TFV2]":
        if joinType == JoinType.INNER:
            return self.InnerJoin(iterable, innerFunc, outerFunc, joinFunc)
        elif joinType == JoinType.LEFT:
            return self.LeftJoin(iterable, innerFunc, outerFunc, joinFunc)
        elif joinType == JoinType.RIGHT:
            return self.RightJoin(iterable, innerFunc, outerFunc, joinFunc)
        else:
            raise ValueError(f"The joinType argument cannot take the value '{joinType}', it can only take values ​​within the joinType class.")
    
    def InnerJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue)
    ) -> "EnumerableList[_TFV2]":
        return EnumerableList(EnumerableListTool(self.iterable).InnerJoin(EnumerableListToValue(iterable), innerFunc, outerFunc, joinFunc))
    
    def LeftJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue)
    ) -> "EnumerableList[_TFV2]":
        return EnumerableList(EnumerableListTool(self.iterable).LeftJoin(EnumerableListToValue(iterable), innerFunc, outerFunc, joinFunc))

    def RightJoin(self, iterable: List[_TV2], 
        innerFunc:Callable[[_TV],_TFV]=lambda value: value, 
        outerFunc:Callable[[_TV2],_TFV]=lambda value: value, 
        joinFunc:Callable[[_TV,_TV2],_TFV2]=lambda inValue, outValue: (inValue, outValue)
    ) -> "EnumerableList[_TFV2]":
        return EnumerableList(EnumerableListTool(self.iterable).RightJoin(EnumerableListToValue(iterable), innerFunc, outerFunc, joinFunc))
      
    def OrderBy(self, orderByFunc:Callable[[_TV],Union[Tuple[_TFV],_TFV]]=lambda value: value, desc:bool=False) -> "EnumerableList[_TV]":
        self._orderby.clear()
        self._orderby.append((orderByFunc, desc))
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).OrderBy((orderByFunc, desc)))

    def ThenBy(self, orderByFunc:Callable[[_TV],Union[Tuple[_TFV],_TFV]]=lambda value: value, desc:bool=False) -> "EnumerableList[_TV]":
        self._orderby.append((orderByFunc, desc))
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).OrderBy(*self._orderby))
        
    def GroupBy(self, groupByFunc:Callable[[_TV],Union[Tuple[_TFV],_TFV]]=lambda value: value) -> "EnumerableList[Tuple[Union[Tuple[_TFV],_TFV], List[_TV]]]":
        return EnumerableList(EnumerableListTool(self.iterable).GroupBy(groupByFunc))

    def Reverse(self) -> "EnumerableList[_TV]":
        return EnumerableListCatch(self,EnumerableListTool(self.iterable).Reverse())
        
    def Zip(self, iterable:List[_TV2], zipFunc:Callable[[_TV,_TV2],_TFV]=lambda inValue, outValue: (inValue, outValue)) -> "EnumerableList[_TFV]":
        return EnumerableList(EnumerableListTool(self.iterable).Zip(EnumerableListToValue(iterable), zipFunc))



    def Where(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> "EnumerableList[_TV]":
        items = dict(EnumerableListTool(self.iterable).Where(conditionFunc))
        return EnumerableListCatch(self, list(items.values()), list(items.keys()))
    
    def OfType(self, *type:Type) -> "EnumerableList[_TV]":
        items = dict(EnumerableListTool(self.iterable).OfType(*type))
        return EnumerableListCatch(self, list(items.values()), list(items.keys()))
    
    def First(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional["EnumerableList[_TV]"]:
        firstValue = EnumerableListTool(self.iterable).First(conditionFunc)
        if firstValue is None:
            return None
        else:
            return EnumerableListCatch(self, [firstValue[1]], firstValue[0], oneValue=True)
    
    def Last(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional["EnumerableList[_TV]"]:
        lastValue = EnumerableListTool(self.iterable).Last(conditionFunc)
        if lastValue is None:
            return None
        else:
            return EnumerableListCatch(self, [lastValue[1]], lastValue[0], oneValue=True)
        
    def Single(self, conditionFunc:Callable[[_TV],bool]=lambda value: True) -> Optional["EnumerableList[_TV]"]:
        singleValue = EnumerableListTool(self.iterable).Single(conditionFunc)
        if singleValue is None:
            return None
        else:
            return EnumerableListCatch(self, [singleValue[1]], singleValue[0], oneValue=True)



    def Any(self, conditionFunc:Callable[[_TV],bool]=lambda value: value) -> bool:
        return EnumerableListTool(self.iterable).Any(conditionFunc)
    
    def All(self, conditionFunc:Callable[[_TV],bool]=lambda value: value) -> bool:
        return EnumerableListTool(self.iterable).All(conditionFunc)
    
    def SequenceEqual(self, iterable:List[_TV2]) -> bool:
        return EnumerableListTool(self.iterable).SequenceEqual(EnumerableListToValue(iterable))



    def Accumulate(self, accumulateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> "EnumerableList[_TFV]":
        return EnumerableList(EnumerableListTool(self.iterable).Accumulate(accumulateFunc))

    def Aggregate(self, aggregateFunc:Callable[[_TV,_TV],_TFV]=lambda temp, nextValue: temp + nextValue) -> _TFV:
        return EnumerableListTool(self.iterable).Aggregate(aggregateFunc)



    def Count(self, value:_TV) -> int:
        return EnumerableListTool(self.iterable).Count(value)

    @property
    def Lenght(self) -> int:
        return EnumerableListTool(self.iterable).Lenght()
    
    def Sum(self) -> Optional[_TV]:
        return EnumerableListTool(self.iterable).Sum()
        
    def Avg(self) -> Optional[_TV]:
        return EnumerableListTool(self.iterable).Avg()
        
    def Max(self) -> Optional[_TV]:
        return EnumerableListTool(self.iterable).Max()
        
    def Min(self) -> Optional[_TV]:
        return EnumerableListTool(self.iterable).Min()

    @overload
    def Set(self): ...
    @overload
    def Set(self, value:_Value): ...
    def Set(self, value=...):
        if value is ...:
            self.Set(self.iterable)
        else:
            value = EnumerableListToValue(value)
            if len(self.keyHistory) == 0:
                self._main.Clear()
                self._main.Concat(value)
            else:
                keyHistory = list(filter(lambda k: not isinstance(k, list),self.keyHistory[:len(self.keyHistory)-1]))
                if isinstance(self.ToKey, list):
                    key = keyHistory[-1]
                    keyHistory = keyHistory[:len(keyHistory)-1]
                    if isinstance(key, list):
                        return None
                else:
                    key = self.ToKey
                self._main.Get(*keyHistory).Update(key, value)
                self.iterable = value

    def Add(self, value:_Value):
        EnumerableListTool(self.iterable).Add(EnumerableListToValue(value))

    def Prepend(self, value:_Value):
        EnumerableListTool(self.iterable).Prepend(EnumerableListToValue(value))

    def Insert(self, key:int, value:_Value):
        EnumerableListTool(self.iterable).Insert(key, EnumerableListToValue(value))

    def Update(self, key:int, value:_Value):
        EnumerableListTool(self.iterable).Update(key, EnumerableListToValue(value))

    def Concat(self, *iterable:List[_TV2]):
        EnumerableListTool(self.iterable).Concat(*map(EnumerableListToValue, iterable))

    def Union(self, *iterable:List[_TV2]):
        EnumerableListTool(self.iterable).Union(*map(EnumerableListToValue, iterable))

    @overload
    def Delete(self): ...
    @overload
    def Delete(self, *key:int): ...
    def Delete(self, *key):
        if key == ():
            if isinstance(self.ToKey, (list,tuple)):
                key = self.ToKey
            else:
                key = [self.ToKey]
            self._main.Get(*filter(lambda k: not isinstance(k, (list,tuple)),self.keyHistory[:len(self.keyHistory)-1])).Delete(*key)
        else:
            EnumerableListTool(self.iterable).Delete(*key)

    def Remove(self, *value:_TV):
        EnumerableListTool(self.iterable).Remove(*map(EnumerableListToValue, value))

    def RemoveAll(self, *value:_TV):
        EnumerableListTool(self.iterable).RemoveAll(*map(EnumerableListToValue, value))

    def Clear(self):
        EnumerableListTool(self.iterable).Clear()



    def Loop(self, loopFunc:Callable[[_TV],NoReturn]=lambda value: print(value)):
        EnumerableListTool(self.iterable).Loop(loopFunc)



    @property
    def ToKey(self) -> int:
        if self.keyHistory == []:
            return None
        else:
            return self.keyHistory[-1]
    
    @property
    def ToValue(self) -> _TV:
        if len(self.iterable) == 1 and self._oneValue:
            return self.GetValues().iterable[0]
        else:
            return self.ToList
    
    @property
    def ToDict(self) -> Dict[int,_TV]:
        return EnumerableListTool(self.iterable).ToDict()
    
    @property
    def ToList(self) -> List[_TV]:
        return EnumerableListTool(self.iterable).ToList()

    @property
    def ToItem(self) -> List[Tuple[int,_TV]]:
        return EnumerableListTool(self.iterable).ToItem()


    @property
    def IsEmpty(self) -> bool:
        return EnumerableListTool(self.iterable).IsEmpty()

    def ContainsByKey(self, *key:int) -> bool:
        return EnumerableListTool(self.iterable).ContainsByKey(*key)

    def Contains(self, *value:_TV) -> bool:
        return EnumerableListTool(self.iterable).Contains(*map(EnumerableListToValue, value))



    def __neg__(self) -> "EnumerableList[_TV]":
        return self.Reverse()
    
    def __add__(self, iterable:List[_TV]) -> "EnumerableList[Union[_TV,_TV2]]":
        return self.Copy().Concat(iterable) 
    
    def __iadd__(self, iterable:List[_TV]) -> Self:
        self.Concat(iterable)
        return self

    def __sub__(self, iterable:List[_TV]) -> "EnumerableList[Union[_TV,_TV2]]":
        return self.Copy().Union(iterable)
    
    def __isub__(self, iterable:List[_TV]) -> Self:
        self.Union(iterable)
        return self

    

    def __eq__(self, iterable:List[_TV]) -> bool:
        return self.SequenceEqual(iterable)

    def __ne__(self, iterable:List[_TV]) -> bool:
        return not self.SequenceEqual(iterable)
    
    def __contains__(self, value:_Value) -> bool:
        return self.Contains()



    def __bool__(self) -> bool:
        return not self.IsEmpty
    
    def __len__(self) -> int:
        return self.Lenght
    
    def __str__(self) -> str:
        return "{}({})".format(self.__class__.__name__, str(self.iterable))



    def __iter__(self) -> Iterator[_TV]:
        return iter(self.GetValues().ToList)
    
    def __next__(self): ...
    
    def __getitem__(self, key:int) -> _TV:
        return self.Get(key)
    
    def __setitem__(self, key:int, value:_Value):
        self.Update(key, value)

    def __delitem__(self, key:int):
        self.Delete(key)


    @overload
    def Range(stop:int) -> "EnumerableList[int]": ...
    @overload
    def Range(start:int, stop:int) -> "EnumerableList[int]": ...
    @overload
    def Range(start:int, stop:int, step:int) -> "EnumerableList[int]": ...
    @staticmethod
    def Range(v1, v2=..., v3=...):
        if v2 == ... and v3 == ...:
            return EnumerableList(EnumerableListTool.Range(0, v1))
        else:
            if v3 == ...:
                return EnumerableList(EnumerableListTool.Range(v1, v2))
            else:
                return EnumerableList(EnumerableListTool.Range(v1, v2, v3))
    
    @staticmethod
    def Repeat(value:_TV, count:int) -> "EnumerableList[_TV]":
        return EnumerableList(EnumerableListTool.Repeat(value, count))



__all__ = ["EnumerableList"]
