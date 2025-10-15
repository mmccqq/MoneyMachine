import requests, json
from datetime import datetime
from SQL.Stock_DB import Stock_DB

def get_data_day_tx(stock_id, end_date = '', count = '', frequency = 'day'):
  URL = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={stock_id},{frequency},,{end_date},{count},qfq'
  response = requests.get(URL)
  raw_data = json.loads(response.content)
  stock_day_data = raw_data['data'][f'{stock_id}'][f'qfq{frequency}']
  
  stock = Stock_DB(stock_id)

  if stock.if_table_exists(frequency) == False:
    stock.create_table(frequency)

  # need to avoid duplicate data
  latest = stock.query_rows(frequency, columns='date', 
                            order_by="date DESC", limit=1)
  if not latest:
    latest = '2015-01-01'
  else:
    latest = latest[0][0]
  
  insert_data = []
  date_list = []
  for data in stock_day_data:
    if latest < data[0]:
      insert_data.append([])
      date_list.append(data[0])
      for i in range(5):
        insert_data[-1].append(data[i])
  title = ["date", "open", "close", "high", "low"]
  stock.insert_data(frequency, title, insert_data)

  rows = stock.query_rows(frequency)
  # for row in rows:
  #   print(row)

  return date_list
def get_price(stock_id, end_date = '', count = '', frequency = 'm60'):
  # determine if update is necessary
  if frequency in ['day', 'week', 'month']:
    return get_data_day_tx(stock_id, end_date, count, frequency)
  # else:#frequency in ['m5', 'm15', 'm30', 'm60', 'm120']:
  #   return get_data_min_tx(stock_id, count, frequency)

def main():
  get_price('sh603686', end_date = '2024-07-30', count = '10', frequency = 'day')

if __name__ == '__main__':
  main()