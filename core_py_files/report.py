from datetime import datetime

import os

from SQL.Stock_DB import Stock_DB
import core_py_files.strategy as strategy
from core_py_files.update import update
import core_py_files.process_stock_ids as process_stock_ids
import core_py_files.help_functions as help_functions
from SQL.Metadata_DB import Metadata_DB

def report():
  results = []
  stock_id_list = help_functions.database_list()
  if not stock_id_list:
    print("No database files found in 'stock_data' directory.")
    return
  update(stock_id_list)
  for stock_id in stock_id_list:
    stock = Stock_DB(stock_id)
    # connection = sqlite3.connect(f'stock_data/{stock_id}.db')
    result = strategy.buy_potential(stock, 'day', datetime.today().strftime("%Y-%m-%d"))
    if result:
      results.append(f"{stock_id}: Buy potential detected for today, pass lower bollinger band.\n")
  
  if results:
    with open('report.txt', 'w') as f:
      f.writelines(results)
      print("Report generated: report.txt")
  else:
    print("No buy potential detected today. Report generated: report.txt")



def main():
  report()
if __name__ == '__main__':
  main()