from user import User
from pymongo import MongoClient
from db import get_db_connection

class Driver(User):
    def __init__(self, driver_id, name, phone, license_number):
        super().__init__(driver_id, name, phone)
        self.license_number = license_number
        self.client = get_db_connection() # MongoDB connection
        self.db = self.client["vehicle-db"]  # Use the "vehicle-db" database
        self.drivers_collection = self.db["drivers"]
        self.trips_collection = self.db["trips"]
        self.driver_data = self.drivers_collection.find_one({"driver_id": driver_id})  # Fetch existing driver data
        if not self.driver_data:
            # If the driver does not exist, insert a new driver document
            self.drivers_collection.insert_one(self.__dict__)
            self.driver_data = self.__dict__
        
    def view_trip(self):
        trip_data=self.trips_collection.find()
        trips=list(trip_data)
        for idx,trip in enumerate(trips,start=1):
            print(f"{idx}. Customer:{trip["customer_name"]}, Destination:{trip["destination"]}, Date:{trip["start_date"]}")

    def update_trip(self, destination,vehicle_id,customer_id,update,start_date):
        """
        Finds a specific trip based on vehicle_id, customer_id, and start_date.
        If the trip exists, appends the new update to the 'updates' array and saves it.
        """
        # Step 1: Find the existing trip
        trip_data = self.trips_collection.find_one({
            "vechile_Id": vehicle_id,
            "customer_id": customer_id,
            "start_date": start_date,
            "destination":destination
        })
       

        # Step 2: Check if the trip exists
        if trip_data:
            # Step 3: Append the new update to the 'updates' array
            ups = trip_data.get("updates", [])  # Get the 'updates' field (if exists)
            ups.append(update)  # Append the new update

            # Step 4: Update the document with the new 'updates' array
            result = self.trips_collection.update_one(
                {
                    "vechile_Id": vehicle_id,
                    "customer_id": customer_id,
                    "start_date": start_date,
                    "destination":destination
                },
                {
                    "$set": {
                        "updates": ups  # Set the updated 'updates' array
                    }
                }
            )

            # Feedback on the result of the update
            if result.matched_count > 0:
                print("\nTrip updates successfully added.")
            else:
                print("No trip found for the specified criteria.")
        else:
            print("Trip not found.")

       
        print("Updates Saved.......\n")
    
    def checkout(self):
        """
        Completes the ongoing trip and moves it to the completed trips.
        """
        print("\nCompleted Trip\n Checkinggg Out.......")
