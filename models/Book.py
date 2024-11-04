from typing import Dict

class Book:
  def __init__(self, id, title, author, genre, publicationDate, isAvailable):
    self.id = id
    self.title = title
    self.author = author
    self.genre = genre
    self.publicationDate = publicationDate
    self.isAvailable = isAvailable
    
  def to_dict(self) -> Dict:
    return {
      "id": self.id,
      "title": self.title,
      "author": self.author,
      "genre": self.genre,
      "publicationDate": self.publicationDate,
      "isAvailable": self.isAvailable
    }

  def from_dict(data: Dict) -> 'Book':
    return Book(
      data["id"],
      data["title"],
      data["author"],
      data["genre"],
      data["publicationDate"],
      data["isAvailable"]
    )