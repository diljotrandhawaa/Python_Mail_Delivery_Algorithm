
import csv


def load_package_data(filename):
    packageList = []
    with open(filename) as package_csv:
        reader = csv.DictReader(package_csv, ['package_id', 'address', 'city', 'state', 'zip', 'deadline', 'weight', 'special_notes'])
        next(reader)
        next(reader)
        for row in reader:
            packageList.append(row)
            # print(row)

        return packageList


packages = load_package_data('package_csv.csv')

print(packages[0]['deadline'])

# class PackagesInfo:
#     def __init__(self, key):
#         self.hash_table = {}


    # def add_package(self, key, ):


