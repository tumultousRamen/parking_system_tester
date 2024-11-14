import pytest
from concurrent.futures import ThreadPoolExecutor
from src.models.vehicle import Vehicle, VehicleType
from src.parking_station import (
    ParkingStation,
    ParkingFullException,
    InvalidVehicleTypeException
)

class TestParkingStation:
    def test_park_mini(self, parking_station, mini_vehicle):
        """Test parking a Mini vehicle"""
        spot_id = parking_station.park_vehicle(mini_vehicle)
        assert spot_id is not None
        assert spot_id.startswith("MINI_")
        
        available_spots = parking_station.get_available_spots(VehicleType.MINI)
        assert len(available_spots) == 4  # One spot taken, 4 remaining

    def test_park_bus(self, parking_station, bus_vehicle):
        """Test parking a Bus vehicle"""
        spot_id = parking_station.park_vehicle(bus_vehicle)
        assert spot_id is not None
        assert spot_id.startswith("BUS_")
        
        available_spots = parking_station.get_available_spots(VehicleType.BUS)
        assert len(available_spots) == 2  # One spot taken, 2 remaining

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

    def test_full_parking_lot(self, parking_station):
        """Test behavior when parking lot is full"""
        # Fill all Mini spots
        mini_vehicles = [
            Vehicle(VehicleType.MINI, f"MINI_{i}") for i in range(5)
        ]
        for vehicle in mini_vehicles:
            spot_id = parking_station.park_vehicle(vehicle)
            assert spot_id is not None

        # Attempt to park one more Mini
        extra_mini = Vehicle(VehicleType.MINI, "MINI_EXTRA")
        with pytest.raises(ParkingFullException):
            parking_station.park_vehicle(extra_mini)

    def test_remove_vehicle(self, parking_station, mini_vehicle):
        """Test removing a vehicle from a spot"""
        spot_id = parking_station.park_vehicle(mini_vehicle)
        removed_vehicle = parking_station.remove_vehicle(spot_id)
        
        assert removed_vehicle == mini_vehicle
        assert len(parking_station.get_available_spots(VehicleType.MINI)) == 5

    def test_remove_vehicle_from_empty_spot(self, parking_station):
        """Test removing a vehicle from an empty spot"""
        removed_vehicle = parking_station.remove_vehicle("MINI_0")
        assert removed_vehicle is None

    def test_remove_vehicle_invalid_spot(self, parking_station):
        """Test removing a vehicle from an invalid spot"""
        removed_vehicle = parking_station.remove_vehicle("INVALID_SPOT")
        assert removed_vehicle is None

    def test_invalid_vehicle_type(self, parking_station):
        """Test parking a vehicle with invalid type"""
        class MockVehicle:
            type = "TRUCK"
            plate_number = "MOCK-001"

        with pytest.raises(InvalidVehicleTypeException):
            parking_station.park_vehicle(MockVehicle())

    def test_parking_status(self, parking_station, mini_vehicle, bus_vehicle):
        """Test parking status reporting"""
        initial_status = parking_station.get_parking_status()
        assert initial_status == (5, 5, 3, 3)  # All spots available

        parking_station.park_vehicle(mini_vehicle)
        parking_station.park_vehicle(bus_vehicle)
        
        new_status = parking_station.get_parking_status()
        assert new_status == (4, 5, 2, 3)  # One spot each taken

    def test_negative_spot_count(self):
        """Test creating parking station with negative spot count"""
        with pytest.raises(ValueError):
            ParkingStation(mini_spots=-1, bus_spots=3)

    @pytest.mark.parametrize("mini_count,bus_count", [
        (0, 3),  # No Mini spots
        (5, 0),  # No Bus spots
        (0, 0)   # No spots at all
    ])
    def test_zero_capacity(self, mini_count, bus_count):
        """Test parking station with zero capacity for some vehicle types"""
        station = ParkingStation(mini_spots=mini_count, bus_spots=bus_count)
        status = station.get_parking_status()
        assert status == (mini_count, mini_count, bus_count, bus_count)