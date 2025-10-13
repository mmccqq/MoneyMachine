import os
def database_list():
  stock_id_list = []
  with os.scandir('./stock_data') as entries:
    for entry in entries:
      if entry.is_file() and entry.name.endswith('.db'):
        stock_id = entry.name[:-3]
        stock_id_list.append(stock_id)
  return stock_id_list