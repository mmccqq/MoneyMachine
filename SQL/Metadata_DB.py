from SQL.Abstract_DB import Abstract_DB
class Metadata_DB(Abstract_DB):
  def __init__(self, db_name):
    super().__init__(db_name)

  def create_table(self):
    query = '''
    CREATE TABLE IF NOT EXISTS metadata (
        stock_id TEXT PRIMARY KEY,
        name TEXT,
        price REAL,
        change REAL,
        last_month_updated DATE,
        last_week_updated DATE,
        last_day_updated DATE,
        last_m120_updated DATETIME,
        last_m60_updated DATETIME,
        last_m30_updated DATETIME,
        last_m15_updated DATETIME,
        last_m5_updated DATETIME
    );
    '''
    try:
      with self.connection:
        self.connection.execute(query)
        print(f"{self.db_name} database created successfully")
        return True
    except Exception as e:
      print(f"Error creating metadata table: {e}")
      raise
  
  def update_metadata(self, stock_id, name, price, change, frequency, update_time):

    query = f"""
    INSERT INTO metadata (stock_id, name, price, change, last_{frequency}_updated)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(stock_id) DO UPDATE SET last_{frequency}_updated=excluded.last_{frequency}_updated;
    """
    try:
      with self.connection:
        self.connection.execute(query, (stock_id, name, price, change, update_time))
        return True
    except Exception as e:
      print(f"Error updating metadata: {e}")
      raise


