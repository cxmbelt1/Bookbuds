import random
import string
import time
import numpy as np
import matplotlib.pyplot as plt

class ArrayListLibros:
    def __init__(self):
        self.libros = []

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def eliminar_libro(self, libro):
        if libro in self.libros:
            self.libros.remove(libro)

    def buscar_libro(self, libro):
        return libro in self.libros

    def imprimir_lista(self):
        print(" ".join(self.libros))

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
    lista = ArrayListLibros()  # Cambiado a la nueva implementación
    
    libros = generar_libros_aleatorios(1000000, 10)
    
    add_times = []
    libro_names = []
    
    total_start_time = time.time()
    
    for libro in libros:
        start_time = time.perf_counter()  
        lista.agregar_libro(libro)  
        end_time = time.perf_counter()  
        add_time = end_time - start_time  
        add_times.append(add_time)  
        libro_names.append(libro)  
        
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    avg_time = sum(add_times) / len(add_times) if add_times else 0
    
    print(f"\nTiempo promedio para añadir un libro: {avg_time:.20f} segundos")
    print(f"Tiempo total para cargar y añadir todos los libros: {total_time:.20f} segundos")
    
    # [El resto del código para graficar y manejar el menú se mantiene igual]

    
    plt.figure(figsize=(12, 6))

    # Gráfica de los tiempos de adición
    plt.plot(libro_names, add_times, marker='o', linestyle='', color='c', label='Tiempo de adición')
    plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')

    # Calcular y graficar la línea de tendencia
    x = np.arange(len(libro_names))  # Crear un array con el número de libros
    y = np.array(add_times)  # Convertir los tiempos de adición a un array numpy
    m, b = np.polyfit(x, y, 1)  # Calcular la pendiente y la intersección y de la línea de tendencia
    plt.plot(x, m*x + b, color='g', label='Línea de tendencia')  # Añadir la línea de tendencia a la gráfica

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
            search_times = []
            
            start_all_time = time.time()
            for libro in libros:
                start_time = time.perf_counter()
                lista.buscar_libro(libro)
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
            x = np.arange(len(libro_names))  # Crear un array con el número de libros
            y = np.array(search_times)  # Convertir los tiempos de búsqueda a un array numpy
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente y la intersección y de la línea de tendencia
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
                lista.eliminar_libro(libro)
                end_time = time.perf_counter()
                deletion_time = end_time - start_time
                deletion_times.append(deletion_time)
                
            end_all_time = time.time()
            all_deletion_time = end_all_time - start_all_time
            
            avg_time = sum(deletion_times) / len(deletion_times) if deletion_times else 0
            print(f"\nTiempo promedio de eliminación: {avg_time:.20f} segundos")
            print(f"Tiempo total para eliminar todos los libros: {all_deletion_time:.20f} segundos")
            
            
            
            plt.plot(libro_names, deletion_times, marker='o', linestyle='', color='b', label='Tiempo de eliminación')
            plt.axhline(y=avg_time, color='r', linestyle='--', label='Tiempo promedio')
            x = np.arange(len(libro_names))  # Crear un array con el número de libros
            y = np.array(deletion_times)  # Convertir los tiempos de eliminación a un array numpy
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente y la intersección y de la línea de tendencia
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
                lista.eliminar_libro(libro)  # Elimina el libro de la lista enlazada
                end_time = time.perf_counter()
                
                deletion_time = end_time - start_time
                deletion_times.append(deletion_time)
                
            end_all_time = time.time()
            all_deletion_time = end_all_time - start_all_time
            
            avg_time = sum(deletion_times) / len(deletion_times) if deletion_times else 0
            print(f"\nTiempo promedio de eliminación: {avg_time:.20f} segundos")
            print(f"Tiempo total para eliminar todos los libros: {all_deletion_time:.20f} segundos")
            
            plt.plot(deletion_times, marker='o', linestyle='', color='b', label='Tiempo de eliminación')
            x = np.arange(len(deletion_times))  # Crear un array con el número de libros
            y = np.array(deletion_times)  # Convertir los tiempos de eliminación a un array numpy
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente y la intersección y de la línea de tendencia
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
                lista.buscar_libro(libro)  # Busca el libro en la lista enlazada
                end_time = time.perf_counter()
                
                search_time = end_time - start_time
                search_times.append(search_time)
                
            end_all_time = time.time()
            all_search_time = end_all_time - start_all_time
            
            avg_time = sum(search_times) / len(search_times) if search_times else 0
            print(f"\nTiempo promedio de búsqueda: {avg_time:.20f} segundos")
            print(f"Tiempo total para buscar todos los libros: {all_search_time:.20f} segundos")
            
            plt.plot(search_times, marker='o', linestyle='', color='b', label='Tiempo de búsqueda')
            x = np.arange(len(search_times))  # Crear un array con el número de libros
            y = np.array(search_times)  # Convertir los tiempos de búsqueda a un array numpy
            m, b = np.polyfit(x, y, 1)  # Calcular la pendiente y la intersección y de la línea de tendencia
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