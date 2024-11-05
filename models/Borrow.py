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
    returnDate = None
    if self.returnDate:
      returnDate = self.returnDate.strftime("%Y-%m-%d")

    return {
      "id": self.id,
      "bookId": self.bookId,
      "memberId": self.memberId,
      "borrowDate": self.borrowDate.strftime("%Y-%m-%d"),
      "expectedReturnDate": self.expectedReturnDate.strftime("%Y-%m-%d"),
      "returnDate": returnDate,
      "status": self.status
    }
  
  def from_dict(data: Dict) -> 'Borrow':
    borrowDate = None
    if data["borrowDate"]:
      borrowDate = datetime.datetime.strptime(data["borrowDate"], "%Y-%m-%d")
    
    expectedReturnDate = None
    if data["expectedReturnDate"]:
      expectedReturnDate = datetime.datetime.strptime(data["expectedReturnDate"], "%Y-%m-%d")
    
    returnDate = None
    if data["returnDate"]:
      returnDate = datetime.datetime.strptime(data["returnDate"], "%Y-%m-%d")
    
    return Borrow(
      data["id"],
      data["bookId"],
      data["memberId"],
      borrowDate,
      expectedReturnDate,
      returnDate,
      data["status"]
    )