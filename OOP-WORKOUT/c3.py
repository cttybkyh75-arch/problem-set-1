from c1 import vehicle
from c2 import FuelTank

class FuelledVehicle(vehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, capacity: float, consumption: float) -> None:
        super().__init__(plate, make, model, year)
        self.tank = FuelTank(capacity)
        self.consumption = float(consumption)

    def refuel(self, litres: float) -> None:
        self.tank.fill(litres)

    def drive(self, km: int) -> float:
        if km <= 0:
            raise ValueError("Distance must be greater than zero.")
        fuel_needed = (self.consumption / 100.0) * km
        self.tank.consume(fuel_needed)
        super().drive(km)
        
        print(fuel_needed)

    def range_remaining(self) -> float:
        current_fuel = self.tank.get_level()
        if self.consumption == 0:
            return 0.0
        return (current_fuel / self.consumption) * 100.0
    print(range_remaining)


class Car(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, seats: int = 5) -> None:
        super().__init__(plate, make, model, year, capacity=50.0, consumption=6.0)
        self.seats = seats

    def describe(self) -> str:
        base_desc = super().describe()
        print(f"{base_desc}, car, {self.seats} seats")


class Truck(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, payload_kg: float) -> None:
        super().__init__(plate, make, model, year, capacity=200.0, consumption=18.0)
        self.payload_kg = payload_kg

    def describe(self) -> str:
        base_desc = super().describe()
        print(f"{base_desc}, truck, {self.payload_kg} kg payload")


class Motorcycle(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int) -> None:
        super().__init__(plate, make, model, year, capacity=15.0, consumption=3.5)

    def describe(self) -> str:
        base_desc = super().describe()
        print(f"{base_desc}, motorcycle")


class Van(FuelledVehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, volume_m3: float) -> None:
        # Predefined capacity: 75.0, consumption: 9.0
        super().__init__(plate, make, model, year, capacity=75.0, consumption=9.0)
        self.volume_m3 = volume_m3

    def describe(self) -> str:
        base_desc = super().describe()
        print( f"{base_desc}, van, {self.volume_m3} m3 volume")
        

c = Car("B-CD-5678", "Toyota", "Yaris", 2023, seats=5)
c.describe()
tr = Truck("B-EF-9012", "MAN", "TGX", 2021, payload_kg=18000)
tr.describe()
m = Motorcycle("B-GH-3456", "Yamaha", "MT-07", 2024)
m.describe()
 