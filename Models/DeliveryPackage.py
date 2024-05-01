
class Package:
    def __init__(self, p_id, address, city, state, zip, delivery_deadline, weight, status):
        self.p_id = p_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.p_id, self.address, self.city, self.state, self.zip,
                                                   self.delivery_deadline, self.weight,
                                                   self.status)
