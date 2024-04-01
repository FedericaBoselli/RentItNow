# Import packages
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Class car creation: A car has (at least) a type, a license plate, a brand, a name. The location is present as well to track the default location of the car
class Car: 
    def __init__(self, car_type, license_plate, brand, name, location):
        self.car_type = car_type
        self.license_plate = license_plate
        self.brand = brand
        self.name = name
        self.location = location
        self.total_distance_travelled = 0  # total distance travelled is by default equal to 0
        self.next_service_time = 1500  # next service time is by default programmed in 1500 km
        self.availability = True  # availability is by default set to true
        self.is_in_service = False # by default the status is set to "not in service"

    def __str__(self):
        return f"{self.name} ({self.car_type})"

    # define the maximum number of passengers for each type of car
    def get_max_passengers(self):  
        if self.car_type == "ECO":
            return 2
        elif self.car_type == "MID-CLASS":
            return 4
        elif self.car_type == "DELUXE":
            return 7
        else:
            return None

# Class User creation: User has (at least) name, surname, address, credit card, driving license
class User:
    def __init__(self, name, surname, address, credit_card, driving_license):
        self.name = name
        self.surname = surname
        self.address = address
        self.credit_card = credit_card
        self.driving_license = driving_license

# Class RentItNow creation to manage the rental process
class RentItNow:
    def __init__(self):
        # initialize empty lists to store cars and users in database and currently rented cars
        self.cars = [] 
        self.users = []
        self.rented_cars = []

    # method to generate a receipt after the rental and the payment details are confirmed
    # https://www.reportlab.com/docs/reportlab-userguide.pdf
    def generate_rental_receipt(self, username, car, start_circle, end_circle, distance, total_cost):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        filename = f"{username}_rental_receipt_{timestamp}.pdf"

        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        body_style = styles["BodyText"]

        title_text = f"Rental Receipt for {username}"
        title = Paragraph(title_text, title_style)
        elements.append(title)

        # information to show in the receipt
        data = [
            ("Date:", datetime.now().strftime("%Y-%m-%d %H:%M")),
            ("Car:", car.name),
            ("Car Type:", car.car_type),
            ("Start Circle:", start_circle),
            ("End Circle:", end_circle),
            ("Distance Travelled (km):", str(distance)),
            ("Total Cost ($):", str(total_cost)),
        ]

        for item in data:
            item_text = f"<b>{item[0]}</b> {item[1]}"
            item_paragraph = Paragraph(item_text, body_style)
            elements.append(item_paragraph)

        elements.append(Spacer(1, 12))

        doc.build(elements)

        print(f"Rental receipt coorectly generated and saved as: {filename}")

        return filename

    # method to let the user/Boss to login in the program. There is also the possibility to register a new account 
    def login_or_register(self):
        while True:
            choice = input("Do you want to login or register an account? (login/register/exit): ").lower()
            if choice == "login":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                # Case in which the boss is logging in into the program
                if username == "Boss" and password == "admin":
                    return "boss"
                elif username != "Boss" and password != "admin":  
                    return username
                else:
                    print("Invalid username or password. Enter the correct username and password")
            # in case of choice equal to "register" the user can enter all the required personal details
            elif choice == "register":
                name = input("Enter your name: ")
                surname = input("Enter your surname: ")
                address = input("Enter your address: ")
                credit_card = input("Enter your credit card number: ")
                driving_license = input("Enter your driving license number: ")
                user = User(name, surname, address, credit_card, driving_license)
                # the user is now added to the list of users in database previously initialized 
                self.users.append(user)
                print("Account registered successfully")
                return "user"
            elif choice == "exit":
                return None  
            else:
                # if the user inserts a value different from "login, register or exit" the program gives a 
                # warning and lets the user insert again the value
                print("Invalid choice, enter login, register, or exit.") 

    # After the login as a user, the user can choose among 3 different actions:
    # start a rental process and rent a car, manage the account (update or delete it) or exit the program
    def manage_account(self, username):
        print("Account management options:")
        print("1. Proceed with rental")
        print("2. Manage account")
        print("3. Exit")
        while True:
            option = input("Enter your choice or select 'back' to go back to the login menu: ")
            if option == "1":
                self.process_rental(username)
            elif option == "2":
                self.manage_user_account(username)
            elif option == "3":
                print("Exiting the program")
                return  
            elif option.lower() == "back":  
                return None  
            else:
                # if the user inserts a value different from 1,2,3 or "back"
                # it gives a warning and lets the user choose the corect value
                print("Invalid choice. Please enter 1, 2, 3, or 'back' to go back to the menu.") 

    # if the user chooses to manage his/her account, it has the possibility to update, delete it (or exit the program)
    def manage_user_account(self, username):
        print("User account management options:")
        print("1. Update account")
        print("2. Delete account")
        print("3. Exit")
        option = input("Select 'back' to go back in the login menu: ")
        if option == "1":
            self.update_user_account(username)
        elif option == "2":
            self.delete_user_account(username)
        elif option == "3":
            print("Exiting the program")
            return  
        elif option.lower() == "exit":  
            return None  
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 'exit'")

    # if the user decides to update his/her account it is then possible to update the account details
    def update_user_account(self, username):
        print("Update your account details:")
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        address = input("Enter your address: ")
        credit_card = input("Enter your credit card number: ")
        driving_license = input("Enter your driving license number: ")
        user = self.find_user(username)
        if user:
            user.name = name
            user.surname = surname
            user.address = address
            user.credit_card = credit_card
            user.driving_license = driving_license
            print("Account details updated successfully")
        else:
            print("User not found. Please enter an existing user")

    # the user can also delete his/her account if the user is present in the database
    def delete_user_account(self, username):
        confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
        if confirm == "yes":
            user = self.find_user(username)
            if user:
                self.users.remove(user)
                print("Account deleted successfully")
            else:
                print("User not found. Please insert an existing user")
        elif confirm == "no":
            print("Account deletion cancelled")
        elif confirm.lower() == "exit":  
            return None  
        else:
            print("Invalid choice.")

    # method to check if the user is present in the database based on his/her name
    def find_user(self, username):
        for user in self.users:
            if user.name == username:
                return user
        return None

    # method to manage the rental process
    def process_rental(self, username):
        # car type and number of passangers have to be coherent with the selected car
        car_type, num_passengers = self.car_selection() 
        while True:
            # input the start circle
            start_circle = input("Enter starting circle (Inner Circle, Middle Circle, Outer Circle): ").title()
            # check if the start circle is correctly inserted 
            if start_circle in ["Inner Circle", "Middle Circle", "Outer Circle"]:
                break
            else:
                # if the input is not among the accepted values the program give a warning and lets the user choose the correct value
                print("Invalid input. Please enter Inner Circle, Middle Circle, or Outer Circle")

        selected_car = self.select_best_car(car_type, num_passengers, start_circle)  
        if selected_car:
            # Check if the car is available
            if selected_car.availability:  
                while True:
                    # input the end circle
                    end_circle = input("Enter ending circle (Inner Circle, Middle Circle, Outer Circle): ").title()
                    # check if the end circle is correctly inserted 
                    if end_circle in ["Inner Circle", "Middle Circle", "Outer Circle"]:
                        break
                    else:
                        # if the input is not among the accepted values the program give a warning and lets the user choose the correct value
                        print("Invalid input. Please enter Inner Circle, Middle Circle, or Outer Circle")

                # distance is calculated from the start to the end circle
                distance = self.calculate_distance(start_circle, end_circle)
                # retrieve the trip cost
                trip_cost = self.calculate_trip_cost(selected_car.car_type, distance)
                if trip_cost:
                    # process the payment 
                    self.make_payment(username, trip_cost)  
                    print(f"Trip completed with {selected_car} from {start_circle} to {end_circle}.")
                    receipt_filename = self.generate_rental_receipt(username, selected_car, start_circle, end_circle, distance, trip_cost)
                    print(f"Rental receipt coorectly saved as: {receipt_filename}")
                    # new location of the car will be equal to the end circle
                    selected_car.location = end_circle  
                    # new distance of the car will be the original total distance + the one selected for the rental
                    selected_car.total_distance_travelled += distance  

                    # Update the next service time in terms of kilometers. It is given by the default service distance (1500 km) - the  one selected for the rental
                    selected_car.next_service_time = 1500 - selected_car.total_distance_travelled

                    if selected_car.total_distance_travelled >= 1500:  
                        selected_car.is_in_service = True
                        selected_car.total_distance_travelled = 0  
                        print(f"Car {selected_car.name} ({selected_car.car_type}) requires service!")
                    # Consequently, the availability of the car will be set to False
                    selected_car.availability = False  
                    # the car is added to the rented_cars list previously initialized 
                    self.rented_cars.append((selected_car, start_circle, end_circle))  # Memorizza anche la tratta
                else:
                    print("Failed to calculate trip cost")
            else:
                print("The selected car is not available for rental. Please, select another car")
        else:
            print("No available car found")

    # The software select the best car for the user based on the following metric:
    # it selects the closest car to the start circle selected by the user (so the user will always get the closest car to him/her)
    # if the closest car is not available it selects another car (keeping the same specifications: car type, number of passengers, start and end circles)
    def select_best_car(self, car_type, num_passengers, start_circle):
        # checks the available cars
        available_cars = [car for car in self.cars if car.car_type == car_type and car.availability]
        # check the correct number of passengers
        suitable_cars = [car for car in available_cars if car.get_max_passengers() >= num_passengers]
        if suitable_cars:
            # if a car is available the program calculates the distance from the current location of the car and the start circle selected by the user
            distances = {car: self.calculate_distance(car.location, start_circle) for car in suitable_cars}
            # order the cars based on the closest distance to the start circle
            sorted_cars = sorted(distances.keys(), key=lambda car: distances[car])
            # return the first closest car
            return sorted_cars[0]  
        else:
            # Calculate waiting time
            # Maximum distance for a car: going from Inner to Outer Circle and viceversa (4 hops = 5*4 = 20 km). 
            max_distance = 20 
            # Fixed Speed of each type of car
            car_speeds = {"ECO": 15, "MID-CLASS": 25, "DELUXE": 50} 
            if car_type in car_speeds:
                # calculate the maximum waiting time based on the distance and the car's speed 
                waiting_time = max_distance / car_speeds[car_type]
                print(f"Sorry, the requested {car_type} car is not available. The maximum waiting time is approximately {waiting_time:.2f} hours")
            else:
                print("No suitable car is available")
            return None

    # method to process the payment
    def make_payment(self, username, total_cost):
        print(f"Payment of ${total_cost} processed for user {username}")

    # method to let the Boss check the currently rented cars status 
    def check_rented_car_status(self): 
        print("Checking currently rented car status:")
        # the Boss has to input the license plate of the car to see its status
        license_plate = input("Enter license plate of the rented car: ")
        for car in self.rented_cars:
            # the car has to be present in the rented cars list
            if car.license_plate == license_plate:
                print(f"Rented car {car.name} ({car.car_type}) status:")
                print(f"Location: {car.location}")
                print(f"Total distance traveled: {car.total_distance_travelled} km")
                print(f"Next service time: {car.next_service_time} km")
                print(f"Service status: {'In Service' if car.is_in_service else 'Not in Service'}")
                break
        else:
            print("Rented car not found. Please, enter an existing license plate")

    # method to check the correct insertion of car types
    def car_selection(self):
        valid_car_types = {"ECO", "MID-CLASS", "DELUXE"}
        while True:
            car_type = input("Enter car type (ECO, MID-CLASS, DELUXE): ").upper()
            if car_type in valid_car_types:
                break
            elif car_type.lower() == "exit":  
                return None, None  
            else:
                print("Invalid car type. Please enter ECO, MID-CLASS, or DELUXE")

        # check the correct insertion of number of passengers
        while True:
            num_passengers = input("Enter number of passengers: ")
            if num_passengers.isdigit():
                num_passengers = int(num_passengers)
                if car_type == "ECO" and num_passengers > 2:
                    print("Maximum number of passengers for ECO car is 2.")
                elif car_type == "MID-CLASS" and num_passengers > 4:
                    print("Maximum number of passengers for MID-CLASS car is 4.")
                elif car_type == "DELUXE" and num_passengers > 7:
                    print("Maximum number of passengers for DELUXE car is 7.")
                else:
                    break
            elif num_passengers.lower() == "exit":  
                return None, None  
            else:
                print("Invalid input. Please enter a number or 'exit'")

        return car_type, num_passengers

    # calculate the final trip costs 
    def calculate_trip_cost(self, car_type, distance):
        rental_price_per_km = self.get_rental_price_per_km(car_type)
        if rental_price_per_km is not None:
            return distance * rental_price_per_km
        else:
            return None

    # each type of car has its rental price per km
    def get_rental_price_per_km(self, car_type):
        if car_type == "ECO":
            return 1
        elif car_type == "MID-CLASS":
            return 2
        elif car_type == "DELUXE":
            return 5
        else:
            return None

    # The distance is calculated based on hops: an hop is 5km; an hops is going from one circle to the next one.
    # (e.g. travelling from Inner Circle to Middle Circle is 2 hops, not 1 hop). Travelling in the same circle is 1 hop.
    def calculate_distance(self, start_circle, end_circle):
        circle_positions = {"Inner Circle": 1, "Middle Circle": 2, "Outer Circle": 3}
        start_position = circle_positions.get(start_circle)
        end_position = circle_positions.get(end_circle)
        if start_position is not None and end_position is not None:
            if start_position == end_position:
                distance = 5  # same circle
            else:
                distance = abs(end_position - start_position) * 10  # Different circles
            return distance
        else:
            return None

    def main(self):
        # Test data - Add some cars
        self.cars.append(Car("ECO", "ABC123", "Toyota", "Yaris", "Inner Circle"))
        self.cars.append(Car("MID-CLASS", "XYZ456", "Honda", "Accord", "Middle Circle"))
        self.cars.append(Car("DELUXE", "DEF789", "Mercedes", "S-Class", "Outer Circle"))
        self.cars.append(Car("ECO", "ABC1234", "Toyota", "Yaris_2", "Outer Circle"))
        self.cars.append(Car("MID-CLASS", "ABC1234", "Honda", "Accord_2", "Outer Circle"))

        # Test data - Add some users
        self.users.append(User("Federica", "Ferrari", "Via A", "ABC", "DEF"))
        self.users.append(User("Giulia", "Bianchi", "Via B", "GHI", "LMN"))
        self.users.append(User("Martina", "Rossi", "Via C", "OPQ", "RST"))

        # users have their actions, and Boss has its own functions
        while True:
            user_type = self.login_or_register()

            if user_type == "boss":
                self.boss_operations()
            elif user_type:
                username = user_type
                print(f"\nWelcome in the RentItNow service, {username}!")
                self.manage_account(username)
            else:
                print("Exiting the program")
                break

    # set the Boss' operations. he boss needs to: Add, update and remove cars; Check the status of the car: location, total distance traveled, 
    # next service time, availability. Add, update and remove users;
    def boss_operations(self):
        print("Boss operations:")
        while True:
            print("\nSelect an operation:")
            print("1. Add car")
            print("2. Update car")
            print("3. Remove car")
            print("4. Check car status")
            print("5. Add user")
            print("6. Update user")
            print("7. Remove user")
            print("8. Check rented car status")  
            print("9. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_car()
            elif choice == "2":
                self.update_car()
            elif choice == "3":
                self.remove_car()
            elif choice == "4":
                self.check_car_status()
            elif choice == "5":
                self.add_user()
            elif choice == "6":
                self.update_user()
            elif choice == "7":
                self.remove_user()
            elif choice == "8":
                self.check_rented_car_status()
            elif choice == "9":
                print("Exiting the program")
                return  
            else:
                print("Invalid choice. Please enter a number from 1 to 9")

    # define in more details all the functions of the Boss
    def add_car(self):
        print("Adding a new car:")
        car_type, license_plate, brand, name, location = self.get_car_details_from_user()
        new_car = Car(car_type, license_plate, brand, name, location)
        self.cars.append(new_car)
        print("Car added successfully.")

    def get_car_details_from_user(self):
        car_type = input("Enter car type (ECO, MID-CLASS, DELUXE): ").upper()
        license_plate = input("Enter license plate: ").upper()
        brand = input("Enter brand: ")
        name = input("Enter name: ")
        location = input("Enter location (Inner Circle, Middle Circle, Outer Circle): ").title()
        return car_type, license_plate, brand, name, location

    def update_car(self):
        print("Updating car details:")
        license_plate = input("Enter license plate of the car to update: ").upper()
        # car has to be present in the database
        car = self.find_car_by_license_plate(license_plate)
        if car:
            car_type, _, brand, name, location = self.get_car_details_from_user()
            car.car_type = car_type
            car.brand = brand
            car.name = name
            car.location = location
            print("Car details updated successfully!")
        else:
            print("Car not found. Please enter an existing license plate")

    def find_car_by_license_plate(self, license_plate):
        for car in self.cars:
            if car.license_plate == license_plate:
                return car
        return None

    def remove_car(self):
        print("Removing a car:")
        license_plate = input("Enter license plate of the car to remove: ").upper()
        # car has to be present in the database
        car = self.find_car_by_license_plate(license_plate)
        if car:
            self.cars.remove(car)
            print("Car removed successfully!")
        else:
            print("Car not found. Please enter an existing license plate")

    def check_rented_car_status(self): 
        print("Checking rented car status:")
        license_plate = input("Enter license plate of the rented car: ")
        for car, start_circle, end_circle in self.rented_cars:  
            # when checking the rented car status the location is shown as "start circle - end circle"
            if car.license_plate == license_plate:
                print(f"Rented car {car.name} ({car.car_type}) status:")
                if start_circle in ["Inner Circle", "Middle Circle", "Outer Circle"]:
                    print(f"Start Circle: {start_circle}")  
                else:
                    print(f"Start Circle: {start_circle}") 
                if end_circle in ["Inner Circle", "Middle Circle", "Outer Circle"]:
                    print(f"End Circle: {end_circle}") 
                else:
                    print(f"End Circle: {end_circle}") 
                # then show total distance travelled, next service time (1500 km - total distance travelled) and service status
                print(f"Total distance traveled: {car.total_distance_travelled} km")
                print(f"Next service time: {car.next_service_time} km")
                print(f"Service status: {'In Service' if car.is_in_service else 'Not in Service'}")
                break
        else:
            print("Rented car not found. Please enter an existing license plate in rental")

    def add_user(self):
        print("Adding a new user:")
        name = input("Enter name: ")
        surname = input("Enter surname: ")
        address = input("Enter address: ")
        credit_card = input("Enter credit card number: ")
        driving_license = input("Enter driving license number: ")
        new_user = User(name, surname, address, credit_card, driving_license)
        self.users.append(new_user)
        print("User added successfully!")

    def update_user(self):
        print("Updating user details:")
        name = input("Enter name of the user to update: ")
        # user has to be present in the database
        user = self.find_user(name)
        if user:
            surname = input("Enter surname: ")
            address = input("Enter address: ")
            credit_card = input("Enter credit card number: ")
            driving_license = input("Enter driving license number: ")
            user.surname = surname
            user.address = address
            user.credit_card = credit_card
            user.driving_license = driving_license
            print("User details updated successfully!")
        else:
            print("User not found. Enter an existing user")

    def remove_user(self):
        print("Removing a user:")
        name = input("Enter name of the user to remove: ")
        # user has to be present in the database
        user = self.find_user(name)
        if user:
            self.users.remove(user)
            print("User removed successfully.")
        else:
            print("User not found. Enter an existing user")

rental_system = RentItNow()
rental_system.main()
