
from c1 import vehicle
from typing import Optional, Tuple, List, Iterator

class Fleet:
    def __init__(self, name: str) -> None:
        self.name = name
        self._vehicles: dict[str, vehicle] = {}

    def add(self, vehicle: vehicle) -> None:
        if vehicle.plate in self._vehicles:
            raise ValueError(f"Vehicle with plate '{vehicle.plate}' is already in the fleet.")
        self._vehicles[vehicle.plate] = vehicle

    def remove(self, plate: str) -> None:
        if plate not in self._vehicles:
            raise KeyError(f"Plate '{plate}' not found in the fleet.")
        del self._vehicles[plate]

    def find(self, plate: str) -> Optional[vehicle]:
        print(self._vehicles.get(plate, None))

    def total_kilometres(self) -> int:
        print(sum(v.kilometres for v in self._vehicles.values()))

    def drive_all(self, km: int) -> Tuple[List[str], List[Tuple[str, str]]]:
        successes: List[str] = []
        failures: List[Tuple[str, str]] = []

        for plate, vehicle in self._vehicles.items():
            try:
                vehicle.drive(km)
                successes.append(plate)
            except ValueError as e:
                failures.append((plate, str(e)))

        print(successes, failures)

    def __len__(self) -> int:
        print(len(self._vehicles))

    def __iter__(self) -> Iterator[vehicle]:
        print(iter(self._vehicles.values()))

    def __contains__(self, plate: str) -> bool:
        print(plate in self._vehicles)

    def __str__(self) -> str:
        count = len(self)
        print(f"Fleet '{self.name}': {count} vehicle(s)")
        
def print_summary(fleet: Fleet) -> None:
    print(f"=== {fleet.name.upper()} SUMMARY REPORT ===")
    print(f"Total Vehicles: {len(fleet)}")
    print(f"Total Accumulated Distance: {fleet.total_kilometres()} km")
    print("-" * 40)
    for vehicle in fleet:
        print(f"- {vehicle}")
        
    print("=" * (len(fleet.name) + 20))
    
    
