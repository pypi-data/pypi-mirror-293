from linqex.utils import *
from linqex.tools.iterdicttool import EnumerableDictTool
from linqex.enumerable.iterlist import EnumerableList, EnumerableListCatch

from typing import Dict, List, Callable, Union, NoReturn, Optional, Tuple, Type, Generic, overload, Self
from collections.abc import Iterator

def EnumerableDictCatch(enumerableDict:"EnumerableDict", iterable:Optional[Dict[_TK,_TV]], *keyHistoryAdd:_Key, oneValue:bool=False) -> Optional["EnumerableDict[_TK,_TV]"]:
    if iterable is None:
        return None
    else:
        newEnumerableDict = EnumerableDict(iterable)
        newEnumerableDict._main = enumerableDict._main
        newEnumerableDict.keyHistory = enumerableDict.keyHistory.copy()
        if keyHistoryAdd != ():
            if isinstance(keyHistoryAdd[0], (list, tuple)) and len(enumerableDict.keyHistory) != 0:
                if isinstance(enumerableDict.keyHistory[-1], (list, tuple)):
                    newEnumerableDict.keyHistory[-1].extend(keyHistoryAdd[0])
                else:
                    newEnumerableDict.keyHistory.extend(keyHistoryAdd)
            else:
                newEnumerableDict.keyHistory.extend(keyHistoryAdd)
        newEnumerableDict._oneValue = oneValue
        return newEnumerableDict

def EnumerableDictToValue(enumerableDictOrValue:Union["EnumerableDict[_TK,_TV]",_TV]) -> _TV:
    if isinstance(enumerableDictOrValue, EnumerableDict):
        return enumerableDictOrValue.ToValue
    else:
        return enumerableDictOrValue

class EnumerableDict(Iterator[Tuple[_TK,_TV]], Generic[_TK,_TV]):
    
    def __init__(self, iterable:Dict[_TK,_TV]=None):
        self.iterable:Dict[_TK,_TV] = EnumerableDictTool(EnumerableDictToValue(iterable)).Get()
        self.keyHistory:list = list()
        self._main:EnumerableDict = self
        self._orderby:list = list()
        self._oneValue:bool = False

    def __call__(self, iterable:Dict[_TK,_TV]=None):
        self.__init__(iterable)

    def Get(self, *key:_TK) -> Union["EnumerableDict[_TK,_TV]",_TV]:
        iterable = EnumerableDictTool(self.iterable).Get(*key)
        if isinstance(iterable,dict):
            return EnumerableDictCatch(self, iterable, key)
        else:
            return iterable
    
    def GetKey(self, value:_TV) -> _TK:
        return EnumerableDictTool(self.iterable).GetKey(EnumerableDictToValue(value))
    
    def GetKeys(self) -> EnumerableList[_TK]:
        return EnumerableListCatch(self, EnumerableDictTool(self.iterable).GetKeys())
    
    def GetValues(self) -> EnumerableList[_TV]:
        return EnumerableListCatch(self, EnumerableDictTool(self.iterable).GetValues())
    
    def GetItems(self) -> EnumerableList[Tuple[_TK,_TV]]:
        return EnumerableListCatch(self, EnumerableDictTool(self.iterable).GetItems())
    
    def Copy(self) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDict(EnumerableDictTool(self.iterable).Copy())



    def Take(self, count:int) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).Take(count))
    
    def TakeLast(self, count:int) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).TakeLast(count))
    
    def Skip(self, count:int) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).Skip(count))
    
    def SkipLast(self, count:int) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).SkipLast(count))
    
    def Select(self, 
        selectFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value,
        selectFuncByKey:Callable[[_TK,_TV],_TFK]=lambda key, value: key
    ) -> "EnumerableDict[_TFK,_TFV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).Select(selectFunc, selectFuncByKey))
    
    def Distinct(self, distinctFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).Distinct(distinctFunc))
    
    def Except(self, *value:_TV) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).Except(*map(EnumerableDictToValue, value)))
    
    def ExceptByKey(self, *key:_TK) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).ExceptByKey(*map(EnumerableDictToValue, key)))

    def Join(self, iterable: Dict[_TK2,_TV2], 
        innerFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[_TK2,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK2]=lambda inKey, inValue, outKey, outValue: inKey,
        joinType:JoinType=JoinType.INNER
    ) -> "EnumerableDict[_TFK2,_TFV2]":
        if joinType == JoinType.INNER:
            return self.InnerJoin(iterable, innerFunc, outerFunc, joinFunc, joinFuncByKey)
        elif joinType == JoinType.LEFT:
            return self.LeftJoin(iterable, innerFunc, outerFunc, joinFunc, joinFuncByKey)
        elif joinType == JoinType.RIGHT:
            return self.RightJoin(iterable, innerFunc, outerFunc, joinFunc, joinFuncByKey)
        else:
            raise ValueError(f"The joinType argument cannot take the value '{joinType}', it can only take values ​​within the joinType class.") 
    
    def InnerJoin(self, iterable: Dict[_TK2,_TV2], 
        innerFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[_TK2,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK2]=lambda inKey, inValue, outKey, outValue: inKey
    ) -> "EnumerableDict[_TFK2,_TFV2]":
        return EnumerableDict(EnumerableDictTool(self.iterable).InnerJoin(EnumerableDictToValue(iterable), innerFunc, outerFunc, joinFunc, joinFuncByKey))
    
    def LeftJoin(self, iterable: Dict[_TK2,_TV2], 
        innerFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[_TK2,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK2]=lambda inKey, inValue, outKey, outValue: inKey
    ) -> "EnumerableDict[_TFK2,_TFV2]":
        return EnumerableDict(EnumerableDictTool(self.iterable).LeftJoin(EnumerableDictToValue(iterable), innerFunc, outerFunc, joinFunc, joinFuncByKey))
    
    def RightJoin(self, iterable: Dict[_TK2,_TV2], 
        innerFunc:Callable[[_TK,_TV],_TFV]=lambda key, value: value, 
        outerFunc:Callable[[_TK2,_TV2],_TFV]=lambda key, value: value, 
        joinFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV2]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        joinFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK2]=lambda inKey, inValue, outKey, outValue: inKey
    ) -> "EnumerableDict[_TFK2,_TFV2]":
        return EnumerableDict(EnumerableDictTool(self.iterable).RightJoin(EnumerableDictToValue(iterable), innerFunc, outerFunc, joinFunc, joinFuncByKey))
      
    def OrderBy(self, orderByFunc:Callable[[_TK,_TV],Union[Tuple[_TFV],_TFV]]=lambda key, value: value, desc:bool=False) -> "EnumerableDict[_TK,_TV]":
        self._orderby.clear()
        self._orderby.append((orderByFunc, desc))
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).OrderBy((orderByFunc, desc)))

    def ThenBy(self, orderByFunc:Callable[[_TK,_TV],Union[Tuple[_TFV],_TFV]]=lambda key, value: value, desc:bool=False) -> "EnumerableDict[_TK,_TV]":
        self._orderby.append((orderByFunc, desc))
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).OrderBy(*self._orderby))
        
    def GroupBy(self, groupByFunc:Callable[[_TK,_TV],Union[Tuple[_TFV],_TFV]]=lambda key, value: value) -> "EnumerableDict[Union[Tuple[_TFV],_TFV], Dict[_TK,_TV]]":
        return EnumerableDict(EnumerableDictTool(self.iterable).GroupBy(groupByFunc))

    def Reverse(self) -> "EnumerableDict[_TK,_TV]":
        return EnumerableDictCatch(self,EnumerableDictTool(self.iterable).Reverse())
        
    def Zip(self, iterable:Dict[_TK2,_TV2], 
        zipFunc:Callable[[_TK,_TV,_TK2,_TV2],_TFV]=lambda inKey, inValue, outKey, outValue: (inValue, outValue),
        zipFuncByKey:Callable[[_TK,_TV,_TK2,_TV2],_TFK]=lambda inKey, inValue, outKey, outValue: inKey
    ) -> "EnumerableDict[_TFK,_TFV]":
        return EnumerableDict(EnumerableDictTool(self.iterable).Zip(EnumerableDictToValue(iterable), zipFunc))



    def Where(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> "EnumerableDict[_TK,_TV]":
        items = EnumerableDictTool(self.iterable).Where(conditionFunc)
        return EnumerableDictCatch(self, items, list(items.keys()))
    
    def OfType(self, *type:Type) -> "EnumerableDict[_TK,_TV]":
        items = dict(EnumerableDictTool(self.iterable).OfType(*type))
        return EnumerableDictCatch(self, items, list(items.keys()))
    
    def OfTypeByKey(self, *type:Type) -> "EnumerableDict[_TK,_TV]":
        items = dict(EnumerableDictTool(self.iterable).OfTypeByKey(*type))
        return EnumerableDictCatch(self, items, list(items.keys()))

    def First(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> Optional["EnumerableDict[_TK,_TV]"]:
        firstValue = EnumerableDictTool(self.iterable).First(conditionFunc)
        if firstValue is None:
            return None
        else:
            return EnumerableDictCatch(self, {None:firstValue[1]}, firstValue[0], oneValue=True)
    
    def Last(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> Optional["EnumerableDict[_TK,_TV]"]:
        lastValue = EnumerableDictTool(self.iterable).Last(conditionFunc)
        if lastValue is None:
            return None
        else:
            return EnumerableDictCatch(self, {None:lastValue[1]}, lastValue[0], oneValue=True)
        
    def Single(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: True) -> Optional["EnumerableDict[_TK,_TV]"]:
        singleValue = EnumerableDictTool(self.iterable).Single(conditionFunc)
        if singleValue is None:
            return None
        else:
            return EnumerableDictCatch(self, {None:singleValue[1]}, singleValue[0], oneValue=True)



    def Any(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: value) -> bool:
        return EnumerableDictTool(self.iterable).Any(conditionFunc)
    
    def All(self, conditionFunc:Callable[[_TK,_TV],bool]=lambda key, value: value) -> bool:
        return EnumerableDictTool(self.iterable).All(conditionFunc)
    
    def SequenceEqual(self, iterable:Dict[_TK2,_TV2]) -> bool:
        return EnumerableDictTool(self.iterable).SequenceEqual(EnumerableDictToValue(iterable))



    def Accumulate(self, accumulateFunc:Callable[[_TV,_TK,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> "EnumerableList[_TFV]":
        return EnumerableDict(EnumerableDictTool(self.iterable).Accumulate(accumulateFunc))

    def Aggregate(self, accumulateFunc:Callable[[_TV,_TK,_TV],_TFV]=lambda temp, key, nextValue: temp + nextValue) -> _TFV:
        return EnumerableDictTool(self.iterable).Aggregate(accumulateFunc)



    def Count(self, value:_TV) -> int:
        return EnumerableDictTool(self.iterable).Count(value)

    @property
    def Lenght(self) -> int:
        return EnumerableDictTool(self.iterable).Lenght()
    
    def Sum(self) -> Optional[_TV]:
        return EnumerableDictTool(self.iterable).Sum()
        
    def Avg(self) -> Optional[_TV]:
        return EnumerableDictTool(self.iterable).Avg()
        
    def Max(self) -> Optional[_TV]:
        return EnumerableDictTool(self.iterable).Max()
        
    def Min(self) -> Optional[_TV]:
        return EnumerableDictTool(self.iterable).Min()

    @overload
    def Set(self): ...
    @overload
    def Set(self, value:_Value): ...
    def Set(self, value=...):
        if value is ...:
            self.Set(self.iterable)
        else:
            value = EnumerableDictToValue(value)
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

    def Add(self, key:_Key, value:_Value):
        EnumerableDictTool(self.iterable).Add(key,EnumerableDictToValue(value))

    def Update(self, key:_TK, value:_Value):
        EnumerableDictTool(self.iterable).Update(key, EnumerableDictToValue(value))

    def Concat(self, *iterable:Dict[_TK2,_TV2]):
        EnumerableDictTool(self.iterable).Concat(*map(EnumerableDictToValue, iterable))

    def Union(self, *iterable:Dict[_TK2,_TV2]):
        EnumerableDictTool(self.iterable).Union(*map(EnumerableDictToValue, iterable))

    @overload
    def Delete(self): ...
    @overload
    def Delete(self, *key:_TK): ...
    def Delete(self, *key):
        if key == ():
            if isinstance(self.ToKey, (list,tuple)):
                key = self.ToKey
            else:
                key = [self.ToKey]
            self._main.Get(*filter(lambda k: not isinstance(k, (list,tuple)),self.keyHistory[:len(self.keyHistory)-1])).Delete(*key)
        else:
            EnumerableDictTool(self.iterable).Delete(*key)

    def Remove(self, *value:_TV):
        EnumerableDictTool(self.iterable).Remove(*map(EnumerableDictToValue, value))

    def RemoveAll(self, *value:_TV):
        EnumerableDictTool(self.iterable).RemoveAll(*map(EnumerableDictToValue, value))

    def Clear(self):
        EnumerableDictTool(self.iterable).Clear()



    def Loop(self, loopFunc:Callable[[_TK,_TV],NoReturn]=lambda key, value: print(key,value)):
        EnumerableDictTool(self.iterable).Loop(loopFunc)



    @property
    def ToKey(self) -> _TK:
        if self.keyHistory == []:
            return None
        else:
            return self.keyHistory[-1]
    
    @property
    def ToValue(self) -> _TV:
        if len(self.iterable) == 1 and self._oneValue:
            return self.GetValues().iterable[0]
        else:
            return self.ToDict
    
    @property
    def ToList(self) -> List[_TV]:
        return EnumerableDictTool(self.iterable).ToList()
    
    @property
    def ToItem(self) -> List[Tuple[int,_TV]]:
        return EnumerableDictTool(self.iterable).ToItem()
    
    @property
    def ToDict(self) -> Dict[_TK,_TV]:
        return EnumerableDictTool(self.iterable).ToDict()
    


    @property
    def IsEmpty(self) -> bool:
        return EnumerableDictTool(self.iterable).IsEmpty()

    def ContainsByKey(self, *key:_TK) -> bool:
        return EnumerableDictTool(self.iterable).ContainsByKey(*key)

    def Contains(self, *value:_TV) -> bool:
        return EnumerableDictTool(self.iterable).Contains(*map(EnumerableDictToValue, value))



    def __neg__(self) -> "EnumerableDict[_TK,_TV]":
        return self.Reverse()
    
    def __add__(self, iterable:Dict[_TK2,_TV2]) -> "EnumerableDict[Union[_TK,_TK2],Union[_TV,_TV2]]":
        return self.Copy().Concat(iterable)
    
    def __iadd__(self, iterable:Dict[_TK2,_TV2]) -> Self:
        self.Concat(iterable)
        return self

    def __sub__(self, iterable:Dict[_TK2,_TV2]) -> "EnumerableDict[Union[_TK,_TK2],Union[_TV,_TV2]]":
        return self.Copy().Union(iterable)

    def __isub__(self, iterable:Dict[_TK2,_TV2]) -> Self:
        self.Union(iterable)
        return self
    
    

    def __eq__(self, iterable:Dict[_TK2,_TV2]) -> bool:
        return self.SequenceEqual(iterable)

    def __ne__(self, iterable:Dict[_TK2,_TV2]) -> bool:
        return not self.SequenceEqual(iterable)
    
    def __contains__(self, value:_Value) -> bool:
        return self.Contains(value)



    def __bool__(self) -> bool:
        return self.IsEmpty
    
    def __len__(self) -> int:
        return self.Lenght
    
    def __str__(self) -> str:
        return "{}({})".format(self.__class__.__name__, str(self.iterable))



    def __iter__(self) -> Iterator[Tuple[_TK,_TV]]:
        return iter(self.GetItems().ToList)
    
    def __next__(self): ...
    
    def __getitem__(self, key:_TK) -> _TV:
        return self.Get(key)
    
    def __setitem__(self, key:_TK, value:_Value):
        if self.ContainsByKey(key):
            self.Update(key, value)
        else:
            self.Add(key, value)

    def __delitem__(self, key:_TK):
        self.Delete(key)
        



__all__ = ["EnumerableDict"]
