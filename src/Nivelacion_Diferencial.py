class NivelacionGeodesica:
    def __init__(self):
        self.estaciones = []  # Lista para almacenar las estaciones, cotas y alturas instrumentales
        self.vistas_intermedias = []  # Lista para almacenar vistas intermedias

    def agregar_punto_inicial(self):
        # Solicitar el primer punto y la cota inicial
        estacion = input("Ingrese el nombre del punto inicial (Ej: BM1): ")
        cota = float(input(f"Ingrese la cota para {estacion} (con decimales): "))
        vista_mas = float(input(f"Ingrese la vista más para {estacion} (con decimales): "))
        cota_instrumental = cota + vista_mas
        self.estaciones.append({'estacion': estacion, 'cota': cota, 'vista_mas': vista_mas, 'vista_menos': None,
                                'cota_instrumental': cota_instrumental})
        print(f"Estación {estacion} registrada con cota = {cota:.6f} y altura instrumental = {cota_instrumental:.6f}.")

    def registrar_vista_intermedia(self, cota_instrumental):
        # Registrar vistas intermedias
        estacion_intermedia = input("Ingrese el nombre de la vista intermedia: ")
        vista_menos = float(input(f"Ingrese la vista menos para {estacion_intermedia} (con decimales): "))
        cota_intermedia = cota_instrumental - vista_menos
        self.vistas_intermedias.append(
            {'estacion': estacion_intermedia, 'vista_menos': vista_menos, 'cota': cota_intermedia})
        print(f"Vista intermedia {estacion_intermedia} registrada con cota = {cota_intermedia:.6f}.")

    def registrar_punto(self, estacion_origen):
        # Registrar una nueva estación
        estacion_destino = input(f"¿A qué estación se mira desde {estacion_origen}? ")
        vista_menos = float(input(f"Ingrese la vista menos para {estacion_destino} (con decimales): "))
        cota_instrumental = self.estaciones[-1]['cota_instrumental']
        cota = cota_instrumental - vista_menos
        vista_mas = float(input(f"Ingrese la vista más para {estacion_destino} (con decimales): "))
        nueva_cota_instrumental = cota + vista_mas
        self.estaciones.append(
            {'estacion': estacion_destino, 'cota': cota, 'vista_mas': vista_mas, 'vista_menos': vista_menos,
             'cota_instrumental': nueva_cota_instrumental})
        print(
            f"Estación {estacion_destino} registrada con cota = {cota:.6f} y altura instrumental = {nueva_cota_instrumental:.6f}.")

    def registrar_ultimo_punto(self):
        # Registrar el último punto (solo vista menos)
        estacion_destino = input("Ingrese el nombre del último punto: ")
        vista_menos = float(input(f"Ingrese la vista menos para {estacion_destino} (con decimales): "))
        cota_instrumental = self.estaciones[-1]['cota_instrumental']
        cota = cota_instrumental - vista_menos
        self.estaciones.append(
            {'estacion': estacion_destino, 'cota': cota, 'vista_mas': None, 'vista_menos': vista_menos,
             'cota_instrumental': None})
        print(f"Última estación {estacion_destino} registrada con cota = {cota:.6f}.")

    def calcular(self):
        # Ingresar el punto inicial
        self.agregar_punto_inicial()

        # Bucle para solicitar vistas y puntos adicionales
        while True:
            continuar = input(
                "\n¿Qué sigue? (1: Registrar nueva vista/punto, 2: Registrar vista intermedia, 3: Registrar último punto, 4: Finalizar): ")

            if continuar == '1':
                # Registrar un nuevo punto (vista más y vista menos)
                estacion_origen = self.estaciones[-1]['estacion']
                self.registrar_punto(estacion_origen)

            elif continuar == '2':
                # Registrar una vista intermedia
                cota_instrumental = self.estaciones[-1]['cota_instrumental']
                self.registrar_vista_intermedia(cota_instrumental)

            elif continuar == '3':
                # Registrar el último punto (solo vista menos)
                self.registrar_ultimo_punto()
                break

            elif continuar == '4':
                print("Cálculo finalizado.")
                break

            else:
                print("Opción inválida, intente nuevamente.")

        # Mostrar los resultados
        self.mostrar_resultados()

    def mostrar_resultados(self):
        # Mostrar todas las cotas y alturas instrumentales calculadas
        print("\n--- Resultados ---")
        for estacion in self.estaciones:
            estacion_str = f"Estación {estacion['estacion']}:"
            if estacion['cota_instrumental'] is not None:
                estacion_str += f" Altura instrumental = {estacion['cota_instrumental']:.6f} m"
            if estacion['cota'] is not None:
                estacion_str += f", Cota = {estacion['cota']:.6f} m"
            print(estacion_str)

        if self.vistas_intermedias:
            print("\n--- Vistas Intermedias ---")
            for vista in self.vistas_intermedias:
                print(f"Vista intermedia {vista['estacion']}: Cota = {vista['cota']:.6f} m")


def nivelacion_geodesica_subes_bajas():
    # Variables iniciales
    puntos = []  # Lista para almacenar los puntos y sus cotas
    cota_inicial = 0
    cota_punto_anterior = 0
    cota_intermedia_anterior = 0
    vista_mas_inicial = 0
    vista_mas_punto_anterior = 0
    vista_intermedia_anterior = 0

    # Solicitar datos del primer punto
    nombre_punto_inicial = input("Ingrese el nombre del primer punto: ")
    cota_inicial = round(float(input("Ingrese la cota del primer punto: ")), 3)
    vista_mas_inicial = round(float(input("Ingrese la vista más del primer punto: ")), 3)

    # Registrar el primer punto
    puntos.append((nombre_punto_inicial, cota_inicial, "cota inicial"))
    cota_punto_anterior = cota_inicial
    vista_mas_punto_anterior = vista_mas_inicial

    while True:
        # Preguntar si sigue un punto nuevo, una vista intermedia, o si es el último punto
        tipo = input(
            "¿Sigue una 'vista intermedia', un 'punto nuevo' o es el 'último punto'? (intermedia/punto/ultimo): ").strip().lower()

        if tipo == "punto":
            # Solicitar datos del nuevo punto
            nombre_punto = input("Ingrese el nombre del nuevo punto: ")
            vista_mas_punto = round(float(input("Ingrese la vista más del nuevo punto: ")), 3)
            vista_menos_punto = round(float(input("Ingrese la vista menos del nuevo punto: ")), 3)

            # Calcular cota del nuevo punto
            delta = round(vista_mas_punto_anterior - vista_menos_punto, 3)
            if delta > 0:
                cota_punto_anterior = round(cota_punto_anterior + delta, 3)
                print(f"Sube: {delta}")
            else:
                cota_punto_anterior = round(cota_punto_anterior + delta, 3)
                print(f"Baja: {abs(delta)}")

            # Guardar y actualizar la cota del punto
            puntos.append((nombre_punto, cota_punto_anterior, "cota punto"))
            print(f"Cota del punto '{nombre_punto}': {cota_punto_anterior}")

            # Actualizar vista más anterior
            vista_mas_punto_anterior = vista_mas_punto

        elif tipo == "intermedia":
            # Solicitar datos de la vista intermedia
            nombre_intermedia = input("Ingrese el nombre de la vista intermedia: ")
            vista_menos_intermedia = round(float(input("Ingrese la vista menos de la vista intermedia: ")), 3)

            # Determinar el caso para la vista intermedia
            if len(puntos) == 1:
                # Caso 1: Vista intermedia después del punto inicial
                delta = round(vista_mas_inicial - vista_menos_intermedia, 3)
                if delta > 0:
                    cota_intermedia_anterior = round(cota_inicial + delta, 3)
                    print(f"Sube: {delta}")
                else:
                    cota_intermedia_anterior = round(cota_inicial + delta, 3)
                    print(f"Baja: {abs(delta)}")
            elif puntos[-1][2] == "cota punto":
                # Caso 2: Vista intermedia después de un punto
                delta = round(vista_mas_punto_anterior - vista_menos_intermedia, 3)
                if delta > 0:
                    cota_intermedia_anterior = round(cota_punto_anterior + delta, 3)
                    print(f"Sube: {delta}")
                else:
                    cota_intermedia_anterior = round(cota_punto_anterior + delta, 3)
                    print(f"Baja: {abs(delta)}")
            else:
                # Caso 3: Vista intermedia después de otra vista intermedia
                delta = round(vista_intermedia_anterior - vista_menos_intermedia, 3)
                if delta > 0:
                    cota_intermedia_anterior = round(cota_intermedia_anterior + delta, 3)
                    print(f"Sube: {delta}")
                else:
                    cota_intermedia_anterior = round(cota_intermedia_anterior + delta, 3)
                    print(f"Baja: {abs(delta)}")

            # Guardar la cota de la vista intermedia
            puntos.append((nombre_intermedia, cota_intermedia_anterior, "cota intermedia"))
            print(f"Cota de la vista intermedia '{nombre_intermedia}': {cota_intermedia_anterior}")

            # Actualizar vista intermedia anterior
            vista_intermedia_anterior = vista_menos_intermedia

        elif tipo == "ultimo":
            # Solicitar datos del último punto
            nombre_ultimo = input("Ingrese el nombre del último punto: ")
            vista_menos_ultimo = round(float(input("Ingrese la vista menos del último punto: ")), 3)

            # Calcular cota del último punto
            delta = round(vista_mas_punto_anterior - vista_menos_ultimo, 3)
            if delta > 0:
                cota_punto_anterior = round(cota_punto_anterior + delta, 3)
                print(f"Sube: {delta}")
            else:
                cota_punto_anterior = round(cota_punto_anterior + delta, 3)
                print(f"Baja: {abs(delta)}")

            # Guardar la cota del último punto y salir del bucle
            puntos.append((nombre_ultimo, cota_punto_anterior, "cota último"))
            print(f"Cota del último punto '{nombre_ultimo}': {cota_punto_anterior}")
            break

        else:
            print("Opción no válida. Por favor, ingrese una opción válida (intermedia/punto/ultimo).")

    print("\n--- Resumen de cotas ---")
    for punto in puntos:
        print(f"{punto[0]}: {punto[1]}")




