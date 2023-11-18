import pandas as pd
import time

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

    def add(self, key):
        self.root = self.bst.insert(self.root, key)

    def remove(self, key):
        self.root = self.bst.delete(self.root, key)

    def get_all_elements(self):
        return self.bst.preOrder(self.root)
    
    def imprimir_lista(self):
        elements = self.get_all_elements()
        for element in elements:
            print(element)
    
    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def importar_desde_csv(self, archivo_csv):
        df = pd.read_csv(archivo_csv)
        for libro in df['title']:  # Usando la columna 'title' para los nombres de los libros
            self.add(libro)
        return df['title'].tolist()  # Devuelve la lista de libros

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

    archivo_csv = 'books.csv'  # El archivo CSV
    libros = lista.importar_desde_csv(archivo_csv)

    while True:
        opcion = menu()

        if opcion == "1":
            libro = input("Ingrese el nombre del libro a agregar: ")
            lista.add(libro)
            libros.append(libro)  # Añadir a la lista de libros

        elif opcion == "2":
            libro = input("Ingrese el nombre del libro a eliminar: ")
            if libro in libros:
                lista.remove(libro)
                libros.remove(libro)  # Eliminar de la lista de libros

        elif opcion == "3":
            libro = input("Ingrese el nombre del libro a buscar: ")
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
