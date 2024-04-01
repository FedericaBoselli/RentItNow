# RentItNow
Python program for managing a car rental system. The system allows users to rent cars, manage their accounts, and provides administrative functionalities for the system administrator.

## Key Features

### Users Operations:
- **Car Rental**: Users can easily rent cars by specifying the type of car, number of passengers, and start/end location. A car has (at least)a type, a license plate, a brand,a name. Some cars are already given as test data and represent the cars present in the database. There are three types of car: ECO for max 2 persons, MID-CLASS for max 4 persons,DELUXE for max 7 persons.
When making a rental, the software selects the best car for the user choosing the closest car to the user (i.e: if the user selects as start circle the "Inner Circle", the software will first scan all the available cars, and then select for the user the car with location "Inner Circle", otherwise the car present in the closest circle to the Inner Circle). If no available cars are present, the software will give a warning.
Each time a rental is performed, the cars are added to the "rented_cars" list and a receipt in pdf format is generated storing date of rental, name, type, selected start circle annd end circle, distance and total cost of the rent. Each type of car has a rental price per km:ECO 1$/km, MID-CLASS 2$/km, DELUXE 5$/km and a fixed speed: ECO 15km/h, MID-CLASS 25km/h, DELUXE 50km/h. If the user selects a car that is currently on rent, the program gives a warning telling the user that the car is not available and the expected maximum waiting time. The expected maximum waiting time is calculated performing: maximum distance that can be travelled by a car (20 km, so 4 hops, from Inner to Outer Circle and viceversa) divided by the fixed speed of the selected type of car. The choice of using as distance the maximum distance is used to have some margin in the calculation of the waiting time, accounting for possible delays in the next availability of the car. 
  
- **Users account management options**: Users have the possibility to manage their accounts, update personal details, and delete their accounts if needed. In case they are updating their personal details or deleting their account, the program first checks that the user is already present in the database

--Users have (at least) name, surname, address, credit card, driving license--

### Administrative Operations: 
System administrators (referred to as "Boss") have access to administrative functionalities including:
- **Adding, updating, and removing cars from the system**. In case of cars updates or removals, the program first checks that the cars are present in the database
- **Checking the status of cars (currently on rental and not on rental), including location, distance traveled, next service time, and   availability**. The location will be showed as route "Start Circle - End Circle", the distance travelled will be set to the distance   selected for the rental performed by the user. The company must service its cars every 1500km, so the next service time will be calculated in terms of kilometers as: 1500 - total distance travelled. Moreover, the car status will be set to "Not in Service" and tthe car won't be available. 
- **Adding, updating, and removing user accounts**.

## Next possible steps
- Extend the rental system to support multi-day rentals
- Implement a reservation system that allows users to reserve cars in advance for specific dates and times
- Implement reporting functionalities to generate insights into rental trends
- Expand the variety of car types available for rental



