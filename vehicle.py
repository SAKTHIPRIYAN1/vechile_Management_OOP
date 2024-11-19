class Vehicle:
    def __init__(self, model, vehicle_type, rent_per_day, mileage):
        self.model = model
        self.vehicle_type = vehicle_type
        self.rent_per_day = rent_per_day
        self.available = True
        self.mileage = mileage  # Added mileage attribute
        self.reviews = []

    def is_available_between(self, start_date, end_date):
        """Checks availability of the vehicle (stubbed for simplicity)."""
        # Example logic could check bookings against this date range.
        return self.available

    def add_review(self, review):
        """Add a review for the vehicle."""
        self.reviews.append(review)
        print(f"Review added for {self.model}: {review}")
    
    def update_availability(self, availability):
        """Update the availability of the vehicle."""
        self.available = availability
        print(f"{self.model} availability updated to {self.available}")

    def get_details(self):
        """Return the details of the vehicle."""
        return f"{self.vehicle_type} {self.model} - Rent: {self.rent_per_day}/day, Mileage: {self.mileage} km/l"

class Car(Vehicle):
    def __init__(self, model, rent_per_day, mileage):
        super().__init__(model, "Car", rent_per_day, mileage)

class Bike(Vehicle):
    def __init__(self, model, rent_per_day, mileage):
        super().__init__(model, "Bike", rent_per_day, mileage)

class Bus(Vehicle):
    def __init__(self, model, rent_per_day, mileage, seating_capacity):
        super().__init__(model, "Bus", rent_per_day, mileage)
        self.seating_capacity = seating_capacity  # Added seating capacity for buses

    def get_details(self):
        """Return the details of the bus, including seating capacity."""
        return f"Bus {self.model} - Rent: {self.rent_per_day}/day, Mileage: {self.mileage} km/l, Seating Capacity: {self.seating_capacity}"
