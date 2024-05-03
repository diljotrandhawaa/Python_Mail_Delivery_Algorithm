# the class Package is to store the information of a Package like
# it's id, address, city, state zip, package's delivery deadline time, weight of package,
# current status of the package and
# delivery_time, the time it was delivered (only updates after delivered), initially set to "At the hub"
# and last the truck_id, the id of truck it is loaded in or was loaded in
class Package:
    def __init__(self, p_id, address, city, state, pk_zip, delivery_deadline, weight, status, delivery_time, truck_id):
        self.p_id = p_id
        self.address = address
        self.city = city
        self.state = state
        self.pk_zip = pk_zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time
        self.truck_id = truck_id

    # the __str__ function is to simply print the Package object and it's properties
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.p_id, self.address, self.city, self.state, self.pk_zip,
                                                   self.delivery_deadline, self.weight,
                                                   self.status, self.delivery_time)
