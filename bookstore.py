class Product:

    def __init__(self, sell_price, buy_price, tax):
        self.parameters = {}
        self.parameters['sell_price'] = sell_price
        self.parameters['buy_price'] = buy_price
        self.parameters['tax'] = tax


class Book(Product):
    
    def __init__(self, title, author, genre, edition, publisher, sell_price, buy_price):
        tax = self.calculate_tax(genre, sell_price, buy_price)
        super().__init__(sell_price, buy_price, tax)
        self.parameters['title'] = title
        self.parameters['author'] = author
        self.parameters['genre'] = genre
        self.parameters['edition'] = edition
        self.parameters['publisher'] = publisher
        author.books.append(self)

    def __str__(self):
        return str(self.parameters)

    def __repr__(self):
        return str(self.parameters)

    def calculate_tax(self, genre, sell_price, buy_price):
        if genre == 'Fiction':
            return (sell_price - buy_price) * 0.20
        if genre == 'Horror ':
            return (sell_price - buy_price) * 0.15
        return (sell_price - buy_price) * 0.10


class Author:

    def __init__(self, name, email, books = []):
        self.name = name
        self.email = email
        self.books = []
        self.books.extend(books)

    def __str__(self):
        return str({'name': self.name, 'email': self.email})
    
    def __repr__(self):
        return str({'name': self.name, 'email': self.email})
    

class Client:

    def __init__(self, name, email, orders = []):
        self.name = name
        self.email = email
        self.orders = []
        self.orders.extend(orders)

    def __str__(self):
        return str({'name': self.name, 'email': self.email})
        
    def __repr__(self):
        return str({'name': self.name, 'email': self.email})


class Order:

    def __init__(self, client, products_details):
        self.client = client
        self.products_details = []
        self.products_details.extend(products_details)
        client.orders.append(self)

    def __str__(self):
        return str({'client': self.client, 'products_details': self.products_details})

    def __repr__(self):
        return str({'client': self.client, 'products_details': self.products_details})


class Bookstore():

    def __init__(self, products_lists, clients, authors, orders = []):
        self.clients = []
        self.clients.extend(clients)
        self.authors = []
        self.authors.extend(authors)
        self.orders = []
        self.orders.extend(orders)
        self.products = {}
        for products_type in products_lists:
            self.products[products_type] = []
        for products_type, products_list in products_lists.items():
            self.products[products_type].extend(products_list)
        
    def insert_item(self, item):
        self.products[item.__class__].append(item)

    def insert_book(self, book):
        self.insert_item(book)

    def get_books(self, title = None, author = None, genre = None, edition = None, publisher = None):
        books = self.products[Book].copy()
        filters = {
            'title': title,
            'author': author,
            'genre': genre,
            'edition': edition,
            'publisher': publisher
        }
        for key in list(filters):
            if filters[key] == None:
                filters.pop(key)
        total = len(books)
        i = 0
        while i < total:
            for key in filters:
                if books[i].parameters[key] != filters[key]:
                    books.pop(i)
                    i -= 1
                    total -= 1
                    break
            i += 1
        return books

    def remove_books(self, title, author, genre, edition, publisher):
        books = self.products[Book]
        total = len(books)
        i = 0
        while i < total:
            book = books[i]
            params = ['title', 'author', 'genre', 'edition', 'publisher']
            book_params = [book.parameters[i] for i in params]
            if book_params == [title, author, genre, edition, publisher]:
                books.pop(i)
                i -= 1
                total -= 1
            i += 1

    def modify_books(self, title, author, genre, edition, publisher, new_parameters):
        books = self.products[Book]
        for i in range(len(books)):
            book = books[i]
            params = ['title', 'author', 'genre', 'edition', 'publisher']
            book_params = [book.parameters[i] for i in params]
            if book_params == [title, author, genre, edition, publisher]:
                for parameter in new_parameters:
                    books[i].parameters[parameter] = new_parameters[parameter]

    def insert_client(self, name, email, orders = []):
        client = Client(name, email, orders)
        self.clients.append(client)

    def remove_client(self, name, email):
        client = self.get_client(name, email)
        self.clients.remove(client)

    def modify_client(self, name, email, new_name = None, new_email = None, new_orders = None):
        client = self.get_client(name, email)
        if new_name != None:
            client.name = new_name
        if new_email != None:
            client.email = new_email
        if new_orders != None:
            client.orders.extend(new_orders)

    def get_client(self, name, email):
        for client in self.clients:
            if client.name == name and client.email == email:
                return client

    def get_all_clients(self):
        return self.clients

    def insert_order(self, order):
        self.orders.append(order)

    def remove_order(self, products_details, client_name, client_email):
        client = self.get_client(client_name, client_email)
        for i in range(len(self.orders)):
            if self.orders[i].client == client and self.orders[i].products_details == products_details:
                self.orders.pop(i)
                break

    def modify_order(self, products_details, client, new_products_details = None, new_client = None):
        orders = self.get_orders(products_details, client.name, client.email)
        for order in orders:
            if new_products_details != None:
                order.products_details = new_products_details
            if new_client != None:
                order.client = new_client

    def get_orders(self, products_details = None, client_name = None, client_email = None):
        orders = self.orders.copy()
        if not any([products_details, client_name, client_email]):
            return orders
        total = len(orders)
        i = 0
        client = self.get_client(client_name, client_email)
        while i < total:
            if orders[i].products_details != products_details or orders[i].client != client:
                orders.pop(i)
                i -= 1
                total -= 1
            i += 1
        return orders

    def get_product_types(self):
        return self.products.keys()


def run():
    # Registrando autores
    author1 = Author(name = 'Felipe', email = 'felipe@gmail.com')
    author2 = Author(name = 'Gustavo', email = 'gustavo@gmail.com')

    # Registrando livros
    book1 = Book(title = 'Livro Amarelo', author = author1, genre = 'Fiction', edition = 1, publisher = 'Editora Nova', sell_price = 70, buy_price = 30)
    book2 = Book(title = 'Livro Azul', author = author2, genre = 'Horror', edition = 6, publisher = 'Editora Velha', sell_price = 20, buy_price = 5)
    book3 = Book(title = 'Livro Verde', author = author1, genre = 'Classic', edition = 1, publisher = 'Editora Antiga', sell_price = 80, buy_price = 30)

    # Registrando clientes
    client1 = Client(name = 'Pedro', email = 'pedro@gmail.com')
    client2 = Client(name = 'Anna', email = 'anna@gmail.com')

    # Definindo variáveis auxiliares para compras
    buy1 = {'product': book1, 'price': book1.parameters['buy_price'], 'amount': 2}
    buy2 = {'product': book3, 'price': book3.parameters['buy_price'], 'amount': 1}
    buy3 = {'product': book2, 'price': book2.parameters['buy_price'], 'amount': 5}
    buy4 = {'product': book3, 'price': book3.parameters['buy_price'], 'amount': 1}
    buy5 = {'product': book2, 'price': book2.parameters['buy_price'], 'amount': 1}

    # Registrando compras
    order1 = Order(client = client1, products_details = [buy1, buy2, buy3])
    order2 = Order(client = client2, products_details = [buy4, buy5])
    order3 = Order(client = client2, products_details = [buy1])

    # Criando livraria
    my_bookstore = Bookstore(products_lists = {Book: [book1, book2, book3]}, clients = [client1, client2], authors = [author1, author2], orders = [order1, order2, order3])

    # Testando consulta de livros
    books = my_bookstore.get_books(title = 'Livro Amarelo')
    for book in books:
        print(book)


    books = my_bookstore.get_books(author = author1)
    for book in books:
        print(book)


    # Testando inserção de livro
    book4 = Book(title = 'Livro Preto', author = author2, genre = 'Drama', edition = 1, publisher = 'Editora Brasileira', sell_price = 100, buy_price = 15)
    my_bookstore.insert_book(book4)
    books = my_bookstore.get_books()
    for book in books:
        print(book)


    # Testando modificação de livros
    new_parameters = {'sell_price': 1000}
    my_bookstore.modify_books(title = 'Livro Preto', author = author2, genre = 'Drama', edition = 1, publisher = 'Editora Brasileira', new_parameters = new_parameters)
    books = my_bookstore.get_books(title = 'Livro Preto')
    for book in books:
        print(book)


    # Testando remoção de livros
    my_bookstore.remove_books(title = 'Livro Amarelo', author = author1, genre = 'Fiction', edition = 1, publisher = 'Editora Nova')
    books = my_bookstore.get_books()
    for book in books:
        print(book)


    # Testando consulta de clientes
    clients = my_bookstore.get_all_clients()
    for client in clients:
        print(client)


    client = my_bookstore.get_client(name = 'Pedro', email = 'pedro@gmail.com')
    print(client)

    # Testando inserção de clientes
    my_bookstore.insert_client(name = 'Julia', email = 'julia@gmail.com')
    clients = my_bookstore.get_all_clients()
    for client in clients:
        print(client)


    # Testando modificação de clientes
    new_email = 'pedro_novo@gmail.com'
    my_bookstore.modify_client(name = 'Pedro', email = 'pedro@gmail.com', new_email = new_email)
    clients = my_bookstore.get_all_clients()
    for client in clients:
        print(client)


    # Testando remoção de clientes
    my_bookstore.remove_client(name = 'Anna', email = 'anna@gmail.com')
    clients = my_bookstore.get_all_clients()
    for client in clients:
        print(client)


    # Testando consulta de ordens de compra
    orders = my_bookstore.get_orders()
    for order in orders:
        print(order)


    orders = my_bookstore.get_orders(products_details = [buy1, buy2, buy3], client_name = 'Pedro', client_email = 'pedro_novo@gmail.com')
    for order in orders:
        print(order)


    # Testando inserção de ordens de compra
    buy6 = {'product': book2, 'price': book2.parameters['buy_price'], 'amount': 1}
    order4 = Order(client = client1, products_details = [buy6])
    my_bookstore.insert_order(order4)
    orders = my_bookstore.get_orders()
    for order in orders:
        print(order)


    # Testando modificação de ordens de compra
    buy7 = {'product': book3, 'price': book3.parameters['buy_price'], 'amount': 1}
    my_bookstore.modify_order(products_details = [buy6], client = client1, new_products_details = [buy6, buy7])
    orders = my_bookstore.get_orders()
    for order in orders:
        print(order)


    # Testando remoção de ordens de compra
    my_bookstore.remove_order(products_details = [buy1, buy2, buy3], client_name = 'Pedro', client_email = 'pedro_novo@gmail.com')
    orders = my_bookstore.get_orders()
    for order in orders:
        print(order)


if __name__ == '__main__':
    run()