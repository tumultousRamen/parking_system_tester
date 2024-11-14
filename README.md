# Parking System Tester

## Framework: PyTest
The project uses PyTest framework because of its:
1. Excellent support for test fixtures and dependency injection 
2. Built-in support for parameterization and parallel execution 
3. Strong mocking capabilities with pytest-mock
4. Seamless integration with CI/CD platforms
5. Excellent readability and maintainability

Particularly, PyTest addresses our need to integrate the automation testing suite seamlessly into CI/CD pipelines. 

## Key Components
### Models
Contains the projects two key domain models, Vehicle and Parking Station. 
1. Vehicle 
VehicleType supports types mini and bus. 

A Vehicle object can be initalized by passing the vehicle type (see above) and license plate number. 

2. Parking Spot
A parking spot object can be initialized by passing the spot type and id. By default, we assume that the spot is unoccupied (and therefore has no vehicles as well.)

### Parking Station 
Parking station defines the critical business logic. 

A parking station object has a list mini and bus spots.

Function _park_vehicle_ attempts to park a particular vehicle of type of MINI or BUS in an appropriate spot if available. 
