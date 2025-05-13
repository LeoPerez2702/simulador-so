class Memoria:
    def __init__(self, marcos):
        self.marcos = marcos
        self.ocupados = {}
        self.tamano_marco = 8  # KB

    def asignar_paginas(self, proceso):
        if len(self.ocupados) + len(proceso.paginas) <= self.marcos:
            for p in proceso.paginas:
                self.ocupados[p] = proceso.pid
            return True
        else:
            return False

    def liberar_paginas(self, proceso):
        for p in list(self.ocupados):
            if self.ocupados[p] == proceso.pid:
                del self.ocupados[p]

    def mostrar(self):
        if self.ocupados:
            print(">> Memoria en uso (por PID):")
            por_pid = {}
            for pagina, pid in self.ocupados.items():
                por_pid.setdefault(pid, []).append(pagina)
            for pid, paginas in por_pid.items():
                print(f"PID {pid} -> Páginas: {paginas} ({len(paginas)*self.tamano_marco/1024:.2f} MB)")
        else:
            print(">> Memoria vacía.")

    def disponible(self):
        return (self.marcos - len(self.ocupados)) * self.tamano_marco  # en KB

    def total(self):
        return self.marcos * self.tamano_marco  # en KB
