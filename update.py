import os, csv
import SQL_operation as SQL
from datetime import datetime
import fetch 
from calculation import calculation

def update(share_id_list):
  # for each database, find the latest date in each table.
  for share_id in share_id_list:
    connection = SQL.create_connection(f'share_data/{share_id}.db')
    for frequency in ['day']:
      latest = SQL.search_data_by_condition(connection, frequency, f"date <= '{datetime.today().strftime("%Y-%m-%d")}'", 1);      
      # fetch new data from that date to today.
      if not latest:
        latest = '2015-01-01'
      else:
        latest = latest[0][1]
      if frequency == 'day':
        count = (datetime.today() - datetime.strptime(latest, "%Y-%m-%d")).days
        if count == 0:
          print(f"No new data for {share_id} in {frequency} table.")
          continue
        date_list = fetch.get_price(share_id, datetime.today().strftime("%Y-%m-%d"), count, 'day')
      
      
      for date in date_list:
        indicators = calculation(connection, frequency, date)
        indicators.append(date)
        SQL.update_data(connection, frequency, indicators)

        

      
      

def main():
  connection = SQL.create_connection("share_data/sh603686.db")
 
  # for row in SQL.fetch_all_data(connection, 'day'):
  #   print(row)
  # fetch.get_price('sh603686', end_date = '2024-01-01', count = '10', frequency = 'day')

  update(['sh603686'])
  SQL.create_table(connection, 'day')
  cursor = connection.cursor()

  # Query data
  cursor.execute("SELECT * FROM day")
  rows = cursor.fetchall()

  # Save to CSV
  with open("students.csv", "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow([description[0] for description in cursor.description])  # header
      writer.writerows(rows)

  connection.close()

if __name__ == '__main__':
  main()