import streamlit as st
import heapq
import os
import random
from collections import Counter

# ── Import all logic from recomendador.py ──────────────────────
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recomendador import (
    JERARQUIA, GENEROS_JUEGOS, GENEROS_PELICULAS,
    ANCLAS_JUEGOS_MAYOR, ANCLAS_JUEGOS_MENOR,
    ANCLAS_PELIS_MAYOR, ANCLAS_PELIS_MENOR,
    TablaHash, BST, GrafoSimilitud,
    Videojuego, Pelicula,
    cargar_base_datos, _calcular_heap,
)

# ── Page config ─────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS Multimedia",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

/* Configuración global de fuentes */
html, body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #0b0f17;
    color: #f8fafc;
}

/* Aplicar tipografía general sin romper íconos */
.stMarkdown, p, label, .stSelectbox, .stRadio, .stSlider {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Fondo de la aplicación */
.stApp {
    background-color: #0b0f17 !important;
    color: #f8fafc !important;
}

/* Encabezados modernos */
h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
    letter-spacing: -0.5px;
}

/* ════════════════════════════════════════════════════════════════
   BARRA LATERAL (SIDEBAR)
   ════════════════════════════════════════════════════════════════ */

[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1f2937 !important;
}

[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span {
    color: #ffffff !important;
}

/* Botones de radio en la Sidebar */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: #1f2937 !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin-bottom: 6px !important;
    width: 100% !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    border-color: #3b82f6 !important;
    background: #2563eb22 !important;
}

/* ════════════════════════════════════════════════════════════════
   TARJETAS Y DESPLEGABLES (EXPANDERS)
   ════════════════════════════════════════════════════════════════ */

/* Estilo para los desplegables (expanders) */
.stExpander {
    background-color: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 10px !important;
    margin-bottom: 10px !important;
}

.stExpander [data-testid="stExpanderToggleIcon"] {
    color: #60a5fa !important;
}

/* Tarjetas de resultados */
.card {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 14px !important;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    transition: all 0.2s ease;
}

.card:hover {
    border-color: #3b82f6 !important;
}

.card-rank {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 12px;
    font-weight: 700;
    color: #60a5fa !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.card-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 20px;
    font-weight: 700;
    color: #ffffff !important;
    margin-bottom: 10px;
}

.card-rating {
    display: inline-block;
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.4);
    color: #93c5fd !important;
    font-size: 13px;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 20px;
    margin-bottom: 10px;
}

.card-meta { 
    font-size: 13px; 
    color: #9ca3af !important; 
    margin: 4px 0; 
}

.card-meta span { 
    color: #ffffff !important; 
    font-weight: 600;
}

.tag {
    display: inline-block;
    background: #1f2937;
    border: 1px solid #374151;
    color: #f3f4f6 !important;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 8px;
    margin: 3px 3px 3px 0;
}

.section-header {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px;
    font-weight: 700;
    color: #60a5fa !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin: 28px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1f2937;
}

/* Botones */
.stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.2rem !important;
}

.stButton > button:hover {
    background: #1d4ed8 !important;
}

/* Cajas de información */
.info-box {
    background: rgba(30, 58, 138, 0.3);
    border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: #e0f2fe !important;
    margin: 12px 0;
}

.warning-box {
    background: rgba(120, 53, 15, 0.3);
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: #fef3c7 !important;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Data loading (cached) ────────────────────────────────────────
@st.cache_resource(show_spinner="Cargando base de datos y estructuras...")
def cargar_todo():
    juegos, peliculas = cargar_base_datos()

    hash_j = TablaHash(); bst_j = BST()
    hash_p = TablaHash(); bst_p = BST()
    for j in juegos:
        hash_j.insertar(j); bst_j.insertar(j)
    for p in peliculas:
        hash_p.insertar(p); bst_p.insertar(p)

    grafo_j = GrafoSimilitud.construir(juegos,    umbral=0.25)
    grafo_p = GrafoSimilitud.construir(peliculas, umbral=0.20)

    return juegos, peliculas, hash_j, bst_j, hash_p, bst_p, grafo_j, grafo_p

juegos, peliculas, hash_j, bst_j, hash_p, bst_p, grafo_j, grafo_p = cargar_todo()


# ── Helpers ──────────────────────────────────────────────────────
def filtrar_edad(base, es_mayor):
    return base if es_mayor else [i for i in base if not i.es_adultos]

def heap_to_list(items, top_n=20):
    h = []
    for item in items:
        heapq.heappush(h, (-item.calificacion, item))
    result = []
    while h and len(result) < top_n:
        _, item = heapq.heappop(h)
        result.append(item)
    return result

def render_card(item, rank):
    if isinstance(item, Videojuego):
        precio_txt = "Gratis" if item.precio in ("0","0.0","0.00") else f"${item.precio}"
        try:    rev_txt = f"{int(item.reviews):,}".replace(",",".")
        except: rev_txt = item.reviews
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in item.generos_raw[:8])
        st.markdown(f"""
        <div class="card">
            <div class="card-rank">#{rank}</div>
            <div class="card-title">{item.nombre}</div>
            <div class="card-rating">⭐ {item.calificacion:.1f} / 10</div>
            <div class="card-meta">💰 Precio: <span>{precio_txt}</span> &nbsp;|&nbsp; 🎮 Steam Deck: <span>{item.steam_deck}</span></div>
            <div class="card-meta">📊 Reseñas: <span>{rev_txt}</span> &nbsp;|&nbsp; 👥 Propietarios est.: <span>{item.owners}</span></div>
            <div style="margin-top:10px">{tags_html}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card">
            <div class="card-rank">#{rank}</div>
            <div class="card-title">{item.nombre}</div>
            <div class="card-rating">⭐ {item.calificacion:.1f} / 10</div>
            <div class="card-meta">⏳ Duración: <span>{item.duracion}</span></div>
            <div class="card-meta" style="margin-top:8px;color:#c9d1d9;font-size:13px">{item.sinopsis[:200]}...</div>
        </div>""", unsafe_allow_html=True)

def render_results(items):
    if not items:
        st.markdown('<div class="warning-box">No se encontraron resultados para esta busqueda.</div>',
                    unsafe_allow_html=True)
        return
    cols = st.columns(2)
    for i, item in enumerate(items):
        with cols[i % 2]:
            render_card(item, i + 1)


# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Recomendador Multimedia")
    st.markdown("*Proyecto — Estructuras de Datos*")
    st.divider()

    edad = st.number_input("Tu edad", min_value=1, max_value=99, value=18, step=1)
    es_mayor = edad >= 18
    if es_mayor:
        st.success("Acceso completo")
    else:
        st.warning("Modo seguro activado")

    st.divider()
    tipo = st.radio("¿Qué deseas explorar?", ["Videojuegos", "Peliculas"])
    es_juego = tipo == "Videojuegos"
    base_raw = juegos if es_juego else peliculas
    base     = filtrar_edad(base_raw, es_mayor)
    tabla_h  = hash_j if es_juego else hash_p
    bst      = bst_j  if es_juego else bst_p
    grafo    = grafo_j if es_juego else grafo_p

    st.divider()
    modo = st.radio("Modo de busqueda", [
        "Buscar por nombre",
        "Explorar por genero",
        "Multiples generos",
        "Recomendacion personalizada",
    ])

    st.divider()
    st.caption(f"Base: {len(juegos)} juegos · {len(peliculas)} peliculas")


# ── Main header ──────────────────────────────────────────────────
st.markdown(f"# {'🎮 Videojuegos' if es_juego else '🎬 Peliculas'}")
st.markdown(f"**Modo:** {modo}")
st.divider()


# ════════════════════════════════════════════════════════════════
# MODO 1 — BUSCAR POR NOMBRE
# ════════════════════════════════════════════════════════════════
if modo == "Buscar por nombre":
    termino = st.text_input("Nombre o parte del nombre", placeholder="Ej: portal, godfather, minecraft...")

    if termino:
        base_nombres = set(i.nombre.lower() for i in base)

        exacto = tabla_h.buscar_exacto(termino)
        if exacto and exacto.nombre.lower() in base_nombres:
            st.markdown('<div class="section-header">Coincidencia exacta</div>', unsafe_allow_html=True)
            render_results([exacto])
        else:
            por_prefijo = [i for i in bst.buscar_prefijo(termino) if i.nombre.lower() in base_nombres]
            por_hash    = [i for i in tabla_h.buscar_parcial(termino) if i.nombre.lower() in base_nombres]
            vistos      = set(i.nombre for i in por_prefijo)
            resultados  = por_prefijo + [i for i in por_hash if i.nombre not in vistos]

            if not resultados:
                st.markdown(f'<div class="warning-box">No se encontro "{termino}" en la base de datos.</div>',
                            unsafe_allow_html=True)
            else:
                top = heap_to_list(resultados, top_n=20)
                st.markdown(f'<div class="section-header">{len(resultados)} resultado(s) para "{termino}"</div>',
                            unsafe_allow_html=True)
                render_results(top)


# ════════════════════════════════════════════════════════════════
# MODO 2 — EXPLORAR POR GENERO
# ════════════════════════════════════════════════════════════════
elif modo == "Explorar por genero":
    raices = GENEROS_JUEGOS if es_juego else GENEROS_PELICULAS
    col1, col2 = st.columns(2)
    with col1:
        principal = st.selectbox("Genero principal", raices)
    with col2:
        subs = list(JERARQUIA.get(principal, {}).keys())
        sub  = st.selectbox("Subgenero", subs)

    if st.button("Buscar", type="primary"):
        resultados = [i for i in base if i.pertenece_a(principal, sub)]
        top = heap_to_list(resultados, top_n=20)
        st.markdown(f'<div class="section-header">Top {len(top)} — {principal} › {sub}</div>',
                    unsafe_allow_html=True)
        render_results(top)


# ════════════════════════════════════════════════════════════════
# MODO 3 — MULTIPLES GENEROS
# ════════════════════════════════════════════════════════════════
elif modo == "Multiples generos":
    raices = GENEROS_JUEGOS if es_juego else GENEROS_PELICULAS
    st.markdown('<div class="info-box">Selecciona hasta 3 generos. Solo apareceran titulos que pertenezcan a todos.</div>',
                unsafe_allow_html=True)

    generos_sel = []
    for idx in range(1, 4):
        with st.expander(f"Genero {idx}", expanded=(idx == 1)):
            p = st.selectbox(f"Genero principal {idx}", ["(ninguno)"] + raices, key=f"mg_p{idx}")
            if p != "(ninguno)":
                subs = list(JERARQUIA.get(p, {}).keys())
                s = st.selectbox(f"Subgenero {idx}", subs, key=f"mg_s{idx}")
                generos_sel.append((p, s))

    if st.button("Buscar combinacion", type="primary") and generos_sel:
        resultados = [i for i in base if all(i.pertenece_a(p, s) for p, s in generos_sel)]
        if not resultados:
            desc = " + ".join(s for _, s in generos_sel)
            st.markdown(f'<div class="warning-box">No hay titulos que combinen: {desc}</div>',
                        unsafe_allow_html=True)
        else:
            top = heap_to_list(resultados, top_n=20)
            desc = " + ".join(s for _, s in generos_sel)
            st.markdown(f'<div class="section-header">Top {len(top)} — {desc}</div>',
                        unsafe_allow_html=True)
            render_results(top)


# ════════════════════════════════════════════════════════════════
# MODO 4 — RECOMENDACION PERSONALIZADA
# ════════════════════════════════════════════════════════════════
elif modo == "Recomendacion personalizada":
    accion_txt = "jugado" if es_juego else "visto"
    anclas = (ANCLAS_JUEGOS_MAYOR if es_mayor else ANCLAS_JUEGOS_MENOR) if es_juego \
             else (ANCLAS_PELIS_MAYOR if es_mayor else ANCLAS_PELIS_MENOR)

    # Inicializar muestra en session_state para que no cambie con cada interaccion
    if "muestra" not in st.session_state or st.session_state.get("tipo_muestra") != tipo:
        st.session_state.muestra = random.sample(anclas, min(5, len(anclas)))
        st.session_state.tipo_muestra = tipo
        st.session_state.resultados_pref = None
        st.session_state.pesos_totales   = None
        st.session_state.negativos       = None
        st.session_state.excluidos       = None

    st.markdown('<div class="info-box">Responde sobre cada titulo para que el sistema detecte tus gustos.</div>',
                unsafe_allow_html=True)

    contador_positivo = Counter()
    contador_negativo = []
    contador_conocido = Counter()
    nombres_excluidos = set()
    respuestas_validas = 0

    opciones_resp = ["No lo conozco (?)", f"Lo conozco pero no lo he {accion_txt} (k)",
                     "Lo conoci y NO me gusto (n)", "Lo conoci y me gusto (s)"]

    for nombre_ancla, tags in st.session_state.muestra:
        st.markdown(f"**{nombre_ancla}**")
        resp = st.radio(
            f"Tu opinion sobre '{nombre_ancla}'",
            opciones_resp,
            key=f"pref_{nombre_ancla}",
            label_visibility="collapsed",
            horizontal=True,
        )

        if resp == "Lo conoci y me gusto (s)":
            intensidad = st.slider(f"¿Cuanto te gusto? (1=poco, 5=mucho)", 1, 5, 3,
                                   key=f"int_{nombre_ancla}")
            for tag in tags:
                contador_positivo[tag] += intensidad
            nombres_excluidos.add(nombre_ancla.lower())
            respuestas_validas += 1
        elif resp == "Lo conoci y NO me gusto (n)":
            contador_negativo.extend(tags)
            nombres_excluidos.add(nombre_ancla.lower())
            respuestas_validas += 1
        elif resp == f"Lo conozco pero no lo he {accion_txt} (k)":
            for tag in tags:
                contador_conocido[tag] += 0.3
            respuestas_validas += 1

        st.divider()

    # Mostrar perfil detectado
    pesos_totales = Counter(contador_positivo)
    for tag, p in contador_conocido.items():
        pesos_totales[tag] += p

    if pesos_totales:
        st.markdown('<div class="section-header">Perfil de gustos detectado</div>', unsafe_allow_html=True)
        top_tags = pesos_totales.most_common(6)
        for tag, peso in top_tags:
            st.progress(min(peso / 5.0, 1.0), text=f"{tag}  ({peso:.1f})")

    if st.button("Generar recomendaciones", type="primary"):
        if respuestas_validas == 0:
            st.warning("Responde al menos una pregunta para continuar.")
        else:
            heap = _calcular_heap(base, pesos_totales, contador_negativo, nombres_excluidos)
            top5 = []
            h_temp = list(heap)
            heapq.heapify(h_temp)
            while h_temp and len(top5) < 5:
                _, it = heapq.heappop(h_temp)
                top5.append(it)

            st.session_state.resultados_pref = top5
            st.session_state.pesos_totales   = pesos_totales
            st.session_state.negativos       = contador_negativo
            st.session_state.excluidos       = nombres_excluidos

    if st.session_state.get("resultados_pref"):
        top5 = st.session_state.resultados_pref
        st.markdown('<div class="section-header">Primera ronda — Top 5 para ti</div>', unsafe_allow_html=True)
        render_results(top5)

        st.markdown("**¿Cuantos de estos titulos conocias antes de ver la lista?**")
        conocidos_rec = st.slider("Titulos conocidos previamente", 0, 5, 0)
        desconocidos = 5 - conocidos_rec

        if desconocidos >= 3:
            st.markdown(f'<div class="warning-box">{desconocidos} de 5 recomendaciones eran desconocidas. Prueba con nueva seleccion.</div>',
                        unsafe_allow_html=True)
            if st.button("Nueva seleccion de titulos"):
                st.session_state.muestra = random.sample(anclas, min(5, len(anclas)))
                st.session_state.resultados_pref = None
                st.rerun()
        else:
            st.markdown('<div class="section-header">Refinamiento</div>', unsafe_allow_html=True)
            titulo_ref = st.text_input("Escribe el nombre del titulo que mas te llamo la atencion (o dejalo vacio)")

            if titulo_ref and st.button("Refinar recomendaciones", type="primary"):
                candidato = next((i for i in top5 if titulo_ref.lower() in i.nombre.lower()), None)
                if not candidato:
                    st.warning("No se encontro ese titulo en los resultados.")
                else:
                    pesos_ref = Counter(st.session_state.pesos_totales)
                    for tag in candidato.generos_raw:
                        pesos_ref[tag] += 3.0
                    exc2 = set(st.session_state.excluidos)
                    exc2.add(candidato.nombre.lower())
                    heap2 = _calcular_heap(base, pesos_ref, st.session_state.negativos, exc2)
                    top2  = []
                    h2 = list(heap2); heapq.heapify(h2)
                    while h2 and len(top2) < 5:
                        _, it = heapq.heappop(h2)
                        top2.append(it)
                    st.markdown(f'<div class="section-header">Segunda ronda — Refinado desde "{candidato.nombre}"</div>',
                                unsafe_allow_html=True)
                    render_results(top2)

        if st.button("Nueva busqueda personalizada"):
            st.session_state.muestra = random.sample(anclas, min(5, len(anclas)))
            st.session_state.resultados_pref = None
            st.rerun()
