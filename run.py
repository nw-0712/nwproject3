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



# Calculate total shipments per location
def calculate_shipments(shipment_data):
    shipments_summary = defaultdict(int)
    for shipment in shipment_data:
        shipments_summary[shipment["location"]] += shipment["quantity"]
    return shipments_summary

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