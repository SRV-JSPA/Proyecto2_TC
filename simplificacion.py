from producciones_epsilon import procesar_gramatica
from producciones_unarias import unarias
from simbolos_inutiles import inutiles

procesar_gramatica('gramatica.txt', 'gramatica2.txt')
unarias('gramatica2.txt', 'gramatica3.txt')
inutiles('gramatica3.txt', 'gramatica4.txt')

def cnf(archivo_input, archivo_output):
    with open(archivo_input, 'r') as archivo:
        with open(archivo_output, 'w') as salida:
            for linea in archivo:
                salida.write(linea)
    

    with open(archivo_output, 'r') as archivo:
        lineas = archivo.readlines()


    no_terminales = set()
    producciones = {}
    terminal_a_no_terminal = {}
    producciones_simples = {}
    producciones_inversas = {}  


    for linea in lineas:
        if '->' in linea:
            izquierda, derecha = linea.split('->')
            no_terminal = izquierda.strip()
            reglas = [prod.strip() for prod in derecha.split('|')]
            producciones[no_terminal] = reglas
            no_terminales.add(no_terminal)


    terminales = set()
    for reglas in producciones.values():
        for regla in reglas:
            for simbolo in regla:
                if simbolo not in no_terminales:
                    terminales.add(simbolo)


    for no_terminal, reglas in producciones.items():
        for regla in reglas:
            if len(regla) == 1 and regla in terminales:
                terminal_a_no_terminal[regla] = no_terminal

    contador = 1
    def generar_no_terminal():
        nonlocal contador
        nuevo = f"C_{contador}"
        contador += 1
        return nuevo


    nuevas_producciones = {}
    for no_terminal, reglas in producciones.items():
        nuevas_reglas = []
        for regla in reglas:
           
            simbolos = []
            buffer = ""
            for char in regla:
                buffer += char
                if buffer in no_terminales or buffer in terminales:
                    simbolos.append(buffer)
                    buffer = ""
            if buffer:
                simbolos.append(buffer)

            
            nueva_regla = []
            for simbolo in simbolos:
                if simbolo in terminales and len(simbolos) > 1:
                    
                    if simbolo in terminal_a_no_terminal:
                        nueva_regla.append(terminal_a_no_terminal[simbolo])
                    else:
                       
                        nuevo_no_terminal = generar_no_terminal()
                        terminal_a_no_terminal[simbolo] = nuevo_no_terminal
                        nueva_regla.append(nuevo_no_terminal)
                        nuevas_producciones[nuevo_no_terminal] = [simbolo]
                else:
                    nueva_regla.append(simbolo)

            nuevas_reglas.append(' '.join(nueva_regla))
        nuevas_producciones[no_terminal] = nuevas_reglas


    producciones_finales = {}
    producciones_almacenadas = set()  
    for no_terminal, reglas in nuevas_producciones.items():
        reglas_modificadas = []
        for regla in reglas:
            simbolos = regla.split()
            while len(simbolos) > 2:
                parte = ' '.join(simbolos[:2])

                if parte in producciones_inversas:
                    nuevo_no_terminal = producciones_inversas[parte]
                else:
                    nuevo_no_terminal = generar_no_terminal()
                    producciones_inversas[parte] = nuevo_no_terminal
                    if (nuevo_no_terminal, parte) not in producciones_almacenadas:
                        producciones_finales[nuevo_no_terminal] = [parte]
                        producciones_almacenadas.add((nuevo_no_terminal, parte))

                simbolos = [nuevo_no_terminal] + simbolos[2:]

            regla_modificada = ' '.join(simbolos)
            if (no_terminal, regla_modificada) not in producciones_almacenadas:
                reglas_modificadas.append(regla_modificada)
                producciones_almacenadas.add((no_terminal, regla_modificada))
        
        producciones_finales[no_terminal] = reglas_modificadas


    for terminal, nuevo_no_terminal in terminal_a_no_terminal.items():
        if (nuevo_no_terminal, terminal) not in producciones_almacenadas:
            producciones_finales[nuevo_no_terminal] = [terminal]
            producciones_almacenadas.add((nuevo_no_terminal, terminal))


    for no_terminal, regla in producciones_simples.items():
        producciones_finales[no_terminal] = regla


    with open(archivo_output, 'w') as salida:
        for no_terminal, reglas in producciones_finales.items():
            salida.write(f"{no_terminal} -> {' | '.join(reglas)}\n")

    with open(archivo_output, 'r') as archivo:
        for linea in archivo:
            print(linea, end='')

cnf('gramatica4.txt', 'gramatica5.txt')