class FileManager:
  def __init__(self, file_path):
    self.file_path = file_path

  def read(self):
    with open(self.file_path, 'r') as file:
      return file.read()

  def write(self, data):
    with open(self.file_path, 'w') as file:
      file.write(data)