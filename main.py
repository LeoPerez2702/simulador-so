import time
from planificador import Planificador
from memoria import Memoria

def menu_administrativo(planificador, memoria):
    while True:
        print("\n=========== MENÚ ADMINISTRATIVO ===========")
        planificador.mostrar_estado(memoria)
        print("Opciones:")
        print("1. Finalizar proceso por PID")
        print("2. Suspender proceso por PID")
        print("3. Reanudar simulación")
        print("===========================================\n")

        opcion = input("Selecciona opción: ")
        if opcion == '1':
            try:
                pid = int(input("PID a finalizar: "))
                planificador.finalizar_proceso(pid, memoria)
            except ValueError:
                print("PID inválido.")
        elif opcion == '2':
            try:
                pid = int(input("PID a suspender: "))
                planificador.suspender_proceso(pid)
            except ValueError:
                print("PID inválido.")
        elif opcion == '3':
            print("Reanudando simulación...\n")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    planificador = Planificador(quantum=3)
    memoria = Memoria(marcos=20)

    for _ in range(5):
        planificador.crear_proceso()

    ciclo_actual = 0
    ciclos_para_menu = 20  # Cada 20 ciclos se pausa y muestra el menú

    try:
        while True:
            planificador.siguiente_evento(memoria)
            planificador.mostrar_estado(memoria)
            time.sleep(1)
            ciclo_actual += 1

            if ciclo_actual >= ciclos_para_menu:
                ciclo_actual = 0
                menu_administrativo(planificador, memoria)

    except KeyboardInterrupt:
        print("\nSimulación finalizada por el usuario.")

