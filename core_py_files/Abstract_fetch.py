from abc import ABC, abstractmethod
class Abstract_fetch(ABC):
  @abstractmethod
  def fetch_stock_list(self):
    pass
  @abstractmethod
  def fetch_stock_metadata(self, stock_code:str):
    pass