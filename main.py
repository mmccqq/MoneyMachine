from update import update
import report
import process_share_ids
import help_functions
def main():
  print("options: add, update, report, exit")
  option = input("Enter your choice: ").strip().lower()
  while (option != 'exit'):
    if option == 'add':
      with open('share_list.txt', 'r') as f:
        share_id_list = [line.strip() for line in f if line.strip()]
      if not share_id_list:
        print("No share IDs found in 'share_list.txt'.")
        return
      share_id_list = process_share_ids.to_tx_ids(share_id_list)
      print(f"Processed {len(share_id_list)} Share IDs:")
      update(share_id_list)

    elif option == 'update':
      share_id_list = help_functions.database_list()
      if not share_id_list:
        print("No database files found in 'share_data' directory.")
        return
      update(share_id_list)

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