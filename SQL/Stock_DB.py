from SQL.Abstract_DB import Abstract_DB
class Stock_DB(Abstract_DB):
  def __init__(self, db_name):
    super().__init__(db_name)
    # self.create_table()
  
  def construt_table_name(self, frequency:str):
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
    return query

  def create_table(self, frequency:str = None):
    if frequency:
      query = self.construt_table_name(frequency)
      try:
        with self.connection:
          self.connection.execute(query)
          print(f"{self.db_name} database created successfully")
          return True
      except Exception as e:
        print(f"Error creating table: {e}")
        raise
    else:
      for frequency in ['week', 'month', 'day', 'm5', 'm15', 'm30', 'm60', 'm120']:
        query = self.construt_table_name(frequency)
        try:
          with self.connection:
            self.connection.execute(query)
            print(f"{self.db_name} database created successfully")
            return True
        except Exception as e:
          print(f"Error creating table: {e}")
          raise