
# PackagesHashtable is the data structure we are going to use to store our packages information
# and update them as needed.
class PackagesHashtable:
    # initialise the list to have 200 entries
    def __init__(self):
        self.max = 200
        self.packages = []
        for i in range(self.max):
            self.packages.append([])

    # hash function
    def get_hash(self, key):
        return hash(key) % len(self.packages)

    # performs Insertion calculate the index using hash function and
    # also handles collisions using buckets called packages_list
    def insert(self, key, value):
        hash_index = self.get_hash(key)
        package_list = self.packages[hash_index]

        for package in package_list:
            if package[0] == key:
                package[1] = value
                return True

        self.packages[hash_index].append([key, value])
        return True

    # Look up function that performs hashing using the same key and
    # then returning the bucket's value at that index
    def look(self, key):
        hash_index = self.get_hash(key)
        package_list = self.packages[hash_index]

        for package in package_list:
            if package[0] == key:
                return package[1]

        return None

    
