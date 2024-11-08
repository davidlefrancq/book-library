import os
import json
from services.FileManager import FileManager
from models.Book import Book
from models.Member import Member
from models.Reservation import Reservation
from models.Borrow import Borrow

class DataPersistence:
  def __init__(self, file_path):
    if not os.path.exists(file_path):
      self.__fileManager = FileManager(file_path)
      self.__writeData({
        "reservations": [],
        "books": [],
        "members": [],
        "borrows": []
      })
    else:
      self.__fileManager = FileManager(file_path)

  def __readData(self):
    try:
      data = self.__fileManager.read()
      return json.loads(data)
    except FileNotFoundError:
      print(f"File not found: {self.__fileManager.file_path}")
      exit()
    except json.JSONDecodeError:
      print(f"Error decoding JSON file: {self.__fileManager.file_path}")
      exit()
  
  def __writeData(self, data):
    try:
      json_data = json.dumps(data)
      self.__fileManager.write(json_data)
    except FileNotFoundError:
      print(f"File not found: {self.__fileManager.file_path}")
      exit()
    except:
      print(f"Error encoding JSON file: {self.__fileManager.file_path}")
      exit()
    
  def getReservations(self):
    data = self.__readData()
    return [Reservation.from_dict(dataReservation) for dataReservation in data["reservations"]]
  
  def getBooks(self):
    data = self.__readData()
    return [Book.from_dict(dataBook) for dataBook in data["books"]]
  
  def getMembers(self):
    data = self.__readData()
    return [Member.from_dict(dataMember) for dataMember in data["members"]]
  
  def getBorrows(self):
    data = self.__readData()
    return [Borrow.from_dict(dataBorrow) for dataBorrow in data["borrows"]]
  
  def saveReservations(self, reservations):
    data = self.__readData()
    data["reservations"] = [reservation.to_dict() for reservation in reservations]
    self.__writeData(data)
    
  def saveBooks(self, books):
    data = self.__readData()
    data["books"] = [book.to_dict() for book in books]
    self.__writeData(data)
    
  def saveMembers(self, members):
    data = self.__readData()
    data["members"] = [member.to_dict() for member in members]
    self.__writeData(data)
    
  def saveBorrows(self, borrows):
    data = self.__readData()
    data["borrows"] = [borrow.to_dict() for borrow in borrows]
    self.__writeData(data)
    
  def saveAll(self, reservations, books, members, borrows):
    try:
      data = {
        "reservations": [reservation.to_dict() for reservation in reservations],
        "books": [book.to_dict() for book in books],
        "members": [member.to_dict() for member in members],
        "borrows": [borrow.to_dict() for borrow in borrows]
      }
      self.__writeData(data)
      print("Data saved.")
    except:
      print("Error saving data.")