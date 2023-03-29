from tabulate import tabulate

# Define a Shoe class with country, code, product, cost, and quantity attributes
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    #Define methods to get the cost and quantity of a shoe
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def get_value_per_item(self):
        return self.cost / self.quantity if self.quantity > 0 else 0

    #Define a method to print out the shoe object in a specific format
    def __str__(self):
        return f"{self.country}\t{self.code}\t{self.product}\t{self.cost}\t{self.quantity}"

#Initialize an empty list to store shoe objects
shoes_list = []

#Define a function to read shoe data from a file and store it in the shoes_list
def read_shoes_data():
    try:
        #Open the file named "inventory.txt"
        with open('inventory.txt', 'r') as file:
            next(file)  # Skip header line
            #For each line in the file, create a Shoe object and append it to the shoes_list
            for line in file:
                data = line.strip().split(',')
                shoes_list.append(Shoe(*data))
        print("Inventory data loaded successfully from file.")
    #If the file is not found, print an error message
    except FileNotFoundError:
        print("File not found. Please check the file name and try again.")

def capture_shoes():
    global shoes_list  #declare that shoes_list is a global variable
    #prompt user for input data
    country = input("Enter country: ")
    code = input("Enter code: ")
    product = input("Enter product name: ")
    cost = float(input("Enter cost: "))
    quantity = int(input("Enter quantity: "))
    #create new Shoe object with input data
    new_shoe = Shoe(country, code, product, cost, quantity)
    #append new Shoe object to global shoes_list
    shoes_list.append(new_shoe)
    #write new data to "inventory.txt" file
    with open("inventory.txt", "a") as f:
        f.write(f"{country},{code},{product},{cost},{quantity}\n")
    #print success message
    print("Shoe added successfully.")

def view_all():
    global shoes_list
    #Create headers for the table
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    #Initialize empty list to store data
    data = []
    try:
        with open("inventory.txt", "r") as file:
            next(file)  # skip the header row
            #Parse each line and append to data list
            for line in file:
                fields = line.strip().split(",")
                data.append(fields)
        #Print table of inventory data from file using tabulate
        print(tabulate(data, headers=headers))
    except FileNotFoundError:
        print("Error: inventory file not found.")
        #Add shoe data from the shoes_list to data list
    for shoe in shoes_list:
        data.append([shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity])
    #Print table of all inventory data using tabulate
    print(tabulate(data, headers=headers))

def re_stock():
    global shoes_list
    #Check if there are shoes in the inventory
    if not shoes_list:
        print("Error: no shoes in inventory.")
        return

    #Get the shoe with the lowest quantity
    lowest_qty_shoe = min(shoes_list, key=lambda shoe: shoe.quantity)

    #Prompt user for the quantity of the shoe to restock
    restock_qty = int(input(f"Enter quantity of {lowest_qty_shoe.product} to re-stock: "))

    #Update the quantity of the shoe in the inventory
    lowest_qty_shoe.quantity += restock_qty

    #Print confirmation message
    print(f"{restock_qty} {lowest_qty_shoe.product} added to inventory.")

    #Validate the input quantity
    try:
        restock_qty = int(restock_qty)
        if restock_qty < 0:
            raise ValueError
    except ValueError:
        print("Error: invalid quantity entered.")
        return

    #Update the quantity of the shoe in the inventory
    lowest_qty_shoe.quantity += restock_qty

    #Print confirmation message
    print(f"{restock_qty} units of {lowest_qty_shoe.product} restocked successfully.")


def search_shoe():
    global shoes_list
    #Get the shoe code from user input
    shoe_code = input("Enter shoe code to search: ")
    #Initialize variables for displaying the search results
    found = False
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    data = []
    try:
        with open("inventory.txt", "r") as file:
            next(file)  # skip the header row
            for line in file:
                fields = line.strip().split(",")
                #If the shoe code matches, display the shoe data and set found flag to True
                if fields[1] == shoe_code:
                    found = True
                    print(tabulate([fields], headers=headers))
                    break
        #If no shoe is found, display an appropriate message
        if not found:
            print(f"No shoe found with code {shoe_code}.")
    #If the inventory file is not found, display an error message
    except FileNotFoundError:
        print("Error: inventory file not found.")

#Method for value per item
def value_per_item():
    try:
        with open("inventory.txt", "r") as file:
            next(file)  # skip the header row
            value_data = []
            #Loop through each line in the file and calculate the value per item
            for line in file:
                fields = line.strip().split(",")
                value_data.append([fields[1], int(fields[3]) / int(fields[4])])
            #Print a table of the code and value per item for each shoe
            print(tabulate(value_data, headers=["Code", "Value"]))
    except FileNotFoundError:
        print("Error: inventory file not found.")

def highest_qty():
    global shoes_list
    #Check if the inventory is empty
    if not shoes_list:
        print("Error: no shoes in inventory.")
        return
    #Find the product with the highest quantity using the max() function with a lambda
    highest_qty_shoe = max(shoes_list, key=lambda shoe: shoe.quantity)
    #Print the product with the highest quantity
    print(f"The product with the highest quantity is {highest_qty_shoe.product} from {highest_qty_shoe.country}.")



while True:
    #Display the available options to the user.
    print("1. Read shoes data from file")
    print("2. Capture new shoe")
    print("3. View all shoes")
    print("4. Re-stock shoes")
    print("5. Search for a shoe")
    print("6. Calculate value per item")
    print("7. Determine product with highest quantity")
    print("0. Exit")
    #Ask the user to enter their choice.
    choice = input("Enter your choice: ")
    #Use a series of if/elif statements to perform the desired action based on the user's choice.
    if choice == "1":
        read_shoes_data()
    elif choice == "2":
        capture_shoes()
    elif choice == "3":
        view_all()
    elif choice == "4":
        re_stock()
    elif choice == "5":
        search_shoe()
    elif choice == "6":
        value_per_item()
    elif choice == "7":
        highest_qty()
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")