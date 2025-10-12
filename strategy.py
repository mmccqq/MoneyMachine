import SQL_operation as SQL
# close_price reach a certain price
def buy_potential(connection, frequency, date):
  condition = f"date = '{date}'"
  # just for day frequency now
  data = SQL.search_data_by_condition(connection, frequency, condition, 1)
  close = data[8]
  low = data[10]
  boll_lower = data[19]
  below_boll = False
  if (low - boll_lower) / boll_lower < 0.02:
    below_boll = True
  return below_boll