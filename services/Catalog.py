from models.Book import Book

class Catalog:
  def __init__(self, books = []):
    self.books = books
    
  def addBook(self, book):
    self.books.append(book)
    
  def searchBook(self, id):
    for book in self.books:
      if book.id == id:
        return book
    return None

  def searchBookByTitle(self, id):
    for book in self.books:
      if book.title == id:
        return book
    return None

  def deleteBook(self, title):
    book = self.searchBook(title)
    if book:
      self.books.remove(book)
      return True
    return False