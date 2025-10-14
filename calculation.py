import formulas
import SQL_operation as SQL
from SQL.Stock_DB import Stock_DB
# calculate indicators.
def calculation(stock, table, date):
  
  indicators = {}
  # MA5, MA10, MA20, MA30, MA60, MA120, MA250,
  # BOLL_UPPER, BOLL_MIDDLE, BOLL_LOWER, EMA12, EMA26, DEA, MACD
  data = stock.query_rows(table, columns='*', where_dict={"date <= ": f"{date}"}, order_by="date DESC", limit=250)
  if not data:
    return [None]*14
  close_list = []

  for row in data:
    close_list.append(row[9])
  # MA
  for n in [5, 10, 20, 30, 60, 120, 250]:
    indicators[f'MA{n}'] = (
        formulas.MA(close_list[:n], n) if len(close_list) >= n else None
    )

  # BOLL
  if len(close_list) >= 20:
    boll = formulas.BOLL(indicators['MA20'], close_list[0:20], 20, 2)
    indicators['BOLL_UPPER'] = boll[0]
    indicators['BOLL_LOWER'] = boll[1]
  else:
    indicators['BOLL_UPPER'] = None
    indicators['BOLL_LOWER'] = None
  # BOLL_MIDDLE is just MA20

  if len(data) <= 1:
    EMA12_list = None
    EMA26_list = None
    DEA_list = None
  else:
    EMA12_list = data[1][21]
    EMA26_list = data[1][22]
    DEA_list = data[1][23]
  # MACD
  if EMA12_list is None:
    indicators["EMA12"] = close_list[0]
    indicators["EMA26"] = close_list[0]
    indicators['DEA'] = 0
    indicators['MACD'] = 0
  else:
    indicators["EMA12"] = formulas.EMA(close_list[0], EMA12_list, 12)
    indicators['EMA26'] = formulas.EMA(close_list[0], EMA26_list, 26)
    DIF = indicators["EMA12"] - indicators["EMA26"]
    indicators['DEA'] = formulas.EMA(DIF, DEA_list, 9)
    indicators['MACD'] = (DIF - indicators['DEA']) * 2
  return indicators
def main():
  # test
  stock = Stock_DB('sh603686')
  indicators = calculation(stock, 'day', '2025-07-26')

if __name__ == '__main__':
  main()