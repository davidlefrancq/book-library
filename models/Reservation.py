import datetime
from typing import Dict

class Reservation:
  def __init__(self, id, bookId, memberId, reservationDateStart, reservationDateEnd, status):
    self.id = id
    self.bookId = bookId
    self.memberId = memberId
    self.reservationDateStart = reservationDateStart
    self.reservationDateEnd = reservationDateEnd
    self.status = status
  
  def acceptReservation(self):
    self.status = "Accepted"  
  
  def cancelReservation(self):
    self.status = "Cancelled"
  
  def to_dict(self) -> Dict:
    return {
      "id": self.id,
      "bookId": self.bookId,
      "memberId": self.memberId,
      "reservationDateStart": self.reservationDateStart.strftime("%Y-%m-%d"),
      "reservationDateEnd": self.reservationDateEnd.strftime("%Y-%m-%d"),
      "status": self.status
    }

  def from_dict(data: Dict) -> 'Reservation':
    reservationDateStart = None
    if data["reservationDateStart"]:
      reservationDateStart = datetime.datetime.strptime(data["reservationDateStart"], "%Y-%m-%d")
    
    reservationDateEnd = None
    if data["reservationDateEnd"]:
      reservationDateEnd = datetime.datetime.strptime(data["reservationDateEnd"], "%Y-%m-%d")
      
    return Reservation(
      data["id"],
      data["bookId"],
      data["memberId"],
      reservationDateStart,
      reservationDateEnd,
      data["status"]
    )