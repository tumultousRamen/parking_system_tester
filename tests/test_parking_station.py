import pytest
from src.models.vehicle import VehicleType,Vehicle
from src.parking_station import ParkingStation
from concurrent.futures import ThreadPoolExecutor

class TestParkingStation:
    def test_park_mini(self, parking_station, mini_vehicle):
        """
        Test parking a Mini Vehicle
        """

        spot_id = parking_station.park_vehicle(mini_vehicle)
        assert spot_id is not None 
        assert spot_id.startswith("MINI_")

        available_spots = parking_station.get_available_spots(VehicleType.MINI)
        assert len(available_spots) == 4 

    def test_park_bus(self, parking_station, bus_vehicle):
        """
        This function tests parking a bus
        """

        spot_id = parking_station.park_vehicle(bus_vehicle)
        assert spot_id is not None
        assert spot_id.startsWith("BUS_")

        available_spots = parking_station.get_available_spots(VehicleType.BUS)
        assert len(available_spots) == 2

    def test_simultaneous_parking(self, parking_station, mini_vehicle, bus_vehicle):
        """Test parking Mini and Bus vehicles simultaneously"""
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_mini = executor.submit(parking_station.park_vehicle, mini_vehicle)
            future_bus = executor.submit(parking_station.park_vehicle, bus_vehicle)
            
            spot_mini = future_mini.result()
            spot_bus = future_bus.result()
            
            assert spot_mini is not None
            assert spot_bus is not None
            assert spot_mini.startswith("MINI_")
            assert spot_bus.startswith("BUS_")

    @pytest.mark.parametrize("vehicle_type,expected_count", [
        (VehicleType.MINI, 5),
        (VehicleType.BUS, 3)
    ])
    def test_initial_available_spots(self, parking_station, vehicle_type, expected_count):
        """Test initial number of available spots for each vehicle type"""
        available_spots = parking_station.get_available_spots(vehicle_type)
        assert len(available_spots) == expected_count