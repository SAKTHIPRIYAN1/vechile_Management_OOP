from user import User
from pymongo import MongoClient
from db import get_db_connection

class Admin(User):
    def __init__(self, user_id):
        super().__init__(user_id)  # Initialize User class
        self.client =get_db_connection()  # MongoDB connection
        self.db = self.client["vehicle-db"]  # Use the "vehicle-db" database
        self.vehicles_collection = self.db["vehicles"]
        self.drivers_collection = self.db["drivers"]
        self.customers_collection = self.db["customers"]
        self.trips_collection = self.db["trips"]

    def manage_vehicles(self):
        """Displays a choice menu and executes actions based on user's input."""
        while True:
            print("\n--- Vehicle Management Menu ---")
            print("1. Add Vehicle")
            print("2. Update Vehicle")
            print("3. Delete Vehicle")
            print("4. View All Vehicles")
            print("5. Exit")

            choice = input("Please choose an option: ")

            if choice == '1':
                # Get vehicle details from user to add
                model = input("Enter vehicle model: ")
                vehicle_type = input("Enter vehicle type (Car,Bus): ")
                vechile_id=input("enter the vechile id:")
                mile=input("enter milage:")
                self.add_vehicle(model,vehicle_type,vechile_id,mile)
            
            elif choice == '2':
                # Get vehicle model to update
                vechile_id= input("Enter vehicle id to update: ")
                vehicle = self.vehicles_collection.find_one({"vehicle_Id": vechile_id})
                if vehicle:
                    model = input("Enter vehicle model: ")
                    vehicle_type = input("Enter vehicle type (e.g., Sedan, SUV): ")
                    mile=input("enter milage:")
                    self.update_vehicle(model,vehicle_type,vechile_id,mile)
                else:
                    print(f"Vehicle not found.")
            
            elif choice == '3':
                # Get vehicle model to delete
                vechile_id = input("Enter vehicle id to delete: ")
                vehicle = self.vehicles_collection.delete_one({"vechile_Id":vechile_id})
                print("\n Vechile deleted.....")
            
            elif choice == '4':
                # View all vehicle records
                self.see_vehicle_records()
            
            elif choice == '5':
                print("Exiting vehicle management.")
                break
            
            else:
                print("Invalid choice. Please try again.")




    def add_vehicle(self, model,vehicle_type,vechile_id,mile):
        """Adds a new vehicle to the system."""
        new_data={
                "model": model,
                "vehicle_Id":vechile_id,
                "vehicle_type": vehicle_type,
                "mileage": mile,
        }
        self.vehicles_collection.insert_one(new_data)
        print(f"Vehicle  added successfully.")
    
    def update_vehicle(self, model,vehicle_type,vechile_id,mile):
        """Updates vehicle details."""
        new_data={
                "model": model,
                "vehicle_type": vehicle_type,
                "mileage": mile,
        }
        result = self.vehicles_collection.update_one(
            {"vehicle_Id":vechile_id},
            {"$set": new_data}
        )
        if result.modified_count > 0:
            print(f"Vehicle details updated successfully.")
        else:
            print(f"Vehicle  not found.")

    
    def see_vehicle_records(self):
        """Displays all the vehicle records."""
        vehicles = self.vehicles_collection.find()
        if not vehicles:
            print("No vehicles found in the system.")
            return
        print("\n--- Vehicle Records ---")
        vehicle_list=list(vehicles)
        for vehicle in vehicle_list:
            print(f"{vehicle['model']} ({vehicle['vehicle_type']}) - Id: {vehicle['vehicle_Id']}")

    
    def manage_drivers(self):
        """Displays a choice menu and executes actions based on user's input."""
        while True:
            print("\n--- Driver Management Menu ---")
            print("1. Add Driver")
            print("2. Update Driver")
            print("3. Delete Driver")
            print("4. View All Drivers")
            print("5. Exit")

            choice = input("Please choose an option: ")

            if choice == '1':
                # Get driver details from user to add
                name = input("Enter driver's name: ")
                license_number = input("Enter driver's license number: ")
                experience = input("Enter years of driving experience: ")
                phone=input("enter Phone:")
                vehicle_Id=input("Assign Vechile:")
                driver_id=input("enter driver_id:")
                
                self.drivers_collection.insert_one({
                    "name":name,
                     "license_number" :license_number,
                    "experience" :experience,
                    "phone":phone,
                    "vehicle_Id":vehicle_Id,
                    "driver_id":driver_id
                })

                print("added Successfully..\n")
            
            elif choice == '2':
                # Get driver name to update
                driver_id = input("Enter driver's id to update: ")
                name = input("Enter driver's name: ")
                license_number = input("Enter driver's license number: ")
                experience = input("Enter years of driving experience: ")
                phone=input("enter Phone:")
                vehicle_Id=input("Assign Vechile:")
                driver = self.drivers_collection.find_one({"driver_id": driver_id})
                if driver:
                    result = self.drivers_collection.update_one(
                        {"driver_id": driver_id},{
                    "name":name,
                     "license_number" :license_number,
                    "experience" :experience,
                    "phone":phone,
                    "vehicle_Id":vehicle_Id,
                        }   
                    )
                    if result.modified_count > 0:
                        print(f"Driver details updated successfully.")
                    else:
                        print(f"Driver  not found.")

            
            elif choice == '3':
                # Get driver name to delete
                driver_id = input("Enter driver's id to update: ")
                driver = self.drivers_collection.delete_one({"driver_id": driver_id})
                print("deleted Successfully....\n")
            
            elif choice == '4':
                # View all driver records
                self.see_driver_records()
            
            elif choice == '5':
                print("Exiting driver management.")
                break


    
    
    
    def see_driver_records(self):
        """Displays all the driver records."""
        drivers = self.drivers_collection.find()
        if not drivers:
            print("No drivers found in the system.")
            return
        print("\n--- Driver Records ---")
        driv=list(drivers)
        for driver in driv:
            print(f"{driver['name']} - License: {driver['license_number']}")
    
   
    def see_customer_records(self):
        """Displays all the customer records."""
        customers = self.customers_collection.find()
        if not customers:
            print("No customers found in the system.")
            return
        print("\n--- Customer Records ---")
        cus=list(customers)
        for customer in cus:
            print(f"{customer['name']} - Phone: {customer['phone']}")
