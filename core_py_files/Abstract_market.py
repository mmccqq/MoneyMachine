from abc import ABC, abstractmethod

class Abstract_market(ABC):
  _name = ""
  _stocks = []
  @abstractmethod
  def update_stock_data(self, stock):
    pass
  @abstractmethod
  def update_all(self):
    pass
