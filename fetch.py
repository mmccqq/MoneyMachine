import requests, json
from datetime import datetime
import SQL_operation as SQL

def get_data_min_tx(share_id, count = '', frequency = '60m'):

  URL = f'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={share_id},m{frequency},,{count}'

  response = requests.get(URL)
  raw_data = json.loads(response.content)
  share_min_data = raw_data['data'][f'{share_id}'][f'm{frequency}']
  result = []
  
  connection = SQL.create_connection(f'{share_id}.db')
  latest = SQL.search_latest_date(connection, frequency)

  for index, data in enumerate(share_min_data):
    result.append([])
    if int(latest) < int(data[0]):
      result[index].append(data[0][0:4])
      result[index].append(data[0][4:8])
      result[index].append(data[0][8:12])
      for i in range(1, 5):
        result[index].append(data[i])

  SQL.create_table(connection, frequency)
  #need to avoid duplicate data
  SQL.insert_raw_data(connection, frequency, result)

def get_data_day_tx(share_id, end_date = '', count = '', frequency = 'day'):
  URL = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={share_id},{frequency},,{end_date},{count},qfq'
  response = requests.get(URL)
  raw_data = json.loads(response.content)
  share_day_data = raw_data['data'][f'{share_id}'][f'qfq{frequency}']
  
  connection = SQL.create_connection(f'share_data/{share_id}.db')
  SQL.create_table(connection, frequency)
  #   EMA12, EMA25, DEA = input("Please input the latest " \
  #   "EMA12, EMA25, DEA values separated by commas: ").split(',')


  # need to avoid duplicate data
  latest = SQL.search_latest_date(connection, frequency)
  result = []
  date_list = []
  for data in share_day_data:
    if latest < data[0]:
      result.append([])
      date_list.append(data[0])
      for i in range(0, 5):
        result[-1].append(data[i])
  
  SQL.insert_raw_data(connection, frequency, result)
  # for row in SQL.fetch_all_data(connection, frequency):
  #   print(row)
  return date_list
def get_price(share_id, end_date = '', count = '', frequency = '60'):
  # determine if update is necessary
  if frequency in ['day', 'week', 'month']:
    return get_data_day_tx(share_id, end_date, count, frequency)
  else:
    return get_data_min_tx(share_id, count, frequency)

def main():
  get_price('sh603686', end_date = '2025-07-30', count = '10', frequency = 'day')

if __name__ == '__main__':
  main()