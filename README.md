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
```


## Arquitectura y Funcionamiento del Código

El sistema está estructurado en dos capas principales: el motor de datos y algoritmos (`recomendador.py`) y la interfaz gráfica interactiva (`app.py`).

---

### 1. Motor de Datos y Estructuras (`recomendador.py`)

El archivo `recomendador.py` procesa los datasets en formato CSV y construye las siguientes estructuras de datos optimizadas:

* **Tabla Hash (`TablaHash`):**
  * Implementa la función hash *djb2* con direccionamiento encadenado para el manejo de colisiones.
  * Permite la búsqueda directa de títulos en tiempo constante promedio $O(1)$, así como búsquedas por coincidencias parciales.

* **Árbol Binario de Búsqueda (`BST`):**
  * Mantiene los títulos ordenados alfabéticamente en un árbol binario.
  * Permite realizar recorridos *inorden* y búsquedas por prefijo en tiempo promedio $O(\log n)$.

* **Grafo de Similitud (`GrafoSimilitud`):**
  * Modela los títulos como nodos y sus relaciones de afinidad como aristas pesadas.
  * Calcula la similitud temática entre pares de ítems utilizando el **Índice de Jaccard** sobre sus conjuntos de etiquetas/géneros:
    $$\text{Jaccard}(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
  * Conecta únicamente los ítems cuyo valor de Jaccard supera un umbral definido.

* **Montículo de Prioridad (`heapq`):**
  * Utiliza un *Heap* para la extracción eficiente de los Top N títulos con mayor puntaje sin necesidad de ordenar la base de datos completa.

* **Pila de Historial (`PilaHistorial`):**
  * Estructura LIFO (*Last-In, First-Out*) que almacena el registro de búsquedas efectuadas durante la sesión.

---

### 2. Algoritmo de Recomendación Personalizada

El flujo del motor de recomendación se ejecuta en cinco etapas:

1. **Muestreo de Anclas:** Se seleccionan dinámicamente 5 títulos representativos cumpliendo con las restricciones de edad.
2. **Captura de Preferencias:** El usuario evalúa los títulos marcando aquellos de su interés y excluyendo géneros o ítems no deseados.
3. **Ponderación de Atributos:** Las etiquetas de los ítems aceptados incrementan su peso en un contador de frecuencias, mientras que las elecciones negativas aplican filtros de exclusión estricta.
4. **Evaluación de Candidatos:** Para cada título de la base de datos se calcula un puntaje ponderado que combina la coincidencia de etiquetas con la calificación original (*rating*). Los candidatos con mayor puntuación se procesan mediante la cola de prioridad.
5. **Refinamiento en Segunda Ronda:** El usuario puede seleccionar cualquiera de los resultados obtenidos para otorgar peso adicional a sus etiquetas asociadas y recalcular recomendaciones en tiempo real.

---

### 3. Interfaz de Usuario (`app.py`)

El archivo `app.py` gestiona la presentación web mediante la librería Streamlit:

* **Gestión de Memoria:** Emplea la directiva `@st.cache_resource` para cargar los datasets y construir las estructuras de datos (Tabla Hash, BST y Grafo) una sola vez durante el inicio de la aplicación.
* **Control de Acceso:** Aplica filtros automáticos sobre las estructuras de datos según el perfil de edad definido en el panel lateral.
* **Navegación:** Proporciona interfaces dedicadas para búsqueda por nombre, exploración jerárquica de géneros, filtros combinados y el cuestionario interactivo de recomendación.
## Ejecución del Proyecto

Para iniciar la interfaz web interactiva en tu entorno local, ejecuta el siguiente comando en la terminal:

```bash
python -m streamlit run app.py
