# ============================================================================================================
# PRUEBA: INFERENCIA ESTADÍSTICA
# ============================================================================================================
# Autor        : David González Santibañez
# Curso        : Fundamentos de Análisis de Datos
# Generación   : RTD-25-01-13-0056-1
# Descripción  : Evaluación de satisfacción estudiantil mediante técnicas de inferencia estadística.
#                Incluye simulación de datos, análisis descriptivo, visualización, intervalo de confianza
#                y prueba de hipótesis, según los requerimientos de la prueba.
# ============================================================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st

# Configuración de gráficos
plt.rcParams["figure.figsize"] = (10, 5)

# ============================================================================================================
# FUNCIONES AUXILIARES DE FORMATO DE SALIDA
# ============================================================================================================
def print_titulo(texto, ancho=80):
    """Imprime un título destacado con líneas horizontales de igual."""
    print("\n" + "=" * ancho)
    print(texto.center(ancho))
    print("=" * ancho)

def print_seccion(texto, ancho=80):
    """Imprime un separador de sección con líneas de guiones."""
    print("\n" + "-" * ancho)
    print(texto.center(ancho))
    print("-" * ancho)

def print_ok(mensaje):
    """Imprime un mensaje de éxito."""
    print(f"  ✅ {mensaje}")

def print_info(mensaje):
    """Imprime un mensaje informativo."""
    print(f"  ℹ️  {mensaje}")


def print_tabla(df, titulo=None):
    """
    Imprime un DataFrame dentro de una tabla perfectamente cerrada.
    """
    if df.empty:
        return

    df_str = df.astype(str)
    encabezados = list(df_str.columns)
    filas_datos = df_str.values.tolist()

    anchos = []
    for i, col in enumerate(encabezados):
        max_len = len(col)
        for fila in filas_datos:
            if i < len(fila):
                max_len = max(max_len, len(str(fila[i])))
        anchos.append(max_len + 2)

    num_columnas = len(anchos)
    ancho_total = sum(anchos) + num_columnas - 1

    def linea_superior():
        partes = ["┌"]
        for i, ancho in enumerate(anchos):
            partes.append("─" * ancho)
            if i < num_columnas - 1:
                partes.append("┬")
        partes.append("┐")
        return "".join(partes)

    def linea_separadora():
        partes = ["├"]
        for i, ancho in enumerate(anchos):
            partes.append("─" * ancho)
            if i < num_columnas - 1:
                partes.append("┼")
        partes.append("┤")
        return "".join(partes)

    def linea_inferior():
        partes = ["└"]
        for i, ancho in enumerate(anchos):
            partes.append("─" * ancho)
            if i < num_columnas - 1:
                partes.append("┴")
        partes.append("┘")
        return "".join(partes)

    def formato_fila(fila):
        partes = ["│"]
        for i, ancho in enumerate(anchos):
            if i < len(fila):
                partes.append(str(fila[i]).center(ancho))
            else:
                partes.append(" " * ancho)
            partes.append("│")
        return "".join(partes)

    if titulo:
        print(f"\n{titulo.center(ancho_total)}")

    print(linea_superior())
    print(formato_fila(encabezados))
    print(linea_separadora())
    for fila in filas_datos:
        print(formato_fila(fila))
    print(linea_inferior())
    print()


# ============================================================================================================
# REQUERIMIENTO 1: CARGA Y EXPLORACIÓN DE DATOS
# ============================================================================================================
def cargar_y_explorar_datos():
    """
    Simula un DataFrame de 200 estudiantes con:
    - Edad (18-35)
    - Género (Masculino/Femenino)
    - Puntaje de satisfacción (1-10)
    - Horas de estudio semanales (1-20)
    """
    np.random.seed(42)
    n = 200

    edades = np.random.randint(18, 36, size=n)
    generos = np.random.choice(["Masculino", "Femenino"], size=n)
    puntaje_satisfaccion = np.round(np.random.normal(loc=7.2, scale=1.5, size=n), 1).clip(1, 10)
    horas_estudio = np.random.randint(1, 21, size=n)

    df = pd.DataFrame({
        "Edad": edades,
        "Género": generos,
        "Puntaje_Satisfaccion": puntaje_satisfaccion,
        "Horas_Estudio": horas_estudio
    })

    # Introducir algunos nulos intencionales (~2.5% en puntaje)
    mascara_nulos = np.random.random(n) < 0.025
    df.loc[mascara_nulos, "Puntaje_Satisfaccion"] = np.nan

    return df


def analisis_exploratorio(df):
    """Muestra estadísticas descriptivas y análisis de nulos."""
    print_titulo("REQUERIMIENTO 1: CARGA Y EXPLORACIÓN DE DATOS")

    print_seccion("Primeras filas del DataFrame")
    print_tabla(df.head(10), titulo="Vista previa de los datos")

    # Estadísticas descriptivas de variables numéricas
    desc = df.describe().round(2)
    print_seccion("Estadísticas descriptivas")
    print_tabla(desc, titulo="Resumen estadístico de variables numéricas")

    # Análisis de nulos
    nulos = df.isnull().sum()
    print_seccion("Análisis de valores nulos")
    for col in df.columns:
        if nulos[col] > 0:
            print(f"  • {col}: {nulos[col]} nulos detectados.")
    print("  ℹ️  Los valores nulos en 'Puntaje_Satisfaccion' se pueden tratar imputando con la mediana")
    print("      o la media, dependiendo de la distribución. Para este análisis, se imputarán con la mediana.")

    # Imputar nulos con la mediana
    mediana = df["Puntaje_Satisfaccion"].median()
    df["Puntaje_Satisfaccion"] = df["Puntaje_Satisfaccion"].fillna(mediana)
    print(f"  ✅ Nulos imputados con la mediana ({mediana:.2f}).")

    return df


# ============================================================================================================
# REQUERIMIENTO 2: DISTRIBUCIÓN Y VISUALIZACIÓN
# ============================================================================================================
def distribucion_y_visualizacion(df):
    """Histograma y cálculo de media/varianza con NumPy."""
    print_titulo("REQUERIMIENTO 2: DISTRIBUCIÓN Y VISUALIZACIÓN")

    puntajes = df["Puntaje_Satisfaccion"].values

    # Histograma
    plt.figure(figsize=(8, 5))
    plt.hist(puntajes, bins=15, color="steelblue", edgecolor="black", alpha=0.7)
    plt.axvline(np.mean(puntajes), color="red", linestyle="--", label="Media")
    plt.title("Histograma de Puntajes de Satisfacción")
    plt.xlabel("Puntaje (1-10)")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
    print("\n")

    # Cálculos con NumPy
    media = np.mean(puntajes)
    varianza = np.var(puntajes, ddof=1)   # muestral

    print(f"  • Media del puntaje de satisfacción: {media:.2f}")
    print(f"  • Varianza muestral: {varianza:.2f}")

    print("\n  Interpretación de la distribución:")
    print("  El histograma muestra una forma aproximadamente simétrica alrededor de la media,")
    print("  con una ligera concentración hacia valores altos. Aunque no es perfectamente normal,")
    print("  la distribución se asemeja a una campana, lo que permite aplicar técnicas paramétricas.")


# ============================================================================================================
# REQUERIMIENTO 3: INTERVALO DE CONFIANZA
# ============================================================================================================
def intervalo_confianza(df):
    """Calcula el IC del 95% para la media del puntaje de satisfacción."""
    print_titulo("REQUERIMIENTO 3: INTERVALO DE CONFIANZA")

    puntajes = df["Puntaje_Satisfaccion"].values
    n = len(puntajes)
    media = np.mean(puntajes)
    s = np.std(puntajes, ddof=1)

    # IC con t-Student (σ desconocida)
    alpha = 0.05
    t = st.t.ppf(1 - alpha/2, df=n-1)
    ee = s / np.sqrt(n)
    ic_low = media - t * ee
    ic_high = media + t * ee

    tabla_ic = pd.DataFrame({
        "Parámetro": [
            "Media muestral",
            "Desviación estándar muestral",
            "Tamaño de muestra",
            "Valor crítico t (0.975, 199 gl)",
            "Error estándar",
            "Intervalo de confianza 95%"
        ],
        "Valor": [
            f"{media:.2f}",
            f"{s:.2f}",
            str(n),
            f"{t:.4f}",
            f"{ee:.4f}",
            f"({ic_low:.2f}, {ic_high:.2f})"
        ]
    })
    print_tabla(tabla_ic, titulo="Intervalo de confianza del 95% para la media")

    print("  Interpretación: Con un 95% de confianza, el verdadero puntaje promedio de satisfacción")
    print("  de todos los estudiantes se encuentra entre esos límites. Es decir, si repitiéramos el")
    print("  estudio muchas veces, el 95% de los intervalos calculados contendrían la media real.")


# ============================================================================================================
# REQUERIMIENTO 4: PRUEBA DE HIPÓTESIS
# ============================================================================================================
def prueba_hipotesis(df):
    """Realiza una prueba t de una muestra para H0: media = 7."""
    print_titulo("REQUERIMIENTO 4: PRUEBA DE HIPÓTESIS")

    puntajes = df["Puntaje_Satisfaccion"].values
    n = len(puntajes)
    media = np.mean(puntajes)
    s = np.std(puntajes, ddof=1)

    # Hipótesis
    mu0 = 7.0
    t_stat = (media - mu0) / (s / np.sqrt(n))
    p_valor = 2 * (1 - st.t.cdf(abs(t_stat), df=n-1))   # bilateral

    print(f"  • Hipótesis nula (H₀): μ = {mu0}")
    print(f"  • Hipótesis alternativa (H₁): μ ≠ {mu0}")
    print(f"  • Estadístico t: {t_stat:.4f}")
    print(f"  • Valor-p: {p_valor:.4f}")

    alpha = 0.05
    if p_valor < alpha:
        print(f"  • Como p-valor < {alpha}, se rechaza H₀ al nivel de significancia del 5%.")
        print("    Hay evidencia suficiente para afirmar que la media de satisfacción es diferente de 7.")
    else:
        print(f"  • Como p-valor ≥ {alpha}, no se rechaza H₀ al nivel de significancia del 5%.")
        print("    No hay evidencia suficiente para afirmar que la media sea diferente de 7.")

    print("\n  Interpretación práctica para la empresa:")
    print("  Si la media real es mayor que 7, la empresa puede considerar que el curso supera")
    print("  las expectativas mínimas y puede usar esta información en campañas de marketing.")
    print("  Si no se puede descartar que sea 7, se recomienda investigar áreas de mejora.")


# ============================================================================================================
# REQUERIMIENTO 5: REFLEXIÓN FINAL
# ============================================================================================================
def reflexion_final():
    """Reflexión sobre el rol de la estadística inferencial en la toma de decisiones empresariales."""
    print_titulo("REQUERIMIENTO 5: REFLEXIÓN FINAL")

    print("  La estadística inferencial permite a las empresas tomar decisiones informadas a partir")
    print("  de muestras, cuantificando la incertidumbre mediante intervalos de confianza y pruebas")
    print("  de hipótesis. Esto evita depender de intuiciones y ayuda a asignar recursos de manera")
    print("  eficiente, reduciendo riesgos. Por ejemplo, saber con cierta confianza que la satisfacción")
    print("  supera un umbral puede justificar una inversión en publicidad o en mejoras del curso.")


# ============================================================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================================================
def main():
    # --- Presentación del estudiante ---
    print("\n" + "=" * 60)
    print("INFORMACIÓN DEL ESTUDIANTE".center(60))
    print("=" * 60)
    print(f"Estudiante   : David González Santibañez".center(60))
    print(f"Curso        : Fundamentos de Análisis de Datos".center(60))
    print(f"Generación   : RTD-25-01-13-0056-1".center(60))
    print("=" * 60)

    print_titulo("PRUEBA: INFERENCIA ESTADÍSTICA")

    # 1. Carga y exploración
    df = cargar_y_explorar_datos()
    df = analisis_exploratorio(df)

    # 2. Distribución y visualización
    distribucion_y_visualizacion(df)

    # 3. Intervalo de confianza
    intervalo_confianza(df)

    # 4. Prueba de hipótesis
    prueba_hipotesis(df)

    # 5. Reflexión
    reflexion_final()

    print_titulo("PRUEBA COMPLETADA CON ÉXITO")


if __name__ == "__main__":
    main()