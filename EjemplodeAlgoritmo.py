import random
import time
from typing import List, Dict, Any


class OrdenCompra:
    """Representa una orden de compra en un sistema de inventario."""

    def __init__(self, id_orden: str, cliente: str, prioridad: int):
        self.id_orden = id_orden
        self.cliente = cliente
        self.prioridad = prioridad  # 1: Alta, 2: Media, 3: Baja

    # Permite comparar objetos OrdenCompra por su prioridad
    def __lt__(self, other: "OrdenCompra") -> bool:
        return self.prioridad < other.prioridad

    def __gt__(self, other: "OrdenCompra") -> bool:
        return self.prioridad > other.prioridad

    def __repr__(self) -> str:
        etiquetas = {1: "URGENTE", 2: "NORMAL", 3: "PROGRAMADO"}
        return f"[{self.id_orden} | {self.cliente} | Prioridad: {etiquetas[self.prioridad]}]"


class SistemaGestionEnvíos:
    """Sistema que organiza los envíos del almacén usando Quicksort de 3 Vías (Quick3)."""

    @staticmethod
    def ordenar_pedidos_quick3(pedidos: List[OrdenCompra]) -> Dict[str, Any]:
        """Ordena la lista de pedidos in-place priorizando la atención de almacén."""
        comparaciones = [0]
        intercambios = [0]

        def _quick3(low: int, high: int):
            if low >= high:
                return

            pivot = pedidos[low]
            lt = low
            i = low + 1
            gt = high

            while i <= gt:
                comparaciones[0] += 1
                if pedidos[i] < pivot:
                    pedidos[lt], pedidos[i] = pedidos[i], pedidos[lt]
                    intercambios[0] += 1
                    lt += 1
                    i += 1
                elif pedidos[i] > pivot:
                    pedidos[i], pedidos[gt] = pedidos[gt], pedidos[i]
                    intercambios[0] += 1
                    gt -= 1
                else:
                    i += 1

            # Recursión omitiendo todo el bloque central de pedidos con igual prioridad
            _quick3(low, lt - 1)
            _quick3(gt + 1, high)

        inicio = time.perf_counter()
        _quick3(0, len(pedidos) - 1)
        fin = time.perf_counter()

        return {
            "tiempo_ms": round((fin - inicio) * 1000, 2),
            "comparaciones": comparaciones[0],
            "intercambios": intercambios[0],
        }


# --- DEMOSTRACIÓN DEL CASO REAL ---
if __name__ == "__main__":
    nombres = ["Carlos", "Ana", "Beatriz", "David", "Elena", "Fernando"]

    print("=== CREANDO 50,000 ÓRDENES DE COMPRA EN EL SISTEMA ===")
    # Generamos 50,000 pedidos aleatorios con solo 3 prioridades (Pocas llaves únicas)
    lista_pedidos = [
        OrdenCompra(
            id_orden=f"ORD-{i:05d}",
            cliente=random.choice(nombres),
            prioridad=random.choice([1, 2, 3]),
        )
        for i in range(1, 50001)
    ]

    print("\nPrimeros 5 pedidos sin ordenar:")
    for p in lista_pedidos[:5]:
        print("  ", p)

    print("\nProcesando y ordenando con Quick3...")
    metricas = SistemaGestionEnvíos.ordenar_pedidos_quick3(lista_pedidos)

    print("\n=== RESULTADO DEL PROCESAMIENTO DE ALMACÉN ===")
    print(f"✓ Total de pedidos procesados: {len(lista_pedidos):,}")
    print(f"✓ Tiempo consumido: {metricas['tiempo_ms']} ms")
    print(f"✓ Comparaciones realizadas: {metricas['comparaciones']:,}")
    print(f"✓ Intercambios realizados: {metricas['intercambios']:,}")

    print("\nPrimeros 10 pedidos listos para despacho (Prioridad URGENTE primero):")
    for p in lista_pedidos[:10]:
        print("  ", p)