# import sys
# sys.path.append("src")
# from src.logic.call_center_logic_normal import Mensaje, PriorityQueue, Agente, CallCenter

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.logic.call_center_logic_normal import Mensaje, PriorityQueue, Agente, CallCenter


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

    while not cola_prioridad.isEmpty():
        mensaje, tiempo_respuesta, agente_id = call_center.atender_mensaje()
        if mensaje:
            print(f"📩 Mensaje atendido: '{mensaje.mensaje}'")
            print(f"🤵 Agente #{agente_id} respondió en {tiempo_respuesta} segundos\n")
        else:
            print("No hay mensajes por atender")
            break


if __name__ == "__main__":
    main()