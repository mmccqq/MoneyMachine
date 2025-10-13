import requests, json
import SQL_operation as SQL
from datetime import datetime

def get_data_min_tx(stock_id, count = '', frequency = '60m'):

  URL = f'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={stock_id},m{frequency},,{count}'

  response = requests.get(URL)
  raw_data = json.loads(response.content)
  stock_min_data = raw_data['data'][f'{stock_id}'][f'm{frequency}']
  result = []
  
  connection = SQL.create_connection(f'{stock_id}.db')
  latest = SQL.search_data_by_condition(connection, frequency, f"date <= '{datetime.today().strftime("%Y-%m-%d")}'", 1);      
  if not latest:
    latest = '2015-01-01'
  else:
    latest = latest[0][1]
  # convert raw data to required format
  for index, data in enumerate(stock_min_data):
    result.append([])
    if int(latest) < int(data[0]):
      result[index].append(data[0][0:4])
      result[index].append(data[0][4:8])
      result[index].append(data[0][8:12])
      for i in range(1, 5):
        result[index].append(data[i])
  if SQL.if_table_exists(connection, frequency) == False:
    SQL.create_table(connection, frequency)

  #need to avoid duplicate data
  SQL.insert_raw_data(connection, frequency, result)

def get_data_day_tx(stock_id, end_date = '', count = '', frequency = 'day'):
  URL = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={stock_id},{frequency},,{end_date},{count},qfq'
  response = requests.get(URL)
  raw_data = json.loads(response.content)
  stock_day_data = raw_data['data'][f'{stock_id}'][f'qfq{frequency}']
  
  connection = SQL.create_connection(f'stock_data/{stock_id}.db')

  if SQL.if_table_exists(connection, frequency) == False:
    SQL.create_table(connection, frequency)

  # need to avoid duplicate data
  latest = SQL.search_data_by_condition(connection, frequency, f"date <= '{datetime.today().strftime("%Y-%m-%d")}'", 1);      
  if not latest:
    latest = '2015-01-01'
  else:
    latest = latest[0][1]
  
  insert_data = []
  date_list = []
  for data in stock_day_data:
    if latest < data[0]:
      insert_data.append([])
      date_list.append(data[0])
      for i in range(0, 5):
        insert_data[-1].append(data[i])
  
  SQL.insert_raw_data(connection, frequency, insert_data)
  # for row in SQL.fetch_all_data(connection, frequency):
  #   print(row)
  return date_list
def get_price(stock_id, end_date = '', count = '', frequency = '60'):
  # determine if update is necessary
  if frequency in ['day', 'week', 'month']:
    return get_data_day_tx(stock_id, end_date, count, frequency)
  else:
    return get_data_min_tx(stock_id, count, frequency)

def main():
  get_price('sh603686', end_date = '2025-07-30', count = '10', frequency = 'day')

if __name__ == '__main__':
  main()