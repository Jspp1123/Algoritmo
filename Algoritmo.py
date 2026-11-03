import random
import time
from typing import List, TypeVar, Tuple, Dict, Any

# Definición de un tipo genérico que soporta comparación
T = TypeVar('T')

class Quick3Sorter:
    """
    Implementación profesional de Quicksort de 3 vías (Bentley-McIlroy / Quick3).
    Diseñado para ordenar eficientemente colecciones con elementos duplicados (Few Unique Keys).
    """

    def __init__(self):
        self.comparaciones = 0
        self.intercambios = 0

    def _mediana_de_tres(self, arr: List[T], low: int, high: int) -> int:
        """Selecciona el índice de la mediana entre el inicio, centro y fin."""
        mid = low + (high - low) // 2
        
        # Ordena low, mid y high para encontrar la mediana
        if arr[mid] < arr[low]:
            arr[low], arr[mid] = arr[mid], arr[low]
            self.intercambios += 1
        if arr[high] < arr[low]:
            arr[low], arr[high] = arr[high], arr[low]
            self.intercambios += 1
        if arr[high] < arr[mid]:
            arr[mid], arr[high] = arr[high], arr[mid]
            self.intercambios += 1

        self.comparaciones += 3
        # El pivote óptimo queda situado en 'mid'
        return mid

    def _particionar_3vias(self, arr: List[T], low: int, high: int) -> Tuple[int, int]:
        # Optimización: uso de mediana de 3 para el pivote
        pivot_idx = self._mediana_de_tres(arr, low, high)
        arr[low], arr[pivot_idx] = arr[pivot_idx], arr[low]
        self.intercambios += 1

        pivot = arr[low]
        lt = low
        i = low + 1
        gt = high

        while i <= gt:
            self.comparaciones += 1
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                self.intercambios += 1
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                self.intercambios += 1
                gt -= 1
            else:
                i += 1

        return lt, gt

    def _quicksort_recursivo(self, arr: List[T], low: int, high: int) -> None:
        if low >= high:
            return

        lt, gt = self._particionar_3vias(arr, low, high)

        # Recursión omitiendo la sección de duplicados centrales [lt...gt]
        self._quicksort_recursivo(arr, low, lt - 1)
        self._quicksort_recursivo(arr, gt + 1, high)

    def sort(self, arr: List[T]) -> Dict[str, Any]:
        """
        Punto de entrada principal para ordenar la lista.
        
        :param arr: Lista a ordenar (modificada in-place)
        :return: Diccionario con métricas de desempeño
        """
        if not isinstance(arr, list):
            raise TypeError("El parámetro debe ser una lista.")

        if len(arr) <= 1:
            return {"tiempo_ms": 0.0, "comparaciones": 0, "intercambios": 0}

        self.comparaciones = 0
        self.intercambios = 0
        
        inicio = time.perf_counter()
        self._quicksort_recursivo(arr, 0, len(arr) - 1)
        fin = time.perf_counter()

        return {
            "tiempo_ms": round((fin - inicio) * 1000, 4),
            "comparaciones": self.comparaciones,
            "intercambios": self.intercambios
        }


# --- Ejemplo de uso empresarial / profesional ---
if __name__ == "__main__":
    sorter = Quick3Sorter()

    # Arreglo grande con pocas llaves únicas (solo 3 categorías: 1, 2 y 3)
    datos = [random.choice([1, 2, 3]) for _ in range(10000)]
    
    print("Elementos a ordenar:", len(datos))
    metricas = sorter.sort(datos)
    
    print("\n--- Métricas de Ejecución ---")
    print(f"Tiempo de ejecución: {metricas['tiempo_ms']} ms")
    print(f"Comparaciones totales: {metricas['comparaciones']}")
    print(f"Intercambios realizados: {metricas['intercambios']}")
    print("¿Arreglo verificado como ordenado?:", datos == sorted(datos))