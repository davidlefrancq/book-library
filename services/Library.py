import atexit
import datetime
from models.Book import Book
from models.Member import Member
from models.Reservation import Reservation
from models.Borrow import Borrow
from services.Catalog import Catalog
from services.DataPersistence import DataPersistence

class Library:
  def __init__(self):
    self.dataPersistence = DataPersistence("data.json")
    self.catalog = Catalog(self.dataPersistence.getBooks())
    self.reservations = self.dataPersistence.getReservations()
    self.borrows = self.dataPersistence.getBorrows()
    self.members = self.dataPersistence.getMembers()
    atexit.register(lambda: self.dataPersistence.saveAll(
      self.reservations,
      self.catalog.books,
      self.members,
      self.borrows
    ))
  
  def addMember(self, firstName, lastName, address, phone):
    id = len(self.members) + 1
    member = Member(id, firstName, lastName, address, phone)
    self.members.append(member)
    self.dataPersistence.saveMembers(self.members)
    
  def addBook(self, title, author, genre, publicationDate, isAvailable):
    id = len(self.catalog.books) + 1
    book = Book(id, title, author, genre, publicationDate, isAvailable)
    self.catalog.addBook(book)
    self.dataPersistence.saveBooks(self.catalog.books)
    
  def searchBook(self, title):
    return self.catalog.searchBookByTitle(title)
  
  def deleteBook(self, title):
    isDeleted = self.catalog.deleteBook(title)
    if isDeleted:
      self.dataPersistence.saveBooks(self.catalog.books)
    return isDeleted
  
  def checkDateReservation(self, bookId, dateStart, dateEnd):
    isAvailable = True
    for reservation in self.reservations:
      if reservation.bookId == bookId:
        if reservation.status == "Accepted":
          # dateStart doit être petit que dateStart
          if dateStart < reservation.reservationDateStart:
            # dateEnd doit être plus petit que reservationDateStart sinon false
            if dateEnd > reservation.reservationDateStart:
              isAvailable = False
          # sinon si dateStart est plus grand que dateEnd
          elif dateStart > reservation.reservationDateStart:
            # dateStart doit être plus grand que reservationDateEnd sinon false
            if dateStart < reservation.reservationDateEnd:
              isAvailable = False
    return isAvailable
 
  def reserveBook(self, bookId, memberId, reservationDateStart, reservationDateEnd):
    if not self.checkDateReservation(bookId, reservationDateStart, reservationDateEnd):
      print("Le livre n'est pas disponible pour cette période.")
      return None
    else:
      id = len(self.reservations) + 1
      reservation = Reservation(id, bookId, memberId, reservationDateStart, reservationDateEnd, "Pending")
      self.reservations.append(reservation)
      self.dataPersistence.saveReservations(self.reservations)
      return reservation
    
  def acceptReservation(self, reservationId):
    isAccepted = False
    reservation = self.getReservation(reservationId)
    if reservation:
      reservation.acceptReservation()
      self.dataPersistence.saveBooks(self.catalog.books)
      isAccepted = True
    return isAccepted
  
  def cancelReservation(self, reservationId):
    isCancelled = False
    reservation = self.getReservation(reservationId)
    if reservation:
      reservation.cancelReservation()
      self.dataPersistence.saveReservations(self.reservations)
      isCancelled = True
    return isCancelled
  
  def getReservation(self, reservationId):
    for reservation in self.reservations:
      if reservation.id == reservationId:
        return reservation
    return
  
  def borrowBookFromReservation(self, reservationId):
    raise NotImplementedError
  
  def checkDateBorrowBook(self, bookId, dateStart, dateEnd):
    isAvailable = True
    book = self.catalog.searchBook(bookId)
    if not book.isAvailable:
      isAvailable = False
    else:
      for borrow in self.borrows:
        if borrow.bookId == bookId:
          if borrow.status == "Borrowed":
            # dateStart doit être petit que dateStart
            if dateStart < borrow.borrowDate:
              # dateEnd doit être plus petit que reservationDateStart sinon false
              if dateEnd > borrow.borrowDate:
                isAvailable = False
            # sinon si dateStart est plus grand que dateEnd
            elif dateStart > borrow.borrowDate:
              # dateStart doit être plus grand que reservationDateEnd sinon false
              if dateStart < borrow.expectedReturnDate:
                isAvailable = False
    return isAvailable
  
  def borrowBook(self, bookId, memberId, dateStart, dateEnd):
    isBorrowed = False
    if self.checkDateBorrowBook(bookId, dateStart, dateEnd):
      id = len(self.borrows) + 1
      borrow = Borrow(id, bookId, memberId, dateStart, dateEnd, None, "Borrowed")
      self.borrows.append(borrow)
      book = self.catalog.searchBook(bookId)
      book.isAvailable = False
      # self.dataPersistence.saveBorrows(self.borrows)
      # self.dataPersistence.saveBooks(self.catalog.books)
      self.dataPersistence.saveAll(
        self.reservations,
        self.catalog.books,
        self.members,
        self.borrows
      )
      isBorrowed = True
    return isBorrowed  
    
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
  
  def showAvailableBooks(self):
    for book in self.catalog.books:
      if book.isAvailable:
        print(f"{book.id} - {book.title}")
  
  def searchBorrow(self, borrowId):
    for borrow in self.borrows:
      if borrow.id == borrowId:
        return borrow
    return