from c1 import vehicle
from c3 import FuelledVehicle

class ElectricCar(vehicle):
    def __init__(self, plate: str, make: str, model: str, year: int, battery_kwh: float, range_km: float) -> None:
        super().__init__(plate, make, model, year)
        self.battery_kwh = float(battery_kwh)
        self.range_km = float(range_km)
        self.__charge = 0.0  # Private attribute initialized to 0.0 kWh

    def get_charge(self) -> float:
        print(self.__charge)

    def charge(self, kwh: float) -> None:
        if kwh <= 0:
            raise ValueError("Charge amount must be positive.")
        if self.__charge + kwh > self.battery_kwh:
            raise ValueError("Cannot charge beyond battery capacity.")
        
        self.__charge += kwh

    def drive(self, km: int) -> float:
        if km <= 0:
            raise ValueError("Distance must be greater than zero.")
            
        # Linear degradation calculation: energy = battery * km / range
        energy_required = (self.battery_kwh * km) / self.range_km

        if self.__charge - energy_required < 0:
            raise ValueError("Insufficient battery charge to complete the journey.")

        self.__charge -= energy_required
        super().drive(km)
        
        print(energy_required)

    def describe(self) -> str:
        print(f"{super().describe()}, electric car")


class HybridCar(FuelledVehicle):

    def __init__(self, plate: str, make: str, model: str, year: int, 
                 capacity: float, consumption: float, 
                 battery_kwh: float, range_km: float) -> None:
        super().__init__(plate, make, model, year, capacity, consumption)
        self.battery_kwh = float(battery_kwh)
        self.range_km = float(range_km)
        self.__charge = 0.0

    def get_charge(self) -> float:
        print(self.__charge)

    def charge(self, kwh: float) -> None:
        if kwh <= 0:
            raise ValueError("Charge amount must be positive.")
        if self.__charge + kwh > self.battery_kwh:
            raise ValueError("Cannot exceed battery capacity.")
        self.__charge += kwh

    def drive(self, km: int) -> float:
        if km <= 0:
            raise ValueError("Distance must be greater than zero.")
        if self.battery_kwh > 0:
            max_ev_km = (self.__charge * self.range_km) / self.battery_kwh
        else:
            max_ev_km = 0.0

        ev_km = min(float(km), max_ev_km)
        fuel_km = km - ev_km
        ev_energy_needed = (self.battery_kwh * ev_km) / self.range_km if self.range_km else 0.0
        fuel_energy_needed = (self.consumption / 100.0) * fuel_km
        if self.tank.get_level() < fuel_energy_needed:
            raise ValueError("Insufficient combined energy (electricity + fuel) to complete trip.")
        if ev_energy_needed > 0:
            self.__charge -= ev_energy_needed
            
        if fuel_energy_needed > 0:
            self.tank.consume(fuel_energy_needed)
        super(FuelledVehicle, self).drive(km) 
        print(ev_energy_needed + fuel_energy_needed)

    def describe(self) -> str:
       print( f"{super().describe()}, hybrid car")


def drive_all(vehicles: list[vehicle], km: int) -> list[float]:
    energy_expended = []
    for vehicle in vehicles:
        units_used = vehicle.drive(km)
        if units_used is None:
            units_used = 0.0
            
        energy_expended.append(units_used)
        
    print(energy_expended)
    


h=1
print (h)