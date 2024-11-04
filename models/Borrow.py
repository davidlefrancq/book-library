import datetime
from typing import Dict

class Borrow:
  def __init__(self, id, bookId, memberId, borrowDate, expectedReturnDate, returnDate, status):
    self.id = id
    self.bookId = bookId
    self.memberId = memberId
    self.borrowDate = borrowDate
    self.expectedReturnDate = expectedReturnDate
    self.returnDate = returnDate
    self.status = status
    
  def returnBook(self):
    self.returnDate = datetime.datetime.now()
    self.status = "Returned"
  
  def delayCalculation(self):
    return (self.returnDate - self.expectedReturnDate).days
  
  def to_dict(self) -> Dict:
    return {
      "id": self.id,
      "bookId": self.bookId,
      "memberId": self.memberId,
      "borrowDate": self.borrowDate,
      "expectedReturnDate": self.expectedReturnDate,
      "returnDate": self.returnDate,
      "status": self.status
    }
  
  def from_dict(data: Dict) -> 'Borrow':
    return Borrow(
      data["id"],
      data["bookId"],
      data["memberId"],
      data["borrowDate"],
      data["expectedReturnDate"],
      data["returnDate"],
      data["status"]
    )