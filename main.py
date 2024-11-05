import datetime
import signal
from services.Library import Library
from services.Menu import Menu

class Notifier:
  def notify(self, message):
    print(message)

class App:
  def __init__(self):
    self.library = Library()
    self.notifier = Notifier()
    self.menu = Menu(self.library, self.notifier)
  
  def run(self):
    self.menu.run()
  
  def test(self):   
    # Add books
    self.library.addBook("The Great Gatsby", "F. Scott Fitzgerald", "Novel", "1925", True)
    self.library.addBook("To Kill a Mockingbird", "Harper Lee", "Novel", "1960", True)
    self.library.addBook("1984", "George Orwell", "Dystopian novel", "1949", True)
    self.library.addBook("The lord of the rings", "J.R.R. Tolkien", "High fantasy", "1954", True)
    self.library.addBook("The Catcher in the Rye", "J.D. Salinger", "Novel", "1951", True)
    
    # Show books
    self.library.showBooks()
    
    # Add members
    self.library.addMember("John", "Doe", "1234 Elm St", "555-5555")
    self.library.addMember("Jane", "Watson", "21 Baker St", "444-4444")
    
    # Reserve a book
    self.library.reserveBook(1, 1, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=7))
    self.library.reserveBook(2, 2, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=7))
    self.library.reserveBook(3, 1, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=7))
    
    # Accept reservation
    self.library.acceptReservation(1)
    self.library.acceptReservation(2)
    
    # Cancel reservation
    self.library.cancelReservation(3)
    
    # Borrow a book
    borrowBook1 = self.library.borrowBook(1)
    if borrowBook1:
      self.notifier.notify("Book borrowed successfully")
    borrowBook2 = self.library.borrowBook(2)
    if borrowBook2:
      self.notifier.notify("Book borrowed successfully")
    
    # Fail to borrow a book (reservation not accepted)
    borrowBook3 = self.library.borrowBook(3)
    if borrowBook3:
      self.notifier.notify("Book borrowed successfully")
    else:
      self.notifier.notify("Book not borrowed. Reservation not accepted.")
    
    # Return a book
    returnBook1 = self.library.returnBook(1)
    if returnBook1:
      self.notifier.notify("Book returned successfully")
      print(f"Delay: {self.library.borrows[0].delayCalculation()}")
    else:
      self.notifier.notify("Book not returned. Borrow not found.")

if __name__ == "__main__":
  app = App()
  app.run()
  # app.test()
