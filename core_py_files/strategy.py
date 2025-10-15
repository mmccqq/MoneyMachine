import SQL_operation as SQL
# close_price reach a certain price
def buy_potential(stock_id, frequency, date):
  # just for day frequency now
  data = stock_id.query_rows(frequency, columns='*', where_dict={"date <= ": f"{date}"}, order_by="date DESC", limit=1)
  # data = SQL.search_data_by_condition(connection, frequency, condition, 1)
  close = data[0][9]
  low = data[0][11]
  boll_lower = data[0][20]
  below_boll = False
  if boll_lower > 0 and (low - boll_lower) / boll_lower < 0.01:
    below_boll = True
  return below_boll
