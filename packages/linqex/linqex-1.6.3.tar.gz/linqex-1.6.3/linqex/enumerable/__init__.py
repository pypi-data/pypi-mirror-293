from linqex.enumerable.iterlist import EnumerableList
from linqex.enumerable.iteritem import EnumerableItem
from linqex.enumerable.iterdict import EnumerableDict
from linqex.utils import _TK, _TV

from typing import Any, Dict, List, TypeVar, Union, overload

class Enumerable:
    @staticmethod
    def Iterable(iterable:Union[List[_TV],Dict[_TK,_TV]]) -> Union[EnumerableItem[_TV], EnumerableDict[_TK,_TV]]:
        if isinstance(iterable, list):
            return Enumerable.Item(iterable)
        elif isinstance(iterable, dict):
            return Enumerable.Dict(iterable)
        else:
            raise TypeError("Must be list or dict, not {}".format(str(type(iterable))[8,-2]))

    @staticmethod
    def Item(iteritem:List[_TV]=None) -> EnumerableItem[_TV]:
        if iteritem is None:
            iteritem:List[_TV]=list()
        return EnumerableItem(iteritem)

    @staticmethod
    def List(iterlist:List[_TV]=None) -> EnumerableList[_TV]:
        if iterlist is None:
            iterlist:List[_TV]=list()
        return EnumerableList(iterlist)

    @staticmethod
    def Dict(iterdict:Dict[_TK,_TV]=None) -> EnumerableDict[_TK,_TV]:
        if iterdict is None:
            iterdict:Dict[_TK,_TV]=dict()
        return EnumerableDict(iterdict)
    
    @overload
    def Range(stop:int) -> "EnumerableList[int]": ...
    @overload
    def Range(start:int, stop:int) -> "EnumerableList[int]": ...
    @overload
    def Range(start:int, stop:int, step:int) -> "EnumerableList[int]": ...
    @staticmethod
    def Range(v1, v2=..., v3=...):
        return EnumerableList.Range(v1, v2, v3)
            
    def Repeat(value:Any, count:int):
        return EnumerableList.Repeat(value, count)



__all__ = ["EnumerableList", "EnumerableItem", "EnumerableDict", "Enumerable"]