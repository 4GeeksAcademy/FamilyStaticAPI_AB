
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        # example list of members
        self._members = []
    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):

        self._members.append(member)
        return

    def delete_member(self, id):
        find = {} 
        for mem in self._members:
            print("id ", id)
            if  mem.memberId == int(id):
                self._members.remove(mem)
                return True
        return False
        

    def get_member(self, id):
        # fill this method and update the return
        find = {} 
        print(type(id))
        for mem in self._members:
            print(mem.memberId)
            print("id ", id)
            if  mem.memberId == int(id):
                print("found")
                find = mem
        print(find)
        return find

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
