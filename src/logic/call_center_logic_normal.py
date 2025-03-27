import time
import random

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

    # def mirar_agente_disponible(self):
    #     agentes_disponibles = []
    #     for agente in self.agentes:
    #         if agente.estado == "disponible":
    #             agentes_disponibles.append(agente)
    #     if len(agentes_disponibles) > 0:
    #         return sorted(agentes_disponibles, key=lambda x: x.factor_de_nivel())[0]
    #     else: 
    #         return None

    def mirar_agente_disponible(self):
        agentes_disponibles = []
        for agente in self.agentes:
            if agente.estado == "disponible":
                agentes_disponibles.append(agente)
        if len(agentes_disponibles) > 0:
            return random.choice(agentes_disponibles)
        else:
            return None

    def atender_mensaje(self):
        agente = self.mirar_agente_disponible()
        if agente and not self.cola_prioridad.isEmpty():
            mensaje = self.cola_prioridad.dequeue()
            agente.estado = "ocupado"
            tiempo_respuesta = agente.tiempo_estimado(mensaje)
            time.sleep(tiempo_respuesta)
            agente.estado = "disponible"
            return mensaje, tiempo_respuesta, agente.id
        else:
            return None