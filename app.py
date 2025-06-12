from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

# permisos para consultas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funcion que simula apd
def simula_apd(transiciones, aceptarPorFinal, estadoInicial, estadoFinal, palabra):
    estado = estadoInicial
    palabra = palabra.strip()
    stack = ["R"]
    i = 0

    while i <= len(palabra):
        if i < len(palabra):
            simbolo = palabra[i]
        else:
            simbolo = 'ε'
        simbolo_en_stack = stack[-1]

        transicion = (estado, simbolo, simbolo_en_stack)

        if transicion in transiciones:
            nuevo_estado, escribir_en_stack = transiciones[transicion]
            estado = nuevo_estado
            if escribir_en_stack == 'ε' and len(stack)!=1:
                stack.pop()
            elif len(escribir_en_stack)==1:
                pass
            else:
                escribir_en_stack = escribir_en_stack[:-1]
                for simbolo_transicion in reversed(escribir_en_stack):
                    stack.append(simbolo_transicion)

            if simbolo != 'ε' or (simbolo == 'ε' and simbolo_en_stack == 'R'):
                i += 1

        else:
            return False
    if aceptarPorFinal:
        return estado == estadoFinal
    else:
        return stack == ['R']
# Modelos Pydantic para validar entrada
class SimulationRequest(BaseModel):
    transitions: List[dict]  # cada dict tiene from y to (listas)
    initial_state: str
    acceptance_type: str
    final_state: Optional[str] = None
    input_word: str

@app.post("/simulate")
async def simulate(data: SimulationRequest):
    # Convertir lista de transiciones (dicts) a dict de tuplas
    # Ejemplo entrada de transicion: {"from": ["q0", "a", "R"], "to": ["q1", "AR"]}
    transiciones = {}
    for t in data.transitions:
        from_tuple = tuple(t["from"])
        to_tuple = tuple(t["to"])
        transiciones[from_tuple] = to_tuple

    aceptarPorFinal = (data.acceptance_type == "estado")
    estadoInicial = data.initial_state
    estadoFinal = data.final_state if data.final_state else ""
    palabra = data.input_word

    aceptada = simula_apd(transiciones, aceptarPorFinal, estadoInicial, estadoFinal, palabra)

    return {"accepted": aceptada}

# monta archivos estaticos (frontend)
app.mount("/", StaticFiles(directory=os.path.dirname(__file__), html=True), name="static")
