def to_tx_ids(share_ids):
  tx_ids = []
  for share_id in share_ids:
    share_id.lower().strip()
    if len(share_id) > 8:
      print(f"Share ID {share_id} is too long. Skipping.")
      continue
    if len(share_id) < 6:
      for i in range(6 - len(share_id)):
        share_id = '0' + share_id

    if share_id.startswith('sh') or share_id.startswith('sz'):
      tx_ids.append(share_id)
    elif share_id.startswith('60'):
      tx_ids.append('sh' + share_id)
    elif share_id.startswith('00') or share_id.startswith('30'):
      tx_ids.append('sz' + share_id)
    else:
      print(f"Unrecognized share ID format: {share_id}. Skipping.")
  return tx_ids