from datetime import datetime
import help_functions
from update import update
import strategy
import sqlite3  
def report():
  share_id_list = help_functions.database_list()
  if not share_id_list:
    print("No database files found in 'share_data' directory.")
    return
  update(share_id_list)
  for share_id in share_id_list:
    connection = sqlite3.connect(f'share_data/{share_id}.db')
    result = strategy.buy_potential(connection, 'day', datetime.today().strftime("%Y-%m-%d"))
    if result:
      print(f"Buy potential detected for {share_id} today, pass lower bollinger band.")
    else:
      print(f"No buy potential for {share_id}.")
    connection.close()


def main():
  report()
if __name__ == '__main__':
  main()