# Importamos los modulos que utilizaremos 
import numpy as np
import pandas as pd

#lista de estados
derivationList = []
lastItems = {}

# Función para obtener el estado resultante de una transición
# param state: estado inicial
# param symbol: símbolo de transición
# param transition_matrix: matriz de transiciones
def transition(state, symbol, transition_matrix):
    # print(state,symbol)
    elements = transition_matrix[(transition_matrix['state'] == state)]['symbol']
    # second = transition_matrix[]['s']
    # if symbol in list(elements[0]):
    value = transition_matrix[(transition_matrix['state'] == state) & (transition_matrix['symbol'].map(lambda x:symbol in  x))]['δ(q,s)']

    return value.values[0]

# Función recursiva para obtener el estado final despues de darle al automata una cadena de símbolos
# param state: estado inicial
# param word: cadena de símbolos
# param transition_matrix: matriz de transiciones
def getFinalState(state,word,transition_matrix):
    n = len(word)
    if n == 0:
        return state
    else:
        symbol =word[0]
        lastItems['state'] = state
        lastItems['symbol'] = symbol
        qq = transition(state,symbol,transition_matrix)
        derivationList.append(f"δ({state},{symbol}) -> {qq}")
        value = getFinalState(qq,word[1:],transition_matrix)
        return value

# funcion para obtener los movimientos realizados por el automata
def derivation():
    for item in derivationList:
        print(item)
        
# Función para obtener si el automata termino en estado de aceptación
# param state: estado final
# param acceptance_states: estados de aceptación
def accepted(state,acceptance_states):
    return state in acceptance_states


# estado, signo, δ(q,s)
# Automata que acepta numeros decimales
numeros = ["0","1","2","3","4","5","6","7","8","9"]
table = np.array([
    ["q0", ["+","-"], "q0,q1"],
    ["q0", numeros, "q1,q4"], 
    ["q0,q1", numeros, "q1,q4"], 
    ["q0,q1", ["+","-"], "q0,q1"], 
    ["q1,q4", numeros, "q1,q4"], 
    ["q1,q4", ["."], "q2,q3,q5"], 
    ["q2,q3,q5",numeros ,"q3,q5" ],
    ["q3,q5", numeros, "q3,q5"]],dtype=object)

tab = pd.DataFrame(table, columns=['state', 'symbol', 'δ(q,s)'])
# print(tab)
cadena = "2022.3.3.3"
acceptance_states = ["q2,q3,q5","q3,q5"]
try:
    estadoFinal = getFinalState("q0",cadena,tab)
    print(f"termino en estado de aceptacion: {accepted(estadoFinal,acceptance_states)}")
    print("\nδ(estado,simbolo) -> nuevo estado\n")
    derivation()
except:
    #Si falla es porque no esta definido a donde se debe mover en la matriz de transición, por lo que lo interpretamos como un error
    derivationList.append(f"δ({lastItems['state']},{lastItems['symbol']}) -> Error")
    derivationList.append(f"Error: No esta definido a donde se debe mover en la matriz de transiciones")
    derivation()

    print("Cadena no aceptada")