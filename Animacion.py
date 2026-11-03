import pygame
import random
import sys


pygame.init()


ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación Quick3 (3-Way Partitioning) - Exposición")


BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS_CLARO = (220, 220, 220)
ROJO_PIVOTE = (231, 76, 60)      
AZUL_MENOR = (52, 152, 219)      
VERDE_IGUAL = (46, 203, 113)     
AMARILLO_MAYOR = (241, 196, 15)  
MORADO_I = (155, 89, 182)        


FUENTE = pygame.font.SysFont("Arial", 18)
FUENTE_TITULO = pygame.font.SysFont("Arial", 22, bold=True)

def generar_datos():
   
    return [random.choice([100, 250, 400]) for _ in range(40)]

def dibujar_escena(arr, low, high, lt, i, gt, pivot_val, estado_texto):
    VENTANA.fill(BLANCO)
    
   
    txt_titulo = FUENTE_TITULO.render("Algoritmo Quick3 (3-Way Partitioning) - Simulación en Vivo", True, NEGRO)
    txt_estado = FUENTE.render(f"Estado: {estado_texto}", True, NEGRO)
    VENTANA.blit(txt_titulo, (30, 20))
    VENTANA.blit(txt_estado, (30, 50))

  
    margen_izq = 50
    ancho_barra = (ANCHO - 100) / len(arr)
    
    for idx, val in enumerate(arr):
        x = margen_izq + idx * ancho_barra
        h = val 
        y = ALTO - 100 - h

        
        color = GRIS_CLARO
        if low <= idx <= high:
            if idx < lt:
                color = AZUL_MENOR     
            elif lt <= idx <= gt:
                color = VERDE_IGUAL    
            else:
                color = AMARILLO_MAYOR 

            
            if val == pivot_val and idx == low:
                color = ROJO_PIVOTE

        pygame.draw.rect(VENTANA, color, (x + 2, y, ancho_barra - 4, h))

        
        if idx == lt:
            txt_lt = FUENTE.render("lt", True, AZUL_MENOR)
            VENTANA.blit(txt_lt, (x, ALTO - 80))
        if idx == i:
            txt_i = FUENTE.render("i", True, MORADO_I)
            VENTANA.blit(txt_i, (x, ALTO - 60))
        if idx == gt:
            txt_gt = FUENTE.render("gt", True, AMARILLO_MAYOR)
            VENTANA.blit(txt_gt, (x, ALTO - 40))

    
    leyendas = [
        ("Menores (<)", AZUL_MENOR),
        ("Iguales (==)", VERDE_IGUAL),
        ("Mayores (>)", AMARILLO_MAYOR),
        ("Pivote", ROJO_PIVOTE),
        ("Escáner (i)", MORADO_I)
    ]
    
    x_leyenda = 30
    for texto, col in leyendas:
        pygame.draw.rect(VENTANA, col, (x_leyenda, ALTO - 25, 15, 15))
        txt = FUENTE.render(texto, True, NEGRO)
        VENTANA.blit(txt, (x_leyenda + 20, ALTO - 27))
        x_leyenda += 140

    pygame.display.flip()

def quicksort_3way_animado(arr, low, high):
    if low >= high:
        return

    pivot = arr[low]
    lt = low
    i = low + 1
    gt = high

    
    def procesar_eventos():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    while i <= gt:
        procesar_eventos()
        pygame.time.delay(100) 

        dibujar_escena(arr, low, high, lt, i, gt, pivot, f"Comparando elemento con pivote ({pivot})")

        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    dibujar_escena(arr, low, high, lt, i, gt, pivot, "Partición completada. Congelando bloque central.")
    pygame.time.delay(300)

    
    quicksort_3way_animado(arr, low, lt - 1)
    quicksort_3way_animado(arr, gt + 1, high)

def main():
    arr = generar_datos()
    
    
    while True:
        VENTANA.fill(BLANCO)
        txt = FUENTE_TITULO.render("Presiona ESPACIO para iniciar la simulación Quick3", True, NEGRO)
        VENTANA.blit(txt, (ANCHO // 2 - 220, ALTO // 2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                
                quicksort_3way_animado(arr, 0, len(arr) - 1)
                
                
                while True:
                    VENTANA.fill(BLANCO)
                    txt_fin = FUENTE_TITULO.render("¡Arreglo Ordenado con Éxito! (Presiona ESC para salir)", True, VERDE_IGUAL)
                    VENTANA.blit(txt_fin, (ANCHO // 2 - 250, ALTO // 2))
                    pygame.display.flip()
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    main()