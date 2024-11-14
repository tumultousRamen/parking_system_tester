import pytest
from src.models.vehicle import Vehicle, VehicleType
from src.parking_station import ParkingStation

@pytest.fixture
def parking_station():
    """
    This function creates a parking station with 5 Mini spots and 3 Bus spots
    """

    return ParkingStation(mini_spots=5, bus_spots=3)

@pytest.fixture
def mini_vehicle():
    "This function creates a Mini vehicle with a test plate number"
    
    return Vehicle(VehicleType.MINI, "TEST-MINI-001")

@pytest.fixture
def bus_vehcile():
    """
    This function creates a Bus vehicle with a test plate number
    """

    return Vehicle(VehicleType.BUS, "TEST-BUS-001")

