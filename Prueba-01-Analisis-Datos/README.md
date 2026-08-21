# Prueba 1: Introducción al análisis de datos
[![Excel](https://img.shields.io/badge/Excel-F%C3%B3rmulas_y_An%C3%A1lisis-green?logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/)

## 📜 Enunciado
"En una empresa de retail, te entregan una base de datos de ventas y te piden analizar las tendencias. Describe las 4 etapas principales del proceso de análisis de datos que seguirías y explica brevemente qué harías en cada una. Además, se te proporciona un conjunto de datos con celdas vacías, filas duplicadas, formatos de fecha variables y errores de escritura en los nombres de productos. Enumera 4 técnicas específicas de Excel que utilizarías para limpiar estos datos y explica por qué las usarías."

## 🎯 Objetivo
Limpiar datos y calcular métricas de ventas.

## 📊 Resumen Ejecutivo (Impacto)
- 🔍 **Exploración:** Identifiqué 316 registros y 7 columnas, detectando 10 duplicados y 17 celdas vacías en la columna Producto.
- 🧹 **Limpieza:** Normalicé fechas (DD/MM/AAAA vs MM/DD/AAAA) y corregí errores de tipeo en nombres de productos (ej. "Gaming" -> "Gaming").
- 📈 **Análisis:** Calculé estadísticas descriptivas (promedio, mediana, desviación) y gráficos de tendencia mensual.
- 💡 **Conclusión:** La categoría "Computación" es la de mayor ingreso, pero la categoría "Tecnología" presenta mejor margen de ganancia.

## 🏆 Resultados Destacados
| Resultado | Herramienta | Evidencia |
| :--- | :--- | :--- |
| Análisis exploratorio y limpieza | Excel | ![Análisis](pregunta1_analisis_conceptual.png) |
| Estadísticas y visualización | Excel | ![Estadísticas](pregunta2_estadisticas_descriptivas.png) |
| Modelo de Margen (BUSCARV + DAX) | Excel | ![Margen](pregunta3_margen_ganancia.png) |

## 📸 Resultados Visuales
### 1. Análisis Conceptual
![Análisis](pregunta1_analisis_conceptual.png)

### 2. Estadísticas Descriptivas
![Estadísticas](pregunta2_estadisticas_descriptivas.png)

### 3. Gráfico de Tendencia
![Gráfico](pregunta2_grafico_tendencia.png)

### 4. Margen de Ganancia con BUSCARV
![Margen](pregunta3_margen_ganancia.png)

## 🛠️ Mejora Post-Evaluación
Tras recibir feedback del docente, agregué el cálculo de **Margen de Ganancia** usando BUSCARV. Como mi Mac OS Mojave no tiene Power Pivot, escribí la fórmula DAX equivalente como referencia para demostrar mi comprensión del lenguaje (la cual está documentada en el archivo Excel).

## 💡 Conclusión de Negocio
Este modelo permitió identificar qué productos generan mayores márgenes, permitiendo optimizar el inventario y las estrategias de venta.

📄 **Ver enunciado original:** [⬇️ Descargar enunciado (PDF)](https://github.com/icqdgonzalezs/Sence-talentodigital-pruebas/raw/main/Prueba-01-Analisis-Datos/enunciado.pdf)

---
**[⬆️ Volver al repositorio principal](../README.md)**
