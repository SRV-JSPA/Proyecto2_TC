from producciones_epsilon import procesar_gramatica
from producciones_unarias import unarias
from simbolos_inutiles import inutiles

procesar_gramatica('gramatica.txt', 'gramatica2.txt')
unarias('gramatica2.txt', 'gramatica3.txt')
inutiles('gramatica3.txt', 'gramatica4.txt')
