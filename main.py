
import csv
import datetime

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

        return True


modified_distance_data = []
with open('distance_csv.csv') as distance_csv:
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
        delivered_package.status = 'Delivered by Truck-'+ delivered_package.truck_id

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
load_package_data('package_csv.csv', Packages_data)

truck1 = Truck('1', 16, 18, ['7', '29', '2', '33', '1', '4', '40', '12'], datetime.timedelta(hours=8), 0, datetime.timedelta(hours=8))
truck2 = Truck('2', 16, 18, ['3', '5', '6', '8', '9', '18', '22', '24', '25', '26', '28', '31', '32', '35', '36', '38'], datetime.timedelta(hours=9, minutes=15), 0, datetime.timedelta(hours=9, minutes=15))
truck3 = Truck('3', 16, 18, ['10', '11', '13', '14', '15', '16', '17', '19', '20', '21', '23', '27', '30', '34', '37', '39'], datetime.timedelta(hours=8), 0, datetime.timedelta(hours=8))

packages_delivery(truck1)
packages_delivery(truck2)
packages_delivery(truck3)

# print(find_truck_for_package(Packages_data.look('7')))

# print(Packages_data.look('15'))


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
        package_truck = find_truck_for_package(package)

        packages[package_id] = package
        if time_given > package_truck.depart_time:
            if time_given >= package.delivery_time:
                packages[package_id].status = 'Delivered by Truck-' + package.truck_id
            else:
                packages[package_id].status = 'En route by Truck-' + package.truck_id
        else:
            packages[package_id].status = 'At the hub'

    for package_id in packages:
        print(packages[package_id])
    return packages


# the class Main is for UI, takes user input and prints the data requested by user
class Main:
    print('Western Governors University C950')
    print('Student ID: Diljot Singh')
    print('The mileage travelled by trucks is: ')
    print(round(truck1.miles_travelled + truck2.miles_travelled + truck3.miles_travelled, 1), " miles")

    time_to_give = datetime.timedelta(hours=8, minutes=15)
    packages_to_view = ['7', '29', '2', '33', '1', '4', '40', '12']

    print(get_packages_at_this_time(time_to_give, packages_to_view))





