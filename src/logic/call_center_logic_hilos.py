import time
import random
import threading

class EmptyQueue(Exception):
    pass


class Mensaje:
    def __init__(self, mensaje: str):
        self.mensaje: str = mensaje
        self.prioridad: int = self.calcular_prioridad()
        self.longitud: int = self.determinar_longitud()

    def __repr__(self) -> str:
        return f"'{self.mensaje}': {self.prioridad}"

    def calcular_prioridad(self) -> int:
        prioridad = 0
        palabras_clave = {
            'emergencia': 10,
            'urgente': 8,
            'fallo crítico': 9,
            'problema': 5,
            'consulta': 2,
            'duda': 1
        }
        for palabra_clave, importancia in palabras_clave.items():

            if palabra_clave in self.mensaje.lower():
                prioridad += importancia

        return prioridad

    def determinar_longitud(self) -> int:
        return len(self.mensaje.split())


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, mensaje: Mensaje) -> None:
        self.queue.append(mensaje)
        self.queue.sort(key=lambda x: x.prioridad, reverse=True)  # Mayor prioridad primero - prioridad maxima 
        return None

    def dequeue(self) -> Mensaje:
        if self.isEmpty():
            raise EmptyQueue("Cola vacía...")
        first = self.queue[0]
        del self.queue[0]
        return first

    def first(self) -> Mensaje:
        if (len(self.queue) == 0):
            raise EmptyQueue("Cola vacía...")
        return self.queue[0]

    def isEmpty(self) -> bool:
        return len(self.queue) == 0

    def __repr__(self) -> str:
        return str(self.queue)


class Agente:
    def __init__(self, nivel_experiencia: str):
        self.id: int = self.establecer_id()
        self.nivel_experiencia: str = nivel_experiencia
        self.estado: str = "disponible"
    
    def establecer_id(self) -> int:
        return random.randint(100, 999)

    def factor_de_nivel(self):
        if self.nivel_experiencia.lower() == "basico":
            return 1

        elif self.nivel_experiencia.lower() == "intermedio":
            return 0.75

        elif self.nivel_experiencia.lower() == "experto":
            return 0.5

    def tiempo_estimado(self, mensaje: Mensaje):
        tiempo_de_respuesta = (mensaje.determinar_longitud()/2) + (mensaje.prioridad/2)
        factor_de_nivel = self.factor_de_nivel()
        return tiempo_de_respuesta * factor_de_nivel


class CallCenter():
    def __init__(self, agentes: list[Agente], cola_prioridad_mensajes: PriorityQueue):
        self.agentes: list[Agente] = agentes
        self.cola_prioridad: PriorityQueue = cola_prioridad_mensajes
        self.lock_acceso_pila_prioridad = threading.Lock()
        self.flag: bool = True

    def mirar_agente_disponible(self):
        agentes_disponibles = []
        for agente in self.agentes:
            if agente.estado == "disponible":
                agentes_disponibles.append(agente)
        if len(agentes_disponibles) > 0:
            return sorted(agentes_disponibles, key=lambda x: x.factor_de_nivel())[0]
        return None

        
    def atender_mensaje(self):
        self.lock_acceso_pila_prioridad.acquire()  # Se pide acceso
        try:
            if not self.cola_prioridad.isEmpty():
                mensaje_analizando = self.cola_prioridad.dequeue()

                agente = self.mirar_agente_disponible()
                if agente is None:
                    return "No hay agentes disponibles en este momento"
                
                agente.estado = "ocupado"
                tiempo_estimado = agente.tiempo_estimado(mensaje_analizando)
                salida = (f"📩 Mensaje atendido: '{mensaje_analizando.mensaje}' \n"
                          f"🤵 Agente #{agente.id} respondió en {tiempo_estimado} segundos\n")
            
            else:
                self.flag = False
                return f"No hay más mensajes por atender"
            
        finally:
            self.lock_acceso_pila_prioridad.release()

        time.sleep(tiempo_estimado)
        agente.estado = "disponible"
        return salida

    def procesar_mensajes(self):
        while self.flag:
            resultado = self.atender_mensaje()
            if resultado:
                print(resultado)
            time.sleep(0.1)