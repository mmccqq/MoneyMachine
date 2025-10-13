def to_tx_ids(stock_ids):
  tx_ids = []
  for stock_id in stock_ids:
    stock_id.lower().strip()
    if len(stock_id) > 8:
      print(f"stock ID {stock_id} is too long. Skipping.")
      continue
    if len(stock_id) < 6:
      for i in range(6 - len(stock_id)):
        stock_id = '0' + stock_id

    if stock_id.startswith('sh') or stock_id.startswith('sz'):
      tx_ids.append(stock_id)
    elif stock_id.startswith('60'):
      tx_ids.append('sh' + stock_id)
    elif stock_id.startswith('00') or stock_id.startswith('30'):
      tx_ids.append('sz' + stock_id)
    else:
      print(f"Unrecognized stock ID format: {stock_id}. Skipping.")
  return tx_ids