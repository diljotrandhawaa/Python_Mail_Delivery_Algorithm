
# The class Truck creates a truck object with properties id, truck's capacity, speed, packages it has to deliver,
# depart time of the truck, miles travelled by the truck and the current time of the
# truck with respect to the packages it has delivered

class Truck:
    def __init__(self, id, capacity, speed, packages, depart_time, miles_travelled, time):
        self.id = id
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.depart_time = depart_time
        self.miles_travelled = miles_travelled
        self.time = time

    # the __str__ function is to simply print the truck object and it's properties
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.id, self.capacity, self.speed, self.packages,
                                               self.depart_time, self.miles_travelled, self.time)