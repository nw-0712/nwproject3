import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('shipping_inventory')

sales = SHEET.worksheet('sales')
data = sales.get_all_values()

# Function to validate data
def validate_data(values):
    """
    Validates that the input contains exactly 10 numbers.
    """
    try:
        if len(values) != 10:
            raise ValueError(
                f"Expected 10 values, but got {len(values)}"
            )
        [int(value) for value in values]  # Ensure all are integers
    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    return True

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a loop to collect a valid string of data from the terminal, 
    which must be a string of 10 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be 10 numbers, separated by commas.")
        print("Example: 1,2,3,4,5,7,8,9,10\n")

        data_str = input("Enter your data here:/n")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def calculate_and_update_surplus():
    """
    Calculate surplus data from the 'inventory' worksheet.
    Surplus = Stock - Sales.
    Update the surplus values in column 4 ('Surplus') for each row.
    """
    print("\nCalculating surplus data from the 'inventory' worksheet...")

    # Open the "inventory" worksheet
    inventory_sheet = SHEET.worksheet("inventory")

    # Fetch all rows of data from the worksheet
    data = inventory_sheet.get_all_values()

    # Ensure the worksheet has at least 4 columns (Sales, Stock, and Surplus columns must exist)
    if len(data[0]) < 4:
        print("Error: 'inventory' worksheet must have at least 4 columns: Sales, Stock, and Surplus.")
        return

    # Iterate through each row (skipping the header row)
    updated_surplus = []
    for i, row in enumerate(data[1:], start=2):  # Start from the second row (index 2 in Google Sheets)
        try:
            sales = int(row[0])  # Column 1: Sales
            stock = int(row[1])  # Column 2: Stock
            surplus = stock - sales  # Calculate surplus
            updated_surplus.append(surplus)

            # Update the surplus value in column 4 ('Surplus') for the current row
            inventory_sheet.update_cell(i, 4, surplus)  # Column 4 is the Surplus column
        except ValueError:
            print(f"Row {i} contains invalid data: {row}")
            continue

    print("Surplus data updated successfully in the 'inventory' worksheet.\n")
    return updated_surplus



# Main execution
def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    # Get sales data from worksheet
    sales_data = [int(num) for num in data]
    # Calculate surplus data and update the "surplus" worksheet
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    # Update surplus data in the "inventory" worksheet
    update_inventory_surplus(new_surplus_data)
   
   

# Run the program
if __name__ == "__main__":
  
  