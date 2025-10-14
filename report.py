from datetime import datetime
import help_functions
from update import update
import strategy
from SQL.Stock_DB import Stock_DB
import os
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