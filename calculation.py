import formulas
import SQL_operation as SQL
# calculate indicators.
def calculation(connection, table, date):
  
  indicators = []
  # MA5, MA10, MA20, MA30, MA60, MA120, MA250,
  # BOLL_UPPER, BOLL_MIDDLE, BOLL_LOWER, EMA12, EMA26, DEA, MACD
  data = SQL.search_data_by_condition(connection, table, f'date <= \'{date}\'', 250)
  close_list = []
  if len(data) <= 1:
    EMA12_list = None
    EMA26_list = None
    DEA_list = None
  else:
    EMA12_list = data[1][21]
    EMA26_list = data[1][22]
    DEA_list = data[1][23]
  for row in data:
    close_list.append(row[9])
  # MA
  if len(close_list) >= 5:
    indicators.append(formulas.MA(close_list[0:5], 5))
    if len(close_list) >= 10:
      indicators.append(formulas.MA(close_list[0:10], 10))
      if len(close_list) >= 20:
        indicators.append(formulas.MA(close_list[0:20], 20))
        if len(close_list) >= 30:  
          indicators.append(formulas.MA(close_list[0:30], 30))
          if len(close_list) >= 60:  
            indicators.append(formulas.MA(close_list[0:60], 60))
            if len(close_list) >= 120:
              indicators.append(formulas.MA(close_list[0:120], 120))
              if len(close_list) >= 250:
                indicators.append(formulas.MA(close_list[0:250], 250))
  
  # fill None for missing MA values
  while len(indicators) < 7:
    indicators.append(None)

  # BOLL
  if len(close_list) >= 20:
    boll = formulas.BOLL(indicators[2], close_list[0:20], 20, 2)
    indicators.append(boll[0])
    indicators.append(boll[1])
  
  # fill None for missing BOLL values
  while len(indicators) < 9:
    indicators.append(None)
  
  # MACD
  if EMA12_list is None:
    indicators.extend([close_list[0], close_list[0], 0, 0])
  else:
    EMA12 = formulas.EMA(close_list[0], EMA12_list, 12)
    indicators.append(EMA12)
    EMA26 = formulas.EMA(close_list[0], EMA26_list, 26)
    indicators.append(EMA26)
    DIF = EMA12 - EMA26
    DEA = formulas.EMA(DIF, DEA_list, 9)
    indicators.append(DEA)
    MACD = (DIF - DEA) * 2
    indicators.append(MACD)
  
  return indicators