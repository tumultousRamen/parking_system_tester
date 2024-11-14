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

### GitHub Actions Workflow
The test.yaml configuration runs tets for every push to the projects main branch, and runs on every pull request as well. The workflow ensures immediate feedback on code changes. It uses the ubtuntu-latest for consistent environment, and Python v3.9 for reproducability. It also configures automated dependency installation. 

Additionally, the workflow uploads test results if test fails (if: always()) and preserves reports for debugging and analysis. It also maintains historical test data.

### PyTest Configuration

pytest.ini automatically discovers tests in the test directory, and automatically runs tests in parallel based on CPU cores which reduces test execution time signiicantly. It also helps catch race conditions in concurrent operations. 

The reports generated contain detailed execution output (--verbose) and its generates machine-readable test results (--junit-xml) for CI systems. It also generates human-readable (--html) HTML test reports. It covers code coverage tracking (--cov) and generates HTML (--cov-report) coverage report.  
