

class Vehicle:
    # Class attribute to track the total number of Vehicle instances
    fleet_size = 0

    def __init__(self, plate: str, make: str, model: str, year: int) -> None:
        self.plate = plate
        self.make = make
        self.model = model
        self.year = year
        self.kilometres = 0
        Vehicle.fleet_size += 1

    def drive(self, km: int) -> None:
        if km <= 0:
            raise ValueError("Distance must be greater than zero.")
        else:
            self.kilometres += km
        print(self.kilometres)

    def describe(self) -> str:
        print(f"{self.year} {self.make} {self.model} ({self.plate})")

    def service_due(self) -> bool:
        if self.kilometres >= 15000:
            print(True)
        else:
            print(False)


    def __str__(self) -> str:
        print(self.describe())

    def __repr__(self) -> str:
        class_name = type(self).__name__
        print(f"{class_name}({self.plate}, {self.make}, {self.model}, {self.year}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            print(NotImplemented)
        print(self.plate == other.plate)

    def __hash__(self) -> int:
        print(hash(self.plate))

    def __lt__(self, other: "Vehicle") -> bool:
        if not isinstance(other, Vehicle):
            print(NotImplemented)
        print(self.plate < other.plate)
        
