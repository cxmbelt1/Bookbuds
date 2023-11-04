import random
import string
import time
import numpy as np
import matplotlib.pyplot as plt

class HashNode:
    def __init__(self, key):
        self.key = key
        self.next = None

class HashTable:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash(self, key):
        hashsum = 0
        for idx, c in enumerate(key):
            hashsum += (idx + len(key)) ** ord(c)
            hashsum = hashsum % self.capacity
        return hashsum

    def insert(self, key):
        self.size += 1
        index = self.hash(key)
        node = self.buckets[index]
        if node is None:
            self.buckets[index] = HashNode(key)
            return
        prev = node
        while node is not None:
            prev = node
            node = node.next
        prev.next = HashNode(key)

    def delete(self, key):
        index = self.hash(key)
        node = self.buckets[index]
        prev = None
        while node is not None and node.key != key:
            prev = node
            node = node.next
        if node is None:
            return None
        else:
            self.size -= 1
            result = node
            if prev is None:
                self.buckets[index] = node.next
            else:
                prev.next = prev.next.next
            return result

    def search(self, key):
        index = self.hash(key)
        node = self.buckets[index]
        while node is not None and node.key != key:
            node = node.next
        return node is not None

    def get_all_elements(self):
        elements = []
        for item in self.buckets:
            while item is not None:
                elements.append(item.key)
                item = item.next
        return elements



class Storage:
    def __init__(self):
        self.hash_table = HashTable()

    def add(self, key):
        self.hash_table.insert(key)

    def remove(self, key):
        self.hash_table.delete(key)

    def search(self, key):
        return self.hash_table.search(key)

    def get_all_elements(self):
        return self.hash_table.get_all_elements()

    def imprimir_lista(self):
        elements = self.get_all_elements()
        for element in elements:
            print(element)


def generar_libros_aleatorios(num_libros, longitud_nombre):
    libros = []
    for _ in range(num_libros):
        nombre_libro = ''.join(random.choices(string.ascii_letters + string.digits, k=longitud_nombre))
        libros.append(nombre_libro)
    return libros

def menu():
    print("\n--- Menú ---")
    print("1. Agregar un libro")
    print("2. Eliminar un libro")
    print("3. Buscar un libro")
    print("4. Imprimir lista de libros")
    print("5. Buscar todos los libros y calcular tiempo promedio")
    print("6. Salir")
    print("7. Eliminar todos los libros y calcular tiempo promedio")
    print("8. Eliminar libros aleatorios y calcular tiempo promedio")
    print("9. Buscar libros aleatorios y calcular tiempo promedio")
    opcion = input("Seleccione una opción: ")
    return opcion


if __name__ == "__main__":
    lista = Storage()  
    
    libros = generar_libros_aleatorios(10000, 10)
    
    add_times = []
    libro_names = []
    
    total_start_time = time.time()
    
    for libro in libros:
        start_time = time.perf_counter()  
        lista.add(libro)  
        end_time = time.perf_counter()  
        add_time = end_time - start_time  
        add_times.append(add_time)  
        libro_names.append(libro)  
        
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    avg_time = sum(add_times) / len(add_times) if add_times else 0
    
    print(f"\nTiempo promedio para añadir un libro: {avg_time:.20f} segundos")
    print(f"Tiempo total para cargar y añadir todos los libros: {total_time:.20f} segundos")
    
   

    
    plt.figure(figsize=(12, 6))

    # Gráfica de los tiempos de adición
    plt.plot(libro_names, add_times, marker='o', linestyle='', color='c', label='Tiempo de adición')
    plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')

    # Calcular y graficar la línea de tendencia
    x = np.arange(len(libro_names))  
    y = np.array(add_times)  
    m, b = np.polyfit(x, y, 1)  # Calcular la pendiente 
    plt.plot(x, m*x + b, color='g', label='Línea de tendencia')  

    plt.xlabel('Libro')
    plt.ylabel('Tiempo (s)')
    plt.title('Tiempos de Adición de Libros')
    plt.legend()
    plt.xticks([])  
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()

    while True:
        opcion = menu()
        
        if opcion == "1":
            libro = input("Ingrese el nombre del libro a agregar: ")
            lista.add(libro)
        
        elif opcion == "2":
            libro = input("Ingrese el nombre del libro a eliminar: ")
            lista.remove(libro)
        
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



            
            plt.plot(libro_names, search_times, marker='o', linestyle='', color='c', label='Tiempo de búsqueda')
            plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')
            x = np.arange(len(libro_names))  
            y = np.array(search_times)  
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente 
            plt.plot(x, m*x + b, color='g', label='Línea de tendencia') 
            plt.xlabel('Libro')
            plt.ylabel('Tiempo (s)')
            plt.title('Tiempos de Búsqueda de Libros')
            plt.legend()
            plt.xticks([])
            plt.tight_layout()
            plt.grid(axis='y')
            plt.show()
        
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        
        elif opcion == "7":
            deletion_times = []
            
            start_all_time = time.time()
            for libro in libros:
                start_time = time.perf_counter()
                lista.remove(libro)
                end_time = time.perf_counter()
                deletion_time = end_time - start_time
                deletion_times.append(deletion_time)
                
            end_all_time = time.time()
            all_deletion_time = end_all_time - start_all_time
            
            avg_time = sum(deletion_times) / len(deletion_times) if deletion_times else 0
            print(f"\nTiempo promedio de eliminación: {avg_time:.20f} segundos")
            print(f"Tiempo total para eliminar todos los libros: {all_deletion_time:.20f} segundos")
            
            
            
            plt.plot(libro_names, deletion_times, marker='o', linestyle='', color='c', label='Tiempo de eliminación')
            plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')
            x = np.arange(len(libro_names))  
            y = np.array(deletion_times)  
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente
            plt.plot(x, m*x + b, color='g', label='Línea de tendencia')
            plt.xlabel('Libro')
            plt.ylabel('Tiempo (s)')
            plt.title('Tiempos de Eliminación de Libros')
            plt.legend()
            plt.xticks([])
            plt.tight_layout()
            plt.grid(axis='y')
            plt.show()

        elif opcion == "8":
            deletion_times = []
            
            start_all_time = time.time()
            for _ in range(len(libros)):
                libro = random.choice(libros)  # Selecciona un libro aleatorio
                libros.remove(libro)  # Elimina el libro de la lista de libros
                
                start_time = time.perf_counter()
                lista.remove(libro)  # Elimina el libro de la lista enlazada
                end_time = time.perf_counter()
                
                deletion_time = end_time - start_time
                deletion_times.append(deletion_time)
                
            end_all_time = time.time()
            all_deletion_time = end_all_time - start_all_time
            
            avg_time = sum(deletion_times) / len(deletion_times) if deletion_times else 0
            print(f"\nTiempo promedio de eliminación: {avg_time:.20f} segundos")
            print(f"Tiempo total para eliminar todos los libros: {all_deletion_time:.20f} segundos")
            
            plt.plot(deletion_times, marker='o', linestyle='', color='c', label='Tiempo de eliminación')
            x = np.arange(len(deletion_times))  
            y = np.array(deletion_times)  
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente 
            plt.plot(x, m*x + b, color='g', label='Línea de tendencia')
            plt.xlabel('Libro')
            plt.ylabel('Tiempo (s)')
            plt.title('Tiempos de Eliminación de Libros Aleatorios')
            plt.legend()
            plt.xticks([])
            plt.tight_layout()
            plt.grid(axis='y')
            plt.show()

        elif opcion == "9":
            search_times = []
            
            start_all_time = time.time()
            for _ in range(len(libros)):
                libro = random.choice(libros)  # Selecciona un libro aleatorio
                
                start_time = time.perf_counter()
                lista.search(libro)  # Busca el libro en la lista enlazada
                end_time = time.perf_counter()
                
                search_time = end_time - start_time
                search_times.append(search_time)
                
            end_all_time = time.time()
            all_search_time = end_all_time - start_all_time
            
            avg_time = sum(search_times) / len(search_times) if search_times else 0
            print(f"\nTiempo promedio de búsqueda: {avg_time:.20f} segundos")
            print(f"Tiempo total para buscar todos los libros: {all_search_time:.20f} segundos")
            
            plt.plot(search_times, marker='o', linestyle='', color='b', label='Tiempo de búsqueda')
            x = np.arange(len(search_times))  
            y = np.array(search_times)  
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente 
            plt.plot(x, m*x + b, color='g', label='Línea de tendencia')
            plt.xlabel('Libro')
            plt.ylabel('Tiempo (s)')
            plt.title('Tiempos de Búsqueda de Libros Aleatorios')
            plt.legend()
            plt.xticks([])
            plt.tight_layout()
            plt.grid(axis='y')
            plt.show()


        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")