import numpy as np
import matplotlib.pyplot as plt
from pyproj import Geod
import math
import math
import numpy as np
import plotly.graph_objects as go
import plotly.offline as pyo
import Nivelacion_Diferencial


def latitudes():
    """PUNTO LATITUDES"""
    print("PUNTO LATITUDES")
    # Parámetros del elipsoide WGS84
    a = 6378137.0
    b = 6356752.3142
    f = 1 / 297
    e2 = (2 * f - f ** 2)

    def calcular_conocido_phi(phi_en_grados):
        phi = math.radians(phi_en_grados)

        # Fórmulas del profesor (como tú las tienes)
        theta = math.atan((1 - f) * math.tan(phi))  # fórmula de θ
        w = math.atan((1 - e2) * math.tan(phi))  # fórmula de ω

        # Convertir resultados a grados
        theta_grados = math.degrees(theta)
        w_grados = math.degrees(w)

        print(f"\nConocido φ = {phi_en_grados:.6f}°")
        print(f"θ = {theta_grados:.6f}°")
        print(f"ω = {w_grados:.6f}°")

        graficar_elipse(phi_en_grados, theta_grados, w_grados)

    def calcular_conocido_theta(theta_en_grados):
        theta = math.radians(theta_en_grados)

        # Tus fórmulas
        phi = math.atan(a / b * math.tan(theta))
        w = math.atan((1 - e2) * math.tan(phi))

        phi_grados = math.degrees(phi)
        w_grados = math.degrees(w)

        print(f"\nConocido θ = {theta_en_grados:.6f}°")
        print(f"φ = {phi_grados:.6f}°")
        print(f"ω = {w_grados:.6f}°")

        graficar_elipse(phi_grados, theta_en_grados, w_grados)

    def calcular_conocido_w(w_en_grados):
        w = math.radians(w_en_grados)

        # Tus fórmulas
        phi = math.atan(math.tan(w) / (1 - e2))
        theta = math.atan((b / a) * (math.tan(w) / (1 - e2)))

        phi_grados = math.degrees(phi)
        theta_grados = math.degrees(theta)

        print(f"\nConocido ω = {w_en_grados:.6f}°")
        print(f"φ = {phi_grados:.6f}°")
        print(f"θ = {theta_grados:.6f}°")

        graficar_elipse(phi_grados, theta_grados, w_en_grados)

    def graficar_elipse(phi_en_grados, theta_en_grados, w_en_grados):
        # Convertir ángulos a radianes
        phi = math.radians(phi_en_grados)
        theta = math.radians(theta_en_grados)
        w = math.radians(w_en_grados)

        # Dibujar la elipse meridiana
        t = [math.radians(i) for i in range(-90, 91)]
        x = [a * math.cos(i) for i in t]
        y = [b * math.sin(i) for i in t]

        plt.figure(figsize=(6, 6))
        plt.plot(x, y, label="Elipse meridiana", color="black")

        # Líneas de los tres ángulos
        plt.plot([0, a * math.cos(phi)], [0, b * math.sin(phi)], label="φ (geodésica)", color="red")
        plt.plot([0, a * math.cos(theta)], [0, b * math.sin(theta)], label="θ (reducida)", color="blue")
        plt.plot([0, a * math.cos(w)], [0, b * math.sin(w)], label="ω (geocéntrica)", color="green")

        plt.xlabel("Eje X (ecuador)")
        plt.ylabel("Eje Y (meridiano)")
        plt.title("Elipse meridiana y las tres latitudes")
        plt.legend()
        plt.axis("equal")
        plt.grid(True)
        plt.show()

    while True:
        print("\n==============================")
        print("   CÁLCULO DE LATITUDES")
        print("==============================")
        print("1. Conocido φ → calcular θ y ω")
        print("2. Conocido θ → calcular φ y ω")
        print("3. Conocido ω → calcular φ y θ")
        print("4. Salir")

        opcion = input("Seleccione una opción (1-4): ")

        if opcion == "1":
            try:
                phi_usuario = float(input("Ingrese la latitud geodésica φ en grados (-90 a 90): "))
                if -90 <= phi_usuario <= 90:
                    calcular_conocido_phi(phi_usuario)
                else:
                    print("Error: la latitud debe estar entre -90° y 90°.")
            except ValueError:
                print("Error: ingrese un número válido.")

        elif opcion == "2":
            try:
                theta_usuario = float(input("Ingrese la latitud reducida θ en grados (-90 a 90): "))
                if -90 <= theta_usuario <= 90:
                    calcular_conocido_theta(theta_usuario)
                else:
                    print("Error: la latitud debe estar entre -90° y 90°.")
            except ValueError:
                print("Error: ingrese un número válido.")

        elif opcion == "3":
            try:
                w_usuario = float(input("Ingrese la latitud geocéntrica ω en grados (-90 a 90): "))
                if -90 <= w_usuario <= 90:
                    calcular_conocido_w(w_usuario)
                else:
                    print("Error: la latitud debe estar entre -90° y 90°.")
            except ValueError:
                print("Error: ingrese un número válido.")

        elif opcion == "4":
            print("\nPrograma finalizado. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


def elipsoideHcero():
    """PUNTO ELIPSOIDE H=0"""
    print("PUNTO ELIPSOIDE H=0")

    # === Conversión de Coordenadas Geodésicas a Cartesianas (ECEF) ===
    def dms_a_decimal(grados, minutos, segundos):
        return grados + minutos / 60 + segundos / 3600

    def geodesicas_a_ecef(phi, lam, h):
        a = 6378137.0  # Semieje mayor (WGS84)
        e2 = 0.00669437999014  # Excentricidad²

        phi = math.radians(phi)
        lam = math.radians(lam)

        N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2)

        X = (N + h) * math.cos(phi) * math.cos(lam)
        Y = (N + h) * math.cos(phi) * math.sin(lam)
        Z = (N * (1 - e2) + h) * math.sin(phi)

        return X, Y, Z

    # === Gráfico 3D del elipsoide WGS84 y el punto ===
    def graficar_elipsoide_y_punto(Xp, Yp, Zp):
        a = 6378137.0  # Semieje mayor
        b = 6356752.3142  # Semieje menor

        # Malla del elipsoide
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = a * np.outer(np.cos(u), np.sin(v))
        y = a * np.outer(np.sin(u), np.sin(v))
        z = b * np.outer(np.ones_like(u), np.cos(v))

        fig = go.Figure()

        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            opacity=0.7,
            colorscale="Earth",
            showscale=False
        ))

        fig.add_trace(go.Scatter3d(
            x=[Xp], y=[Yp], z=[Zp],
            mode='markers',
            marker=dict(size=6, color='red'),
            name='Punto'
        ))

        fig.update_layout(
            title="🌍 Elipsoide WGS84 con punto geográfico",
            scene=dict(aspectmode='data'),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        # Abre el gráfico en el navegador como HTML
        pyo.plot(fig, filename='elipsoide.html', auto_open=True)

    # === Programa Principal ===
    if __name__ == "__main__":
        print("=== Conversión de Coordenadas + Gráfico 3D ===")

        # Validación de latitud
        while True:
            phi_g = float(input("Grados latitud (φ): "))
            phi_m = float(input("Minutos latitud: "))
            phi_s = float(input("Segundos latitud: "))
            lat_decimal = dms_a_decimal(phi_g, phi_m, phi_s)
            if -90 <= lat_decimal <= 90:
                break
            else:
                print("Latitud fuera de rango (-90 a 90). Intente nuevamente.\n")

        # Validación de longitud
        while True:
            lam_g = float(input("Grados longitud (λ): "))
            lam_m = float(input("Minutos longitud: "))
            lam_s = float(input("Segundos longitud: "))
            lon_decimal = -dms_a_decimal(lam_g, lam_m, lam_s)  # Longitud Oeste = negativa
            if -180 <= lon_decimal <= 180:
                break
            else:
                print("Longitud fuera de rango (-180 a 180). Intente nuevamente.\n")

        h = float(input("Altura sobre el elipsoide (m): "))

        # Conversión
        X, Y, Z = geodesicas_a_ecef(lat_decimal, lon_decimal, h)

        print("\nCoordenadas ECEF (X, Y, Z) en metros:")
        print(f"X = {X}")
        print(f"Y = {Y}")
        print(f"Z = {Z}")

        # 1️⃣ Primero grafica
        graficar_elipsoide_y_punto(X, Y, Z)


def elipsoideHdiferente():
    """PUNTO ELIPSOIDE H!=0"""
    print("PUNTO ELIPSOIDE H!=0")

    def ecef_a_geodesicas(X, Y, Z):
        """
        Convierte coordenadas ECEF (X, Y, Z) en metros a geodésicas (latitud, longitud, altura)
        usando el elipsoide WGS84.
        """
        a = 6378137.0  # Semieje mayor
        e2 = 0.00669437999014  # Excentricidad²

        # Longitud (λ)
        lam = math.atan2(Y, X)

        # Distancia desde el eje Z
        p = math.sqrt(X ** 2 + Y ** 2)

        # Estimación inicial de φ
        phi = math.atan2(Z, p * (1 - e2))
        phi_anterior = 0
        iteraciones = 0

        # Iteración para refinar la latitud geodésica
        while abs(phi - phi_anterior) > 1e-12 and iteraciones < 1000:
            phi_anterior = phi
            N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2)
            h = p / math.cos(phi) - N
            phi = math.atan2(Z + e2 * N * math.sin(phi), p)
            iteraciones += 1

        N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2)
        h = p / math.cos(phi) - N

        # Convertir a grados decimales
        lat = math.degrees(phi)
        lon = math.degrees(lam)

        return lat, lon, h

    # === Gráfico 3D del elipsoide WGS84 y el punto ===
    def graficar_elipsoide_y_punto(Xp, Yp, Zp):
        """
        Genera un gráfico 3D del elipsoide WGS84 y marca el punto ECEF (Xp, Yp, Zp).
        """
        a = 6378137.0  # Semieje mayor
        b = 6356752.3142  # Semieje menor

        # Malla del elipsoide
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = a * np.outer(np.cos(u), np.sin(v))
        y = a * np.outer(np.sin(u), np.sin(v))
        z = b * np.outer(np.ones_like(u), np.cos(v))

        fig = go.Figure()

        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            opacity=0.7,
            colorscale="Earth",
            showscale=False
        ))

        fig.add_trace(go.Scatter3d(
            x=[Xp], y=[Yp], z=[Zp],
            mode='markers',
            marker=dict(size=6, color='red'),
            name='Punto'
        ))

        fig.update_layout(
            title="🌍 Elipsoide WGS84 con punto ECEF",
            scene=dict(aspectmode='data'),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        # Abre el gráfico en el navegador como HTML
        pyo.plot(fig, filename='elipsoide_ecef.html', auto_open=True)

    # === Programa Principal ===
    if __name__ == "__main__":
        print("=== Conversión de Coordenadas ECEF → Geodésicas + Gráfico 3D ===")

        X = float(input("Coordenada X (m): "))
        Y = float(input("Coordenada Y (m): "))
        Z = float(input("Coordenada Z (m): "))

        # Conversión
        lat, lon, h = ecef_a_geodesicas(X, Y, Z)

        print("\n📌 Coordenadas geodésicas (WGS84):")
        print(f"Latitud  (φ): {lat}°")
        print(f"Longitud (λ): {lon}°")
        print(f"Altura   (h): {h} m")

        # 1️⃣ Grafica el elipsoide y el punto
        graficar_elipsoide_y_punto(X, Y, Z)


def longitudArcoParalelo():
    """PUNTO LONGITUD DE ARCO DE PARALELO"""
    print("PUNTO LONGITUD DE ARCO DE PARALELO")
    # excentricidad al cuadrado
    a = 6378137.0  # Semieje mayor en metros
    b = 6356752.3142
    e2 = 1 - (b ** 2 / a ** 2)

    while True:
        try:
            print("\n Ingrese coordenadas")
            lat = float(input("Latitud del paralelo (-90° a 90°): "))
            lon1 = float(input("Longitud inicial (-180° a 180°): "))
            lon2 = float(input("Longitud final (-180° a 180°): "))

            # ✅ Validaciones de rango estrictas
            if lat < -90 or lat > 90:
                print("Error: la latitud debe estar entre -90° y 90°.")
                continue
            if lon1 < -180 or lon1 > 180:
                print("Error: la longitud inicial debe estar entre -180° y 180°.")
                continue
            if lon2 < -180 or lon2 > 180:
                print("Error: la longitud final debe estar entre -180° y 180°.")
                continue

            break  # Todos los valores son válidos

        except ValueError:
            print("❌ Error: ingrese datos numéricos válidos.")

    phi = np.radians(lat)
    R_phi = (a * np.cos(phi)) / np.sqrt(1 - e2 * np.sin(phi) ** 2)

    delta_lambda = np.radians(abs(lon2 - lon1))
    longitud_arco = delta_lambda * R_phi

    print(f"\nRESULTADO")
    print(f"Radio del paralelo a {lat}°: {R_phi:.2f} m")
    print(f"Longitud del arco entre {lon1}° y {lon2}°: {longitud_arco:.2f} m")

    lons = np.linspace(lon1, lon2, 100)
    lats = np.full_like(lons, lat)

    # Convertir a coordenadas cartesianas
    def esfericas_a_cartesianas(lat, lon):
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)
        N = a / np.sqrt(1 - e2 * np.sin(lat_rad) ** 2)  # Gran normal
        x = N * np.cos(lat_rad) * np.cos(lon_rad)
        y = N * np.cos(lat_rad) * np.sin(lon_rad)
        z = (N * (1 - e2)) * np.sin(lat_rad)
        return x, y, z

    x, y, z = esfericas_a_cartesianas(lats, lons)

    # Crear figura 3D
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Graficar elipsoide (simplificado)
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_elip = a * np.outer(np.cos(u), np.sin(v))
    y_elip = a * np.outer(np.sin(u), np.sin(v))
    z_elip = b * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x_elip, y_elip, z_elip, color='lightblue', alpha=0.2)

    # Graficar arco de paralelo
    ax.plot(x, y, z, color='red', linewidth=3,
            label=f'Arco: {longitud_arco / 1000:.2f} km')

    # Ajustes visuales
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(f'Arco de Paralelo a {lat}°N\n{lon1}°E a {lon2}°E')
    ax.legend()
    plt.tight_layout()
    plt.show()



def longitudArcoMeridiano():
    """PUNTO LONGITUD DE ARCO MERIDIANO"""
    print("PUNTO LONGITUD DE ARCO MERIDIANO")
    a = 6378137.0  # Semieje mayor en metros
    b = 6356752.3142  # Semieje menor en metros
    while True:
        try:
            lat1 = float(input('Angulo latitud 1: '))
            lat2 = float(input('Angulo latitud 2: '))
            lon = float(input('Angulo longitud: '))
            if (-90 <= lat1 <= 90 and -90 <= lat2 <= 90) and (-180 <= lon <= 180):
                break
            else:
                print("Error: las latitudes deben estar entre -90° y 90°, y la longitud entre -180° y 180°")
        except ValueError:
            print("Error: ingrese un número válido")

    geod = Geod(ellps="WGS84")
    _, _, distancia = geod.inv(lon, lat1, lon, lat2)

    print(f"Distancia: {distancia:.2f} metros")

    # Generar puntos del arco
    latitudes = np.linspace(lat1, lat2, 100)
    longitudes = np.full_like(latitudes, lon)

    # Convertir a coordenadas cartesianas
    def esfericas_a_cartesianas(lat, lon):
        lat_rad = np.radians(lat)
        lon_rad = np.radians(lon)
        x = a * np.cos(lat_rad) * np.cos(lon_rad)
        y = a * np.cos(lat_rad) * np.sin(lon_rad)
        z = b * np.sin(lat_rad)
        return x, y, z

    x_arco, y_arco, z_arco = esfericas_a_cartesianas(latitudes, longitudes)

    # Crear figura 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Graficar elipsoide (simplificado)
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_elipsoide = a * np.outer(np.cos(u), np.sin(v))
    y_elipsoide = a * np.outer(np.sin(u), np.sin(v))
    z_elipsoide = b * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x_elipsoide, y_elipsoide, z_elipsoide, color='lightblue', alpha=0.3)

    # Graficar arco de meridiano
    ax.plot(x_arco, y_arco, z_arco, color='red', linewidth=3, label='Arco de meridiano')

    # Ajustes visuales
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Arco de Meridiano sobre el Elipsoide WGS84')
    ax.legend()
    plt.tight_layout()
    plt.show()


def nivelacionDiferencial():
    """PUNTO NIVELACION DIFERENCIAL"""
    print("PUNTO NIVELACION DIFERENCIAL")
    print("Seleccione el método de nivelación geodésica:")
    print("1. Método de líneas de nivel")
    print("2. Método de subidas y bajadas")
    opcion = input("Ingrese el número de opción (1/2): ").strip()

    if opcion == '1':
        nivelacion = Nivelacion_Diferencial.NivelacionGeodesica()
        nivelacion.calcular()
    elif opcion == '2':
        Nivelacion_Diferencial.nivelacion_geodesica_subes_bajas()
    else:
        print("Opción no válida. Por favor, seleccione 1 o 2.")



def biseccion():
    """PUNTO BISECCION"""
    print("PUNTO BISECCION")
    print("*" * 28)
    print("Programa Bisección Geodésica")

    # Lectura de coordenadas de A y B con validación
    while True:
        NA = float(input("Inserte Norte de A: "))
        if -90 <= NA <= 90:
            break
        print("Valor inválido. La latitud debe estar entre -90 y 90.")

    while True:
        EA = float(input("Inserte Este de A: "))
        if -180 <= EA <= 180:
            break
        print("Valor inválido. La longitud debe estar entre -180 y 180.")

    while True:
        NB = float(input("Inserte Norte de B: "))
        if -90 <= NB <= 90:
            break
        print("Valor inválido. La latitud debe estar entre -90 y 90.")

    while True:
        EB = float(input("Inserte Este de B: "))
        if -180 <= EB <= 180:
            break
        print("Valor inválido. La longitud debe estar entre -180 y 180.")

    #  Función auxiliar DMS → grados decimales
    def dms_a_grados(g, m, s):
        return g + m / 60 + s / 3600

    # Lectura de ángulos α y β en DMS
    ag = float(input("α: grados: "))
    am = float(input("α: minutos: "))
    ase = float(input("α: segundos: "))
    alpha = dms_a_grados(ag, am, ase)

    bg = float(input("β: grados: "))
    bm = float(input("β: minutos: "))
    bse = float(input("β: segundos: "))
    beta = dms_a_grados(bg, bm, bse)

    # Distancia AB y ángulo Ro de la ley de senos
    dx = EB - EA
    dy = NB - NA
    AB = math.hypot(dx, dy)  # distancia entre A y B
    Ro = 180.0 - alpha - beta  # tercer ángulo del triángulo

    # Longitud AP según ley de senos —
    AP = AB * math.sin(math.radians(beta)) / math.sin(math.radians(Ro))

    # Azimut de AB (bearing desde A hacia B)
    az_AB = (math.degrees(math.atan2(dx, dy))) % 360

    # Azimut desde A hacia P
    az_AP = (az_AB + alpha) % 360

    #  Desplazamientos en Este y Norte
    dE = AP * math.sin(math.radians(az_AP))
    dN = AP * math.cos(math.radians(az_AP))

    # Coordenadas de P
    NP = NA + dN
    EP = EA + dE

    #  Salida de resultados
    print("*" * 28)
    print(f"Np = {NP:.3f}  m")
    print(f"Ep = {EP:.3f}  m")

    #  Opción de gráfica
    if int(input("¿Quieres dibujarlo? (1=Sí, 2=No): ")) == 1:
        xs = [EA, EB, EP, EA]
        ys = [NA, NB, NP, NA]

        plt.figure()
        plt.plot(xs, ys, 'b--o', linewidth=1.5)
        plt.scatter([EA, EB, EP], [NA, NB, NP], c='red')
        plt.annotate("A", (EA, NA), textcoords="offset points", xytext=(5, 5))
        plt.annotate("B", (EB, NB), textcoords="offset points", xytext=(5, 5))
        plt.annotate("P", (EP, NP), textcoords="offset points", xytext=(5, 5))
        plt.xlabel("Este (m)")
        plt.ylabel("Norte (m)")
        plt.title("Bisección Geodésica")
        plt.grid(True)
        plt.axis('equal')
        plt.show()


def areaCuadrilatero():
    """PUNTO ÁREA DE CUADRILÁTERO"""
    print("PUNTO ÁREA DE CUADRILÁTERO")
    while True:
        print("Se trabajara con el elipspide WGS-84")
        a = 6378137  # Radio ecuatorial
        b = 6356752.3142  # Radio polar
        f_inv = 282.257223563  # Aplanamiento inverso
        f = 1 / f_inv  # Aplamamiento
        e = np.sqrt(1 - (b / a) ** 2)  # Excentricidad
        e2 = (2 / f_inv) - (1 / f_inv ** 2)
        print("Radio ecuatorial (m) =", a)
        print("Radio polar (m) =", b)
        print("Aplanamiento inverso =", f_inv)
        print("Aplanamiento =", f)
        print("Excentricidad =", e)
        break

    def geodetic_to_cartesian(lat, lon):
        lat = np.radians(lat)
        lon = np.radians(lon)
        N = a / np.sqrt(1 - e ** 2 * np.sin(lat) ** 2)
        X = (N) * np.cos(lat) * np.cos(lon)
        Y = (N) * np.cos(lat) * np.sin(lon)
        Z = ((1 - e ** 2) * N) * np.sin(lat)
        return X, Y, Z

    def input_latitud(label):
        while True:
            g = int(input(f"{label} (°): "))
            if -90 <= g <= 90:
                break
            print("⚠️ La latitud debe estar entre -90° y 90°.")
        while True:
            m = int(input(f"{label} ('): "))
            if 0 <= m < 60:
                break
            print("⚠️ Los minutos deben estar entre 0 y 59.")
        while True:
            s = int(input(f"{label} (\"): "))
            if 0 <= s < 60:
                break
            print("⚠️ Los segundos deben estar entre 0 y 59.")
        return g + m / 60 + s / 3600

    def input_longitud(label):
        while True:
            g = int(input(f"{label} (°): "))
            if -180 <= g <= 180:
                break
            print("⚠️ La longitud debe estar entre -180° y 180°.")
        while True:
            m = int(input(f"{label} ('): "))
            if 0 <= m < 60:
                break
            print("⚠️ Los minutos deben estar entre 0 y 59.")
        while True:
            s = int(input(f"{label} (\"): "))
            if 0 <= s < 60:
                break
            print("⚠️ Los segundos deben estar entre 0 y 59.")
        return g + m / 60 + s / 3600

    while True:
        print("Ingrese la latitud del vértice A")
        ala = input_latitud("(w)")
        print(ala)

        print("Ingrese la longitud del vértice A")
        alo = input_longitud("(ω)")
        print(alo)

        print("Ingrese la latitud del vértice B")
        bla = input_latitud("(ω)")
        print(bla)

        print("Ingrese la longitud del vértice B")
        blo = input_longitud("(ω)")
        print(blo)

        print("Ingrese la latitud del vértice C")
        cla = input_latitud("(ω)")
        print(cla)

        print("Ingrese la longitud del vértice C")
        clo = input_longitud("(ω)")
        print(clo)

        print("Ingrese la latitud del vértice D")
        dla = input_latitud("(ω)")
        print(dla)

        print("Ingrese la longitud del vértice D")
        dlo = input_longitud("(ω)")
        print(dlo)
        break

    coords_geod = [(ala, alo), (bla, blo), (cla, clo), (dla, dlo)]

    def calcular_area_bagratuni(coords_geod):
        area = 0
        R = (a + b) / 2
        for i in range(len(coords_geod)):
            lat1, lon1 = coords_geod[i]
            lat2, lon2 = coords_geod[(i + 1) % len(coords_geod)]

            lat1, lon1 = np.radians(lat1), np.radians(lon1)
            lat2, lon2 = np.radians(lat2), np.radians(lon2)

            delta_lambda = lon2 - lon1
            dA = R ** 2 * delta_lambda * np.sin((lat1 + lat2) / 2)
            area += dA
        return abs(area)

    area_bagratuni = calcular_area_bagratuni(coords_geod)
    print("Área del cuadrilátero (Método de Bagratuni) =", area_bagratuni, "metros cuadrados")

    # Proyección 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = a * np.outer(np.cos(u), np.sin(v))
    y = a * np.outer(np.sin(u), np.sin(v))
    z = b * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='c', alpha=0.5, rstride=4, cstride=4, linewidth=0)

    coords_cart = [geodetic_to_cartesian(lat, lon) for lat, lon in coords_geod]
    vertices = np.array(coords_cart)
    num_steps = 10
    for i in range(len(vertices)):
        start = vertices[i]
        end = vertices[(i + 1) % len(vertices)]
        points = []
        for t in np.linspace(0, 1, num_steps):
            point = (1 - t) * start + t * end
            norm = np.linalg.norm(point)
            point = (point / norm) * np.linalg.norm(vertices[0])
            points.append(point)
        first_point = points[0]
        ax.plot([start[0], first_point[0]], [start[1], first_point[1]], [start[2], first_point[2]], color='r')
        for j in range(num_steps - 1):
            ax.plot([points[j][0], points[j + 1][0]], [points[j][1], points[j + 1][1]],
                    [points[j][2], points[j + 1][2]], color='r')

    ax.set_xlim([-a, a])
    ax.set_ylim([-a, a])
    ax.set_zlim([-b, b])
    ax.axis('off')
    plt.show()


def mostrar_menu():
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Latitudes")
    print("2. Elipsoide (h=0)")
    print("3. Elipsoide (h!=0)")
    print("4. Longitud de arco paralelo")
    print("5. Longitud de arco meridiano")
    print("6. Nivelacion diferencial")
    print("7. Biseccion")
    print("8. Area del cuadrilatero")

def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            latitudes()
        elif opcion == "2":
            elipsoideHcero()
        elif opcion == "3":
            elipsoideHdiferente()
        elif opcion == "4":
            longitudArcoParalelo()
        elif opcion == "5":
            longitudArcoMeridiano()
        elif opcion == "6":
            nivelacionDiferencial()
        elif opcion == "7":
            biseccion()
        elif opcion == "8":
            areaCuadrilatero()



        elif opcion == "0":
            print("Saliendo del programa... ¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()