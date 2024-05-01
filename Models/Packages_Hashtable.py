
class PackagesHashtable:
    def __init__(self):
        self.max = 200
        self.packages = []
        for i in range(self.max):
            self.packages.append([])

    def get_hash(self, key):
        return hash(key) % len(self.packages)

    def insert(self, key, value):
        hash_index = self.get_hash(key)
        package_list = self.packages[hash_index]

        for package in package_list:
            if package[0] == key:
                package[1] = value
                return True

        self.packages[hash_index].append([key, value])
        return True

    def look(self, key):
        hash_index = self.get_hash(key)
        package_list = self.packages[hash_index]

        for package in package_list:
            if package[0] == key:
                return package[1]

        return None

    
