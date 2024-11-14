from typing import List, Optional, Tuple
from .models.vehicle import Vehicle, VehicleType
from .models.parking_spot import ParkingSpot

class ParkingFullException(Exception):
    """Raised when attempting to park in a full parking station"""
    pass

class InvalidVehicleTypeException(Exception):
    """Raised when attempting to park an invalid vehicle type"""
    pass

class InvalidVehicleException(Exception):
    """Raised when an invalid vehicle object is provided"""
    pass

class ParkingStation:
    def __init__(self, mini_spots: int, bus_spots: int):
        if mini_spots < 0 or bus_spots < 0:
            raise ValueError("Number of parking spots cannot be negative")
            
        self.spots = (
            [ParkingSpot(f"MINI_{i}", VehicleType.MINI) for i in range(mini_spots)] +
            [ParkingSpot(f"BUS_{i}", VehicleType.BUS) for i in range(bus_spots)]
        )
        self._max_mini_spots = mini_spots
        self._max_bus_spots = bus_spots

    def park_vehicle(self, vehicle) -> str:
        """
        Attempts to park a vehicle in an available spot.
        Returns spot ID if successful, raises exception if no spots available.
        """

        if not isinstance(vehicle, Vehicle):
            raise InvalidVehicleException("Expected Vehicle instance")
            
        if not isinstance(vehicle.type, VehicleType):
            raise InvalidVehicleTypeException(f"Unsupported vehicle type: {vehicle.type}")

        for spot in self.spots:
            if not spot.is_occupied and spot.type == vehicle.type:
                spot.is_occupied = True
                spot.vehicle = vehicle
                return spot.id
                
        raise ParkingFullException(f"No available spots for {vehicle.type.value}")

    def remove_vehicle(self, spot_id: str) -> Optional[Vehicle]:
        """
        Removes vehicle from the given spot.
        Returns the removed vehicle or None if spot was empty/not found.
        """
        for spot in self.spots:
            if spot.id == spot_id:
                vehicle = spot.vehicle
                spot.is_occupied = False
                spot.vehicle = None
                return vehicle
        return None

    def get_available_spots(self, vehicle_type: VehicleType) -> List[str]:
        """Returns list of available spot IDs for given vehicle type"""
        return [
            spot.id for spot in self.spots
            if spot.type == vehicle_type and not spot.is_occupied
        ]

    def get_parking_status(self) -> Tuple[int, int, int, int]:
        """
        Returns current parking status as tuple:
        (available_mini_spots, total_mini_spots, available_bus_spots, total_bus_spots)
        """
        available_mini = len(self.get_available_spots(VehicleType.MINI))
        available_bus = len(self.get_available_spots(VehicleType.BUS))
        return (available_mini, self._max_mini_spots, available_bus, self._max_bus_spots)

    def is_full(self, vehicle_type: VehicleType) -> bool:
        """Returns True if no spots available for given vehicle type"""
        return len(self.get_available_spots(vehicle_type)) == 0