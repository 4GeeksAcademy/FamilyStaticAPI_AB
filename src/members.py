import json


class FamilyMember:
    def __init__(self, memberId, first_name, last_name, age, lucky_numbers): 
        self.memberId = memberId
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.lucky_numbers = lucky_numbers

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)





