import sqlite3
def create_connection(db_name):
  try:
    return sqlite3.connect(db_name)
  except Exception as e:
    print(f"Error connecting to database: {e}")
    raise

def create_table(connection, frequency:str):
  cursor = connection.cursor()
  cursor.execute("""
                 SELECT name FROM sqlite_master WHERE type='table' AND name=?;
                 """, (frequency,))
  table_exists = cursor.fetchone()
  if table_exists:
    print(f"Table {frequency} already exists.")
    return False

  # Create table if it does not exist

  if frequency in ['week', 'month']:
    query = f"""
    CREATE TABLE IF NOT EXISTS {frequency} (
        id INTEGER PRIMARY KEY,
        date DATE NOT NULL
    """
  elif frequency == 'day':
      query = """
      CREATE TABLE IF NOT EXISTS day (
          id INTEGER PRIMARY KEY,
          date DATE NOT NULL,
          MaCap  REAL,
          NeMaCap REAL,
          PE_TTM REAL,
          PE_DY REAL,
          PE_ST REAL,
          PB REAL
      """
  else:
      query = f"""
      CREATE TABLE IF NOT EXISTS m{frequency} (
          id INTEGER PRIMARY KEY,
          datetime DATETIME NOT NULL
      """
      
  query += '''
  , open REAL,
    close REAL,
    high REAL,
    low REAL, 
    MA5 REAL,
    MA10 REAL,
    MA20 REAL,
    MA30 REAL,
    MA60 REAL,
    MA120 REAL,
    MA250 REAL,
    BOLL_UPPER REAL,
    BOLL_LOWER REAL,
    EMA12 REAL,
    EMA26 REAL,
    DEA REAL,
    MACD REAL
  );
  '''
  try:
    with connection:
      connection.execute(query)
      print("Table created successfully")
      return True
  except Exception as e:
    print(f"Error creating table: {e}")
    raise


def insert_raw_data(connection, frequency:str, data:tuple):
  if frequency in ['day', 'week', 'month']:
    query = f"""
    INSERT INTO {frequency} (date, open, close, high, 
    low) 
    VALUES (?, ?, ?, ?, ?)
    """
  else:
    query = f"""
    INSERT INTO m{frequency} (datetime, open, close, high, 
    low) 
    VALUES (?, ?, ?, ?, ?, ?)
    """
  try:
    with connection:
      connection.executemany(query, data)
    print("Data inserted successfully")
  except Exception as e:
    print(f"Error inserting data: {e}")
    raise

def update_data(connection, frequency:str, data:tuple):
  query = f"""
  UPDATE {frequency}
  SET MA5 = ?, MA10 = ?, MA20 = ?, MA30 = ?, MA60 = ?, MA120 = ?, MA250 = ?,
      BOLL_UPPER = ?, BOLL_LOWER = ?, EMA12 = ?, EMA26 = ?, DEA = ?, MACD = ?
  WHERE date = ?
  """
  try:
    with connection:
      connection.execute(query, data)
    print("Data updated successfully")
  except Exception as e:
    print(f"Error updating data: {e}")
    raise
def fetch_all_data(connection, frequency:str):
  query = f"SELECT * FROM {frequency} ORDER BY date ASC"
  try:
    with connection:
      cursor = connection.execute(query)
      rows = cursor.fetchall()
    return rows
  except Exception as e:
    print(f"Error fetching data: {e}")
    raise

def search_latest_date(connection, frequency:str):
  query = f"SELECT date FROM {frequency} ORDER BY date DESC LIMIT 1"
  try:
    with connection:
      cursor = connection.execute(query)
      result = cursor.fetchone()
      return result[0] if result else '2015-01-01'
  except Exception as e:
    print(f"Error fetching latest date: {e}")
    raise

def search_data_by_condition(connection, frequency:str, condition:str, count:int):
  query = f"SELECT close, EMA12, EMA26, DEA FROM {frequency} WHERE {condition} ORDER BY date DESC LIMIT {count}"
  try:
    with connection:
      cursor = connection.execute(query)
      rows = cursor.fetchall()
      if rows:  # check if any data was returned
        close_list, EMA12_list, EMA26_list, DEA_list = zip(*rows)
        return list(close_list), list(EMA12_list), list(EMA26_list), list(DEA_list)
      else:
        return [], [], [], []  # return empty lists if no rows  
  except Exception as e:
    print(f"Error fetching data by condition: {e}")
    raise