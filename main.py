
import csv

from Models.DeliveryPackage import Package
from Models.Packages_Hashtable import PackagesHashtable


def load_package_data(filename, packages_hash_table):
    packageList = []
    with open(filename) as package_csv:
        reader = csv.DictReader(package_csv, ['package_id', 'address', 'city', 'state', 'zip', 'deadline', 'weight', 'special_notes'])
        next(reader)
        next(reader)
        for row in reader:
            packageList.append(row)
            delivery_package = Package(row['package_id'], row['address'], row['city'], row['state'], row['zip'], row['deadline'], row['weight'], "At the hub")
            packages_hash_table.insert(row['package_id'], delivery_package)

        return packageList


Packages_data = PackagesHashtable()

load_package_data('package_csv.csv', Packages_data)

print(Packages_data.look('19'))



