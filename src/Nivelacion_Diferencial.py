import matplotlib.pyplot as plt

class NivelacionGeodesica:
    def __init__(self):
        self.estaciones = []  # Lista para almacenar estaciones, cotas, alturas instrumentales y alturas elipsoidales
        self.vistas_intermedias = []  # Lista para almacenar vistas intermedias

    def agregar_punto_inicial(self):
        estacion = input("Ingrese el nombre del punto inicial (Ej: BM1): ")
        cota = float(input(f"Ingrese la cota (H) para {estacion} (con decimales): "))
        vista_mas = float(input(f"Ingrese la vista más para {estacion} (con decimales): "))
        cota_instrumental = cota + vista_mas
        N = float(input(f"Ingrese la ondulación geoidal N (metros) para {estacion}: "))
        h = N + cota

        self.estaciones.append({
            'estacion': estacion,
            'N': N,
            'cota': cota,
            'h': h,
            'vista_mas': vista_mas,
            'vista_menos': None,
            'cota_instrumental': cota_instrumental
        })

        print(f"Estación {estacion} registrada con cota = {cota:.6f}, "
              f"altura elipsoidal h = {h:.6f} y altura instrumental = {cota_instrumental:.6f}.")

    def registrar_vista_intermedia(self, cota_instrumental):
        estacion_intermedia = input("Ingrese el nombre de la vista intermedia: ")
        vista_menos = float(input(f"Ingrese la vista menos para {estacion_intermedia} (con decimales): "))
        cota_intermedia = cota_instrumental - vista_menos
        N = float(input(f"Ingrese la ondulación geoidal N (metros) para {estacion_intermedia}: "))
        h = N + cota_intermedia

        self.vistas_intermedias.append({
            'estacion': estacion_intermedia,
            'N': N,
            'vista_menos': vista_menos,
            'cota': cota_intermedia,
            'h': h
        })

        print(f"Vista intermedia {estacion_intermedia} registrada con cota = {cota_intermedia:.6f}, "
              f"altura elipsoidal h = {h:.6f}.")

    def registrar_punto(self, estacion_origen):
        estacion_destino = input(f"¿A qué estación se mira desde {estacion_origen}? ")
        vista_menos = float(input(f"Ingrese la vista menos para {estacion_destino} (con decimales): "))
        cota_instrumental = self.estaciones[-1]['cota_instrumental']
        cota = cota_instrumental - vista_menos
        vista_mas = float(input(f"Ingrese la vista más para {estacion_destino} (con decimales): "))
        nueva_cota_instrumental = cota + vista_mas
        N = float(input(f"Ingrese la ondulación geoidal N (metros) para {estacion_destino}: "))
        h = N + cota

        self.estaciones.append({
            'estacion': estacion_destino,
            'N': N,
            'cota': cota,
            'h': h,
            'vista_mas': vista_mas,
            'vista_menos': vista_menos,
            'cota_instrumental': nueva_cota_instrumental
        })

        print(f"Estación {estacion_destino} registrada con cota = {cota:.6f}, "
              f"altura elipsoidal h = {h:.6f} y altura instrumental = {nueva_cota_instrumental:.6f}.")

    def registrar_ultimo_punto(self):
        estacion_destino = input("Ingrese el nombre del último punto: ")
        vista_menos = float(input(f"Ingrese la vista menos para {estacion_destino} (con decimales): "))
        cota_instrumental = self.estaciones[-1]['cota_instrumental']
        cota = cota_instrumental - vista_menos
        N = float(input(f"Ingrese la ondulación geoidal N (metros) para {estacion_destino}: "))
        h = N + cota

        self.estaciones.append({
            'estacion': estacion_destino,
            'N': N,
            'cota': cota,
            'h': h,
            'vista_mas': None,
            'vista_menos': vista_menos,
            'cota_instrumental': None
        })

        print(f"Última estación {estacion_destino} registrada con cota = {cota:.6f} "
              f"y altura elipsoidal h = {h:.6f}.")

    def calcular(self):
        self.agregar_punto_inicial()

        while True:
            continuar = input(
                "\n¿Qué sigue? (1: Registrar nueva vista/punto, 2: Registrar vista intermedia, 3: Registrar último punto, 4: Finalizar): ")

            if continuar == '1':
                estacion_origen = self.estaciones[-1]['estacion']
                self.registrar_punto(estacion_origen)
            elif continuar == '2':
                cota_instrumental = self.estaciones[-1]['cota_instrumental']
                self.registrar_vista_intermedia(cota_instrumental)
            elif continuar == '3':
                self.registrar_ultimo_punto()
                break
            elif continuar == '4':
                print("Cálculo finalizado.")
                break
            else:
                print("Opción inválida, intente nuevamente.")

        self.mostrar_resultados()
        self.graficar_perfil_topografico()

    def mostrar_resultados(self):
        print("\n--- Resultados ---")
        for estacion in self.estaciones:
            estacion_str = f"Estación {estacion['estacion']}:"
            if estacion['cota_instrumental'] is not None:
                estacion_str += f" Altura instrumental = {estacion['cota_instrumental']:.6f} m"
            if estacion['cota'] is not None:
                estacion_str += f", Cota (H) = {estacion['cota']:.6f} m"
            if estacion['h'] is not None:
                estacion_str += f", Altura elipsoidal (h) = {estacion['h']:.6f} m"
            estacion_str += f", N = {estacion['N']:.3f} m"
            print(estacion_str)

        if self.vistas_intermedias:
            print("\n--- Vistas Intermedias ---")
            for vista in self.vistas_intermedias:
                print(f"Vista intermedia {vista['estacion']}: Cota (H) = {vista['cota']:.6f} m, "
                      f"Altura elipsoidal (h) = {vista['h']:.6f} m, N = {vista['N']:.3f} m")

    def graficar_perfil_topografico(self):
        """Genera el gráfico del perfil topográfico (Cota vs h)."""
        if not self.estaciones:
            print("No hay estaciones registradas para graficar.")
            return

        # Extraer datos
        estaciones = [e['estacion'] for e in self.estaciones]
        cotas = [e['cota'] for e in self.estaciones]
        alturas_h = [e['h'] for e in self.estaciones]

        # Gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(estaciones, cotas, marker='o', color='red', label='Cota (H)')
        plt.plot(estaciones, alturas_h, marker='s', linestyle='--', color='blue', label='Altura elipsoidal (h)')

        # Puntos de inicio y fin
        plt.scatter(estaciones[0], cotas[0], color='black', label='Inicio')
        plt.scatter(estaciones[-1], cotas[-1], color='green', label='Final')

        # Etiquetas
        plt.title("Perfil Topográfico (Cota vs Altura Elipsoidal)")
        plt.xlabel("Estaciones")
        plt.ylabel("Altura (m)")
        plt.grid(True)
        plt.legend()
        plt.show()


import matplotlib.pyplot as plt

def nivelacion_geodesica_subes_bajas():
    # Variables iniciales
    puntos = []  # Lista para almacenar los puntos y sus cotas
    alturas_elipsoidales = []  # Para guardar h = N + H
    nombres_puntos = []  # Para el gráfico
    cota_inicial = 0
    cota_punto_anterior = 0
    cota_intermedia_anterior = 0
    vista_mas_inicial = 0
    vista_mas_punto_anterior = 0
    vista_intermedia_anterior = 0

    # Solicitar ondulación geoidal N
    N = round(float(input("Ingrese el valor de la ondulación geoidal (N): ")), 3)

    # Solicitar datos del primer punto
    nombre_punto_inicial = input("Ingrese el nombre del primer punto: ")
    cota_inicial = round(float(input("Ingrese la cota del primer punto (H): ")), 3)
    vista_mas_inicial = round(float(input("Ingrese la vista más del primer punto: ")), 3)

    # Calcular altura elipsoidal
    h_inicial = round(N + cota_inicial, 3)

    # Registrar el primer punto
    puntos.append((nombre_punto_inicial, cota_inicial, "cota inicial"))
    alturas_elipsoidales.append(h_inicial)
    nombres_puntos.append(nombre_punto_inicial)
    cota_punto_anterior = cota_inicial
    vista_mas_punto_anterior = vista_mas_inicial

    while True:
        tipo = input("¿Sigue una 'vista intermedia', un 'punto nuevo' o es el 'último punto'? (intermedia/punto/ultimo): ").strip().lower()

        if tipo == "punto":
            nombre_punto = input("Ingrese el nombre del nuevo punto: ")
            vista_mas_punto = round(float(input("Ingrese la vista más del nuevo punto: ")), 3)
            vista_menos_punto = round(float(input("Ingrese la vista menos del nuevo punto: ")), 3)

            # Calcular diferencia de nivel
            delta = round(vista_mas_punto_anterior - vista_menos_punto, 3)
            if delta > 0:
                print(f"Sube: {delta}")
            else:
                print(f"Baja: {abs(delta)}")

            # Actualizar cota
            cota_punto_anterior = round(cota_punto_anterior + delta, 3)
            h = round(N + cota_punto_anterior, 3)

            puntos.append((nombre_punto, cota_punto_anterior, "cota punto"))
            alturas_elipsoidales.append(h)
            nombres_puntos.append(nombre_punto)
            print(f"Cota (H) del punto '{nombre_punto}': {cota_punto_anterior}, Altura elipsoidal (h): {h}")

            vista_mas_punto_anterior = vista_mas_punto

        elif tipo == "intermedia":
            nombre_intermedia = input("Ingrese el nombre de la vista intermedia: ")
            vista_menos_intermedia = round(float(input("Ingrese la vista menos de la vista intermedia: ")), 3)

            if len(puntos) == 1:
                delta = round(vista_mas_inicial - vista_menos_intermedia, 3)
                cota_intermedia_anterior = round(cota_inicial + delta, 3)
            elif puntos[-1][2] == "cota punto":
                delta = round(vista_mas_punto_anterior - vista_menos_intermedia, 3)
                cota_intermedia_anterior = round(cota_punto_anterior + delta, 3)
            else:
                delta = round(vista_intermedia_anterior - vista_menos_intermedia, 3)
                cota_intermedia_anterior = round(cota_intermedia_anterior + delta, 3)

            if delta > 0:
                print(f"Sube: {delta}")
            else:
                print(f"Baja: {abs(delta)}")

            h = round(N + cota_intermedia_anterior, 3)
            puntos.append((nombre_intermedia, cota_intermedia_anterior, "cota intermedia"))
            alturas_elipsoidales.append(h)
            nombres_puntos.append(nombre_intermedia)
            print(f"Cota (H) de '{nombre_intermedia}': {cota_intermedia_anterior}, Altura elipsoidal (h): {h}")

            vista_intermedia_anterior = vista_menos_intermedia

        elif tipo == "ultimo":
            nombre_ultimo = input("Ingrese el nombre del último punto: ")
            vista_menos_ultimo = round(float(input("Ingrese la vista menos del último punto: ")), 3)
            delta = round(vista_mas_punto_anterior - vista_menos_ultimo, 3)

            if delta > 0:
                print(f"Sube: {delta}")
            else:
                print(f"Baja: {abs(delta)}")

            cota_punto_anterior = round(cota_punto_anterior + delta, 3)
            h = round(N + cota_punto_anterior, 3)

            puntos.append((nombre_ultimo, cota_punto_anterior, "cota último"))
            alturas_elipsoidales.append(h)
            nombres_puntos.append(nombre_ultimo)
            print(f"Cota (H) del último punto '{nombre_ultimo}': {cota_punto_anterior}, Altura elipsoidal (h): {h}")
            break

        else:
            print("Opción no válida. Por favor, ingrese una opción válida (intermedia/punto/ultimo).")

    # Mostrar resumen de cotas
    print("\n--- RESULTADOS FINALES ---")
    for p, h in zip(puntos, alturas_elipsoidales):
        print(f"{p[0]} -> Cota (H): {p[1]}, Altura elipsoidal (h): {h}")

    # Graficar perfil topográfico
    cotas = [p[1] for p in puntos]

    plt.figure(figsize=(10, 5))
    plt.plot(nombres_puntos, cotas, marker='o', label='Cota ortométrica (H)', color='blue')
    plt.plot(nombres_puntos, alturas_elipsoidales, marker='s', linestyle='--', label='Altura elipsoidal (h)', color='orange')
    plt.title("Perfil Topográfico (Nivelación Geodésica)")
    plt.xlabel("Puntos")
    plt.ylabel("Altura (m)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
