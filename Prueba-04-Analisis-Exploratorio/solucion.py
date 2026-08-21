"""
================================================================================
 ANÁLISIS VISUAL DE DATOS DE VIDEOJUEGOS - SEABORN Y MATPLOTLIB
================================================================================
Estudiante   : David González Santibañez
Curso        : Fundamentos de Análisis de Datos
Generación   : RTD-25-01-13-0056-1
Prueba       : 4 - Análisis exploratorio y personalización de gráficos

Descripción:
Este programa resuelve completamente la Prueba 4 utilizando las librerías
Seaborn y Matplotlib para crear visualizaciones que revelan relaciones
complejas en los datos de videojuegos.
Incluye:
- Pairplot con diferenciación por plataforma.
- Violinplot de puntajes de crítica por plataforma.
- Mapa de calor de correlaciones.
- Gráfico de barras personalizado con anotaciones y guardado en PNG.

Además, guarda TODOS los gráficos generados como archivos PNG y registra
la salida de consola en un archivo de log para facilitar la revisión.

Cada requerimiento de la rúbrica está implementado y documentado.
================================================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# =============================================================================
# CONFIGURACIÓN DE SALIDA DE CONSOLA A ARCHIVO
# =============================================================================
# Redirigimos la salida estándar a un archivo de log para adjuntar como evidencia
log_file = open('salida_consola.txt', 'w', encoding='utf-8')
sys.stdout = log_file

# =============================================================================
# FUNCIONES AUXILIARES PARA FORMATO DE SALIDA
# =============================================================================
def print_titulo(texto, ancho=70):
    """Imprime un título destacado con borde doble."""
    print("\n" + "╔" + "═" * (ancho - 2) + "╗")
    print(f"║{texto.center(ancho - 2)}║")
    print("╚" + "═" * (ancho - 2) + "╝")

def print_seccion(texto, ancho=70):
    """Imprime un separador de sección."""
    print("\n" + "┌" + "─" * (ancho - 2) + "┐")
    print(f"│{texto.center(ancho - 2)}│")
    print("└" + "─" * (ancho - 2) + "┘")

def print_ok(mensaje):
    """Imprime un mensaje de éxito."""
    print(f"  ✅ {mensaje}")

def print_info(mensaje):
    """Imprime un mensaje informativo."""
    print(f"  ℹ️  {mensaje}")

def print_tabla(df, titulo=None):
    """
    Imprime un DataFrame en formato tabla con bordes completos,
    columnas alineadas uniformemente y celdas encerradas.
    """
    if df.empty:
        return

    df_str = df.astype(str)
    encabezados = list(df_str.columns)
    filas = [encabezados] + df_str.values.tolist()

    anchos = []
    for i, col in enumerate(encabezados):
        max_len = len(col)
        for fila in filas[1:]:
            if i < len(fila):
                max_len = max(max_len, len(str(fila[i])))
        anchos.append(max_len + 2)

    def linea_superior():
        partes = ["┌"]
        for i, ancho in enumerate(anchos):
            if i > 0: partes.append("┬")
            partes.append("─" * ancho)
        partes.append("┐")
        return "".join(partes)

    def linea_separadora():
        partes = ["├"]
        for i, ancho in enumerate(anchos):
            if i > 0: partes.append("┼")
            partes.append("─" * ancho)
        partes.append("┤")
        return "".join(partes)

    def linea_inferior():
        partes = ["└"]
        for i, ancho in enumerate(anchos):
            if i > 0: partes.append("┴")
            partes.append("─" * ancho)
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
        print("\n" + "┌" + "─" * (sum(anchos) + len(anchos) - 1) + "┐")
        print(f"│ {titulo.center(sum(anchos) + len(anchos) - 3)} │")
        print("├" + "─" * (sum(anchos) + len(anchos) - 1) + "┤")

    print(linea_superior())
    print(formato_fila(encabezados))
    print(linea_separadora())
    for fila in filas[1:]:
        print(formato_fila(fila))
    print(linea_inferior())


# =============================================================================
# 0. CARGA DE DATOS Y PREPARACIÓN INICIAL
# =============================================================================
def cargar_datos():
    print_titulo("CARGA DEL DATASET", 70)
    try:
        df = pd.read_csv('videojuegos.csv', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv('videojuegos.csv', encoding='latin-1')

    info_dict = {
        "Archivo": ["videojuegos.csv"],
        "Registros": [str(df.shape[0])],
        "Columnas": [str(df.shape[1])],
        "Codificación": ["utf-8"]
    }
    df_info = pd.DataFrame(info_dict)
    print_tabla(df_info, "INFORMACIÓN DEL ARCHIVO")

    print_tabla(df.head(5), "PRIMEROS 5 REGISTROS")

    nulos = df.isna().sum()
    df_nulos = pd.DataFrame({
        "Columna": nulos.index,
        "Nulos": nulos.values,
        "Completos": df.shape[0] - nulos.values
    })
    print_tabla(df_nulos, "ANÁLISIS DE VALORES NULOS")
    return df


df = cargar_datos()

# =============================================================================
# CONFIGURACIÓN GLOBAL DE SEABORN
# =============================================================================
sns.set_style("whitegrid")

# =============================================================================
# PARTE 1: ANÁLISIS VISUAL CON SEABORN
# =============================================================================

# -----------------------------------------------------------------------------
# REQUERIMIENTO 1: GRÁFICO DE PARES (pairplot) – 2 PUNTOS
# -----------------------------------------------------------------------------
def crear_pairplot(df):
    print_seccion("REQUERIMIENTO 1: PAIRPLOT (2 puntos)", 70)
    print_info("Generando pairplot...")

    vars_num = ['Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Critica_Puntaje']
    g = sns.pairplot(
        df, vars=vars_num,
        hue='Plataforma', palette='Set2',
        diag_kind='kde', plot_kws={'alpha': 0.7, 's': 40}, height=2.5
    )
    g.fig.suptitle('Relación entre ventas regionales y puntaje de crítica\n(Diferenciado por plataforma)',
                   y=1.02, fontsize=14, fontweight='bold')
    # Guardar el gráfico
    g.savefig('pairplot.png', dpi=150, bbox_inches='tight')
    plt.show()
    print_ok("Pairplot generado y guardado como 'pairplot.png'.")


crear_pairplot(df)


# -----------------------------------------------------------------------------
# REQUERIMIENTO 2: GRÁFICO DE VIOLÍN (violinplot) – 2 PUNTOS
# -----------------------------------------------------------------------------
def crear_violinplot(df):
    print_seccion("REQUERIMIENTO 2: VIOLINPLOT (2 puntos)", 70)
    print_info("Generando violinplot...")

    df_puntaje = df.dropna(subset=['Critica_Puntaje'])
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Plataforma', y='Critica_Puntaje', data=df_puntaje,
                   hue='Plataforma', palette='Set2', inner='quartile',
                   linewidth=1.2, legend=False)
    sns.swarmplot(x='Plataforma', y='Critica_Puntaje', data=df_puntaje,
                  color='black', size=3, alpha=0.4)
    plt.title('Distribución del puntaje de crítica por plataforma', fontsize=14, fontweight='bold')
    plt.xlabel('Plataforma')
    plt.ylabel('Puntaje de crítica (0-100)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('violinplot.png', dpi=150, bbox_inches='tight')
    plt.show()
    print_ok("Violinplot generado y guardado como 'violinplot.png'.")


crear_violinplot(df)


# -----------------------------------------------------------------------------
# REQUERIMIENTO 3: MAPA DE CALOR (heatmap) – 2 PUNTOS
# -----------------------------------------------------------------------------
def crear_heatmap(df):
    print_seccion("REQUERIMIENTO 3: HEATMAP (2 puntos)", 70)
    print_info("Generando heatmap de correlación...")

    vars_num = ['Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Critica_Puntaje']
    corr = df[vars_num].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                vmin=-1, vmax=1, linewidths=0.5, linecolor='gray',
                square=True, cbar_kws={'shrink': 0.8})
    plt.title('Matriz de correlación de variables numéricas', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('heatmap.png', dpi=150, bbox_inches='tight')
    plt.show()
    print_ok("Heatmap generado y guardado como 'heatmap.png'.")


crear_heatmap(df)


# =============================================================================
# PARTE 2: PERSONALIZACIÓN DE GRÁFICOS CON MATPLOTLIB
# =============================================================================

# -----------------------------------------------------------------------------
# REQUERIMIENTO 4: PREPARACIÓN DE DATOS – 1.5 PUNTOS
# -----------------------------------------------------------------------------
def preparar_datos_barras(df):
    print_seccion("REQUERIMIENTO 4: PREPARACIÓN DE DATOS (1.5 puntos)", 70)
    print_info("Calculando ventas globales y promedios por género...")

    df['Ventas_Globales'] = df['Ventas_NA'] + df['Ventas_EU'] + df['Ventas_JP']
    ventas_genero = df.groupby('Genero')['Ventas_Globales'].mean().sort_values(ascending=False)

    df_prom = pd.DataFrame({
        "Género": ventas_genero.index,
        "Promedio Ventas Globales": [f"{v:.2f}" for v in ventas_genero.values]
    })
    print_tabla(df_prom, "PROMEDIO DE VENTAS GLOBALES POR GÉNERO")
    return ventas_genero


ventas_genero = preparar_datos_barras(df)


# -----------------------------------------------------------------------------
# REQUERIMIENTO 5: GRÁFICO DE BARRAS – 1.5 PUNTOS
# -----------------------------------------------------------------------------
def crear_grafico_barras(ventas_genero):
    print_seccion("REQUERIMIENTO 5: GRÁFICO DE BARRAS (1.5 puntos)", 70)
    print_info("Creando gráfico de barras personalizado...")

    generos = ventas_genero.index
    medias = ventas_genero.values
    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(generos, medias, color='steelblue', edgecolor='black',
                    linewidth=1.2, width=0.6)
    ax.set_title('Promedio de Ventas Globales por Género de Videojuego',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Género', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ventas Globales Promedio (millones)', fontsize=12, fontweight='bold')
    return fig, ax, barras, medias


fig, ax, barras, medias = crear_grafico_barras(ventas_genero)


# -----------------------------------------------------------------------------
# REQUERIMIENTO 6: ANOTACIONES, LÍMITES Y GUARDADO – 1 PUNTO
# -----------------------------------------------------------------------------
def personalizar_y_guardar(fig, ax, barras, medias):
    print_seccion("REQUERIMIENTO 6: ANOTACIONES Y GUARDADO (1 punto)", 70)
    print_info("Añadiendo anotaciones y límites...")

    max_media = medias.max()
    ax.set_ylim(0, max_media * 1.15)

    for barra, valor in zip(barras, medias):
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() + 0.02,
                f'{valor:.2f}',
                ha='center', va='bottom',
                fontsize=11, fontweight='bold', color='black')

    ax.yaxis.grid(True, linestyle='--', alpha=0.6)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig('ventas_por_genero_personalizado.png', dpi=150, bbox_inches='tight')
    plt.show()
    print_ok("Gráfico de barras guardado como 'ventas_por_genero_personalizado.png'.")


personalizar_y_guardar(fig, ax, barras, medias)

# Cerrar el archivo de log y restaurar salida estándar
log_file.close()
sys.stdout = sys.__stdout__
print("✅ Ejecución completada. Todos los gráficos y el log 'salida_consola.txt' han sido generados.")