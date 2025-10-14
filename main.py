from update import update
import report
import process_stock_ids
import help_functions
from SQL.Metadata_DB import Metadata_DB
def main():
  #initialize
  metadata = Metadata_DB("metadata")
  if metadata.if_table_exists('metadata') == False:
    metadata.create_table()

  print("options: add, update, report, exit")
  option = input("Enter your choice: ").strip().lower()
  while (option != 'exit'):
    if option == 'add':
      with open('stock_list.txt', 'r') as f:
        stock_id_list = [line.strip() for line in f if line.strip()]
      if not stock_id_list:
        print("No stock IDs found in 'stock_list.txt'.")
        return
      stock_id_list = process_stock_ids.to_tx_ids(stock_id_list)
      print(f"Processed {len(stock_id_list)} stock IDs:")
      update(stock_id_list)

    elif option == 'update':
      stock_id_list = help_functions.database_list()
      if not stock_id_list:
        print("No database files found in 'stock_data' directory.")
        return
      update(stock_id_list)

    elif option == 'report':
      report.report()
    elif option == 'exit':
      print("Exiting the program.")
      return
    else:
      print("Invalid option. Please choose 'add', 'update', or 'report'.")
    option = input("Enter your choice: ").strip().lower()
if __name__ == '__main__':
  main()