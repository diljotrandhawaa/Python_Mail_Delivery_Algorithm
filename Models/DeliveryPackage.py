
class DeliveryPackage:
    def __init__(self, id, address, city, state, zip, delivery_deadline, special_request):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.special_request = special_request