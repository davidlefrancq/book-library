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
    return self.catalog.searchBook(title)
  
  def deleteBook(self, title):
    isDeleted = self.catalog.deleteBook(title)
    if isDeleted:
      self.dataPersistence.saveBooks(self.catalog.books)
    return isDeleted
  
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
      self.dataPersistence.saveBooks(self.catalog.books)
      return book.isAvailable
    return False
  
  def cancelReservation(self, reservationId):
    reservation = self.getReservation(reservationId)
    if reservation:
      reservation.cancelReservation()
      self.dataPersistence.saveReservations(self.reservations)
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
      self.dataPersistence.saveBorrows(self.borrows)
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