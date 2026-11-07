import random
import time

import streamlit as st

st.set_page_config(page_title="Reino de la Mente Ágil", page_icon="🦄", layout="centered")

# ---------------------------------------------------------------- estilos
st.markdown(
    """
<style>
.stApp{background:linear-gradient(180deg,#fff0f8 0%,#f3e8ff 55%,#e8f4ff 100%);}
h1,h2,h3{color:#6a1b9a !important;}
div.stButton>button{border-radius:18px;border:2px solid #ce93d8;background:#fff;
  font-size:1.15rem;font-weight:700;padding:.6rem .4rem;color:#4a148c;}
div.stButton>button:hover{background:#f8e1ff;border-color:#8e24aa;color:#4a148c;}
div[data-testid="stHorizontalBlock"]{flex-wrap:nowrap !important;gap:.4rem !important;}
div[data-testid="stColumn"],div[data-testid="column"]{min-width:0 !important;flex:1 1 0 !important;}
.stars{background:#fff;border:2px solid #f48fb1;border-radius:20px;padding:.5rem 1rem;
  text-align:center;font-weight:800;color:#ad1457;margin-bottom:.8rem;}
.big{font-size:5rem;text-align:center;line-height:1.2;}
.word{font-size:3.2rem;text-align:center;font-weight:900;letter-spacing:2px;}
.rule{background:#fff;border-left:8px solid #ab47bc;border-radius:14px;padding:.7rem 1rem;
  font-size:1.1rem;margin:.5rem 0 1rem 0;color:#4a148c;}
.card{background:#fff;border-radius:20px;padding:1rem;margin:.6rem 0;border:2px solid #e1bee7;}
.bwrap{display:flex;justify-content:center;align-items:center;margin:34px 0 44px 0;height:240px;}
.bcircle{width:190px;height:190px;border-radius:50%;
  background:radial-gradient(circle,#f8bbd0,#ce93d8);display:flex;align-items:center;
  justify-content:center;position:relative;animation:bgrow 14s ease-in-out infinite;
  box-shadow:0 0 40px #e1bee7;}
.bl{position:absolute;width:140px;text-align:center;font-size:1.15rem;font-weight:800;
  color:#4a148c;opacity:0;}
.b1{animation:l1 14s infinite;}.b2{animation:l2 14s infinite;}.b3{animation:l3 14s infinite;}
@keyframes bgrow{0%{transform:scale(.6)}28.5%{transform:scale(1.15)}57%{transform:scale(1.15)}100%{transform:scale(.6)}}
@keyframes l1{0%{opacity:1}27%{opacity:1}28.5%,100%{opacity:0}}
@keyframes l2{0%,28%{opacity:0}29%{opacity:1}56%{opacity:1}57%,100%{opacity:0}}
@keyframes l3{0%,57%{opacity:0}58%{opacity:1}99%{opacity:1}100%{opacity:0}}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- estado general
PAGES = [
    "🏠 Inicio",
    "🌬️ Respira como un unicornio",
    "🌡️ Mi termómetro de emociones",
    "🚦 Puerta mágica (¡frena!)",
    "🎨 Colores traviesos",
    "🔄 Cambio de regla",
    "🧠 Memoria de hadas",
    "🔎 Ojo de hada",
]
LEVELS = [
    "Aprendiz de hada 🧚",
    "Hada de brillo ✨",
    "Domadora de unicornios 🦄",
    "Guardiana del arcoíris 🌈",
    "Reina de la Mente Ágil 👑",
]

for k, v in dict(stars=0, name="", history=[], page=PAGES[0]).items():
    st.session_state.setdefault(k, v)
S = st.session_state


def add_stars(n):
    S.stars += n


def go(page):
    S.page = page


def stars_bar():
    lvl = min(S.stars // 8, len(LEVELS) - 1)
    st.markdown(
        f"<div class='stars'>⭐ {S.stars} estrellas · {LEVELS[lvl]}</div>",
        unsafe_allow_html=True,
    )


def end_screen(prefix, score, total, reset):
    """Pantalla final común: da estrellas una sola vez."""
    ratio = score / total
    if not S.get(prefix + "_rew"):
        add_stars(1 + (ratio >= 0.6) + (ratio >= 0.9))
        S[prefix + "_rew"] = True
        if ratio >= 0.6:
            st.balloons()
    if ratio >= 0.9:
        msg = "¡Increíble! Tu mente fue ágil como un rayo de arcoíris 🌈"
    elif ratio >= 0.6:
        msg = "¡Muy bien! Cada vez te sale mejor 💪"
    else:
        msg = "¡Buen intento! Entrenar es repetir, y repitiendo se mejora 🌱"
    st.success(f"{msg}\n\nAciertos: **{score} de {total}**")
    st.button("🔁 Jugar otra vez", on_click=reset, use_container_width=True, key=prefix + "_again")


# ---------------------------------------------------------------- INICIO
def page_home():
    nombre = S.name.strip() or "valiente"
    st.title("🦄 Reino de la Mente Ágil")
    st.markdown(f"### ¡Hola, {nombre}! 🧚‍♀️")
    st.write(
        "Tu cerebro es como un músculo mágico: cuanto más lo entrenas, más fácil te resulta "
        "**calmarte, concentrarte y pensar antes de actuar**."
    )

    st.markdown("#### 🚦 La regla de oro: Para · Piensa · Actúa")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='card'><b>1. PARA ✋</b><br>Quieta como una estatua</div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'><b>2. PIENSA 💭</b><br>Respira y piensa</div>", unsafe_allow_html=True)
    c3.markdown("<div class='card'><b>3. ACTÚA ✨</b><br>Elige con calma</div>", unsafe_allow_html=True)

    st.markdown("#### 🎯 Misión de hoy (unos 10 minutos)")
    plan = [
        (PAGES[1], "1️⃣ Respira como un unicornio (calma)"),
        (PAGES[3], "2️⃣ Puerta mágica (frenar impulsos)"),
        (PAGES[6], "3️⃣ Memoria de hadas (concentración)"),
        (PAGES[2], "4️⃣ Cuéntame cómo te sientes"),
    ]
    for i, (p, label) in enumerate(plan):
        st.button(label, on_click=go, args=(p,), use_container_width=True, key=f"plan{i}")

    with st.expander("👩‍👧 Para madres y padres"):
        st.markdown(
            """
**Qué trabaja cada juego** (funciones ejecutivas):
- 🚦 **Puerta mágica** → control de impulsos (inhibición).
- 🎨 **Colores traviesos** → atención selectiva y autocontrol.
- 🔄 **Cambio de regla** → flexibilidad mental (cambiar de tarea sin frustrarse).
- 🧠 **Memoria de hadas** → memoria de trabajo y concentración.
- 🔎 **Ojo de hada** → atención sostenida.
- 🌬️ **Respiración** y 🌡️ **termómetro** → regulación emocional.

**Consejos:** sesiones cortas (10-15 min), mejor a diario que mucho un día. Jugad juntas, celebrad el
esfuerzo y no solo los aciertos, y practicad la respiración **cuando está tranquila**, para poder
usarla cuando haya enfado o nervios.

Esta app es un juego de entrenamiento: **no diagnostica ni sustituye** a un profesional. Si las
dificultades persisten o afectan al colegio o a casa, consultad con pediatría, psicología o el
orientador del centro.
"""
        )


# ---------------------------------------------------------------- RESPIRACIÓN
def page_breath():
    st.header("🌬️ Respira como un unicornio")
    st.write("Sigue la burbuja: **huele la flor** (se hace grande), **aguanta**, y **apaga la vela** (se hace pequeña).")
    st.markdown(
        """
<div class='bwrap'><div class='bcircle'>
<span class='bl b1'>Huele la flor 🌸<br>(4)</span>
<span class='bl b2'>Aguanta 🫧<br>(4)</span>
<span class='bl b3'>Apaga la vela 🕯️<br>(6)</span>
</div></div>
""",
        unsafe_allow_html=True,
    )
    st.info("Haz **3 respiraciones** seguidas. Si te sientes muy enfadada o nerviosa, haz 5. Suelta los hombros y relaja la cara.")
    def done():
        add_stars(1)
        S.br_msg = "¡Cerebro más tranquilo! +1 ⭐"

    st.button("✅ ¡Ya respiré 3 veces!", on_click=done, use_container_width=True, key="br_done")
    if S.get("br_msg"):
        st.success(S.br_msg)


# ---------------------------------------------------------------- TERMÓMETRO DE EMOCIONES
FEEL = {
    "😄 Contenta": ["Cuenta qué te hace sentir así 🗣️", "Dale un abrazo a alguien 🤗", "¡Aprovecha para hacer algo creativo! 🎨"],
    "😠 Enfadada": ["Para y no hables todavía ✋", "Respira como un unicornio 🌬️ (5 veces)", "Aprieta fuerte tus manos y suéltalas despacio 🙌", "Cuando estés más tranquila, di: «Me siento enfadada porque…»"],
    "😰 Nerviosa": ["Pon una mano en la tripa y respira hondo 🌬️", "Mira 5 cosas de tu alrededor y nómbralas 👀", "Dite: «Puedo con esto, voy paso a paso» 💪"],
    "😢 Triste": ["Está bien sentir tristeza 💜", "Pide un abrazo o cuéntale a alguien qué te pasa 🤗", "Dibuja o escribe cómo te sientes ✏️"],
    "🌪️ Revuelta, me cuesta concentrarme": ["Respira como un unicornio 🌬️ (3 veces)", "Haz una sola cosa pequeña: 5 minutos y nada más ⏱️", "Aparta lo que distrae (juguetes, pantalla) 📵", "Juega a Memoria de hadas 🧠 para enfocar la mente"],
    "⚡ Con mucha energía, no paro quieta": ["Estírate como un gato y salta 10 veces 🐱", "Haz «la estatua»: quieta 20 segundos 🗿", "Respira como un unicornio 🌬️ para bajar las revoluciones"],
}


def page_emotions():
    st.header("🌡️ Mi termómetro de emociones")
    feel = st.radio("¿Cómo te sientes ahora?", list(FEEL), key="feel")
    size = st.select_slider(
        "¿Cómo de grande es esa emoción?",
        options=["🌱 Pequeñita", "🌼 Normal", "🔥 Grande", "🌋 Volcán", "🚀 ¡Enorme!"],
        value="🌼 Normal",
        key="size",
    )
    st.markdown("#### 💡 Tu caja de calma")
    if size in ("🌋 Volcán", "🚀 ¡Enorme!"):
        st.warning("Primero lo primero: **para y respira**. Cuando bajes el volcán, elige otra idea.")
        st.button("🌬️ Ir a respirar", on_click=go, args=(PAGES[1],), use_container_width=True, key="go_breath")
    for tip in FEEL[feel]:
        st.markdown(f"<div class='card'>{tip}</div>", unsafe_allow_html=True)

    def save():
        S.history.append({"Emoción": S.feel, "Tamaño": S.size})
        add_stars(1)

    st.button("💾 Guardar cómo me siento (+1 ⭐)", on_click=save, use_container_width=True, key="save_feel")
    if S.history:
        st.caption("Tus últimas emociones de hoy:")
        st.dataframe(S.history[-6:][::-1], use_container_width=True, hide_index=True)


# ---------------------------------------------------------------- 1) PUERTA MÁGICA (Go / No-Go)
GO = ["🦄", "🧚‍♀️", "🌈", "⭐", "🌸", "🦋"]
NOGO = "🐉"


def gng_reset():
    seq = [random.choice(GO) for _ in range(9)] + [NOGO] * 3
    random.shuffle(seq)
    S.gng_seq, S.gng_i, S.gng_score, S.gng_msg, S.gng_rew = seq, 0, 0, "", False


def gng_answer(choice):
    item = S.gng_seq[S.gng_i]
    ok = (choice == "go") == (item != NOGO)
    S.gng_score += ok
    S.gng_msg = "✅ ¡Bien frenado!" if ok else "💭 Casi… ¡Para y piensa antes de pulsar!"
    S.gng_i += 1


def page_gng():
    if "gng_seq" not in S:
        gng_reset()
    st.header("🚦 Puerta mágica")
    st.markdown(
        "<div class='rule'>Si ves un amigo mágico (🦄🧚‍♀️🌈⭐🌸🦋) pulsa <b>✨ Pasar</b>.<br>"
        "Si aparece el dragón <b>🐉</b> pulsa <b>✋ Parar</b>.</div>",
        unsafe_allow_html=True,
    )
    n = len(S.gng_seq)
    if S.gng_i < n:
        st.progress(S.gng_i / n, text=f"Carta {S.gng_i + 1} de {n}")
        st.markdown(f"<div class='big'>{S.gng_seq[S.gng_i]}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("✨ Pasar", on_click=gng_answer, args=("go",), use_container_width=True, key="gng_go")
        c2.button("✋ Parar", on_click=gng_answer, args=("stop",), use_container_width=True, key="gng_stop")
        if S.gng_msg:
            st.caption(S.gng_msg)
    else:
        end_screen("gng", S.gng_score, n, gng_reset)


# ---------------------------------------------------------------- 2) COLORES TRAVIESOS (Stroop)
INK = {"ROJO": "#e53935", "AZUL": "#1e88e5", "VERDE": "#2e9e4f", "AMARILLO": "#f4b400"}


def st_reset():
    seq = []
    for _ in range(10):
        w = random.choice(list(INK))
        c = random.choice([x for x in INK if x != w]) if random.random() < 0.8 else w
        seq.append((w, c))
    S.st_seq, S.st_i, S.st_score, S.st_msg, S.st_rew = seq, 0, 0, "", False


def st_answer(choice):
    ok = choice == S.st_seq[S.st_i][1]
    S.st_score += ok
    S.st_msg = "✅ ¡Correcto!" if ok else "💭 Mira el COLOR de la letra, no lo que dice."
    S.st_i += 1


def page_stroop():
    if "st_seq" not in S:
        st_reset()
    st.header("🎨 Colores traviesos")
    st.markdown(
        "<div class='rule'>Las palabras son traviesas: ¡dicen un color pero están pintadas de otro! "
        "Elige el <b>color de la pintura</b>, no lo que dice.</div>",
        unsafe_allow_html=True,
    )
    n = len(S.st_seq)
    if S.st_i < n:
        st.progress(S.st_i / n, text=f"Palabra {S.st_i + 1} de {n}")
        w, c = S.st_seq[S.st_i]
        st.markdown(f"<div class='word' style='color:{INK[c]}'>{w}</div>", unsafe_allow_html=True)
        names = list(INK)
        for row in (names[:2], names[2:]):
            cols = st.columns(2)
            for col, nm in zip(cols, row):
                col.button(f"● {nm.title()}", on_click=st_answer, args=(nm,), use_container_width=True, key=f"st_{S.st_i}_{nm}")
        if S.st_msg:
            st.caption(S.st_msg)
    else:
        end_screen("st", S.st_score, n, st_reset)


# ---------------------------------------------------------------- 3) CAMBIO DE REGLA (flexibilidad)
SHAPES = {
    "círculo": {"rojo": "🔴", "azul": "🔵", "verde": "🟢", "amarillo": "🟡"},
    "cuadrado": {"rojo": "🟥", "azul": "🟦", "verde": "🟩", "amarillo": "🟨"},
}
COLORS = ["rojo", "azul", "verde", "amarillo"]


def flex_make(i):
    rule = "color" if (i // 3) % 2 == 0 else "forma"
    shape = random.choice(list(SHAPES))
    color = random.choice(COLORS)
    other_shape = [x for x in SHAPES if x != shape][0]
    other_colors = [c for c in COLORS if c != color]
    c_only = (other_shape, color)
    s_only = (shape, random.choice(other_colors))
    oc = random.sample(other_colors, 2)
    opts = [c_only, s_only, (other_shape, oc[0]), (other_shape, oc[1])]
    random.shuffle(opts)
    em = lambda t: SHAPES[t[0]][t[1]]
    return {
        "rule": rule,
        "target": SHAPES[shape][color],
        "opts": [em(o) for o in opts],
        "correct": em(c_only) if rule == "color" else em(s_only),
    }


def flex_reset():
    S.fx_rounds = [flex_make(i) for i in range(12)]
    S.fx_i, S.fx_score, S.fx_msg, S.fx_rew = 0, 0, "", False


def fx_answer(e):
    r = S.fx_rounds[S.fx_i]
    ok = e == r["correct"]
    S.fx_score += ok
    S.fx_msg = "✅ ¡Bien!" if ok else "💭 Ojo: ¿qué regla toca ahora?"
    S.fx_i += 1


def page_flex():
    if "fx_rounds" not in S:
        flex_reset()
    st.header("🔄 Cambio de regla")
    st.markdown(
        "<div class='rule'>La regla cambia cada pocas cartas: a veces hay que elegir el <b>mismo COLOR</b> "
        "y a veces la <b>misma FORMA</b>. ¡Lee bien la regla de cada carta!</div>",
        unsafe_allow_html=True,
    )
    n = len(S.fx_rounds)
    if S.fx_i < n:
        r = S.fx_rounds[S.fx_i]
        st.progress(S.fx_i / n, text=f"Carta {S.fx_i + 1} de {n}")
        if S.fx_i > 0 and S.fx_rounds[S.fx_i - 1]["rule"] != r["rule"]:
            st.warning("⚠️ ¡La regla ha CAMBIADO!")
        if r["rule"] == "color":
            st.markdown("### 🎨 Ahora: elige el mismo **COLOR**")
        else:
            st.markdown("### 🔷 Ahora: elige la misma **FORMA**")
        st.markdown(f"<div class='big'>{r['target']}</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        for j, (col, e) in enumerate(zip(cols, r["opts"])):
            col.button(e, on_click=fx_answer, args=(e,), use_container_width=True, key=f"fx_{S.fx_i}_{j}")
        if S.fx_msg:
            st.caption(S.fx_msg)
    else:
        end_screen("fx", S.fx_score, n, flex_reset)


# ---------------------------------------------------------------- 4) MEMORIA DE HADAS
MEM = ["🦄", "🧚‍♀️", "🌈", "⭐", "🌸", "🦋"]


def mem_init():
    S.mem_len, S.mem_phase, S.mem_seq, S.mem_in, S.mem_ok = 3, "ready", [], [], False


def mem_new():
    S.mem_seq = [random.choice(MEM) for _ in range(S.mem_len)]
    S.mem_in, S.mem_phase = [], "show"


def mem_pick(e):
    S.mem_in.append(e)
    if len(S.mem_in) == len(S.mem_seq):
        S.mem_ok = S.mem_in == S.mem_seq
        if S.mem_ok:
            add_stars(1)
            S.mem_len = min(S.mem_len + 1, 7)
        else:
            S.mem_len = max(3, S.mem_len - 1)
        S.mem_phase = "result"


def mem_ready():
    S.mem_phase = "ready"


def page_memory():
    if "mem_phase" not in S:
        mem_init()
    st.header("🧠 Memoria de hadas")
    st.markdown(
        "<div class='rule'>Mira la secuencia con atención y repítela <b>en el mismo orden</b>. "
        "Si aciertas, ¡la siguiente es más larga!</div>",
        unsafe_allow_html=True,
    )
    st.caption(f"Nivel actual: {S.mem_len} figuras")
    ph = S.mem_phase
    if ph == "ready":
        st.button("▶️ ¡Mostrar secuencia!", on_click=mem_new, use_container_width=True, key="mem_start")
    elif ph == "show":
        box = st.empty()
        box.markdown(f"<div class='big' style='font-size:3rem'>{' '.join(S.mem_seq)}</div>", unsafe_allow_html=True)
        time.sleep(0.9 * len(S.mem_seq) + 1.2)
        box.empty()
        S.mem_phase = "input"
        st.rerun()
    elif ph == "input":
        st.markdown(f"#### Tu respuesta: {' '.join(S.mem_in) or '…'}")
        cols = st.columns(3)
        for j, e in enumerate(MEM):
            cols[j % 3].button(e, on_click=mem_pick, args=(e,), use_container_width=True, key=f"mem_{len(S.mem_in)}_{j}")
    else:
        if S.mem_ok:
            st.success("¡Perfecto! Memoria de hada 🧚‍♀️ +1 ⭐")
        else:
            st.info(f"Era: {' '.join(S.mem_seq)}\n\n¡No pasa nada! Probamos otra vez.")
        st.button("➡️ Siguiente", on_click=mem_ready, use_container_width=True, key="mem_next")


# ---------------------------------------------------------------- 5) OJO DE HADA (atención sostenida)
PAIRS = [("🌸", "🌺"), ("🦄", "🐴"), ("🌙", "🌛"), ("⭐", "🌟"), ("🍎", "🍅"), ("🐱", "🐯"), ("🧚‍♀️", "🧜‍♀️")]


def od_make(r):
    n = 3 + r // 2
    a, b = random.choice(PAIRS)
    if random.random() < 0.5:
        a, b = b, a
    return {"n": n, "a": a, "b": b, "pos": random.randrange(n * n)}


def od_reset():
    S.od_r, S.od_score, S.od_msg, S.od_rew = 0, 0, "", False
    S.od_cur = od_make(0)


def od_pick(idx):
    ok = idx == S.od_cur["pos"]
    S.od_score += ok
    S.od_msg = "✅ ¡La encontraste!" if ok else "💭 Mira despacito, de arriba a abajo."
    S.od_r += 1
    if S.od_r < 6:
        S.od_cur = od_make(S.od_r)


def page_odd():
    if "od_cur" not in S:
        od_reset()
    st.header("🔎 Ojo de hada")
    st.markdown(
        "<div class='rule'>Una figura es <b>diferente</b> a las demás. Mira despacito y púlsala.</div>",
        unsafe_allow_html=True,
    )
    if S.od_r < 6:
        st.progress(S.od_r / 6, text=f"Cuadro {S.od_r + 1} de 6")
        g = S.od_cur
        n = g["n"]
        for row in range(n):
            cols = st.columns(n)
            for c in range(n):
                idx = row * n + c
                e = g["b"] if idx == g["pos"] else g["a"]
                cols[c].button(e, on_click=od_pick, args=(idx,), use_container_width=True, key=f"od_{S.od_r}_{idx}")
        if S.od_msg:
            st.caption(S.od_msg)
    else:
        end_screen("od", S.od_score, 6, od_reset)


# ---------------------------------------------------------------- navegación
with st.sidebar:
    st.text_input("¿Cómo te llamas?", key="name")
    st.caption("Tus estrellas se guardan mientras la app esté abierta.")

stars_bar()
st.selectbox("🗺️ ¿A qué jugamos?", PAGES, key="page")

{
    PAGES[0]: page_home,
    PAGES[1]: page_breath,
    PAGES[2]: page_emotions,
    PAGES[3]: page_gng,
    PAGES[4]: page_stroop,
    PAGES[5]: page_flex,
    PAGES[6]: page_memory,
    PAGES[7]: page_odd,
}[S.page]()
