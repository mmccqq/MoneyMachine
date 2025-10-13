import os
def database_list():
  share_id_list = []
  with os.scandir('./share_data') as entries:
    for entry in entries:
      if entry.is_file() and entry.name.endswith('.db'):
        share_id = entry.name[:-3]
        share_id_list.append(share_id)
  return share_id_list