class Proceso:
    def __init__(self, pid, nombre, prioridad, rafaga, paginas):
        self.pid = pid
        self.nombre = nombre
        self.prioridad = prioridad
        self.rafaga = rafaga
        self.paginas = paginas
        self.estado = "Listo"
        self.rafagas_ejecutadas = 0
        self.semaforo = "Disponible"

    def __str__(self):
        return (f"PID:{self.pid} | {self.nombre} | Ráfaga:{self.rafaga} | "
                f"Prioridad:{self.prioridad} | Páginas:{self.paginas} | "
                f"Estado:{self.estado} | Ráfagas Ejecutadas:{self.rafagas_ejecutadas} | "
                f"Semáforo:{self.semaforo}")
