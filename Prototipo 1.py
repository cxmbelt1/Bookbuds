import pandas as pd
import time

class Nodo:
    def __init__(self, libro):
        self.libro = libro
        self.siguiente = None
        self.anterior = None

class ListaLibros:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar_libro(self, libro):
        nuevo_nodo = Nodo(libro)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def eliminar_libro(self, libro):
        actual = self.cabeza
        while actual:
            if actual.libro == libro:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                del actual
                return
            actual = actual.siguiente

    def buscar_libro(self, libro):
        actual = self.cabeza
        while actual:
            if actual.libro == libro:
                return True
            actual = actual.siguiente
        return False

    def imprimir_lista(self):
        actual = self.cabeza
        while actual:
            print(actual.libro, end=" ")
            actual = actual.siguiente
        print()

def leer_libros_excel(archivo):
    df = pd.read_excel(archivo)
    return df['books'].tolist()

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
    lista = ListaLibros()
    libros = leer_libros_excel("1m.xlsx")
    for libro in libros:
        lista.agregar_libro(libro)

    while True:
        opcion = menu()
        
        if opcion == "1":
            libro = input("Ingrese el nombre del libro a agregar: ")
            lista.agregar_libro(libro)
        
        elif opcion == "2":
            libro = input("Ingrese el nombre del libro a eliminar: ")
            lista.eliminar_libro(libro)
        
        elif opcion == "3":
            libro = input("Ingrese el nombre del libro a buscar: ")
            resultado = lista.buscar_libro(libro)
            print(f"El libro '{libro}' está en la lista:", "Sí" if resultado else "No")
        
        elif opcion == "4":
            lista.imprimir_lista()
        
        elif opcion == "5":
            total_time = 0
            num_searches = len(libros)
            
            for libro in libros:
                start_time = time.time()
                lista.buscar_libro(libro)
                end_time = time.time()
                search_time = end_time - start_time
                total_time += search_time
                print(f"Tiempo para buscar '{libro}': {search_time:.5f} segundos")
            
            avg_time = total_time / num_searches if num_searches > 0 else 0
            print(f"\nTiempo promedio de búsqueda: {avg_time:.5f} segundos")
        
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
