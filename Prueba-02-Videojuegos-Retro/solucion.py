"""
==========================================================================
 SISTEMA DE GESTIÓN DE TORNEO DE VIDEOJUEGOS RETRO - "Pixeles Retro"
==========================================================================
Estudiante: David González Santibañez
Curso: Fundamentos de Análisis de Datos
Generación: RTD-25-01-13-0056-1

Descripción:
Este programa gestiona un torneo de videojuegos retro usando POO.
Incluye carga de participantes desde CSV, registro manual, formación
manual de equipos y ahora también FORMACIÓN AUTOMÁTICA BALANCEADA
de equipos (por nivel). Además registra partidas, asigna puntos y
genera reportes con estadísticas (promedio, mediana, rendimiento).
==========================================================================
"""

import csv
import os
import statistics


# ==========================================================================
# CLASES PRINCIPALES
# ==========================================================================

class Participante:
    def __init__(self, nombre, edad, nivel):
        self.nombre = nombre
        self.edad = edad
        self.nivel = nivel
        self.equipo = None

    def tiene_equipo(self):
        return self.equipo is not None

    def __str__(self):
        return f"{self.nombre} (Edad: {self.edad}, Nivel: {self.nivel})"


class Equipo:
    def __init__(self, nombre, jugador_1, jugador_2):
        self.nombre = nombre
        self.jugadores = [jugador_1, jugador_2]
        self.puntos = 0
        jugador_1.equipo = self
        jugador_2.equipo = self

    def sumar_puntos(self, puntos):
        self.puntos += puntos

    def contiene_jugador(self, nombre_jugador):
        for jugador in self.jugadores:
            if jugador.nombre == nombre_jugador:
                return True
        return False

    def __str__(self):
        nombres = ", ".join(j.nombre for j in self.jugadores)
        return f"{self.nombre} | Integrantes: {nombres} | Puntos: {self.puntos}"


class Partida:
    PUNTOS_POR_VICTORIA = 3

    def __init__(self, equipo_1, equipo_2, ganador):
        self.equipo_1 = equipo_1
        self.equipo_2 = equipo_2
        self.ganador = ganador
        self.puntos_otorgados = Partida.PUNTOS_POR_VICTORIA

    def __str__(self):
        return (f"{self.equipo_1.nombre} vs {self.equipo_2.nombre} "
                f"-> Ganador: {self.ganador.nombre} (+{self.puntos_otorgados} pts)")


# ==========================================================================
# FUNCIONES DE VALIDACIÓN
# ==========================================================================

def validar_nombre(nombre):
    return nombre.strip() != ""

def validar_edad(edad):
    return 12 <= edad <= 70

def validar_nivel(nivel):
    return 1 <= nivel <= 5


# ==========================================================================
# CARGA DE DATOS DESDE CSV
# ==========================================================================

def arreglar_acentos(texto):
    try:
        return texto.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return texto

def encontrar_archivo_csv(nombre_archivo):
    carpetas = [".", "sample_data", "/content", "/content/sample_data"]
    for carpeta in carpetas:
        ruta = os.path.join(carpeta, nombre_archivo)
        if os.path.exists(ruta):
            return ruta
    return None

def cargar_participantes_desde_csv(nombre_archivo):
    participantes = []
    ruta = encontrar_archivo_csv(nombre_archivo)
    if ruta is None:
        print(f" ⚠️ No se encontró '{nombre_archivo}' en ninguna carpeta conocida.")
        return participantes
    try:
        with open(ruta, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                nombre = arreglar_acentos(fila["nombre"].strip())
                try:
                    edad = int(fila["edad"])
                    nivel = int(fila["nivel_experiencia"])
                except ValueError:
                    print(f" ⚠️ Fila con datos no numéricos, se omite: {fila}")
                    continue
                if not validar_nombre(nombre):
                    print(f" ⚠️ Nombre vacío, se omite: {fila}")
                    continue
                if not validar_edad(edad):
                    print(f" ⚠️ Edad fuera de rango: {nombre}")
                    continue
                if not validar_nivel(nivel):
                    print(f" ⚠️ Nivel fuera de rango: {nombre}")
                    continue
                participantes.append(Participante(nombre, edad, nivel))
        print(f" ✅ Se cargaron {len(participantes)} participantes desde '{ruta}'.")
    except FileNotFoundError:
        print(f" ⚠️ No se encontró el archivo. Iniciando sin datos.")
    return participantes


# ==========================================================================
# GESTIÓN DE PARTICIPANTES Y EQUIPOS (manual + automático)
# ==========================================================================

def registrar_participante(participantes, nombre, edad_texto, nivel_texto):
    if not validar_nombre(nombre):
        print(" ❌ Error: el nombre no puede estar vacío.")
        return False
    nombre = nombre.strip()
    for p in participantes:
        if p.nombre.lower() == nombre.lower():
            print(f" ❌ Error: el participante '{nombre}' ya está registrado.")
            return False
    try:
        edad = int(edad_texto)
    except ValueError:
        print(" ❌ Error: la edad debe ser un número entero.")
        return False
    if not validar_edad(edad):
        print(" ❌ Error: la edad debe estar entre 12 y 70 años.")
        return False
    try:
        nivel = int(nivel_texto)
    except ValueError:
        print(" ❌ Error: el nivel debe ser un número entero.")
        return False
    if not validar_nivel(nivel):
        print(" ❌ Error: el nivel de experiencia debe estar entre 1 y 5.")
        return False

    nuevo = Participante(nombre, edad, nivel)
    participantes.append(nuevo)
    print(f" ✅ Participante '{nombre}' registrado con éxito (edad: {edad}, nivel: {nivel}).")
    return True


def buscar_participante(participantes, nombre):
    for p in participantes:
        if p.nombre == nombre:
            return p
    return None


def formar_equipo(equipos, nombre_equipo, jug1_nombre, jug2_nombre, participantes):
    nombre_equipo = nombre_equipo.strip()
    if not nombre_equipo:
        print(" ❌ Error: el nombre del equipo no puede estar vacío.")
        return False
    if nombre_equipo in equipos:
        print(f" ❌ Error: ya existe un equipo llamado '{nombre_equipo}'.")
        return False
    if jug1_nombre == jug2_nombre:
        print(" ❌ Error: un equipo necesita 2 jugadores distintos.")
        return False

    jug1 = buscar_participante(participantes, jug1_nombre)
    jug2 = buscar_participante(participantes, jug2_nombre)
    if jug1 is None or jug2 is None:
        print(" ❌ Error: ambos jugadores deben estar registrados.")
        return False
    if jug1.tiene_equipo():
        print(f" ❌ Error: '{jug1.nombre}' ya está en el equipo '{jug1.equipo.nombre}'.")
        return False
    if jug2.tiene_equipo():
        print(f" ❌ Error: '{jug2.nombre}' ya está en el equipo '{jug2.equipo.nombre}'.")
        return False

    nuevo_equipo = Equipo(nombre_equipo, jug1, jug2)
    equipos[nombre_equipo] = nuevo_equipo
    print(f" ✅ Equipo '{nombre_equipo}' formado: {jug1.nombre} y {jug2.nombre}.")
    return True


# =============== NUEVA FUNCIÓN: FORMACIÓN AUTOMÁTICA BALANCEADA ===============
def formar_equipos_balanceados(participantes, equipos):
    """
    Forma equipos de 2 jugadores automáticamente, balanceando los niveles.
    Se toman todos los participantes que aún NO tienen equipo.
    Se ordenan por nivel y se empareja al más bajo con el más alto,
    al segundo más bajo con el segundo más alto, etc.
    Los equipos reciben un nombre automático (Equipo 1, Equipo 2, ...).
    """
    # Filtramos participantes sin equipo
    sin_equipo = [p for p in participantes if not p.tiene_equipo()]

    if len(sin_equipo) < 2:
        print(" ⚠️ Necesitas al menos 2 participantes sin equipo para formar equipos.")
        return

    if len(sin_equipo) % 2 != 0:
        print(f" ⚠️ Hay un número impar de jugadores sin equipo ({len(sin_equipo)}).")
        print("   Se excluirá al último jugador para poder emparejar.")
        # Excluimos al de mayor nivel (o al último de la lista, tú decides)
        # Vamos a excluir al último de la lista sin ordenar, pero informando.
        sobrante = sin_equipo.pop()
        print(f"   Jugador excluido: {sobrante.nombre}")

    # Ordenamos por nivel (y nombre para estabilidad)
    ordenados = sorted(sin_equipo, key=lambda p: (p.nivel, p.nombre))

    # Generamos nombres automáticos únicos
    num_equipos = len(equipos)  # Para continuar la numeración
    for i in range(len(ordenados) // 2):
        jug1 = ordenados[i]               # más bajo
        jug2 = ordenados[-(i+1)]          # más alto
        num_equipos += 1
        nombre_auto = f"Equipo {num_equipos}"
        # Verificamos que el nombre no exista (muy poco probable con auto numérico)
        while nombre_auto in equipos:
            num_equipos += 1
            nombre_auto = f"Equipo {num_equipos}"
        nuevo_equipo = Equipo(nombre_auto, jug1, jug2)
        equipos[nombre_auto] = nuevo_equipo

    print(f" ✅ Se formaron {len(ordenados)//2} equipos balanceados automáticamente.")
    for eq in equipos.values():
        print(f"    {eq.nombre}: {eq.jugadores[0].nombre} (nivel {eq.jugadores[0].nivel}) + "
              f"{eq.jugadores[1].nombre} (nivel {eq.jugadores[1].nivel})")


# ==========================================================================
# REGISTRO Y ANÁLISIS DE PARTIDAS
# ==========================================================================

def registrar_partida(partidas, equipos, eq1_nombre, eq2_nombre, ganador_nombre):
    if eq1_nombre not in equipos or eq2_nombre not in equipos:
        print(" ❌ Error: ambos equipos deben existir.")
        return False
    if eq1_nombre == eq2_nombre:
        print(" ❌ Error: un equipo no puede jugar contra sí mismo.")
        return False
    if ganador_nombre not in (eq1_nombre, eq2_nombre):
        print(" ❌ Error: el ganador debe ser uno de los dos equipos.")
        return False

    equipo1 = equipos[eq1_nombre]
    equipo2 = equipos[eq2_nombre]
    ganador = equipos[ganador_nombre]

    ganador.sumar_puntos(Partida.PUNTOS_POR_VICTORIA)
    nueva_partida = Partida(equipo1, equipo2, ganador)
    partidas.append(nueva_partida)

    print(f" ✅ Partida registrada: {nueva_partida}")
    return True


def calcular_estadisticas(equipos, partidas):
    if not equipos:
        print(" ⚠️ Aún no hay equipos formados para calcular estadísticas.")
        return None

    lista_puntos = [e.puntos for e in equipos.values()]
    promedio = statistics.mean(lista_puntos)
    mediana = statistics.median(lista_puntos)
    desviacion = statistics.stdev(lista_puntos) if len(lista_puntos) > 1 else 0.0

    equipo_lider = max(equipos.values(), key=lambda e: e.puntos)

    # Rendimiento (puntos por partida jugada)
    partidas_por_equipo = {nombre: 0 for nombre in equipos}
    for p in partidas:
        partidas_por_equipo[p.equipo_1.nombre] += 1
        partidas_por_equipo[p.equipo_2.nombre] += 1

    rendimiento = {}
    for nombre, equipo in equipos.items():
        n = partidas_por_equipo[nombre]
        rendimiento[nombre] = round(equipo.puntos / n, 2) if n > 0 else 0.0

    return {
        "promedio": promedio,
        "mediana": mediana,
        "desviacion_estandar": desviacion,
        "equipo_lider": equipo_lider.nombre,
        "rendimiento": rendimiento
    }


def generar_ranking(equipos):
    return sorted(equipos.values(), key=lambda e: e.puntos, reverse=True)


# ==========================================================================
# REPORTES Y CIERRE
# ==========================================================================

def reporte_participantes(participantes):
    print("\n" + "=" * 60)
    print(" LISTA DE PARTICIPANTES REGISTRADOS".center(60))
    print("=" * 60)
    if not participantes:
        print(" No hay participantes registrados todavía.")
        return
    ordenados = sorted(participantes, key=lambda p: p.nombre)
    print(f" {'Nombre':<22}{'Edad':<8}{'Nivel':<8}{'Equipo':<20}")
    print("-" * 60)
    for p in ordenados:
        eq = p.equipo.nombre if p.tiene_equipo() else "Sin equipo"
        print(f" {p.nombre:<22}{p.edad:<8}{p.nivel:<8}{eq:<20}")
    print("-" * 60)
    print(f" Total de participantes: {len(participantes)}")


def reporte_equipos(equipos):
    print("\n" + "=" * 60)
    print(" EQUIPOS FORMADOS".center(60))
    print("=" * 60)
    if not equipos:
        print(" No hay equipos formados todavía.")
        return
    for equipo in equipos.values():
        nombres = ", ".join(j.nombre for j in equipo.jugadores)
        print(f" 🎮 {equipo.nombre:<20} | Integrantes: {nombres}")
    print("-" * 60)
    print(f" Total de equipos: {len(equipos)}")


def reporte_ranking(equipos, partidas):
    print("\n" + "=" * 60)
    print(" RANKING ACTUAL DEL TORNEO".center(60))
    print("=" * 60)
    if not equipos:
        print(" No hay equipos formados todavía.")
        return

    ranking = generar_ranking(equipos)
    print(f" {'Pos.':<6}{'Equipo':<25}{'Puntos':<10}")
    print("-" * 60)
    for pos, equipo in enumerate(ranking, start=1):
        print(f" {pos:<6}{equipo.nombre:<25}{equipo.puntos:<10}")
    print("-" * 60)

    stats = calcular_estadisticas(equipos, partidas)
    if stats:
        print(f" Promedio de puntos por equipo : {stats['promedio']:.2f}")
        print(f" Mediana de puntos             : {stats['mediana']:.2f}")
        print(f" Desviación estándar           : {stats['desviacion_estandar']:.2f}")
        print(f" 🏆 Equipo líder actual         : {stats['equipo_lider']}")
        print("\n Rendimiento (puntos / partidas jugadas):")
        for nombre, r in stats["rendimiento"].items():
            print(f"   · {nombre:<25} → {r:.2f} pts/partida")
    print("=" * 60)


def reporte_completo(participantes, equipos, partidas):
    print("\n" + "#" * 60)
    print(" REPORTE FINAL - TORNEO PIXELES RETRO ".center(60, "#"))
    print("#" * 60)
    reporte_participantes(participantes)
    reporte_equipos(equipos)
    reporte_ranking(equipos, partidas)


# ==========================================================================
# MENÚS DE ENTRADA
# ==========================================================================

def menu_registrar_participante(participantes):
    print("\n--- Registro de nuevo participante ---")
    nombre = input("Nombre del participante: ")
    edad_texto = input("Edad (12-70): ")
    nivel_texto = input("Nivel de experiencia (1-5): ")
    registrar_participante(participantes, nombre, edad_texto, nivel_texto)


def menu_formar_equipo(equipos, participantes):
    print("\n--- Formación de nuevo equipo (manual) ---")
    if len(participantes) < 2:
        print(" ⚠️ Necesitas al menos 2 participantes para formar un equipo.")
        return
    nombre_eq = input("Nombre del equipo: ")
    jug1 = input("Nombre del jugador 1: ").strip()
    jug2 = input("Nombre del jugador 2: ").strip()
    formar_equipo(equipos, nombre_eq, jug1, jug2, participantes)


def menu_formar_equipos_auto(participantes, equipos):
    """Opción del menú para formar equipos balanceados automáticamente."""
    print("\n--- Formación automática de equipos balanceados ---")
    formar_equipos_balanceados(participantes, equipos)


def menu_registrar_partida(partidas, equipos):
    print("\n--- Registro de partida ---")
    if len(equipos) < 2:
        print(" ⚠️ Necesitas al menos 2 equipos para registrar una partida.")
        return
    eq1 = input("Nombre del equipo 1: ").strip()
    eq2 = input("Nombre del equipo 2: ").strip()
    gan = input("Nombre del equipo ganador: ").strip()
    registrar_partida(partidas, equipos, eq1, eq2, gan)


# ==========================================================================
# PROGRAMA PRINCIPAL
# ==========================================================================

NOMBRE_ARCHIVO_DATASET = "participantes_pixeles_retro.csv"


def menu_principal():
    print("\n🕹️  Iniciando Sistema de Gestión - Torneo Pixeles Retro 🕹️\n")

    participantes = cargar_participantes_desde_csv(NOMBRE_ARCHIVO_DATASET)
    equipos = {}
    partidas = []

    opciones = """
==========================================================
   🕹️  TORNEO DE VIDEOJUEGOS RETRO - PIXELES RETRO  🕹️
==========================================================
 1. Registrar participante
 2. Formar equipo (manual)
 3. Formar equipos automáticos (balanceados)   <-- NUEVO
 4. Registrar partida
 5. Ver lista de participantes
 6. Ver equipos formados
 7. Ver ranking y estadísticas
 8. Generar reporte completo
 0. Salir
==========================================================
"""
    while True:
        print(opciones)
        op = input("Selecciona una opción: ").strip()

        if op == "1":
            menu_registrar_participante(participantes)
        elif op == "2":
            menu_formar_equipo(equipos, participantes)
        elif op == "3":
            menu_formar_equipos_auto(participantes, equipos)
        elif op == "4":
            menu_registrar_partida(partidas, equipos)
        elif op == "5":
            reporte_participantes(participantes)
        elif op == "6":
            reporte_equipos(equipos)
        elif op == "7":
            reporte_ranking(equipos, partidas)
        elif op == "8":
            reporte_completo(participantes, equipos, partidas)
        elif op == "0":
            print("\n ¡Gracias por usar el sistema de Pixeles Retro! Hasta pronto 👋")
            break
        else:
            print(" ❌ Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    menu_principal()
    nz