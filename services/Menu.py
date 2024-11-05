import datetime

class Menu:
	def __init__(self, library, notifier):
		self.library = library
		self.notifier = notifier
		# Dictionnaire des actions disponibles
		self.actions = {
				"1": ("Ajouter un livre", self.add_book),
				"2": ("Voir les livres", self.show_books),
				"3": ("Ajouter un membre", self.add_member),
				"4": ("Voir les membres", self.show_members),
				"5": ("Emprunter un livre", self.borrow_book),
				"6": ("Retourner un livre", self.return_book),
				"7": ("Rechercher un livre", self.search_book),
				"8": ("Quitter", self.quit)
		}
		self.running = True

	def display_menu(self):
		print("\n=== Bibliothèque ===")
		for key, (description, _) in self.actions.items():
				print(f"{key}. {description}")
		return input("\nChoisissez une option: ")

	def run(self):
		while self.running:
				choice = self.display_menu()
				if choice in self.actions:
						_, action = self.actions[choice]
						action()
				else:
						print("Option invalide!")

	def add_book(self):
		title = input("Titre: ")
		author = input("Auteur: ")
		genre = input("Genre: ")
		publication_date = input("Date de publication: ")
		self.library.addBook(title, author, genre, publication_date, True)
		self.notifier.notify("Livre ajouté avec succès!")

	def show_books(self):
		self.library.showAvailableBooks()

	def add_member(self):
		first_name = input("Prénom: ")
		last_name = input("Nom: ")
		address = input("Adresse: ")
		phone = input("Téléphone: ")
		self.library.addMember(first_name, last_name, address, phone)
		self.notifier.notify("Membre ajouté avec succès!")

	def show_members(self):
		if not self.library.members:
				print("Aucun membre enregistré")
				return
		print("\nListe des membres:")
		for member in self.library.members:
				print(f"ID: {member.id} - {member.firstName} {member.lastName}")

	def borrow_book(self):
		if not self.library.members:
			print("Aucun membre enregistré. Veuillez d'abord ajouter un membre.")
			return
		if not self.library.catalog.books:
			print("Aucun livre disponible. Veuillez d'abord ajouter des livres.")
			return

		self.show_books()
		self.show_members()
		
		try:
			book_id = int(input("ID du livre à emprunter: "))
			# Vérifier si le livre existe
			book = self.library.catalog.searchBook(book_id)
			if not book:
				print("Livre non trouvé")
				return
			
			# Vérifier si le livre est disponible
			if not book.isAvailable:
				print("Ce livre n'est pas disponible")
				return

			member_id = int(input("ID du membre: "))
			# Vérifier si le membre existe
			member = next((m for m in self.library.members if m.id == member_id), None)
			if not member:
				print("Membre non trouvé")
				return

			dateStartInput = input("Date de début de l'emprunt (jj/mm/aaaa): ")
			dateStart = datetime.datetime.strptime(dateStartInput, "%d/%m/%Y")
			dateEndInput = input("Date de fin de l'emprunt (jj/mm/aaaa): ")
			dateEnd = datetime.datetime.strptime(dateEndInput, "%d/%m/%Y")
			# Vérifier si le livre est disponible
			if not self.library.checkDateBorrowBook(book_id, dateStart, dateEnd):
				print("Ce livre n'est pas disponible à ces dates.")
				return
			
			if self.library.borrowBook(book_id, member_id, dateStart, dateEnd):
				self.notifier.notify("Livre emprunté avec succès!")
			else:
				self.notifier.notify("Erreur lors de l'emprunt")

		except ValueError:
			print("Veuillez entrer des nombres valides pour les IDs")

	def return_book(self):
		if not self.library.borrows:
			print("Aucun emprunt en cours")
			return

		print("\nEmprunts en cours:")
		for borrow in self.library.borrows:
			if borrow.status != "Returned":
				book = self.library.catalog.searchBook(borrow.bookId)
				member = next((m for m in self.library.members if m.id == borrow.memberId), None)
				print(f"ID Emprunt: {borrow.id} - Livre: {book.title} - Membre: {member.firstName} {member.lastName}")

		try:
			borrow_id = int(input("ID de l'emprunt à retourner: "))
			if self.library.returnBook(borrow_id):
				self.notifier.notify("Livre retourné avec succès!")
				# Calculer et afficher le retard éventuel
				borrow = self.library.searchBorrow(borrow_id)
				if borrow:
					delay = borrow.delayCalculation()
					if delay > 0:
						print(f"Retard de {delay} jours")
			else:
				self.notifier.notify("Erreur lors du retour")
		except ValueError:
			print("Veuillez entrer un nombre valide pour l'ID")

	def search_book(self):
		title = input("Titre à rechercher: ")
		book = self.library.searchBook(title)
		
		disponible = "Non"
		if book.isAvailable:
			disponible = "Oui"
				
		if book:
			print(f"\nLivre trouvé:")
			print(f"ID: {book.id}")
			print(f"Titre: {book.title}")
			print(f"Auteur: {book.author}")
			print(f"Genre: {book.genre}")
			print(f"Date de publication: {book.publicationDate}")
			print(f"Disponible: {disponible}")
		else:
			print("Livre non trouvé")

	def quit(self):
		self.running = False
		print("Au revoir!")