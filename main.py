import datetime

class Member:
  def __init__(self, id, firstName, lastName, address, phone):
    self.id = id
    self.firstName = firstName
    self.lastName = lastName
    self.address = address
    self.phone = phone
 
class Book:
  def __init__(self, id, title, author, genre, publicationDate, isAvailable):
    self.id = id
    self.title = title
    self.author = author
    self.genre = genre
    self.publicationDate = publicationDate
    self.isAvailable = isAvailable

class Catalog:
  def __init__(self):
    self.books = []
    
  def addBook(self, book):
    self.books.append(book)
    
  def searchBook(self, id):
    for book in self.books:
      if book.id == id:
        return book
    return None
  
  def deleteBook(self, title):
    book = self.searchBook(title)
    if book:
      self.books.remove(book)
      return True
    return False
  
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

class Library:
  def __init__(self):
    self.catalog = Catalog()
    self.reservations = []
    self.borrows = []
    self.members = []
  
  def addMember(self, firstName, lastName, address, phone):
    id = len(self.members) + 1
    member = Member(id, firstName, lastName, address, phone)
    self.members.append(member)
    
  def addBook(self, title, author, genre, publicationDate, isAvailable):
    id = len(self.catalog.books) + 1
    book = Book(id, title, author, genre, publicationDate, isAvailable)
    self.catalog.addBook(book)
    
  def searchBook(self, title):
    return self.catalog.searchBook(title)
  
  def deleteBook(self, title):
    return self.catalog.deleteBook(title)
  
  def reserveBook(self, bookId, memberId, reservationDateStart, reservationDateEnd):
    id = len(self.reservations) + 1
    reservation = Reservation(id, bookId, memberId, reservationDateStart, reservationDateEnd, "Pending")
    self.reservations.append(reservation)
    return reservation
    
  def acceptReservation(self, reservationId):
    reservation = self.getReservation(reservationId)
    if reservation:
      reservation.acceptReservation()
      book = self.catalog.searchBook(reservation.bookId)
      book.isAvailable = True
      return book.isAvailable
    return False
  
  def cancelReservation(self, reservationId):
    reservation = self.getReservation(reservationId)
    if reservation:
      reservation.cancelReservation()
      return True
    return False
  
  def getReservation(self, reservationId):
    for reservation in self.reservations:
      if reservation.id == reservationId:
        return reservation
    return
    
  def borrowBook(self, reservationId):
    reservation = self.getReservation(reservationId)
    if reservation and reservation.status == "Accepted":
      id = len(self.borrows) + 1
      borrow = Borrow(id, reservation.bookId, reservation.memberId, datetime.datetime.now(), reservation.reservationDateEnd, None, "Borrowed")
      self.borrows.append(borrow)
      return True
    return False    
    
  def returnBook(self, borrowId):
    borrow = self.searchBorrow(borrowId)
    if borrow:
      borrow.returnBook()
      book = self.catalog.searchBook(borrow.bookId)
      book.isAvailable = True
      borrow.returnDate = datetime.datetime.now()
      return True
    return False
  
  def showBooks(self):
    for book in self.catalog.books:
      print(f"{book.id} - {book.title}")
  
  def searchBorrow(self, borrowId):
    for borrow in self.borrows:
      if borrow.id == borrowId:
        return borrow
    return

class Notifier:
  def notify(self, message):
    print(message)

class App:
  def __init__(self):
    self.library = Library()
    self.notifier = Notifier()
    
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

app = App()
app.test()