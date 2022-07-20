from abc import ABC, abstractmethod
import os

## Strategy interface
class Naming_Strategy(ABC):
    @abstractmethod
    def get_basename(self,name) -> (str,str):
        pass

## Concrete strategies
class Strategy_0_1(Naming_Strategy):
    def get_basename(self,name) -> (str,str):
        base_name = os.path.basename(name)
        base_name = base_name.replace("_merge.png","")
        base_name_left = base_name + "_F0.png"
        base_name_right = base_name + "_F-1.png"
        return base_name_left,base_name_right

class Strategy_0_3(Naming_Strategy):
    def get_basename(self,name) -> (str,str):
        base_name = os.path.basename(name)
        base_name = base_name.replace("_merge.png","")
        base_name_left = base_name + "_F0.png"
        base_name_right = base_name + "_F3.png"
        return base_name_left,base_name_right


class Strategy_fernanda_videos(Naming_Strategy):
    def get_basename(self,name) -> (str,str):
        base_name = os.path.basename(name)
        base_name = base_name.replace("_merge.png","")
        base_name_left = base_name + "_F10.png"
        base_name_right = base_name + "_F-1.png"
        return base_name_left,base_name_right

## Strategy factory
class Naming_Strategy_Factory:
    @staticmethod
    def get_naming_strategy(strategy_name):
        if strategy_name=="0_1":
            return Strategy_0_1()
        if strategy_name=="0_3":
            return Strategy_0_3()
        if strategy_name=="fernanda-videos":
            return Strategy_fernanda_videos()