import pandas as pd
import time
import matplotlib.pyplot as plt

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
    return df['books'].astype(str).tolist()

def menu():
    print("\n--- Menú ---")
    print("1. Agregar un libro")
    print("2. Eliminar un libro")
    print("3. Buscar un libro")
    print("4. Imprimir lista de libros")
    print("5. Buscar todos los libros y calcular tiempo promedio")
    print("6. Salir")
    print("7. Eliminar todos los libros y calcular tiempo promedio")
    opcion = input("Seleccione una opción: ")
    return opcion

if __name__ == "__main__":
    lista = ListaLibros()
    
    # Inicio del tiempo de carga total de libros desde Excel
    total_start_time = time.time()
    
    libros = leer_libros_excel("1m.xlsx")
    
    # Listas para almacenar los tiempos de cada operación de agregar libro y los nombres de los libros
    add_times = []
    libro_names = []
    
    for libro in libros:
        # Inicio del tiempo de adición de un libro
        start_time = time.time()
        
        lista.agregar_libro(libro)
        
        # Fin del tiempo de adición de un libro
        end_time = time.time()
        
        # Cálculo del tiempo utilizado para añadir un libro
        add_time = end_time - start_time
        add_times.append(add_time)
        libro_names.append(libro)
        
        print(f"Tiempo para añadir el libro '{libro}': {add_time:.8f} segundos")
    
    # Fin del tiempo de carga total de libros desde Excel
    total_end_time = time.time()
    
    # Cálculo del tiempo total utilizado para cargar y añadir todos los libros
    total_time = total_end_time - total_start_time
    
    # Cálculo del tiempo promedio utilizado para añadir un libro
    avg_time = sum(add_times) / len(add_times) if add_times else 0
    
    print(f"\nTiempo promedio para añadir un libro: {avg_time:.8f} segundos")
    print(f"Tiempo total para cargar y añadir todos los libros: {total_time:.8f} segundos")
    
    # Gráfica de los tiempos de adición de cada libro
    plt.plot(libro_names, add_times, marker='o', linestyle='', color='b', label='Tiempo de adición')
    plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')
    plt.xlabel('Libro')
    plt.ylabel('Tiempo (s)')
    plt.title('Tiempos de Adición de Libros')
    plt.legend()
    plt.xticks([])
    plt.tight_layout()
    plt.show()


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
            search_times = []
            
            start_all_time = time.time()
            for libro in libros:
                start_time = time.time()
                lista.buscar_libro(libro)
                end_time = time.time()
                search_time = end_time - start_time
                search_times.append(search_time)
                total_time += search_time
                print(f"Tiempo para buscar '{libro}': {search_time:.8f} segundos")
            end_all_time = time.time()
            all_search_time = end_all_time - start_all_time
            
            avg_time = total_time / num_searches if num_searches > 0 else 0
            print(f"\nTiempo promedio de búsqueda: {avg_time:.8f} segundos")
            print(f"Tiempo total para buscar todos los libros: {all_search_time:.8f} segundos")
            
            plt.plot(search_times, marker='o', linestyle='', color='b', label='Tiempo de búsqueda')
            plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')
            plt.xlabel('Libro')
            plt.ylabel('Tiempo (s)')
            plt.title('Tiempos de Búsqueda de Libros')
            plt.legend()
            plt.tight_layout()
            plt.show()
        
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        
        elif opcion == "7":
            total_time = 0
            num_deletions = len(libros)
            deletion_times = []
            
            start_all_time = time.time()
            for libro in libros:
                start_time = time.time()
                lista.eliminar_libro(libro)
                end_time = time.time()
                deletion_time = end_time - start_time
                deletion_times.append(deletion_time)
                total_time += deletion_time
                print(f"Tiempo para eliminar '{libro}': {deletion_time:.8f} segundos")
            end_all_time = time.time()
            all_deletion_time = end_all_time - start_all_time
            
            avg_time = total_time / num_deletions if num_deletions > 0 else 0
            print(f"\nTiempo promedio de eliminación: {avg_time:.8f} segundos")
            print(f"Tiempo total para eliminar todos los libros: {all_deletion_time:.8f} segundos")
            
            plt.plot(deletion_times, marker='o', linestyle='', color='b', label='Tiempo de eliminación')
            plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')
            plt.xlabel('Libro')
            plt.ylabel('Tiempo (s)')
            plt.title('Tiempos de Eliminación de Libros')
            plt.legend()
            plt.tight_layout()
            plt.show()
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
