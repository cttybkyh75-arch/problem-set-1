


class FuelTank:
    def __init__(self, capacity) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero.")
        
        self.__capacity = float(capacity)
        self.__level = 0.0

    def get_level(self):
        print(f"{round(self.__level, 2)}")

    def get_capacity(self):
        print( self.__capacity)

    def fill(self, litres: float) -> None:
        if litres <= 0:
            raise ValueError("Amount to fill must be greater than zero.")
        if self.__level + litres > self.__capacity:
            raise ValueError("Cannot fill beyond the tank's capacity.")
            
        self.__level += litres
        print(self.__level)

    def consume(self, litres: float) -> None:
        if litres <= 0:
            raise ValueError("Amount to consume must be greater than zero.")
        if self.__level - litres < 0:
            raise ValueError("Insufficient fuel in the tank.")
            
        self.__level -= litres
        print(self.__level)
        

    def fill_to_full(self):
        added_litres = self.__capacity - self.__level
        self.__level = self.__capacity
        print(added_litres)

    def percent_full(self):
        if self.__capacity == 0:
            return 0.0
        percentage = (self.__level / self.__capacity) * 100
        print(round(percentage, 1))
    

    
    
