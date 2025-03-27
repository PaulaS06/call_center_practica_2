# import sys
# sys.path.append("src")
# from src.logic.call_center_logic_hilos import Mensaje, PriorityQueue, Agente, CallCenter

import sys
import os
import threading
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.logic.call_center_logic_hilos import Mensaje, PriorityQueue, Agente, CallCenter


def cargar_mensajes(cola_prioridad: PriorityQueue):
    ruta = os.path.join(os.path.dirname(__file__), "mensajes.txt")
    with open(ruta, "r", encoding = "utf-8") as file:
        for linea in file:
            mensaje = Mensaje(linea.strip())
            cola_prioridad.enqueue(mensaje)


def main():

    agentes = [Agente(nivel_experiencia="basico"), Agente(nivel_experiencia="experto"), Agente(nivel_experiencia="intermedio")]
    cola_prioridad = PriorityQueue()
    call_center = CallCenter(agentes, cola_prioridad)

    cargar_mensajes(cola_prioridad)
    if cola_prioridad.isEmpty():
        print("No hay mensajes para procesar, se cerrará el programa")
        return

    call_center_thread = threading.Thread(target=call_center.procesar_mensajes)
    call_center_thread.start() 

    call_center_thread.join()

    print("\n Todos los mensajes fueron procesados correctamente.")


if __name__ == "__main__":
    main()