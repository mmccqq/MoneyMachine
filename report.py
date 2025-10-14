from datetime import datetime
import help_functions
from update import update
import strategy
import sqlite3  
from SQL.Stock_DB import Stock_DB
def report():
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
      print(f"Buy potential detected for {stock_id} today, pass lower bollinger band.")
    else:
      print(f"No buy potential for {stock_id}.")



def main():
  report()
if __name__ == '__main__':
  main()