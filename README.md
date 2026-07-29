# NEXUS Multimedia — Sistema de Recomendaciones

Un sistema de recomendación interactivo para videojuegos (Steam) y películas (IMDb) desarrollado en Python. La aplicación combina estructuras de datos avanzadas construidas desde cero con un motor de filtrado por similitud y una interfaz web moderna en Streamlit.

---

## Características Principales

* **Búsqueda Avanzada:** Búsqueda exacta y por coincidencias parciales de títulos en tiempo óptimo.
* **Exploración por Géneros:** Navegación a través de una jerarquía estructurada de categorías multimedia.
* **Recomendación Personalizada:** Algoritmo dinámico que pondera tus gustos, rechaza lo que no te interesa y refina los resultados en tiempo real.
* **Control Parental Automático:** Filtro estricto por edad que bloquea contenido para adultos si el usuario es menor de 18 años.
* **Grafo de Similitudes:** Red interconectada de ítems basada en el grado de coincidencia temática.

---

## Estructuras de Datos Implementadas

Para garantizar alta eficiencia sin depender únicamente de librerías externas, el motor principal (`recomendador.py`) implementa:

1. **Tabla Hash (Direccionamiento Encadenado):**
   * Función Hash *djb2* para asignación de claves.
   * Permite búsquedas directas en tiempo promedio $O(1)$.
2. **Árbol Binario de Búsqueda (BST):**
   * Mantiene los títulos ordenados alfabéticamente.
   * Facilita el autocompletado y recorridos inorden en $O(\log n)$ promedio.
3. **Grafo de Similitud (Jaccard Index):**
   * Conecta ítems mediante aristas según la intersección de sus etiquetas y géneros.
4. **Montículo / Cola de Prioridad (`Heap`):**
   * Extracción eficiente de los Top N elementos mejor puntuados.
5. **Pila (LIFO):**
   * Mantiene el historial de búsquedas del usuario durante la sesión.

---

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Web:** Streamlit
* **Fuentes de Datos:** Datasets procesados en CSV (`steam_games_2026.csv` e `imdb_top_1000.csv`)

---

## Estructura del Proyecto

```text
├── app.py                 # Interfaz gráfica y control de flujo (Streamlit)
├── recomendador.py        # Motor principal y estructuras de datos
├── steam_games_2026.csv   # Dataset de videojuegos de Steam
├── imdb_top_1000.csv      # Dataset de películas top de IMDb
├── requirements.txt       # Lista de dependencias
└── README.md              # Documentación del proyecto

## ⚙️ Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITTORIO.git](https://github.com/TU_USUARIO/TU_REPOSITTORIO.git)
cd TU_REPOSITTORIO
