import os, csv
from datetime import datetime
import core_py_files.fetch  as fetch
from core_py_files.calculation import calculation
from SQL.Stock_DB import Stock_DB
from SQL.Metadata_DB import Metadata_DB

def update(stock_id_list):
  count = len(stock_id_list)
  # for each database, find the latest date in each table.
  for stock_id in stock_id_list:
    stock = Stock_DB(stock_id)
    for frequency in ['day']:
      if stock.if_table_exists(frequency) == False:
        stock.create_table(frequency)
      metadb = Metadata_DB("metadata")
      if metadb.if_table_exists('metadata') == False:
        metadb.create_table()

      # check if update is necessary
      last_update = metadb.query_rows('metadata', columns=f'last_{frequency}_updated', 
                                      where_dict={"stock_id = ": f"{stock_id}"}, 
                                      limit=1)
      if last_update:
        if (datetime.strptime(last_update[0][0], "%Y-%m-%d %H:%M:%S").date() 
            >= datetime.today().date()):
          print(f"No new data for {stock_id} in {frequency} table.")
          count -= 1
          continue
      
      latest = stock.query_rows(frequency, columns='date',
                                order_by="date DESC", limit=1)
      if not latest:
        latest = '2023-06-01'
      else:
        latest = latest[0][0]
      if frequency == 'day':
        count = (datetime.today() - datetime.strptime(latest, "%Y-%m-%d")).days
        if count == 0:
          print(f"No new data for {stock_id} in {frequency} table.")
          continue
        date_list, name = fetch.get_price(stock_id, datetime.today().strftime("%Y-%m-%d"), count, 'day')
      
      
      for date in date_list:
        indicators = calculation(stock, frequency, date)
        stock.update_row(frequency,indicators, {"date": date})
      
      # update metadata
      info = stock.query_rows(frequency, "open, close", order_by="date DESC", limit=1)
      open = info[0][0]
      close = info[0][1]
      change = (close - open) / open if open != 0 else 0
      metadb.update_metadata(stock_id, name, close, change, frequency, datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
  return count

        

      
      

def main():

  update(['sh603686'])
  stock_id = Stock_DB('sh603686')
  rows = stock_id.query_rows('day')
  # for row in rows:
  #   print(row)
  # SQL.create_table(connection, 'day')
  # cursor = connection.cursor()

  # # Query data
  # cursor.execute("SELECT * FROM day")
  # rows = cursor.fetchall()

  # Save to CSV
  with open("students.csv", "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow([description[0] for description in stock_id.cursor.description])  # header
      writer.writerows(rows)

  # connection.close()

if __name__ == '__main__':
  main()