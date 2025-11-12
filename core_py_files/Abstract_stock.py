from abc import ABC, abstractmethod
class Abstract_stock(ABC):
  _name = ""
  _name_letters = ""
  _code = ""
  _last_updated = None
  _current_price = 0.0
  _open_price = 0.0
  _close_price = 0.0
  _high_price = 0.0
  _low_price = 0.0
  @abstractmethod
  def update_a_frequency_data(self, frequency:str):
    pass
  @abstractmethod
  def update_all_frequency_data(self):
    pass
  @abstractmethod
  def update_indicator_frequency(self, frequency:str):
    pass
  @abstractmethod
  def update_all_indicator(self):
    pass
