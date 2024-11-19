from customer import Customer
from driver import Driver
from admin import Admin
from vehicle import Vehicle, Car, Bike, Bus
from pymongo import MongoClient
from db import get_db_connection


class VehicleRentalApp:
    def __init__(self):
        print("Welcome to the Vehicle Rental Management System!")
        self.running = True
        self.client = get_db_connection() 
        self.db = self.client["vehicle-db"]  # Use the "vehicle-db" database
        self.customers_collection = self.db["customers"]
        self.vehicles_collection = self.db["vehicles"]
        self.drivers_collection = self.db["drivers"]
        self.admin_collection=self.db["admins"]
        self.main_menu()

    def main_menu(self):
        while self.running:
            print("\nLogin Page")
            print("1. Customer")
            print("2. Driver")
            print("3. Admin")
            print("4. Exit")
            
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.customer_page()
                elif choice == 2:
                    self.driver_options()
                elif choice == 3:
                    self.admin_page()
                elif choice == 4:
                    self.exit_app()
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def customer_page(self):
        n=int(input("1.Login\n2.Signin:"))
        if n==1:
            name=input("enter Name:")
            phone=input("enter phone:")
            passw=input("enter password:")
            cid=input("enter Id:")
            self.customers_collection.insert_one({
                "name":name,
                "phone":phone,
                "password":passw,
                "customer_id":cid
            })
            return 
        
        print("\n--- Customer Page ---")
        customer_id = input("Enter your customer ID: ")

        # Check if the customer already exists
        customer_data = self.customers_collection.find_one({"customer_id": customer_id})
        # print(customer_data)
        if(not customer_data):
            return
        passw=customer_data["password"]

        crt_pass=input("enter password:")

        if passw!=crt_pass:
            print("wrong Pass")
            return
        
        name=customer_data["name"]
        phone=customer_data["phone"]
        # customer_data=False

        if customer_data:
            print(f"Welcome back, {customer_data['name']}")
            customer = Customer(customer_id, name, phone)
            # Provide customer options to choose actions
            self.customer_options(customer)
        else:
            # Add a new customer if not found
            new_customer = Customer(customer_id, name, phone)
            print(f"Customer {name} added successfully.")
            customer = new_customer
        
        

    def customer_options(self, customer):
        """
        Provides options for the customer to manage their booking and vehicle.
        """
        while True:
            try:
                print("\nCustomer Menu:")
                print("1. Book Vehicle (with or without driver)")
                print("2. View Booking History")
                print("3. Return Vehicle")
                print("4. Back to Main Menu")
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    destination=str(input("enter Des:"))
                    start_date = str(input("start Date YYYY-MM-DD:"))
                    end_date = str(input("End Date YYYY-MM-DD:"))
                    arr=customer.search_vehicle(start_date, end_date)
                   
                    if(len(arr)>0):
                        vehicle_id = input("Enter the vehicle ID: ")
                        with_driver = input("Would you like a driver? (yes/no): ").lower() == 'yes'
                        customer.choose_vehicle(vehicle_id,start_date, end_date,destination,with_driver)
                    else:
                        print("No avaliable vehicles......\n")
                elif choice == 2:
                    customer.see_booking_history()
                elif choice == 3:
                    vehicle_id = input("Enter the vehicle ID to return: ")
                    start_date = str(input("start Date YYYY-MM-DD:"))
                    end_date = str(input("End Date YYYY-MM-DD:"))
                    customer.return_vehicle(vehicle_id,start_date,end_date)
                elif choice == 4:
                    print("Returning to Main Menu.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def driver_page(self):
        """
        Driver Page where the driver can manage their trips.
        """
        print("\n--- Driver Page ---")
        driver_id = input("Enter your driver ID: ")
        name = input("Enter your name: ")
        phone = input("Enter your phone number: ")
        license_number = input("Enter your license number: ")

        # Initialize the Driver object
        driver = Driver(driver_id, name, phone, license_number)

        # Save driver to the database if it doesn't already exist
        if not self.drivers_collection.find_one({"driver_id": driver_id}):
            self.drivers_collection.insert_one(driver.__dict__)
        else:
            print(f"Driver {driver_id} already exists.")

        # Show the Driver options menu
        self.driver_options(driver)

    def driver_options(self):
        """
        Provides options for the driver to manage their trips (accept customer, update trip, or checkout).
        """
        driver_id = input("Enter your Driver ID: ")
        driver_data = self.drivers_collection.find_one({"driver_id": driver_id})
        if(not driver_data):
            print("Invalid Id")
            return
        
        passw=driver_data["password"]

        crt_pass=input("enter password")

        if passw!=crt_pass:
            print("wrong Pass")
            return

        
        name=driver_data["name"]
        phone=driver_data["phone"]
        lic=driver_data["license_number"]

        driver=Driver(driver_id,name,phone,lic)
        print("\nWelcome {}".format(name))
        while True:
            try:
                print("\nDriver Menu:")
                print("1. View Customer for a Trip")
                print("2. Update Trip Details")
                print("3. Complete the Trip (Checkout)")
                print("4. Exit")
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    print("------Trip Assignment-----\n")
                    driver.view_trip()
                elif choice == 2:
                    start_date = str(input("start Date YYYY-MM-DD:"))
                    vehicle_id = input("Enter the vehicle ID: ").strip()
                    customer_id = input("Enter the customer ID: ").strip()
                    destination=str(input("enter destin:"))

                    update=input("Enter any update:")

                    # Call update_trip_details with the input values
                    driver.update_trip(destination,vehicle_id,customer_id,update,start_date)
                elif choice == 3:
                    driver.checkout()
                    return
                elif choice == 4:
                    print("Exiting Driver Menu.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")




    
    def admin_page(self):
        print("\n--- Admin Page ---")
        admin_id=str(input("enter admin id:"))
        admin_data=self.admin_collection.find_one({
            "admin_id":admin_id
        })

        passw=input("enter password:")
        crt_pass=admin_data["password"]

        if passw != crt_pass:
            print("invalid credential...\n")
            return

        admin=Admin(admin_id)


        while True:
            print("\nAdmin Menu")
            print("1. Manage Vehicles")
            print("2. Manage Drivers")
            print("3. View Customer Records")
            print("4. Back to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    admin.manage_vehicles()  # Calls the method to manage vehicles
                elif choice == 2:
                    admin.manage_drivers()   # Calls the method to manage drivers
                elif choice == 3:
                    admin.see_customer_records()  # Calls the method to view customer records
               # Calls charge_customer_fine method
                elif choice == 4:
                    print("Exiting Admin Menu.")
                    break  # Exit the loop to return to Main Menu
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")





    def exit_app(self):
        print("\nThank you for using the Vehicle Rental Management System!")
        self.running = False


# Start the app
if __name__ == "__main__":
    app = VehicleRentalApp()
