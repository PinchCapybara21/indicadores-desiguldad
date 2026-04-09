"""
Boletin de Indicadores - Colombia 2017-2023
Desempleo, Pobreza, PIB, Inflacion y Gini · Fuente: DANE, Banco Mundial, Banrep
"""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Cien Años de Desigualdad",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #1B2631 0%, #1B4F72 60%, #2E86C1 100%);
        padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem;
        border-left: 6px solid #F39C12;
    }
    .header-box h1 { color: #FDFEFE; font-size: 1.8rem; margin: 0 0 0.3rem 0; }
    .header-box p  { color: #AED6F1; font-size: 0.9rem; margin: 0; }

    .intro-box {
        background: white; border-radius: 10px; padding: 1.5rem 1.8rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border-left: 5px solid #1B4F72; margin-bottom: 1.5rem;
    }
    .intro-pregunta {
        font-size: 1.05rem; font-weight: 700; color: #1B4F72;
        margin-bottom: 0.6rem;
    }
    .intro-label {
        font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.9px;
        color: #F39C12; font-weight: 700; margin-bottom: 0.4rem;
    }
    .intro-text {
        font-size: 0.93rem; color: #2C3E50; line-height: 1.8;
    }

    .kpi-card {
        background: white; border-radius: 10px; padding: 1.2rem;
        text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid;
    }
    .kpi-label { font-size: 0.72rem; text-transform: uppercase;
                 letter-spacing: 0.8px; color: #7F8C8D; margin-bottom: 0.3rem; }
    .kpi-value { font-size: 2rem; font-weight: 700; line-height: 1; }
    .kpi-sub   { font-size: 0.72rem; color: #95A5A6; margin-top: 0.2rem; }

    .analysis-box {
        background: white; border-radius: 8px; padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #2E86C1;
        font-size: 0.91rem; line-height: 1.7; color: #2C3E50; margin-top: 0.5rem;
    }
    .note-box {
        background: #FEF9E7; border-radius: 8px; padding: 0.9rem 1.1rem;
        border-left: 4px solid #F39C12; font-size: 0.85rem;
        color: #7D6608; line-height: 1.6; margin-top: 1rem;
    }
    .conclusion-box {
        background: linear-gradient(135deg, #1B2631 0%, #1B4F72 100%);
        border-radius: 10px; padding: 1.6rem 2rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15); margin-top: 0.5rem;
    }
    .conclusion-box h3 { color: #F39C12; font-size: 1.05rem; margin: 0 0 0.4rem 0; }
    .conclusion-box p  { color: #D6EAF8; font-size: 0.91rem; line-height: 1.75; margin: 0; }

    .section-title {
        font-size: 1.15rem; font-weight: 600; color: white;
        border-bottom: 2px solid #2E86C1; padding-bottom: 0.3rem;
        margin: 1.2rem 0 0.8rem 0;
    }
    .footer {
        margin-top: 2.5rem; padding: 1.2rem; background: #1B2631;
        border-radius: 8px; color: #AED6F1; font-size: 0.8rem; line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# ── Constantes ─────────────────────────────────────────────────────────────────
ANOS  = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
C_DES = "#7D3C98"
C_POB = "#D35400"
C_EXT = "#F0B27A"
C_PIB = "#1A5276"
C_INF = "#C0392B"
C_GIN = "#117A65"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DES = os.path.join(BASE_DIR, "data", "desempleo.csv")
PATH_POB = os.path.join(BASE_DIR, "data", "pobreza.csv")
PATH_PIB = os.path.join(BASE_DIR, "data", "pib.csv")
PATH_INF = os.path.join(BASE_DIR, "data", "inflacion.csv")
PATH_GIN = os.path.join(BASE_DIR, "data", "gini.csv")


@st.cache_data
def load_data():
    df_d = pd.read_csv(PATH_DES, index_col=0)
    df_d.columns = ANOS
    tgp = [float(v) for v in df_d.loc["Tasa Global de Participación (TGP)"].tolist()]
    to_ = [float(v) for v in df_d.loc["Tasa de Ocupación (TO)"].tolist()]
    tdd = [float(v) for v in df_d.loc["Tasa de Desocupación (TD)"].tolist()]

    df_p = pd.read_csv(PATH_POB, header=None)
    mon_nac = df_p.iloc[1, 1:8].astype(float).tolist()
    ext_nac = df_p.iloc[6, 1:8].astype(float).tolist()

    df_pib = pd.read_csv(PATH_PIB, sep=";", encoding="utf-8-sig", header=0)
    df_pib.columns = ["ano", "valor"]
    df_pib["valor"] = (
        df_pib["valor"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    pib = df_pib["valor"].tolist()

    df_inf = pd.read_csv(PATH_INF, sep=";", encoding="utf-8-sig", header=0)
    df_inf.columns = ["ano", "valor"]
    df_inf["valor"] = df_inf["valor"].astype(float)
    inf = df_inf["valor"].tolist()

    df_gin = pd.read_csv(PATH_GIN, sep=",", header=0)
    df_gin.columns = ["ano", "valor"]
    df_gin["valor"] = df_gin["valor"].astype(float)
    gin = df_gin["valor"].tolist()

    return tgp, to_, tdd, mon_nac, ext_nac, pib, inf, gin


try:
    tgp, to_, tdd, mon_nac, ext_nac, pib, inf, gin = load_data()
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.stop()


# ── Helpers ────────────────────────────────────────────────────────────────────
def covid_band(fig, row=None, col=None):
    kwargs = dict(
        x0=2019.5, x1=2020.5, fillcolor="#FADBD8", opacity=0.35,
        layer="below", line_width=0,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font_color="#C0392B", annotation_font_size=10,
    )
    if row is not None:
        kwargs["row"] = row
        kwargs["col"] = col
    fig.add_vrect(**kwargs)
    return fig


def base_layout(fig, title, ytitle, xvals=None):
    if xvals is None:
        xvals = ANOS
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#1C2833")),
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title=ytitle, gridcolor="#ECF0F1"),
        xaxis=dict(tickmode="array", tickvals=xvals, gridcolor="#ECF0F1"),
        margin=dict(t=55, b=40, l=55, r=40),
    )
    return fig


def kpi(col, label, value, unit, sub, color):
    col.markdown(f"""
    <div class="kpi-card" style="border-top-color:{color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color}">{value}<span style="font-size:1rem">{unit}</span></div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ENCABEZADO — título clickbait + subtítulo con el periodo real
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="header-box">
    <h1>&#128202; Cien Años de Desigualdad</h1>
    <p>Análisis de indicadores macroeconómicos y sociales &mdash; Colombia 2017&ndash;2023
       &nbsp;&middot;&nbsp; Nivel Nacional &nbsp;&middot;&nbsp;
       Fuente: DANE · Banco de la República · Banco Mundial</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PREGUNTA GUÍA E INTRODUCCIÓN
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="intro-box">
    <div class="intro-label">🔍 Pregunta guía</div>
    <div class="intro-pregunta">
        ¿Cómo se comportaron los indicadores macro, el desempleo y la pobreza en Colombia post y pre pandemia,
        en los periodos comprendidos entre 2017 y 2023?
    </div>
    <hr style="border:none; border-top:1px solid #D6EAF8; margin:0.9rem 0;">
    <div class="intro-label">📄 Introducción</div>
    <div class="intro-text">
        Entre 2017 y 2023, Colombia experimentó un periodo de alta volatilidad económica y social, marcado no solo 
        por el choque de la pandemia del COVID-19, sino también por cambios en el contexto político y en la 
        orientación de la política económica. Durante el gobierno de Juan Manuel Santos (hasta 2018), la economía 
        venía de un proceso de ajuste tras la caída de los precios del petróleo, con un crecimiento moderado y 
        avances graduales en reducción de pobreza. Posteriormente, bajo la administración de Iván Duque, el país 
        mantuvo estabilidad macroeconómica, pero enfrentó retos estructurales como el alto desempleo, la informalidad 
        y el descontento social reflejado en protestas como el paro nacional de 2019.
        <br><br>
        El año 2020 marcó un punto de quiebre con la llegada del COVID-19, que obligó a implementar confinamientos 
        estrictos y medidas de emergencia económica. Esto provocó una fuerte contracción del PIB, un aumento histórico 
        del desempleo y un deterioro significativo en los niveles de pobreza. Para mitigar estos efectos, el gobierno 
        implementó políticas como transferencias monetarias (Ingreso Solidario), subsidios al empleo (PAEF) y ampliación 
        de programas sociales existentes. Sin embargo, el impacto fue desigual entre sectores y grupos poblacionales.
        <br><br>
        En el periodo pospandemia (2021–2023), Colombia vivió una recuperación económica impulsada por la reapertura, aunque 
        acompañada de tensiones sociales (como el paro nacional de 2021) y presiones inflacionarias. En 2022 se da un cambio 
        político relevante con la llegada al poder de Gustavo Petro, lo que implicó un giro en la agenda económica hacia reformas 
        estructurales enfocadas en equidad social, mercado laboral y sistema tributario.
        <br><br>
        En este contexto, el comportamiento de los principales indicadores macroeconómicos, el desempleo y la pobreza entre 2017 
        y 2023 no puede entenderse de manera aislada, sino como el resultado de la interacción entre choques externos, decisiones 
        de política pública y cambios en el entorno político. Analizar su evolución en los periodos pre y pospandemia permite 
        identificar tanto la magnitud del impacto de la crisis como las fortalezas y limitaciones del proceso de recuperación 
        económica y social del país.
        <br><br>
        En este boletín se analizan cinco indicadores clave: el <strong>Producto Interno
        Bruto (PIB)</strong>, la <strong>inflación</strong>, el <strong>coeficiente de
        Gini</strong>, la <strong>pobreza monetaria y extrema</strong> y el
        <strong>mercado laboral</strong>, con el fin de comprender cómo evolucionaron las
        condiciones económicas y sociales en Colombia durante este periodo. El análisis se
        fundamenta en datos provenientes de fuentes oficiales como el DANE, el Banco de la
        República y el Banco Mundial.
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPIs
# ══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📉 Desempleo",
    "💰 Pobreza",
    "📈 PIB",
    "🔥 Inflación",
    "⚖️ Gini",
    "🔗 Comparativo",
])

# ── TAB 1 — Desempleo ──────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-title">Indicadores del Mercado Laboral Nacional</p>',
                unsafe_allow_html=True)

    fig_des = go.Figure()
    fig_des.add_trace(go.Scatter(
        x=ANOS, y=tgp, name="TGP (%)",
        mode="lines+markers",
        line=dict(color="#1B4F72", width=2.5),
        marker=dict(size=8, symbol="circle"),
        hovertemplate="<b>%{x}</b> TGP: %{y:.1f}%<extra></extra>",
    ))
    fig_des.add_trace(go.Scatter(
        x=ANOS, y=to_, name="TO (%)",
        mode="lines+markers",
        line=dict(color="#27AE60", width=2.5, dash="dash"),
        marker=dict(size=8, symbol="square"),
        hovertemplate="<b>%{x}</b> TO: %{y:.1f}%<extra></extra>",
    ))
    fig_des.add_trace(go.Scatter(
        x=ANOS, y=tdd, name="TD — Desempleo (%)",
        mode="lines+markers+text",
        line=dict(color=C_DES, width=3),
        marker=dict(size=10, symbol="diamond"),
        text=[f"{v:.1f}%" for v in tdd],
        textposition="top center",
        textfont=dict(size=10, color=C_DES),
        fill="tozeroy", fillcolor="rgba(125,60,152,0.07)",
        hovertemplate="<b>%{x}</b> TD: %{y:.1f}%<extra></extra>",
    ))
    fig_des = covid_band(fig_des)
    fig_des = base_layout(
        fig_des, "Mercado Laboral Nacional — Colombia 2017-2023", "Tasa (%)"
    )
    fig_des.update_yaxes(range=[0, 75])
    st.plotly_chart(fig_des, use_container_width=True)

    st.markdown("""
    <div class="analysis-box">
    <strong>Análisis:</strong> En el mercado laboral nacional colombiano entre 2017 y 2023, los indicadores
                mostraron estabilidad prepandemia con una tasa de desempleo que osciló entre el 12,0 % (2017)}
                y el 13,1 % (2019), mientras la tasa global de participación (TGP) se mantuvo cerca del 65-67 % 
                y la de ocupación (TO) alrededor del 57-58 %, reflejando un equilibrio frágil en una economía
                con alto componente informal. La pandemia de COVID-19, con las estrictas cuarentenas decretadas 
                en 2020 que paralizaron micronegocios y sectores como comercio y servicios —donde más de 500 mil 
                establecimientos cerraron temporalmente—, provocó un leve repunte inicial al 13,5 % en 2020 que se 
                agravó en 2021 hasta el pico histórico reciente del 17,6 %, afectando especialmente a mujeres, jóvenes 
                y trabajadores por cuenta propia. La reactivación económica postpandemia, impulsada por la reapertura y 
                el crecimiento en alojamiento, transporte y comercio, permitió una recuperación gradual: el desempleo 
                bajó a 14,6 % en 2022 y 13,7 % en 2023, aunque sin recuperar plenamente los niveles de participación 
                laboral prepandemia, evidenciando las vulnerabilidades estructurales del empleo en Colombia.
    </div>
    <div class="note-box">
    <strong>Nota metodológica:</strong> La TD excluye trabajadores desalentados y subempleados,
    por lo que puede subestimar el deterioro real del mercado laboral. Fuente: DANE GEIH.
    </div>
    """, unsafe_allow_html=True)

# ── TAB 2 — Pobreza ────────────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-title">Pobreza Monetaria Nacional (%)</p>',
                    unsafe_allow_html=True)
        fig_mon = go.Figure()
        fig_mon.add_trace(go.Scatter(
            x=ANOS, y=mon_nac,
            name="Pobreza monetaria (%)",
            mode="lines+markers+text",
            line=dict(color=C_POB, width=3),
            marker=dict(size=9, symbol="circle"),
            text=[f"{v:.1f}%" for v in mon_nac],
            textposition="top center",
            textfont=dict(size=10, color=C_POB),
            fill="tozeroy", fillcolor="rgba(211,84,0,0.07)",
            hovertemplate="<b>%{x}</b> %{y:.1f}%<extra></extra>",
        ))
        fig_mon = covid_band(fig_mon)
        fig_mon = base_layout(
            fig_mon, "Pobreza Monetaria — Colombia 2017-2023", "Porcentaje (%)"
        )
        fig_mon.update_yaxes(range=[0, 50])
        st.plotly_chart(fig_mon, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-title">Pobreza Extrema Nacional (%)</p>',
                    unsafe_allow_html=True)
        fig_ext = go.Figure()
        fig_ext.add_trace(go.Scatter(
            x=ANOS, y=ext_nac,
            name="Pobreza extrema (%)",
            mode="lines+markers+text",
            line=dict(color=C_EXT, width=3),
            marker=dict(size=9, symbol="circle"),
            text=[f"{v:.1f}%" for v in ext_nac],
            textposition="top center",
            textfont=dict(size=10, color=C_POB),
            fill="tozeroy", fillcolor="rgba(240,178,122,0.15)",
            hovertemplate="<b>%{x}</b> %{y:.1f}%<extra></extra>",
        ))
        fig_ext = covid_band(fig_ext)
        fig_ext = base_layout(
            fig_ext, "Pobreza Extrema — Colombia 2017-2023", "Porcentaje (%)"
        )
        fig_ext.update_yaxes(range=[0, 22])
        st.plotly_chart(fig_ext, use_container_width=True)

    st.markdown("""
    <div class="analysis-box">
    <strong>Análisis:</strong> La pobreza monetaria y extrema en Colombia entre 
                2017 y 2023 reflejó avances modestos prepandemia —con tasas monetarias 
                de 35,5 % (2018) a 36,5 % (2019) y extrema de 10,4 % (2018) a 12,0 % (2019)—, 
                pero la crisis del COVID-19 generó un choque severo: los confinamientos 
                estrictos de 2020 provocaron pérdida masiva de ingresos en hogares informales 
                y rurales, elevando la pobreza monetaria al 43,1 % y la extrema al 17,3 %, cifras 
                que golpearon con mayor fuerza a mujeres, jóvenes, indígenas y afrocolombianos 
                de bajos ingresos. Gracias a las transferencias monetarias del Gobierno (como Ingreso Solidario) 
                y la gradual reactivación económica, se logró una recuperación sostenida: la monetaria 
                descendió a 39,7 % (2021), 36,6 % (2022) y 34 % (2023), mientras la extrema cayó a 
                13,7 % (2021), 13,8 % (2022) y 12 % (2023). Aunque se evitó un deterioro mayor, los 
                niveles siguen por encima de algunos prepandemia, destacando la persistente desigualdad 
                estructural que el país enfrenta pese a la resiliencia mostrada en la pospandemia.
    </div>
    """, unsafe_allow_html=True)

# ── TAB 3 — PIB ────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-title">Crecimiento del PIB — Colombia 2017-2023 (%)</p>',
                unsafe_allow_html=True)

    fig_pib = go.Figure()
    fig_pib.add_hline(y=0, line_color="#1C2833", line_width=1.2)
    fig_pib.add_trace(go.Scatter(
        x=ANOS, y=pib,
        name="Crecimiento PIB (%)",
        mode="lines+markers+text",
        line=dict(color=C_PIB, width=3),
        marker=dict(
            size=10,
            symbol="circle",
            color=[C_PIB if v >= 0 else "#E74C3C" for v in pib],
            line=dict(width=2, color="white"),
        ),
        text=[f"{v:+.1f}%" for v in pib],
        textposition="top center",
        textfont=dict(size=10, color=C_PIB),
        fill="tozeroy", fillcolor="rgba(26,82,118,0.07)",
        hovertemplate="<b>%{x}</b> PIB: %{y:+.1f}%<extra></extra>",
    ))
    fig_pib = covid_band(fig_pib)
    fig_pib = base_layout(
        fig_pib, "Crecimiento del PIB — Colombia 2017-2023", "Variación anual (%)"
    )
    fig_pib.update_yaxes(range=[min(pib) - 2, max(pib) + 3])
    st.plotly_chart(fig_pib, use_container_width=True)

    st.markdown("""
    <div class="analysis-box">
    <strong>Análisis:</strong> Colombia registró un crecimiento sostenido entre 2017 y 2019
    (entre 1,4% y 3,2%), impulsado por sectores como la construcción, el comercio y los
    servicios. El año <strong>2020</strong> marcó la mayor contracción económica de las últimas
    décadas con una caída del <strong>−7,2%</strong>, consecuencia directa de las medidas de
    confinamiento, la parálisis del consumo y la caída de los precios del petróleo. La
    recuperación fue notable en <strong>2021</strong>, con un rebote del <strong>+10,8%</strong>
    (efecto estadístico de base baja). En 2022 y 2023 el crecimiento se moderó a 7,3% y 0,7%
    respectivamente, reflejando la presión inflacionaria, el alza en tasas de interés del
    Banco de la República y la menor demanda interna. La recuperación benefició más a los
    sectores formales y de mayor ingreso, profundizando brechas distributivas.
    </div>
    <div class="note-box">
    <strong>Nota metodológica:</strong> Los datos corresponden a la variación porcentual anual
    del PIB real (a precios constantes). Fuente: Banco Mundial — NY.GDP.MKTP.KD.ZG.
    </div>
    """, unsafe_allow_html=True)

# ── TAB 4 — Inflación ──────────────────────────────────────────────────────────
with tab4:
    st.markdown('<p class="section-title">Inflación (IPC) — Colombia 2017-2023 (%)</p>',
                unsafe_allow_html=True)

    fig_inf = go.Figure()
    fig_inf.add_hrect(
        y0=2, y1=4, fillcolor="#D5F5E3", opacity=0.4,
        layer="below", line_width=0,
    )
    fig_inf.add_annotation(
        x=2023, y=3,
        text="Meta Banrep (2–4%)",
        showarrow=False,
        font=dict(color="#1E8449", size=10),
        xanchor="right",
    )
    fig_inf.add_trace(go.Scatter(
        x=ANOS, y=inf,
        name="Inflación IPC (%)",
        mode="lines+markers+text",
        line=dict(color=C_INF, width=3),
        marker=dict(size=10, symbol="circle"),
        text=[f"{v:.1f}%" for v in inf],
        textposition="top center",
        textfont=dict(size=10, color=C_INF),
        fill="tozeroy", fillcolor="rgba(192,57,43,0.07)",
        hovertemplate="<b>%{x}</b> Inflación: %{y:.1f}%<extra></extra>",
    ))
    fig_inf = covid_band(fig_inf)
    fig_inf = base_layout(
        fig_inf, "Inflación (IPC) — Colombia 2017-2023", "Variación IPC anual (%)"
    )
    fig_inf.update_yaxes(range=[0, max(inf) + 3])
    st.plotly_chart(fig_inf, use_container_width=True)

    st.markdown("""
    <div class="analysis-box">
    <strong>Análisis:</strong> La inflación en Colombia se mantuvo dentro del rango meta del
    Banco de la República (2–4%) entre 2017 y 2021, llegando a su punto más bajo en
    <strong>2020 (2,5%)</strong>, explicado por la caída de la demanda interna durante la
    pandemia. Sin embargo, la reapertura económica, los choques de oferta globales (guerra en
    Ucrania, disrupciones logísticas) y la depreciación del peso dispararon la inflación hasta
    <strong>10,2% en 2022</strong> y <strong>11,7% en 2023</strong>, los niveles más altos del
    periodo. El Banco de la República respondió con incrementos agresivos en tasas de interés,
    que contribuyeron a frenar parcialmente el alza pero también encarecieron el crédito y
    moderaron el crecimiento económico. La inflación elevada erosionó el poder adquisitivo de
    los hogares de menores ingresos, agudizando la pobreza real más allá de lo que muestran
    los indicadores monetarios.
    </div>
    <div class="note-box">
    <strong>Nota metodológica:</strong> El IPC mide la variación del costo de una canasta
    representativa de bienes y servicios. La meta de inflación del Banco de la República es
    3% ± 1 punto porcentual. Fuente: Banco Mundial — FP.CPI.TOTL.ZG.
    </div>
    """, unsafe_allow_html=True)

# ── TAB 5 — Gini ───────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<p class="section-title">Coeficiente de Gini — Colombia 2017-2023</p>',
                unsafe_allow_html=True)

    col_g1, col_g2 = st.columns([2, 1])

    with col_g1:
        fig_gin = go.Figure()
        fig_gin.add_hrect(
            y0=50, y1=max(gin) + 2, fillcolor="#FDEDEC", opacity=0.35,
            layer="below", line_width=0,
        )
        fig_gin.add_annotation(
            x=2023, y=51.5,
            text="Zona de alta desigualdad (Gini > 50)",
            showarrow=False,
            font=dict(color="#C0392B", size=10),
            xanchor="right",
        )
        fig_gin.add_trace(go.Scatter(
            x=ANOS, y=gin,
            name="Índice de Gini",
            mode="lines+markers+text",
            line=dict(color=C_GIN, width=3),
            marker=dict(size=11, symbol="diamond", color=C_GIN),
            text=[f"{v:.1f}" for v in gin],
            textposition="top center",
            textfont=dict(size=10, color=C_GIN),
            fill="tozeroy", fillcolor="rgba(17,122,101,0.07)",
            hovertemplate="<b>%{x}</b> Gini: %{y:.1f}<extra></extra>",
        ))
        fig_gin = covid_band(fig_gin)
        fig_gin = base_layout(
            fig_gin,
            "Coeficiente de Gini — Colombia 2017-2023",
            "Índice de Gini (0 = igualdad · 100 = desigualdad total)",
        )
        fig_gin.update_yaxes(range=[45, max(gin) + 3])
        st.plotly_chart(fig_gin, use_container_width=True)

    with col_g2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("**Referencia Gini mundial:**")
        ref_data = {
            "País / Región": [
                "🇸🇪 Suecia",
                "🌍 Promedio OCDE",
                "🌎 AL promedio",
                "🇨🇴 Colombia (2023)",
                "🇧🇷 Brasil",
            ],
            "Gini": ["27.6", "~32", "~46", f"{gin[-1]:.1f}", "~53.4"],
        }
        st.dataframe(
            pd.DataFrame(ref_data).set_index("País / Región"),
            use_container_width=True,
        )

    st.markdown("""
    <div class="analysis-box">
    <strong>Análisis:</strong> Entre 2017 y 2019, el leve aumento de la desigualdad 
                se explica por un crecimiento económico moderado que no logró mejorar 
                significativamente los ingresos de los hogares más vulnerables.Además, la alta 
                informalidad laboral limitó una distribución más equitativa del ingreso.En 2020, 
                la pandemia generó un choque negativo sin precedentes, afectando principalmente a 
                trabajadores informales y sectores como comercio y servicios. Esto provocó una fuerte 
                pérdida de empleo e ingresos en los hogares más pobres.Como resultado, la desigualdad 
                aumentó significativamente, alcanzando su punto máximo en 2021.Aunque en ese año hubo 
                recuperación del PIB, el empleo se recuperó de forma más lenta y desigual.Desde 2022, 
                el Gini empieza a disminuir levemente gracias a la reactivación económica. 
                También influyeron las transferencias sociales y el aumento del salario mínimo.
    </div>
    <div class="note-box">
    <strong>Nota metodológica:</strong> El coeficiente de Gini varía de 0 (igualdad perfecta)
    a 100 (desigualdad total). Valores superiores a 40 se consideran altos; Colombia oscila
    consistentemente por encima de 50. Fuente: Banco Mundial — SI.POV.GINI.
    </div>
    """, unsafe_allow_html=True)

# ── TAB 6 — Comparativo ────────────────────────────────────────────────────────
with tab6:
    st.markdown('<p class="section-title">Panel comparativo — todos los indicadores</p>',
                unsafe_allow_html=True)

    fig_all = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Desempleo TD (%)",
            "PIB — Crecimiento anual (%)",
            "Pobreza monetaria (%)",
            "Inflación IPC (%)",
        ),
        vertical_spacing=0.14,
        horizontal_spacing=0.1,
    )

    fig_all.add_trace(go.Scatter(
        x=ANOS, y=tdd, name="TD (%)",
        mode="lines+markers",
        line=dict(color=C_DES, width=2.5),
        marker=dict(size=8, symbol="diamond"),
        hovertemplate="TD: %{y:.1f}%<extra></extra>",
    ), row=1, col=1)

    fig_all.add_trace(go.Scatter(
        x=ANOS, y=pib, name="PIB (%)",
        mode="lines+markers",
        line=dict(color=C_PIB, width=2.5),
        marker=dict(
            size=8,
            color=[C_PIB if v >= 0 else "#E74C3C" for v in pib],
        ),
        hovertemplate="PIB: %{y:+.1f}%<extra></extra>",
    ), row=1, col=2)

    fig_all.add_trace(go.Scatter(
        x=ANOS, y=mon_nac, name="Pobreza mon. (%)",
        mode="lines+markers",
        line=dict(color=C_POB, width=2.5, dash="dash"),
        marker=dict(size=8),
        hovertemplate="Pobreza: %{y:.1f}%<extra></extra>",
    ), row=2, col=1)

    fig_all.add_trace(go.Scatter(
        x=ANOS, y=inf, name="Inflación (%)",
        mode="lines+markers",
        line=dict(color=C_INF, width=2.5),
        marker=dict(size=8),
        hovertemplate="IPC: %{y:.1f}%<extra></extra>",
    ), row=2, col=2)

    for r, c in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        fig_all.add_vrect(
            x0=2019.5, x1=2020.5, fillcolor="#FADBD8", opacity=0.3,
            layer="below", line_width=0, row=r, col=c,
        )

    fig_all.update_layout(
        height=600,
        title=dict(
            text="Indicadores macroeconómicos y sociales — Colombia 2017-2023",
            font=dict(size=15, color="#1C2833"),
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=-0.15,
                    xanchor="center", x=0.5),
        margin=dict(t=60, b=70, l=50, r=40),
    )
    for axis in fig_all.layout:
        if axis.startswith("xaxis"):
            fig_all.layout[axis].update(
                tickmode="array", tickvals=ANOS, gridcolor="#ECF0F1"
            )
        if axis.startswith("yaxis"):
            fig_all.layout[axis].update(gridcolor="#ECF0F1")

    st.plotly_chart(fig_all, use_container_width=True)

    # Gini vs Pobreza — doble eje
    st.markdown('<p class="section-title">Gini vs. Pobreza monetaria</p>',
                unsafe_allow_html=True)

    fig_gp = make_subplots(specs=[[{"secondary_y": True}]])
    fig_gp.add_trace(go.Scatter(
        x=ANOS, y=gin, name="Gini",
        mode="lines+markers",
        line=dict(color=C_GIN, width=3),
        marker=dict(size=9, symbol="diamond"),
        hovertemplate="Gini: %{y:.1f}<extra></extra>",
    ), secondary_y=False)
    fig_gp.add_trace(go.Scatter(
        x=ANOS, y=mon_nac, name="Pobreza monetaria (%)",
        mode="lines+markers",
        line=dict(color=C_POB, width=3, dash="dash"),
        marker=dict(size=9, symbol="circle"),
        hovertemplate="Pobreza: %{y:.1f}%<extra></extra>",
    ), secondary_y=True)
    fig_gp.add_vrect(
        x0=2019.5, x1=2020.5, fillcolor="#FADBD8", opacity=0.35,
        layer="below", line_width=0,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font_color="#C0392B", annotation_font_size=10,
    )
    fig_gp.update_layout(
        title=dict(
            text="Gini vs. Pobreza Monetaria — Colombia 2017-2023",
            font=dict(size=15, color="#1C2833"),
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
        xaxis=dict(tickmode="array", tickvals=ANOS, gridcolor="#ECF0F1"),
        margin=dict(t=55, b=40, l=55, r=55),
    )
    fig_gp.update_yaxes(title_text="Coeficiente de Gini",
                         secondary_y=False, gridcolor="#ECF0F1",
                         range=[45, max(gin) + 3])
    fig_gp.update_yaxes(title_text="Pobreza Monetaria (%)",
                         secondary_y=True, range=[30, 48])
    st.plotly_chart(fig_gp, use_container_width=True)

    # Tabla resumen
    st.markdown('<p class="section-title">Tabla resumen — todos los indicadores</p>',
                unsafe_allow_html=True)

    df_tabla = pd.DataFrame({
        "Año":               ANOS,
        "TGP (%)":           tgp,
        "TO (%)":            to_,
        "TD Desempleo (%)":  tdd,
        "Pobreza mon. (%)":  mon_nac,
        "Pobreza ext. (%)":  ext_nac,
        "PIB crecim. (%)":   pib,
        "Inflación IPC (%)": inf,
        "Gini":              gin,
    }).set_index("Año")

    st.dataframe(
        df_tabla.style
            .highlight_max(axis=0, color="#FADBD8")
            .highlight_min(axis=0, color="#D5F5E3")
            .format("{:.1f}"),
        use_container_width=True,
    )
    st.caption("🔴 Rojo = máximo del periodo  |  🟢 Verde = mínimo del periodo")

    st.markdown("""
    <div class="analysis-box">
    <strong>Síntesis comparativa:</strong> Los indicadores presentan una correlación positiva
    clara durante el periodo 2017–2023: el deterioro del PIB en 2020 se tradujo en un aumento
    simultáneo del desempleo, la pobreza monetaria y, en el mediano plazo, la inflación
    post-pandemia. El Gini reveló la persistencia estructural de la desigualdad colombiana,
    alcanzando su pico en 2021 junto con el mayor desempleo del periodo. La recuperación
    post-pandemia fue <strong>asimétrica</strong>: más rápida en PIB y más lenta en empleo,
    pobreza y desigualdad, lo que sugiere que el crecimiento económico por sí solo no garantiza
    una mejora equitativa de las condiciones de vida.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONCLUSIONES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="section-title">📝 Conclusión</p>', unsafe_allow_html=True)

st.markdown("""
<div class="conclusion-box">
    <h3>La informalidad como factor estructural de la desigualdad colombiana</h3>
    <p>
    La alta informalidad en Colombia no es solo un problema laboral, sino un factor estructural que limita 
    la productividad del país. Actualmente, alrededor del 55,7% de los trabajadores son informales según el DANE, 
    y en zonas rurales esta cifra alcanza hasta 83,1%, lo que evidencia una economía donde más de la mitad de la 
    fuerza laboral opera fuera de condiciones formales.
    <br><br>
    Esta situación impacta directamente la productividad porque la informalidad está asociada a unidades productivas 
    pequeñas, con baja inversión, escaso acceso a crédito y limitada incorporación de tecnología. De hecho, el propio 
    DANE muestra que la informalidad empresarial alcanza niveles de hasta 90,2% en ciertos sectores, especialmente en actividades 
    de baja productividad como agricultura, transporte y comercio.
     <br><br>   
    Además, el crecimiento del empleo en Colombia no ha resuelto este problema: el 59% de los nuevos empleos creados son informales, 
    lo que indica que el mercado laboral está generando ocupación, pero no empleo productivo ni de calidad.
    <br><br>
    Los datos muestran que la desigualdad en Colombia es un problema estructural y no un 
    episodio aislado. Se evidencia que el mayor deterioro ocurrió en 2020 y 2021, cuando el 
    PIB cayó fuertemente, el desempleo llegó a 17,6%, la pobreza monetaria alcanzó 43,1%, la 
    pobreza extrema 17,3% y el Gini 55,1%. Aunque en 2023 hubo una recuperación del PIB de 0,6% 
    y una reducción parcial de algunos indicadores, la pobreza monetaria todavía fue de 34,6%, la 
    pobreza extrema de 12,6% y el desempleo de 10,2%, lo que demuestra que el crecimiento no se 
    traduce automáticamente en bienestar. Además, la desigualdad territorial sigue siendo muy marcada, 
    pues en 2023 la pobreza monetaria fue de 44,0% en centros poblados y rural disperso frente a 31,8% 
    en cabeceras, y la pobreza extrema fue de 22,0% frente a 9,8%. En consecuencia, la pregunta central 
    se responde señalando que la pobreza, la exclusión y la desigualdad persisten porque el crecimiento 
    económico no ha sido suficientemente inclusivo ni ha corregido las brechas regionales y laborales.
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER / FUENTES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
<strong style="color:#FDFEFE;">Fuentes</strong><br>
• DANE (2023). Gran Encuesta Integrada de Hogares (GEIH) — Series históricas. Bogotá: DANE.<br>
• DANE (2023). Pobreza monetaria y desigualdad — Boletines técnicos 2017–2023. Bogotá: DANE.<br>
• Banco Mundial (2024). Crecimiento del PIB (% anual) — Colombia [NY.GDP.MKTP.KD.ZG].
  Base de datos del Banco Mundial.<br>
• Banco Mundial (2024). Inflación, precios al consumidor (% anual) — Colombia
  [FP.CPI.TOTL.ZG]. Base de datos del Banco Mundial.<br>
• Banco Mundial (2024). Índice de Gini — Colombia [SI.POV.GINI].
  Base de datos del Banco Mundial.<br>
• Banco de la República de Colombia (2024). Informes sobre Inflación y estadísticas
  monetarias. Bogotá: Banrep.<br>
<span style="color:#7FB3D3; font-size:0.78rem;">
Seminario de Desigualdad, Exclusión y Pobreza &nbsp;·&nbsp; Indicadores Colombia 2017–2023
</span>
</div>
""", unsafe_allow_html=True)
