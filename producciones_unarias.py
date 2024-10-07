def unarias(archivo_input, archivo_output):
    with open(archivo_input) as archivo:
        base = []
        no_terminales = []
        producciones = {}

        for linea in archivo:
            linea = linea.strip()
            partes = linea.split('->')
            if len(partes) > 1:
                simbolo_izq = partes[0].strip()  
                no_terminales.append(simbolo_izq)  
                producciones[simbolo_izq] = [prod.strip() for prod in partes[1].split('|')]
                base.append((simbolo_izq, simbolo_izq))  
        
        def es_unaria(produccion):
            return produccion in no_terminales

        for pareja in base[:]:  
            simbolo_inicial, simbolo_actual = pareja
            
            while True:
                producciones_actuales = producciones.get(simbolo_actual, [])
                unaria_encontrada = False
                for prod in producciones_actuales:
                    if es_unaria(prod):  
                        nueva_pareja = (simbolo_inicial, prod)
                        if nueva_pareja not in base:
                            base.append(nueva_pareja) 
                            simbolo_actual = prod  
                            unaria_encontrada = True
                            break  
                if not unaria_encontrada:
                    break 

    resultados_finales = {}

    with open(archivo_input) as archivo:
        for pareja in base:
            simbolo_inicial, simbolo_actual = pareja
            archivo.seek(0)  
            for linea in archivo:
                linea = linea.strip()
                partes = linea.split('->')
                
                if len(partes) > 1 and partes[0].strip() == simbolo_actual:
                    producciones_actuales = [prod.strip() for prod in partes[1].split('|')]
                    
                    for prod in producciones_actuales:
                        if not es_unaria(prod):  
                            if simbolo_inicial not in resultados_finales:
                                resultados_finales[simbolo_inicial] = []
                            if prod not in resultados_finales[simbolo_inicial]:
                                resultados_finales[simbolo_inicial].append(prod)

    with open(archivo_output, 'w') as salida:
        for simbolo_inicial, producciones in resultados_finales.items():
            salida.write(f"{simbolo_inicial} -> {' | '.join(producciones)}\n")
