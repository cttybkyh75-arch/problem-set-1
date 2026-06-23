
    
class vehicle:
    fleet_size = 0

    def __init__(self, plate, make, model, year)->None:
        self.plate = plate
        self.make = make
        self.model = model
        self.year = year
        self.kilometres = 0
        
        vehicle.fleet_size += 1

    def drive(self, km: int) -> None:
        if km <= 0:
            raise ValueError("Distance must be greater than zero.")
        self.kilometres += km
        print(self.kilometres)

    def describe(self):
        print(f"{self.year} {self.make} {self.model} ({self.plate})")

    def service_due(self):
        if self.kilometres >= 15000:
            print(True)
        else:
            print(False)
            
v = vehicle("B-AB-1234", "Volkswagen", "Golf", 2022)


