from abc import ABC, abstractmethod
import sqlite3

class Abstract_DB(ABC):
  def __init__(self, db_name):
    self.connection = sqlite3.connect(f"stock_data/{db_name}.db")
    self.cursor = self.connection.cursor()
    self.db_name = db_name

  @abstractmethod
  def create_table(self):
    pass

  def if_table_exists(self, frequency:str):
    try:
      with self.connection:
        self.cursor.execute("""
                      SELECT name FROM sqlite_master WHERE type='table' AND name=?;
                      """, (frequency,))
        table_exists = self.cursor.fetchone()
        return bool(table_exists)
    except Exception as e:
      print(f"Error checking table existence: {e}")
      raise

# # Insert into a daily table
# insert_row(conn, "day", {"date": "2025-10-12", "close": 182.5, "volume": 1000000})
# # Insert into a weekly table (different columns)
# insert_row(conn, "week", {"week_start": "2025-10-06", "high": 185.0, "low": 178.5})
  def insert_data(self, table_name, titles, data_dict):
    """
    Insert a row into any table with columns specified in data_dict.
    
    :param connection: SQLite connection object
    :param table_name: string, name of the table
    :param data_dict: dictionary, keys = column names, values = values to insert
    """
    columns = ', '.join(titles)
    placeholders = ', '.join(['?'] * len(titles))
    # values = list(data_dict.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
      with self.connection:
        self.cursor.executemany(query, data_dict)
        return True
    except Exception as e:
      print(f"Error inserting data: {e}")
      raise
  
  # Update close price for a specific date
  # update_row(conn, "day", {"close": 183.0}, {"date": "2025-10-12"})
  def update_row(self, table_name, data_dict, where_dict):
    """
    Update a row in any table with columns in data_dict based on conditions in where_dict.
    """
    set_clause = ', '.join([f"{col}=?" for col in data_dict.keys()])
    where_clause = ' AND '.join([f"{col}=?" for col in where_dict.keys()])
    
    values = list(data_dict.values()) + list(where_dict.values())
    
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

    try:
      with self.connection:
        self.cursor.execute(query, values)
        return True
    except Exception as e:
      print(f"Error updating row: {e}")
      raise
  
  # Get the latest daily row
# rows = query_rows(conn, "day", order_by="date DESC", limit=1)
# print(rows)
  def query_rows(self, table_name, columns='*', where_dict=None, order_by=None, limit=None):
    """
    Query rows from a table flexibly.
    """
    col_str = ', '.join(columns) if isinstance(columns, (list, tuple)) else columns
    query = f"SELECT {col_str} FROM {table_name}"
    
    values = []
    if where_dict:
        where_clause = ' AND '.join([f"{col}?" for col in where_dict.keys()])
        query += f" WHERE {where_clause}"
        values = list(where_dict.values())
    
    if order_by:
        query += f" ORDER BY {order_by}"
    
    if limit:
        query += f" LIMIT {limit}"
    
    try:
      with self.connection:
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    except Exception as e:
      print(f"Error querying rows: {e}")
      raise

    