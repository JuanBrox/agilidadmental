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
    "🃏 Memorizar parejas",
    "👑 La Reina dice",
    "🧩 Completa el patrón",
    "🔢 Contador de estrellas",
    "🎭 Mi personaje",
]
LEVELS = [
    "Aprendiz de hada 🧚",
    "Hada de brillo ✨",
    "Domadora de unicornios 🦄",
    "Guardiana del arcoíris 🌈",
    "Reina de la Mente Ágil 👑",
]

for k, v in dict(stars=0, name="", history=[], page=PAGES[0], avatar="🦄 Unicornio", acc="🎀 Lazo", pet="🐞 Mariquita", pet_name="Chispa", theme="🌸 Rosa", acc_msg="").items():
    st.session_state.setdefault(k, v)
S = st.session_state


def add_stars(n):
    S.stars += n


def go(page):
    S.page = page


AVATARS = {
    "🦄 Unicornio": "🦄",
    "🧚‍♀️ Hada": "🧚‍♀️",
    "🧜‍♀️ Sirena": "🧜‍♀️",
    "🦋 Mariposa": "🦋",
    "🐱 Gatita mágica": "🐱",
    "🐲 Dragón amigo": "🐲",
    "🦊 Zorrita": "🦊",
    "🐰 Conejita": "🐰",
}
ACCS = {
    "Sin accesorio": ("", 0),
    "🎀 Lazo": ("🎀", 0),
    "👑 Corona": ("👑", 10),
    "🌈 Arcoíris": ("🌈", 20),
    "💎 Joya": ("💎", 30),
    "🔮 Bola mágica": ("🔮", 40),
}
PETS = {
    "🐞 Mariquita": "🐞",
    "🐥 Pollito": "🐥",
    "🦔 Erizo": "🦔",
    "🐢 Tortuguita": "🐢",
    "🐝 Abejita": "🐝",
}
THEMES = {
    "🌸 Rosa": "linear-gradient(180deg,#fff0f8 0%,#f3e8ff 55%,#e8f4ff 100%)",
    "💜 Lila": "linear-gradient(180deg,#f5eeff 0%,#e8dcff 100%)",
    "🌊 Azul cielo": "linear-gradient(180deg,#e8f7ff 0%,#dbe9ff 100%)",
    "🍃 Menta": "linear-gradient(180deg,#eafff5 0%,#e0f4ff 100%)",
    "🌅 Atardecer": "linear-gradient(180deg,#fff3e0 0%,#ffe0ec 100%)",
}
CHEERS_OK = [
    "¡Qué bien lo haces, {n}!",
    "Me encanta cómo te concentras, {n} ✨",
    "¡Tu mente es cada vez más ágil!",
    "¡Eres una campeona del autocontrol, {n}!",
]
CHEERS_TRY = [
    "Equivocarse también es aprender 🌱 ¡Otra vez, {n}!",
    "Respira hondo y vuelve a intentarlo, {n} 🌬️",
    "Lo importante es el esfuerzo. ¡Tú puedes!",
    "Cada intento entrena tu cerebro 💪",
]


def avatar_str():
    return ACCS[S.acc][0] + AVATARS[S.avatar]


def pref(key, wkey):
    S[key] = S[wkey]


def companion_say(ratio=None):
    n = S.name.strip() or "valiente"
    pool = CHEERS_OK if (ratio is None or ratio >= 0.6) else CHEERS_TRY
    st.markdown(
        f"<div class='card'>{PETS[S.pet]} <b>{S.pet_name or 'Chispa'}</b>: "
        f"«{random.choice(pool).format(n=n)}»</div>",
        unsafe_allow_html=True,
    )


def stars_bar():
    lvl = min(S.stars // 8, len(LEVELS) - 1)
    st.markdown(
        f"<div class='stars'>{avatar_str()} · ⭐ {S.stars} · {LEVELS[lvl]}</div>",
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
    companion_say(ratio)
    st.button("🔁 Jugar otra vez", on_click=reset, use_container_width=True, key=prefix + "_again")


# ---------------------------------------------------------------- INICIO
def page_home():
    nombre = S.name.strip() or "valiente"
    st.title("🦄 Reino de la Mente Ágil")
    st.markdown(f"<div class='big'>{avatar_str()}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center'>¡Hola, {nombre}!</h3>", unsafe_allow_html=True)
    st.button("🎭 Personaliza tu personaje", on_click=go, args=(PAGES[12],), use_container_width=True, key="home_avatar")
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
        st.markdown(
            "<style>div.stButton>button{min-height:5.2rem;}"
            "div.stButton>button p{font-size:3.4rem !important;line-height:1.15 !important;}</style>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='big' style='font-size:3rem;min-height:4rem'>{' '.join(S.mem_in) or '…'}</div>",
            unsafe_allow_html=True,
        )
        st.caption("Tu respuesta")
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


# ---------------------------------------------------------------- MI PERSONAJE
def acc_fmt(k):
    cost = ACCS[k][1]
    return k if S.stars >= cost else f"🔒 {k} (necesita {cost} ⭐)"


def pick_acc():
    k = S.w_acc
    cost = ACCS[k][1]
    if S.stars >= cost:
        S.acc, S.acc_msg = k, ""
    else:
        S.acc_msg = f"🔒 Te faltan {cost - S.stars} ⭐ para desbloquear «{k}». ¡Sigue jugando!"


def page_avatar():
    st.header("🎭 Mi personaje")
    st.markdown(
        f"<div class='card' style='text-align:center'><div class='big'>{avatar_str()}</div>"
        f"<b>{S.name.strip() or 'Tu personaje'}</b><br>"
        f"{PETS[S.pet]} <b>{S.pet_name or 'Chispa'}</b> te acompaña en cada juego</div>",
        unsafe_allow_html=True,
    )
    avs, pets, ths = list(AVATARS), list(PETS), list(THEMES)
    st.selectbox("Elige tu personaje", avs, index=avs.index(S.avatar), key="w_av", on_change=pref, args=("avatar", "w_av"))
    st.selectbox(
        "Elige tu accesorio",
        list(ACCS),
        index=list(ACCS).index(S.acc),
        format_func=acc_fmt,
        key="w_acc",
        on_change=pick_acc,
    )
    if S.acc_msg:
        st.warning(S.acc_msg)
    st.selectbox("Elige a tu compañero", pets, index=pets.index(S.pet), key="w_pet", on_change=pref, args=("pet", "w_pet"))
    st.text_input("Ponle nombre a tu compañero", value=S.pet_name, max_chars=14, key="w_pn", on_change=pref, args=("pet_name", "w_pn"))
    st.selectbox("Color del reino", ths, index=ths.index(S.theme), key="w_th", on_change=pref, args=("theme", "w_th"))
    st.caption("🎁 Accesorios que se desbloquean con estrellas: " + " · ".join(f"{k} ({c[1]}⭐)" for k, c in ACCS.items() if c[1] > 0))
    companion_say()


# ---------------------------------------------------------------- generador de rondas (juegos nuevos)
def rd_reset(prefix, make):
    S[prefix + "_rounds"] = make()
    S[prefix + "_i"], S[prefix + "_score"], S[prefix + "_msg"], S[prefix + "_rew"] = 0, 0, "", False


def rd_answer(prefix, choice):
    r = S[prefix + "_rounds"][S[prefix + "_i"]]
    ok = choice == r["correct"]
    S[prefix + "_score"] += ok
    S[prefix + "_msg"] = "✅ ¡Muy bien!" if ok else r.get("hint", "💭 Casi… ¡mira con calma!")
    S[prefix + "_i"] += 1


# ---------------------------------------------------------------- MEMORIZAR PAREJAS
PR_EMO = ["🦄", "🧚‍♀️", "🌈", "⭐", "🌸", "🦋", "🐱", "🍭", "🐢", "🌙"]
PR_LEVELS = {"Fácil (6 cartas)": 3, "Medio (12 cartas)": 6, "Difícil (16 cartas)": 8}


def pr_reset():
    pairs = PR_LEVELS[S.get("pr_level_sel", "Medio (12 cartas)")]
    cards = random.sample(PR_EMO, pairs) * 2
    random.shuffle(cards)
    S.pr_cards, S.pr_open, S.pr_done, S.pr_moves, S.pr_msg, S.pr_rew = cards, [], set(), 0, "", False


def pr_flip(i):
    S.pr_open.append(i)
    if len(S.pr_open) == 2:
        S.pr_moves += 1
        a, b = S.pr_open
        if S.pr_cards[a] == S.pr_cards[b]:
            S.pr_done |= {a, b}
            S.pr_open = []
            S.pr_msg = "💖 ¡Pareja encontrada!"
        else:
            S.pr_msg = "🤔 No son pareja. Memoriza dónde están y pulsa «Tapar»."


def pr_hide():
    S.pr_open, S.pr_msg = [], ""


def page_pairs():
    if "pr_cards" not in S:
        pr_reset()
    st.header("🃏 Memorizar parejas")
    st.markdown(
        "<div class='rule'>Destapa <b>dos cartas</b> y busca las parejas iguales. "
        "Si no coinciden, <b>memoriza dónde están</b> antes de taparlas. ¡Con calma se gana!</div>",
        unsafe_allow_html=True,
    )
    levels = list(PR_LEVELS)
    cur = levels[list(PR_LEVELS.values()).index(len(S.pr_cards) // 2)]
    st.selectbox("Dificultad", levels, index=levels.index(cur), key="pr_level_sel", on_change=pr_reset)
    n = len(S.pr_cards)
    ncol = 3 if n <= 6 else 4
    pending = len(S.pr_open) == 2
    for r in range(0, n, ncol):
        cols = st.columns(ncol)
        for j, col in enumerate(cols):
            i = r + j
            if i >= n:
                break
            shown = i in S.pr_open or i in S.pr_done
            col.button(
                S.pr_cards[i] if shown else "❓",
                key=f"pr_{i}",
                on_click=pr_flip,
                args=(i,),
                use_container_width=True,
                disabled=shown or pending,
            )
    st.caption(f"Intentos: {S.pr_moves}")
    if pending:
        st.button("🙈 Tapar las cartas", on_click=pr_hide, use_container_width=True, key="pr_hide")
    if S.pr_msg:
        st.info(S.pr_msg)
    if len(S.pr_done) == n:
        pairs = n // 2
        if not S.pr_rew:
            add_stars(1 + (S.pr_moves <= pairs * 2) + (S.pr_moves <= int(pairs * 1.5)))
            S.pr_rew = True
            st.balloons()
        st.success(f"🎉 ¡Encontraste todas las parejas en {S.pr_moves} intentos!")
        companion_say()
        st.button("🔁 Jugar otra vez", on_click=pr_reset, use_container_width=True, key="pr_again")


# ---------------------------------------------------------------- LA REINA DICE (inhibición)
def sm_make():
    flags = [True] * 6 + [False] * 4
    random.shuffle(flags)
    rounds = []
    for simon in flags:
        opts = random.sample(MEM, 4)
        t = random.choice(opts)
        rounds.append(
            {
                "simon": simon,
                "target": t,
                "opts": opts,
                "correct": t if simon else "none",
                "hint": "💭 ¡Ups! La Reina no lo dijo: había que quedarse quieta ✋" if not simon else f"💭 Esta vez sí lo dijo la Reina: era el {t}",
            }
        )
    return rounds


def page_queen():
    if "sm_rounds" not in S:
        rd_reset("sm", sm_make)
    st.header("👑 La Reina dice")
    st.markdown(
        "<div class='rule'>Solo obedece si la orden empieza por <b>«La Reina dice»</b>. "
        "Si no lo dice, ¡no te muevas! Pulsa <b>🙅‍♀️ Me quedo quieta</b>.</div>",
        unsafe_allow_html=True,
    )
    n = len(S.sm_rounds)
    if S.sm_i < n:
        r = S.sm_rounds[S.sm_i]
        st.progress(S.sm_i / n, text=f"Orden {S.sm_i + 1} de {n}")
        txt = f"👑 La Reina dice: toca el {r['target']}" if r["simon"] else f"Toca el {r['target']}"
        st.markdown(f"<div class='word' style='font-size:1.9rem;color:#6a1b9a'>{txt}</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        for j, (col, e) in enumerate(zip(cols, r["opts"])):
            col.button(e, on_click=rd_answer, args=("sm", e), use_container_width=True, key=f"sm_{S.sm_i}_{j}")
        st.button("🙅‍♀️ Me quedo quieta", on_click=rd_answer, args=("sm", "none"), use_container_width=True, key=f"sm_{S.sm_i}_none")
        if S.sm_msg:
            st.caption(S.sm_msg)
    else:
        end_screen("sm", S.sm_score, n, lambda: rd_reset("sm", sm_make))


# ---------------------------------------------------------------- COMPLETA EL PATRÓN (flexibilidad / razonamiento)
def pt_make():
    rounds = []
    for _ in range(8):
        kind = random.choice(["AB", "AAB", "ABC", "ABB", "num"])
        if kind == "num":
            d = random.choice([2, 3, 5, 10])
            start = random.randint(0, 10)
            seq = [start + d * k for k in range(5)]
            ans = seq[4]
            opts = {ans, ans + d, ans - d, ans + 1}
            shown = ", ".join(map(str, seq[:4])) + ", ❓"
            opts = sorted(opts)
            ans = str(ans)
            opts = [str(o) for o in opts]
        else:
            pool = random.sample(MEM + ["🍭", "🐱"], 4)
            a, b, c = pool[:3]
            base = {"AB": [a, b], "AAB": [a, a, b], "ABC": [a, b, c], "ABB": [a, b, b]}[kind]
            seq = (base * 4)[:6]
            ans = seq[5]
            shown = " ".join(seq[:5]) + " ❓"
            opts = list({a, b, c, pool[3]} | {ans})[:4]
            if ans not in opts:
                opts[0] = ans
            random.shuffle(opts)
        rounds.append({"show": shown, "opts": opts, "correct": ans, "hint": f"💭 Era {ans}. Fíjate en cómo se repite."})
    return rounds


def page_pattern():
    if "pt_rounds" not in S:
        rd_reset("pt", pt_make)
    st.header("🧩 Completa el patrón")
    st.markdown(
        "<div class='rule'>Mira cómo se repite la fila y descubre <b>qué viene después</b>.</div>",
        unsafe_allow_html=True,
    )
    n = len(S.pt_rounds)
    if S.pt_i < n:
        r = S.pt_rounds[S.pt_i]
        st.progress(S.pt_i / n, text=f"Patrón {S.pt_i + 1} de {n}")
        st.markdown(f"<div class='word' style='font-size:2.2rem'>{r['show']}</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        for j, (col, e) in enumerate(zip(cols, r["opts"])):
            col.button(e, on_click=rd_answer, args=("pt", e), use_container_width=True, key=f"pt_{S.pt_i}_{j}")
        if S.pt_msg:
            st.caption(S.pt_msg)
    else:
        end_screen("pt", S.pt_score, n, lambda: rd_reset("pt", pt_make))


# ---------------------------------------------------------------- CONTADOR DE ESTRELLAS (atención sostenida)
CT_EMO = ["⭐", "🌸", "🦄", "🦋"]


def ct_make():
    rounds = []
    for r in range(6):
        total = 8 + r * 2
        target = random.choice(CT_EMO)
        others = [e for e in CT_EMO if e != target]
        cnt = random.randint(2, max(3, total // 3))
        items = [target] * cnt + [random.choice(others) for _ in range(total - cnt)]
        random.shuffle(items)
        opts = {cnt}
        while len(opts) < 4:
            opts.add(max(1, cnt + random.randint(-3, 3)))
        rows = "<br>".join("".join(items[i : i + 6]) for i in range(0, total, 6))
        rounds.append(
            {
                "target": target,
                "grid": rows,
                "opts": [str(o) for o in sorted(opts)],
                "correct": str(cnt),
                "hint": f"💭 Había {cnt}. Cuenta fila por fila, despacito.",
            }
        )
    return rounds


def page_count():
    if "ct_rounds" not in S:
        rd_reset("ct", ct_make)
    st.header("🔢 Contador de estrellas")
    st.markdown(
        "<div class='rule'>Cuenta <b>solo</b> la figura que te pido. Ve <b>fila por fila</b> y con calma.</div>",
        unsafe_allow_html=True,
    )
    n = len(S.ct_rounds)
    if S.ct_i < n:
        r = S.ct_rounds[S.ct_i]
        st.progress(S.ct_i / n, text=f"Cuadro {S.ct_i + 1} de {n}")
        st.markdown(f"### ¿Cuántos {r['target']} hay?")
        st.markdown(f"<div class='big' style='font-size:2.2rem'>{r['grid']}</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        for j, (col, e) in enumerate(zip(cols, r["opts"])):
            col.button(e, on_click=rd_answer, args=("ct", e), use_container_width=True, key=f"ct_{S.ct_i}_{j}")
        if S.ct_msg:
            st.caption(S.ct_msg)
    else:
        end_screen("ct", S.ct_score, n, lambda: rd_reset("ct", ct_make))


# ---------------------------------------------------------------- navegación
ORDER = [PAGES[i] for i in (0, 12, 1, 2, 3, 9, 4, 5, 10, 6, 8, 7, 11)]

with st.sidebar:
    st.text_input("¿Cómo te llamas?", key="name")
    st.caption("Tus estrellas y tu personaje se guardan mientras la app esté abierta.")

st.markdown(f"<style>.stApp{{background:{THEMES[S.theme]};}}</style>", unsafe_allow_html=True)
stars_bar()
st.selectbox("🗺️ ¿A qué jugamos?", ORDER, key="page")

{
    PAGES[0]: page_home,
    PAGES[1]: page_breath,
    PAGES[2]: page_emotions,
    PAGES[3]: page_gng,
    PAGES[4]: page_stroop,
    PAGES[5]: page_flex,
    PAGES[6]: page_memory,
    PAGES[7]: page_odd,
    PAGES[8]: page_pairs,
    PAGES[9]: page_queen,
    PAGES[10]: page_pattern,
    PAGES[11]: page_count,
    PAGES[12]: page_avatar,
}[S.page]()
