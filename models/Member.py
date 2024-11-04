from typing import Dict

class Member:
  def __init__(self, id, firstName, lastName, address, phone):
    self.id = id
    self.firstName = firstName
    self.lastName = lastName
    self.address = address
    self.phone = phone

  def to_dict(self) -> Dict:
    return {
      "id": self.id,
      "firstName": self.firstName,
      "lastName": self.lastName,
      "address": self.address,
      "phone": self.phone
    }
    
  def from_dict(data: Dict) -> 'Member':
    return Member(
      data["id"],
      data["firstName"],
      data["lastName"],
      data["address"],
      data["phone"]
    )