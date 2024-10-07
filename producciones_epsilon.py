from itertools import product

def procesar_produccion(produccion, simbolos_anulables):
    print(f'Procesando producción: {produccion}')
    produccion_lista = list(produccion)
    
    indices_anulables = [(i, simbolo) for i, simbolo in enumerate(produccion_lista) if simbolo in simbolos_anulables]
    print(f'Índices de símbolos anulables encontrados: {indices_anulables}')
    
    if not indices_anulables:
        print(f'No se encontraron símbolos anulables en la producción: {produccion}')
        return [produccion]
    
    combinaciones = list(product([True, False], repeat=len(indices_anulables)))
    print(f'Combinaciones de presencia/ausencia: {combinaciones}')
    
    nuevas_producciones = set()  
    
    for combinacion in combinaciones:
        nueva_produccion = produccion_lista.copy()  
        print(f'Procesando combinación: {combinacion}')
        
        for (i, simbolo), presente in zip(indices_anulables, combinacion):
            if not presente:
                nueva_produccion[i] = ''  
        
        nueva_produccion_str = ''.join(nueva_produccion).replace('ε', '')
        print(f'Producción resultante: {nueva_produccion_str}')
        
        if nueva_produccion_str:
            nuevas_producciones.add(nueva_produccion_str)
    
    print(f'Producciones nuevas generadas: {nuevas_producciones}')
    return list(nuevas_producciones)

def procesar_linea(linea, simbolos_anulables):
    print(f'Procesando línea: {linea}')
    if '->' in linea:
        partes = linea.split('->')
        lado_izquierdo = partes[0].strip()  
        lado_derecho = partes[1].strip()  
        
        print(f'Lado izquierdo: {lado_izquierdo}')
        print(f'Lado derecho: {lado_derecho}')
        
        producciones = lado_derecho.split('|')
        nuevas_producciones = set()  
        
        for produccion in producciones:
            print(f'Procesando producción: {produccion}')
            nuevas_producciones.update(procesar_produccion(produccion, simbolos_anulables))

        if nuevas_producciones:
            linea_modificada = f'{lado_izquierdo} -> {"|".join(nuevas_producciones)}'
            print(f'Línea modificada: {linea_modificada}')
            return linea_modificada
        else:
            print(f'No se generaron nuevas producciones para la línea: {linea}')
            return None  
    else:
        print(f'La línea no contiene producción: {linea}')
        return linea  

def procesar_gramatica(input_file, output_file):
    print(f'Procesando gramática desde el archivo: {input_file}')
    
    simbolos_anulables_originales = []  
    simbolos_anulables = set()
    lineas_anulables = []

    with open(input_file, 'r') as archivo:
        lineas = archivo.readlines()  

    print('Primera pasada para identificar símbolos anulables:')
    for linea in lineas:
        linea = linea.strip()  
        if linea:  
            
            if 'ε' in linea:  
                print(f'La línea "{linea}" tiene producción epsilon')
                lineas_anulables.append(linea)  

                partes = linea.split('->')
                if len(partes) == 2:
                    simbolo = partes[0].strip()  
                    simbolos_anulables_originales.append(simbolo)
                    simbolos_anulables.add(simbolo)
                    print(f'Símbolo anulable encontrado: {simbolo}')
                        
                indices = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

                m = len(simbolos_anulables_originales)
                num_formas = 2**m

                m_indice = str(m).translate(indices)

                print(f'm = {m} => ∃ 2ᵐ - 2{m_indice} = {num_formas} formas para elegir presente o ausente para los símbolos anulables')

    cambios = True
    while cambios:
        cambios = False
        for linea in lineas:
            if '->' in linea:
                partes = linea.split('->')
                lado_izquierdo = partes[0].strip()  
                lado_derecho = partes[1].strip()  
                
                producciones = lado_derecho.split('|')
                
                if any(any(simbolo in simbolos_anulables_originales for simbolo in produccion) for produccion in producciones):
                    if lado_izquierdo not in simbolos_anulables:
                        simbolos_anulables.add(lado_izquierdo)
                        cambios = True
                        print(f'Nuevo símbolo anulable encontrado y agregado: {lado_izquierdo}')

    print(f'Símbolos anulables finales: {simbolos_anulables}')

    print('Procesando líneas para generar gramática final:')
    lineas_modificadas = []
    for linea in lineas:
        linea_original = linea.strip()
        if 'ε' in linea:
            if '|ε' in linea:
                linea = linea.replace('|ε', '')
                print(f'Eliminando producción epsilon: "{linea_original}"')
            else:
                partes = linea.split('->')
                if len(partes) == 2:
                    produccion = partes[1].strip()
                    if produccion == 'ε':
                        print(f'Eliminando la línea completa: "{linea_original}"')
                        continue
                    else:
                        linea = linea.replace('ε', '')
                        print(f'Reemplazando epsilon en producción: "{linea}"')

        linea_modificada = procesar_linea(linea, simbolos_anulables)
        if linea_modificada:
            lineas_modificadas.append(linea_modificada)
            print(f'Línea modificada: "{linea_modificada}"')
        else:
            print(f'La línea "{linea}" ha sido eliminada por estar vacía')

    with open(output_file, 'w') as archivo_salida:
        for linea in lineas_modificadas:
            archivo_salida.write(linea + '\n')
            print(f'Escribiendo línea en archivo de salida: {linea}')


