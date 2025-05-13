from collections import deque
import random
from proceso import Proceso

class Planificador:
    def __init__(self, quantum):
        self.listos = deque()
        self.espera = deque()
        self.ejecucion = None
        self.terminados = []
        self.quantum = quantum
        self.tiempo_actual = 0
        self.pid_actual = 1
        self.cambios_contexto = 0
        self.total_procesos = 0

    def crear_proceso(self):
        nombre = f"Proceso{self.pid_actual}"
        prioridad = random.randint(1, 5)
        rafaga = random.randint(4, 10)
        paginas = [random.randint(0, 19) for _ in range(random.randint(3, 7))]
        p = Proceso(self.pid_actual, nombre, prioridad, rafaga, paginas)
        self.pid_actual += 1
        self.listos.append(p)
        self.total_procesos += 1

    def siguiente_evento(self, memoria):
        if not self.ejecucion and self.listos:
            self.ejecucion = self.listos.popleft()
            if memoria.asignar_paginas(self.ejecucion):
                self.ejecucion.estado = "En ejecución"
                self.tiempo_actual = 0
                self.cambios_contexto += 1
            else:
                self.ejecucion.estado = "En espera"
                self.espera.append(self.ejecucion)
                self.ejecucion = None

        if self.ejecucion:
            self.ejecucion.rafaga -= 1
            self.ejecucion.rafagas_ejecutadas += 1
            self.tiempo_actual += 1

            if random.random() < 0.2:
                self.ejecucion.estado = "En espera"
                self.espera.append(self.ejecucion)
                self.ejecucion = None
                self.tiempo_actual = 0
                return

            if self.ejecucion and self.ejecucion.rafaga == 0:
                self.ejecucion.estado = "Terminado"
                memoria.liberar_paginas(self.ejecucion)
                self.terminados.append(self.ejecucion)
                self.ejecucion = None
                self.tiempo_actual = 0

            elif self.ejecucion and self.tiempo_actual == self.quantum:
                self.ejecucion.estado = "Listo"
                self.listos.append(self.ejecucion)
                self.ejecucion = None
                self.tiempo_actual = 0

        for _ in range(len(self.espera)):
            p = self.espera.popleft()
            if memoria.asignar_paginas(p):
                p.estado = "Listo"
                self.listos.append(p)
            else:
                self.espera.append(p)

    def mostrar_estado(self, memoria):
        print("\n==================== SIMULADOR DE GESTOR DE PROCESOS ====================")
        print(f"Algoritmo: Round Robin | Quantum: {self.quantum}")
        print(f"Memoria total: {memoria.total() / 1024:.2f} MB | Disponible: {memoria.disponible() / 1024:.2f} MB")
        print(f"Cambios de contexto: {self.cambios_contexto} | Procesos ejecutados: {self.total_procesos}\n")

        print(">> CPU:")
        if self.ejecucion:
            print(self.ejecucion)
        else:
            print("(Ninguno)")

        memoria.mostrar()

        print("\n>> Cola de Listos:")
        if self.listos:
            for p in self.listos:
                print(p)
        else:
            print("(Vacía)")

        print("\n>> Cola de Espera:")
        if self.espera:
            for p in self.espera:
                print(p)
        else:
            print("(Vacía)")

        print("\n>> Procesos Terminados:")
        if self.terminados:
            for p in self.terminados:
                print(p)
        else:
            print("(Ninguno)")

        print("=======================================================================\n")

    def finalizar_proceso(self, pid, memoria):
        if self.ejecucion and self.ejecucion.pid == pid:
            memoria.liberar_paginas(self.ejecucion)
            self.ejecucion.estado = "Terminado"
            self.terminados.append(self.ejecucion)
            self.ejecucion = None

        self.listos = deque(p for p in self.listos if p.pid != pid)
        self.espera = deque(p for p in self.espera if p.pid != pid)

    def suspender_proceso(self, pid):
        if self.ejecucion and self.ejecucion.pid == pid:
            self.ejecucion.estado = "En espera"
            self.espera.append(self.ejecucion)
            self.ejecucion = None

        for p in list(self.listos):
            if p.pid == pid:
                p.estado = "En espera"
                self.listos.remove(p)
                self.espera.append(p)

