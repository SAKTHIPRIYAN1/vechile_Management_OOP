from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # or MongoDB Atlas connection string
db = client["vehicle-db"]

# Create Customers Collection (explicitly)
# db.create_collection("customers")

# Insert Sample Data into Customers Collection
# customers_collection = db["customers"]
# customers_collection.insert_one({
#     "customer_id": "C001",
#     "name": "John Doe",
#     "phone": "1234567890",
#     "bookings": ["B001"],
#     "reviews": ["R001"]
# # })

# # Create Drivers Collection (explicitly)
# # db.create_collection("drivers")


# #  export PYTHONPATH=$PYTHONPATH:/home/sakthi/.local/lib/python3.10/site-packages












# # # Insert Sample Data into Drivers Collection
# # drivers_collection = db["drivers"]
# # drivers_collection.insert_one({
# #     "driver_id": "D001",
# #     "name": "James Smith",
# #     "phone": "9876543210",
# #     "license_number": "DL1234567",
# #     "vehicles": ["V001"]
# # })

# # Create Vehicles Collection (explicitly)
# # db.create_collection("vehicles")

# # Insert Sample Data into Vehicles Collection
# # vehicles_collection = db["vehicles"]
# # vehicles_collection.insert_one({
# #     "model": "Tesla Model S",
# #     "vehicle_Id":"V001",
# #     "vehicle_type": "Car",
# #     "rent_per_day": 150,
# #     "mileage": 100,
# #     "booked_dates": [],
# #     "reviews": ["R001"]
# # })

# # Create Bookings Collection (explicitly)
# # db.create_collection("bookings")

# # # Insert Sample Data into Bookings Collection
# bookings_collection = db["bookings"]
# bookings_collection.insert_one({
#     "customer_id": "C001",
#     "vehicle_model": "Tesla Model S",
#     "vehicle_Id":"V001",
#     "start_date": "2024-11-20",
#     "end_date": "2024-11-25",
#     "with_driver": True,
#     "status": "Confirmed"
# })

# # # Create Reviews Collection (explicitly)
# # db.create_collection("reviews")

# # # Insert Sample Data into Reviews Collection
# # reviews_collection = db["reviews"]
# # reviews_collection.insert_one({
# #     "vehicle_model": "Tesla Model S",
# #     "customer_id": "C001",
# #     "review_text": "Amazing experience!",
# #     "rating": 5
# # })

# print("Sample data inserted successfully!")


admins_collection = db['admins'] 
admin_data = {
        "admin_id": "A001",     # Unique admin identifier
        "name": "admin",             # Full name of the admin
        "email": "sakthi417@gmail.com",           # Admin's email address
        "password": "12345",  # Hashed password
      # Optional: Keep track of last login time
}
admins_collection.insert_one(admin_data)