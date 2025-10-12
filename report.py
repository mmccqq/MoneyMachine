from datetime import datetime
import os
from update import update
import strategy
import sqlite3  
def report():
  share_id_list = []
  with os.scandir('share_data') as entries:
    for entry in entries:
      if entry.is_file() and entry.name.endswith('.db'):
        share_id = entry.name[:-3]
        share_id_list.append(share_id)
  
  if not share_id_list:
    print("No database files found in 'share_data' directory.")
    return
  update(share_id_list)
  for share_id in share_id_list:
    connection = sqlite3.connect(f'share_data/{share_id}.db')
    result = strategy.buy_potential(connection, 'day', datetime.today().strftime("%Y-%m-%d"))
    if result:
      print(f"Buy potential detected for {share_id} on {result[0]}: Close Price = {result[1]}, Low = {result[2]}, BOLL Lower = {result[3]}")
    else:
      print(f"No buy potential for {share_id}.")
    connection.close()


def main():
  report()
if __name__ == '__main__':
  main()