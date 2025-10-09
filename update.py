import os, csv
import SQL_operation as SQL
from datetime import datetime
import fetch 
from calculation import calculation

def update():
  # find all databases in the data folder.
  share_id_list = []
  with os.scandir('share_data') as entries:
    for entry in entries:
      if entry.is_file() and entry.name.endswith('.db'):
        share_id = entry.name[:-3]
        share_id_list.append(share_id)
  
  if not share_id_list:
    print("No database files found in 'share_data' directory.")
    return
  # for each database, find the latest date in each table.
  for share_id in share_id_list:
    connection = SQL.create_connection(f'share_data/{share_id}.db')
    for table in ['day']:
      latest = SQL.search_latest_date(connection, table)      
      # fetch new data from that date to today.
      if table == 'day':
        count = (datetime.today() - datetime.strptime(latest, "%Y-%m-%d")).days
        date_list = fetch.get_price(share_id, datetime.today().strftime("%Y-%m-%d"), count, 'day')
      
      if not date_list:
        print(f"No new data for {share_id} in {table} table.")
        continue
      for date in date_list:
        indicators = calculation(connection, table, date)
        indicators.append(date)
        SQL.update_data(connection, table, indicators)

        

      
      

def main():
  # connection = SQL.create_connection("share_data/sh603686.db")
  # SQL.create_table(connection, 'day')
  # for row in SQL.fetch_all_data(connection, 'day'):
  #   print(row)
  fetch.get_price('sh603686', end_date = '2025-07-30', count = '10', frequency = 'day')

  update()
  # cursor = connection.cursor()

  # # Query data
  # cursor.execute("SELECT * FROM day")
  # rows = cursor.fetchall()

  # # Save to CSV
  # with open("students.csv", "w", newline="") as file:
  #     writer = csv.writer(file)
  #     writer.writerow([description[0] for description in cursor.description])  # header
  #     writer.writerows(rows)

  # connection.close()

if __name__ == '__main__':
  main()