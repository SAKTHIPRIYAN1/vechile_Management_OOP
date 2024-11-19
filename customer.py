from user import User
from db import get_db_connection

class Customer(User):
    def __init__(self, customer_id, name, phone):
        super().__init__(customer_id, name, phone)
        self.client = get_db_connection()  # Database connection
        self.db = self.client["vehicle-db"]  # Use the "vehicle-db" database
        self.customers_collection = self.db["customers"]
        self.customer_id=customer_id
        self.vehicles_collection = self.db["vehicles"]
        self.booking_coll=self.db["bookings"]
        self.history_coll=self.db["history"]
        self.driv=self.db["drivers"]
        self.customer_data = self.customers_collection.find_one({"customer_id": customer_id})
        self.trips_collection = self.db["trips"]

        # If the customer does not exist, insert a new document
        if not self.customer_data:
            self.customers_collection.insert_one({
            "customer_id":customer_id,
            "name": name,
            "phone": phone
        })

    def search_vehicle(self, start_date, end_date):
        """Searches for available vehicles within a given date range."""

        print(f"Searching for vehicles available from {start_date} to {end_date}...\n")
        
        unavailable_vehicles = self.booking_coll.find({
        "end_date": {"$gte": start_date}  # Vehicles booked until >= start_date are unavailable
        })
    
        # Collect all unavailable vehicle IDs
        unavailable_vehicle_ids = set([doc["vehicle_Id"] for doc in unavailable_vehicles])

        # Find all vehicles in vehicle_collection
        all_vehicles = self.vehicles_collection.find()
        
        # Filter out unavailable vehicles and append the rest to the available list
        available_vehicles = []
        for vehicle in all_vehicles:
            if vehicle["vehicle_Id"] not in unavailable_vehicle_ids:
                available_vehicles.append(vehicle)

        if available_vehicles:
            print("--- Available Vehicles ---")
            for idx, vehicle in enumerate(available_vehicles, start=1):
                print(f"{idx}. {vehicle['model']} ==> {vehicle['vehicle_Id']}")
            print("\n")
            return available_vehicles
        else:
            print("No vehicles are available for the selected dates.")
            return []

    def choose_vehicle(self, vehicle_id, start_date, end_date,destination ,with_driver=False):
        """Books a vehicle for the customer, with or without a driver."""
        
        vehicle = self.vehicles_collection.find_one({"vehicle_Id": vehicle_id})
        
   
        driver_info = "with a driver" if with_driver else "without a driver"

        drivers = self.driv.find({
            "vehicle_Id": vehicle_id  # This checks if the array contains the value
        })

        # Convert to list to display results
        drivers_list = list(drivers)
        if(drivers_list):
            driv=drivers_list[0]

        print(f"Booking confirmed for {vehicle['model']} {driver_info} :: {driv["name"]}.")
        
        # Update vehicle availability and driver assignment
        self.vehicles_collection.update_one(
            {"vehicle_Id": vehicle_id},
            {"$set": {"available": False, "driver_assigned": with_driver}}
        )
        if with_driver:
            self.trips_collection.insert_one({
                "customer_id":self.customer_id,
                "customer_name":self.name,
                "driver_id":driv["driver_id"],
                "vechile_Id":vehicle_id,
                "driver_name":driv["name"],
                "destination":destination,
                "start_date":start_date,
                "end_date":end_date,
                "updates":[]
            })

        # Update customer's booking
        self.customers_collection.update_one(
            {"customer_id": self.customer_id},
            {"$push": {"bookings": vehicle_id}}
        )

        self.booking_coll.insert_one({

            "customer_id":self.customer_id,
            "vehicle_Id":vehicle_id,
            "start_date":start_date,
            "end_date":end_date,
            "with_driver":with_driver,
            "destination":destination,
            "status":"Confirmed"
        })
        
        print(f"{vehicle['vehicle_Id']} ==> {vehicle['model']} has been booked successfully.")

    def write_review(self, vehicle_id, review, rating):
        """Allows the customer to write a review for a vehicle."""
        vehicle = self.vehicles_collection.find_one({"vehicle_Id": vehicle_id})

        if vehicle_id not in self.customer_data.get("bookings", []):
            print("You can only review vehicles you have booked.")
            return
        
        if 1 <= rating <= 5:
            self.vehicles_collection.update_one(
                {"vehicle_id": vehicle_id},
                {"$push": {"reviews": {"customer_name": self.name, "review": review, "rating": rating}}}
            )
            print(f"Review submitted for {vehicle['model']}: {rating} stars - '{review}'")
        else:
            print("Invalid rating. Please provide a rating between 1 and 5.")

    def return_vehicle(self, vehicle_id,start_date,end_date):
        """Handles the return of a booked vehicle."""
        vehicle = self.vehicles_collection.find_one({"vehicle_Id": vehicle_id})

        if vehicle_id not in self.customer_data.get("bookings", []):
            print("You cannot return a vehicle you haven't booked.")
            return
        
        if vehicle :
            booking_data=self.booking_coll.find_one({
                "vehicle_Id":vehicle_id,
                "customer_id":self.customer_id,
                "start_date":start_date,
                "end_date":end_date
            })
 


            if booking_data:
                # Remove the MongoDB-specific _id field to avoid duplicate key errors
                self.booking_coll.delete_one({
                    "vehicle_Id":vehicle_id,
                    "customer_id":self.customer_id
                })

                booking_data.pop("_id", None)
                print(f"Thank you for returning {vehicle['model']}.")
                # Insert the cleaned booking data
                self.history_coll.insert_one(booking_data)
                review = input("Write your review: ")
                rating = int(input("Enter your rating (1-5): "))
                self.write_review(vehicle_id, review, rating)

            

        else:
            print(f"{vehicle['model']} has already been returned or is not in use.")

    def see_booking_history(self):
        """Displays the user's booking history."""
        bookings = self.history_coll.find({
        "customer_id": self.customer_id
        })

        # Convert to a list to view all documents
        bookings_list = list(bookings)
        print("Bookings for customer_id:", bookings_list)

        if not bookings:
            print("No booking history found.")
            return

        print("\n--- Booking History ---")
        for idx, vehicle in enumerate(bookings_list, start=1):
            driver_info = "With Driver" if vehicle["with_driver"] else "Without Driver"
            print(f"{idx}. {vehicle['vehicle_Id']}, {driver_info}")
