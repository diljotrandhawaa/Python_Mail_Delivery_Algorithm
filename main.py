
import csv
import datetime
import re

from Models.Truck import Truck
from Models.DeliveryPackage import Package
from Models.Packages_Hashtable import PackagesHashtable


# To load package file info into a hash table
def load_package_data(filename, packages_hash_table):
    with open(filename) as package_csv:
        reader = csv.DictReader(package_csv, ['package_id', 'address', 'city', 'state', 'zip', 'deadline', 'weight', 'special_notes'])
        next(reader)  # skipped two rows because of extra space of headers
        next(reader)

        # loading each row of packages into our hash table
        for package_row in reader:
            delivery_package = Package(package_row['package_id'], package_row['address'], package_row['city'], package_row['state'], package_row['zip'], package_row['deadline'], package_row['weight'], "At the hub", None, None)

            # with Package ID as key in hashtable and all other info in Package class as the value mapped by key
            packages_hash_table.insert(package_row['package_id'], delivery_package)
            packages_list.append(package_row['package_id'])

        return True


modified_distance_data = []
with open('CSV/distance_csv.csv') as distance_csv:
    reader = csv.reader(distance_csv)
    next(reader)
    reader = list(reader)
    for distance_row in reader:
        modified_address1 = distance_row[1].split('\n')
        distance_row[1] = modified_address1[0].strip()
        modified_distance_data.append(distance_row)


def calculate_distance(address1, address2):
    address1 = address1.strip()
    address2 = address2.strip()
    if address1 == 'HUB':
        index1 = 0
    else:
        for i in range(len(modified_distance_data)):
            if address1 == modified_distance_data[i][1]:
                index1 = i

    for j in range(len(modified_distance_data)):
        if address2 == modified_distance_data[j][1]:
            index2 = j
            break

    if modified_distance_data[index2][index1 + 2] == '':
        return modified_distance_data[index1][index2 + 2]
    return modified_distance_data[index2][index1 + 2]

# datetime.timedelta(hours=9, minutes=5))
# truck3 = Truck(16, 18, [], datetime.timedelta())
#
#

# Function to find minimum from starting address's package id to all remaining packages yet to be delivered
# uses packages hashtable to find the distance of each package address from the starting address using package_id's
def get_min_distance(packages_data, starting_id, packages_id_list):

    if starting_id == '0' or starting_id == 0:
        # address of our hub
        starting_address = 'HUB'
    else:
        # finds the address in packages hashtable using package_id
        starting_address = packages_data.look(starting_id).address

    min_distance_id = packages_id_list[0]
    min_distance_address = packages_data.look(min_distance_id).address
    min_distance = calculate_distance(starting_address, min_distance_address)

    for package_id in packages_id_list:
        pk_address = packages_data.look(package_id).address
        pk_distance = calculate_distance(starting_address, pk_address)
        if float(pk_distance) < float(min_distance):
            min_distance = pk_distance
            min_distance_id = package_id

    packages_id_list.remove(min_distance_id)
    return [min_distance_id, min_distance]


def packages_delivery(truck):
    packages_delivery_list = []
    starting_id = '0'

    for package_id in truck.packages:
        Packages_data.look(package_id).truck_id = truck.id
        Packages_data.look(package_id).status = 'en route by Truck-', truck.id

    while len(truck.packages) > 0:
        min_dist = get_min_distance(Packages_data, starting_id, truck.packages)

        # changes address of package 9 after 10:20 AM
        if min_dist[0] == '9':
            if truck.time > datetime.timedelta(hours=10, minutes=20):
                Packages_data.look('9').address = '410 S State St'
                Packages_data.look('9').pk_zip = '84111'
                truck.packages.append('9')
                min_dist = get_min_distance(Packages_data, starting_id, truck.packages)
            else:
                continue

        # adds the pair of package_id and it's distance from the last address
        packages_delivery_list.append(min_dist)

        # updates the miles travelled by truck
        miles_travelled = float(min_dist[1])
        truck.miles_travelled += round(miles_travelled, 1)

        # gets the current package being delivered
        delivered_package = Packages_data.look(min_dist[0])

        # changes package's status from 'At the hub' to 'Delivered'
        delivered_package.status = 'Delivered by Truck-' + delivered_package.truck_id

        # calculates current time and put it into package's delivery time
        total_minutes = (truck.miles_travelled / truck.speed) * 60
        total_minutes = round(total_minutes, 1)
        current_time = truck.depart_time + datetime.timedelta(minutes=total_minutes)
        delivered_package.delivery_time = current_time

        # update the truck's real time as well
        truck.time = current_time

        starting_id = min_dist[0]

    last_address = Packages_data.look(packages_delivery_list[len(packages_delivery_list) - 1][0]).address
    truck.miles_travelled += float(calculate_distance('HUB', last_address))
    truck.miles_travelled = round(truck.miles_travelled, 1)
    return packages_delivery_list


Packages_data = PackagesHashtable()
packages_list = []
load_package_data('CSV/package_csv.csv', Packages_data)

truck1 = Truck('1', 16, 18, ['7', '29', '2', '33', '1', '4', '40', '12'], datetime.timedelta(hours=8), 0, datetime.timedelta(hours=8))
truck2 = Truck('2', 16, 18, ['3', '5', '6', '8', '9', '18', '22', '24', '25', '26', '28', '31', '32', '35', '36', '38'], datetime.timedelta(hours=9, minutes=15), 0, datetime.timedelta(hours=9, minutes=15))
truck3 = Truck('3', 16, 18, ['10', '11', '13', '14', '15', '16', '17', '19', '20', '21', '23', '27', '30', '34', '37', '39'], datetime.timedelta(hours=8), 0, datetime.timedelta(hours=8))

packages_delivery(truck1)
packages_delivery(truck2)
packages_delivery(truck3)
total_mileage = truck1.miles_travelled + truck2.miles_travelled + truck3.miles_travelled


# ----------------------- UI functions and class -----------------------

# The function below checks if the string passed by user in option 4 of UI menu is valid
# to do that, it splits the string into an array and check if each id is a valid digit between 1 and 40
def is_valid_packages_format(user_packages_string):
    user_packages_list = user_packages_string.split(',')

    for package_id in user_packages_list:
        if not package_id.strip().isdigit():
            return False
        else:
            if int(package_id) < 1 or int(package_id) > len(packages_list):
                return False
    return True


# The function below checks if the time entered by user is valid
# it does that by comparing it to regex string and if hours, mins and secs are under 60
def is_valid_time_format(user_time):
    # Define the regex pattern for the time format
    pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')

    # Check if the input string matches the pattern
    if pattern.match(user_time):
        user_time_divided = user_time.split(':')
        user_hours = int(user_time_divided[0])
        user_minutes = int(user_time_divided[1])
        user_seconds = int(user_time_divided[2])
        if 0 <= user_hours <= 24:
            if 0 <= user_minutes <= 59:
                if 0 <= user_seconds <= 59:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


# converts the time in format 'HH:MM:SS' to a dateTime object
def convert_time_to_delta(user_time):
    user_time_divided = user_time.split(':')
    user_hours = int(user_time_divided[0])
    user_minutes = int(user_time_divided[1])
    user_seconds = int(user_time_divided[2])
    return datetime.timedelta(hours=user_hours, minutes=user_minutes, seconds=user_seconds)

# given package, this function returns the truck object the package is loaded in
def find_truck_for_package(package):
    package_truck = ''
    if package.truck_id == '1':
        package_truck = truck1
    elif package.truck_id == '2':
        package_truck = truck2
    else:
        package_truck = truck3

    return package_truck


# given current time and a list of packages, the function first prints the list of packages with
# their status updated at current time
# and also returns the hashtable of those packages mapped by their package id's
def get_packages_at_this_time(time_given, packages_to_view):
    packages = {}
    for package_id in packages_to_view:
        package = Packages_data.look(package_id)
        if package is None:
            print('\nNo package found with ID: ' + package_id)
            return
        package_truck = find_truck_for_package(package)

        packages[package_id] = package
        if time_given > package_truck.depart_time:
            if time_given >= package.delivery_time:
                packages[package_id].status = 'Delivered by Truck-' + package.truck_id
            else:
                packages[package_id].status = 'En route on Truck-' + package.truck_id
                packages[package_id].delivery_time = 'Not yet delivered'
        else:
            packages[package_id].status = 'At the hub'
            packages[package_id].delivery_time = 'Not yet delivered'

    print("\n")
    for package_id in packages:
        print(packages[package_id])
    return packages


# the class Main is for UI, takes user input and prints the data requested by user
class Main:
    print('Western Governors University C950')
    print('Student ID: Diljot Singh')
    print('The mileage travelled by trucks is: ')
    print(round(truck1.miles_travelled + truck2.miles_travelled + truck3.miles_travelled, 1), " miles")

    time_to_give = datetime.timedelta(hours=9, minutes=25)
    packages_to_view = ['1', '5', '15', '20', '34', '31']

    userInput1 = input("To start the program, please type the word 'Start'\n",)
    if userInput1 == 'start' or userInput1 == 'Start':
        try:
            print("Here are your options:")
            print("1. Print All Package Status and Total Mileage after Delivery")
            print("2. Print All Package Status and Total Mileage at particular Time")
            print("3. Get a Single Package Status at particular Time")
            print("4.Get specific Packages Status at particular Time (more than one Package)")
            print("5. Exit the Program\n")

            userInput2 = input("type in your option number like  '1' or '2'  and so on..\n")
            if userInput2 == '1':
                for key in packages_list:
                    print(Packages_data.look(key))

                print("\nThe Total mileage of all 3 trucks is: ", round(total_mileage, 1), " miles")

            elif userInput2 == '2':
                try:
                    userTimeInput = input("Enter Time in HH:MM:SS format(24-hours): ")
                    if not is_valid_time_format(userTimeInput):
                        raise ValueError

                    userTimeObj = convert_time_to_delta(userTimeInput)
                    get_packages_at_this_time(userTimeObj, packages_list)
                    print("\nThe Total mileage of all 3 trucks is: ", round(total_mileage, 1), " miles")
                except ValueError:
                    print("\nEntry invalid, exiting Program")
                    exit()

            elif userInput2 == '3':
                try:
                    userPackageInput = input("Enter Package ID: ")
                    if int(userPackageInput) < 1 or int(userPackageInput) > len(packages_list):
                        print("\nPackage ID is invalid, exiting Program")
                        exit()
                    userTimeInput2 = input("Enter Time in HH:MM:SS format(24-hours): ")
                    if not is_valid_time_format(userTimeInput2):
                        raise ValueError
                    userTimeObj2 = convert_time_to_delta(userTimeInput2)
                    get_packages_at_this_time(userTimeObj2, [userPackageInput])
                except ValueError:
                    print("\nTime entry is invalid, exiting Program")
                    exit()

            elif userInput2 == '4':
                try:
                    userPackagesInput = input("Enter Packages id's separated by comma(no space): ")
                    if not is_valid_packages_format(userPackagesInput):
                        raise ValueError
                    userTimeInput4 = input("Enter Time in HH:MM:SS format(24-hours): ")
                    if not is_valid_time_format(userTimeInput4):
                        print("\nTime entered is invalid, exiting Program")
                        exit()
                    userTimeObj4 = convert_time_to_delta(userTimeInput4)
                    userPackagesList = userPackagesInput.split(',')
                    userPackagesList = [package.strip() for package in userPackagesList]
                    get_packages_at_this_time(userTimeObj4, userPackagesList)

                except ValueError:
                    print("\nPackages list is invalid, exiting Program")
                    exit()

            elif userInput2 == '5':
                print("Exiting Program")
                exit()

            else:
                print("\nInvalid Input")
                exit()
        except ValueError:
            print("\nInvalid Input")
            exit()




