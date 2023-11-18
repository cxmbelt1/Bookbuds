import pandas as pd
import time

class Libro:
    def __init__(self, book_id, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count, text_reviews_count, publication_date, publisher):
        self.book_id = book_id
        self.title = title
        self.authors = authors
        self.average_rating = average_rating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language_code = language_code
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.text_reviews_count = text_reviews_count
        self.publication_date = publication_date
        self.publisher = publisher

    def __repr__(self):
        return f"'{self.title}' by {self.authors}"
    
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def insert(self, root, key):
        if not root:
            return BSTNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        return root

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def preOrder(self, root):
        if not root:
            return []
        result = [root.key]
        result.extend(self.preOrder(root.left))
        result.extend(self.preOrder(root.right))
        return result

class Storage:
    def __init__(self):
        self.bst = BST()
        self.root = None
        self.libros = []
        self.libros_por_titulo = {}

    def add(self, libro):
        self.root = self.bst.insert(self.root, libro.title)
        self.libros.append(libro)
        self.libros_por_titulo[libro.title] = libro

    def remove(self, title):
        self.root = self.bst.delete(self.root, title)
        libro_a_eliminar = self.libros_por_titulo.pop(title, None)
        if libro_a_eliminar:
            self.libros.remove(libro_a_eliminar)

    def search(self, title):
        return self._search_recursive(self.root, title)

    def _search_recursive(self, node, title):
        if node is None:
            return False
        if title == node.key:
            return True
        elif title < node.key:
            return self._search_recursive(node.left, title)
        else:
            return self._search_recursive(node.right, title)

    def imprimir_lista(self):
        for libro in self.libros:
            print(libro)

    def importar_desde_csv(self, archivo_csv):
        df = pd.read_csv(archivo_csv, on_bad_lines='skip')
        for _, row in df.iterrows():
            libro = Libro(
                book_id=row['bookID'],
                title=row['title'],
                authors=row['authors'],
                average_rating=row['average_rating'],
                isbn=row['isbn'],
                isbn13=row['isbn13'],
                language_code=row['language_code'],
                num_pages=row['  num_pages'],
                ratings_count=row['ratings_count'],
                text_reviews_count=row['text_reviews_count'],
                publication_date=row['publication_date'],
                publisher=row['publisher']
            )
            self.add(libro)


def menu():
    print("\n--- Menú ---")
    print("1. Agregar un libro")
    print("2. Eliminar un libro")
    print("3. Buscar un libro")
    print("4. Imprimir lista de libros")
    print("5. Buscar todos los libros y calcular tiempo promedio")
    print("6. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion

if __name__ == "__main__":
    lista = Storage()

    # Asegúrate de que el archivo 'books.csv' esté en la misma carpeta que este script
    archivo_csv = './books.csv'
    libros = lista.importar_desde_csv(archivo_csv)
    while True:
        opcion = menu()

        if opcion == "1":
            libro = input("Ingrese el título del libro a agregar: ")
            lista.add(libro)
            libros.append(libro)

        elif opcion == "2":
            libro = input("Ingrese el título del libro a eliminar: ")
            if libro in libros:
                lista.remove(libro)
                libros.remove(libro)

        elif opcion == "3":
            libro = input("Ingrese el título del libro a buscar: ")
            resultado = lista.search(libro)
            print(f"El libro '{libro}' está en la lista:", "Sí" if resultado else "No")

        elif opcion == "4":
            lista.imprimir_lista()

        elif opcion == "5":
            search_times = []
            start_all_time = time.time()
            for libro in libros:
                start_time = time.perf_counter()
                lista.search(libro)
                end_time = time.perf_counter()
                search_time = end_time - start_time
                search_times.append(search_time)
            end_all_time = time.time()
            all_search_time = end_all_time - start_all_time
            avg_time = sum(search_times) / len(search_times) if search_times else 0
            print(f"\nTiempo promedio de búsqueda: {avg_time:.20f} segundos")
            print(f"Tiempo total para buscar todos los libros: {all_search_time:.20f} segundos")

        elif opcion == "6":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")
