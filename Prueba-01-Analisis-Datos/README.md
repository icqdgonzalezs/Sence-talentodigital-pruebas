cd "Prueba-01-Analisis-Datos"
cat > README.md << 'EOF'
# Prueba 1: Introducción al análisis de datos
[![Excel](https://img.shields.io/badge/Excel-F%C3%B3rmulas_y_An%C3%A1lisis-green?logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/)

## 📜 Enunciado
"En una empresa de retail, te entregan una base de datos de ventas y te piden analizar las tendencias..."

## 🎯 Objetivo
Limpiar datos y calcular métricas de ventas.

## 📊 Resumen Ejecutivo (Impacto)
- 🔍 **Exploración:** Identifiqué 316 registros y 7 columnas, detectando 10 duplicados y 17 celdas vacías en la columna Producto.
- 🧹 **Limpieza:** Normalicé fechas (DD/MM/AAAA vs MM/DD/AAAA) y corregí errores de tipeo.
- 📈 **Análisis:** Calculé estadísticas descriptivas y gráficos de tendencia.
- 💡 **Conclusión:** "Computación" genera mayor ingreso, pero "Tecnología" presenta mejor margen.

## 🏆 Resultados Destacados
| Resultado | Herramienta | Evidencia |
| :--- | :--- | :--- |
| Análisis exploratorio y limpieza | Excel | ![Análisis](pregunta1_limpieza.png) |
| Estadísticas y visualización | Excel | ![Estadísticas](pregunta2_estadisticas_descriptivas.png) |
| Modelo de Margen (BUSCARV + DAX) | Excel | ![Margen](pregunta3_margen_ganancia.png) |

## 🧹 Técnicas de Limpieza Aplicadas (Pregunta 1)
| Problema Detectado | Técnica de Excel Utilizada | Resultado |
| :--- | :--- | :--- |
| 10-27 celdas vacías | **Ir a Especial → Celdas en blanco** | Datos completados o filas eliminadas para análisis. |
| 10 filas duplicadas | **Quitar duplicados (Datos)** | Se eliminaron duplicados exactos y se revisaron los casos ambiguos. |
| Fechas en 3 formatos | **Texto en columnas + =FECHA()** | Unificación a formato único DD/MM/AAAA. |
| Errores de tipeo (Mouse vs mouse) | **=NOMPROPIO() + Buscar/Reemplazar** | Normalización de nombres de productos y categorías. |

## 📸 Resultados Visuales
### 1. Análisis Conceptual y Limpieza
![Análisis](pregunta1_limpieza.png)

### 2. Estadísticas Descriptivas
![Estadísticas](pregunta2_estadisticas_descriptivas.png)

### 3. Margen de Ganancia con BUSCARV
![Margen](pregunta3_margen_ganancia.png)

## 🛠️ Mejora Post-Evaluación
Tras recibir feedback del docente, agregué el cálculo de **Margen de Ganancia** usando BUSCARV. Como mi Mac OS Mojave no tiene Power Pivot, escribí la fórmula DAX equivalente como referencia (documentada en el Excel).

## 💡 Conclusión de Negocio
Este modelo permitió identificar qué productos generan mayores márgenes, permitiendo optimizar el inventario y las estrategias de venta.

📄 **Ver enunciado original:** [⬇️ Descargar enunciado (PDF)](https://github.com/icqdgonzalezs/Sence-talentodigital-pruebas/raw/main/Prueba-01-Analisis-Datos/enunciado.pdf)

---
**[⬆️ Volver al repositorio principal](../README.md)**
EOF
cd ..
