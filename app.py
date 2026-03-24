"""
Boletín de Indicadores — Colombia 2017–2023
Desempleo y Pobreza · Fuente: DANE
"""
 
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
 
st.set_page_config(
    page_title="Indicadores Colombia 2017–2023",
    page_icon="📊",
    layout="wide",
)
 
# ── Estilos ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #1B2631 0%, #1B4F72 60%, #2E86C1 100%);
        padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem;
        border-left: 6px solid #F39C12;
    }
    .header-box h1 { color: #FDFEFE; font-size: 1.8rem; margin: 0 0 0.3rem 0; }
    .header-box p  { color: #AED6F1; font-size: 0.9rem; margin: 0; }
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
    .section-title {
        font-size: 1.15rem; font-weight: 600; color: #1C2833;
        border-bottom: 2px solid #2E86C1; padding-bottom: 0.3rem;
        margin: 1.2rem 0 0.8rem 0;
    }
    .footer {
        margin-top: 2.5rem; padding: 1.2rem; background: #1B2631;
        border-radius: 8px; color: #AED6F1; font-size: 0.8rem; line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)
 
AÑOS = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
C_DES = "#7D3C98"
C_POB = "#D35400"
C_EXT = "#F0B27A"
 
# ── Cargar datos ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # ── Desempleo ──────────────────────────────────────────────────────────────
    df_d = pd.read_csv("desempleo.csv", index_col=0)
    df_d.columns = AÑOS
    td  = float(df_d.loc["Tasa de Desocupación (TD)"].values[3])       # 2020
    tgp = df_d.loc["Tasa Global de Participación (TGP)"].tolist()
    to_ = df_d.loc["Tasa de Ocupación (TO)"].tolist()
    tdd = df_d.loc["Tasa de Desocupación (TD)"].tolist()
 
    # ── Pobreza ────────────────────────────────────────────────────────────────
    df_p = pd.read_csv("pobreza.csv", header=None)
    mon_nac = df_p.iloc[1, 1:8].astype(float).tolist()  # fila 1 = nacional monetaria
    ext_nac = df_p.iloc[6, 1:8].astype(float).tolist()  # fila 6 = nacional extrema
 
    return tgp, to_, tdd, mon_nac, ext_nac
 
tgp, to_, tdd, mon_nac, ext_nac = load_data()
 
# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>📊 Boletín de Indicadores — Colombia 2017–2023</h1>
    <p>Seminario de Desigualdad, Exclusión y Pobreza &nbsp;·&nbsp; Nivel Nacional &nbsp;·&nbsp; Fuente: DANE</p>
</div>
""", unsafe_allow_html=True)
 
# ── KPIs ───────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📌 Valores clave del periodo</p>', unsafe_allow_html=True)
 
k1, k2, k3 = st.columns(3)
def kpi(col, label, value, unit, sub, color):
    col.markdown(f"""
    <div class="kpi-card" style="border-top-color:{color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color}">{value}<span style="font-size:1rem">{unit}</span></div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)
 
kpi(k1, "Desempleo máximo", "17.6", "%", "2021 — post-COVID", C_DES)
kpi(k2, "Pobreza monetaria máx.", "43.1", "%", "2020 — COVID-19", C_POB)
kpi(k3, "Pobreza extrema máx.", "17.3", "%", "2020 — COVID-19", C_EXT)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ── Helper: banda COVID ────────────────────────────────────────────────────────
def covid_band(fig):
    fig.add_vrect(
        x0=2019.5, x1=2020.5, fillcolor="#FADBD8", opacity=0.35,
        layer="below", line_width=0,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font_color="#C0392B", annotation_font_size=11,
    )
    return fig
 
def base_layout(fig, title, ytitle):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#1C2833")),
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title=ytitle, gridcolor="#ECF0F1"),
        xaxis=dict(tickmode="array", tickvals=AÑOS, gridcolor="#ECF0F1"),
        margin=dict(t=55, b=40, l=55, r=40),
    )
    return fig
 
# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📉 Desempleo", "📊 Pobreza", "🔗 Comparativo"])
 
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-title">Indicadores del Mercado Laboral Nacional</p>',
                unsafe_allow_html=True)
 
    fig_des = go.Figure()
    fig_des.add_trace(go.Scatter(
        x=AÑOS, y=tgp, name="TGP (%)",
        mode="lines+markers",
        line=dict(color="#1B4F72", width=2.5),
        marker=dict(size=8, symbol="circle"),
        hovertemplate="<b>%{x}</b> · TGP: %{y:.1f}%<extra></extra>",
    ))
    fig_des.add_trace(go.Scatter(
        x=AÑOS, y=to_, name="TO (%)",
        mode="lines+markers",
        line=dict(color="#27AE60", width=2.5, dash="dash"),
        marker=dict(size=8, symbol="square"),
        hovertemplate="<b>%{x}</b> · TO: %{y:.1f}%<extra></extra>",
    ))
    fig_des.add_trace(go.Scatter(
        x=AÑOS, y=tdd, name="TD — Desempleo (%)",
        mode="lines+markers+text",
        line=dict(color=C_DES, width=3),
        marker=dict(size=10, symbol="diamond"),
        text=[f"{v:.1f}%" for v in tdd],
        textposition="top center",
        textfont=dict(size=10, color=C_DES),
        fill="tozeroy", fillcolor="rgba(125,60,152,0.07)",
        hovertemplate="<b>%{x}</b> · TD: %{y:.1f}%<extra></extra>",
    ))
    fig_des = covid_band(fig_des)
    fig_des = base_layout(fig_des, "Mercado Laboral Nacional · Colombia 2017–2023", "Tasa (%)")
    fig_des.update_yaxes(range=[0, 75])
    st.plotly_chart(fig_des, use_container_width=True)
 
    st.markdown("""
    <div class="analysis-box">
    <strong>Análisis:</strong> La Tasa de Desocupación (TD) mostró una tendencia al alza moderada
    entre 2017 (12,0%) y 2019 (13,1%), antes del choque externo. En <strong>2020–2021</strong>
    el desempleo alcanzó su pico de <strong>17,6%</strong>, producto del cierre de actividades durante
    la pandemia de COVID-19. La recuperación fue gradual: 14,6% en 2022 y 13,7% en 2023, sin retornar
    aún a niveles pre-pandemia, evidenciando <strong>cicatrices estructurales</strong> en sectores de
    turismo, comercio e informalidad. La caída simultánea en la TGP (2020–2021) refleja el efecto
    del trabajador desalentado: personas que dejaron de buscar empleo activamente.
    </div>
    <div class="note-box">
    ⚠️ <strong>Nota metodológica:</strong> La TD excluye a trabajadores desalentados y subempleados,
    por lo que puede subestimar el deterioro real del mercado laboral. Fuente: DANE — GEIH.
    </div>
    """, unsafe_allow_html=True)
 
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)
 
    with col_a:
        st.markdown('<p class="section-title">Pobreza Monetaria Nacional (%)</p>',
                    unsafe_allow_html=True)
        fig_mon = go.Figure()
        fig_mon.add_trace(go.Bar(
            x=AÑOS, y=mon_nac, name="Pobreza monetaria (%)",
            marker_color=C_POB, opacity=0.85,
            text=[f"{v:.1f}%" for v in mon_nac],
            textposition="outside",
            hovertemplate="<b>%{x}</b> · %{y:.1f}%<extra></extra>",
        ))
        fig_mon.add_trace(go.Scatter(
            x=AÑOS, y=mon_nac, mode="lines+markers",
            name="Tendencia", line=dict(color="#922B21", width=2, dash="dot"),
            marker=dict(size=7),
            hovertemplate="<b>%{x}</b> · %{y:.1f}%<extra></extra>",
        ))
        fig_mon = covid_band(fig_mon)
        fig_mon = base_layout(fig_mon, "Pobreza Monetaria · Colombia 2017–2023", "Porcentaje (%)")
        fig_mon.update_yaxes(range=[0, 50])
        st.plotly_chart(fig_mon, use_container_width=True)
 
    with col_b:
        st.markdown('<p class="section-title">Pobreza Extrema Nacional (%)</p>',
                    unsafe_allow_html=True)
        fig_ext = go.Figure()
        fig_ext.add_trace(go.Bar(
            x=AÑOS, y=ext_nac, name="Pobreza extrema (%)",
            marker_color=C_EXT, opacity=0.9,
            text=[f"{v:.1f}%" for v in ext_nac],
            textposition="outside",
            hovertemplate="<b>%{x}</b> · %{y:.1f}%<extra></extra>",
        ))
        fig_ext.add_trace(go.Scatter(
            x=AÑOS, y=ext_nac, mode="lines+markers",
            name="Tendencia", line=dict(color=C_POB, width=2, dash="dot"),
            marker=dict(size=7),
            hovertemplate="<b>%{x}</b> · %{y:.1f}%<extra></extra>",
        ))
        fig_ext = covid_band(fig_ext)
        fig_ext = base_layout(fig_ext, "Pobreza Extrema · Colombia 2017–2023", "Porcentaje (%)")
        fig_ext.update_yaxes(range=[0, 22])
        st.plotly_chart(fig_ext, use_container_width=True)
 
    st.markdown("""
    <div class="analysis-box">
    <strong>Análisis:</strong> La pobreza monetaria nacional se mantuvo relativamente estable en
    torno a 35–36% entre 2017 y 2019, antes de dar un salto dramático a <strong>43,1%</strong>
    en 2020 — equivalente a aproximadamente <strong>21 millones de personas</strong> por debajo
    de la línea de pobreza. Este aumento está vinculado directamente a la pérdida de ingresos
    laborales durante la pandemia, que afectó desproporcionadamente a trabajadores informales
    (~47% de la fuerza laboral). La pobreza extrema pasó de 12,0% (2019) a <strong>17,3%</strong>
    (2020). La recuperación parcial en 2021–2023 es atribuible a la reactivación económica y
    programas de transferencias como <em>Ingreso Solidario</em>, aunque en 2023 los niveles
    todavía no retornan al mínimo histórico del periodo.
    </div>
    """, unsafe_allow_html=True)
 
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-title">Desempleo vs. Pobreza Monetaria</p>',
                unsafe_allow_html=True)
 
    fig_cmp = make_subplots(specs=[[{"secondary_y": True}]])
    fig_cmp.add_trace(go.Scatter(
        x=AÑOS, y=tdd, name="Desempleo TD (%)",
        mode="lines+markers",
        line=dict(color=C_DES, width=3),
        marker=dict(size=9, symbol="diamond"),
        hovertemplate="TD: %{y:.1f}%<extra></extra>",
    ), secondary_y=False)
    fig_cmp.add_trace(go.Scatter(
        x=AÑOS, y=mon_nac, name="Pobreza monetaria (%)",
        mode="lines+markers",
        line=dict(color=C_POB, width=3, dash="dash"),
        marker=dict(size=9, symbol="circle"),
        hovertemplate="Pobreza: %{y:.1f}%<extra></extra>",
    ), secondary_y=True)
    fig_cmp.add_vrect(
        x0=2019.5, x1=2020.5, fillcolor="#FADBD8", opacity=0.35,
        layer="below", line_width=0,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font_color="#C0392B", annotation_font_size=11,
    )
    fig_cmp.update_layout(
        title=dict(text="Desempleo vs. Pobreza Monetaria · Colombia 2017–2023",
                   font=dict(size=15, color="#1C2833")),
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(tickmode="array", tickvals=AÑOS, gridcolor="#ECF0F1"),
        margin=dict(t=55, b=40, l=55, r=55),
    )
    fig_cmp.update_yaxes(title_text="Tasa de Desocupación (%)", secondary_y=False,
                          gridcolor="#ECF0F1", range=[0, 22])
    fig_cmp.update_yaxes(title_text="Pobreza Monetaria (%)", secondary_y=True,
                          range=[30, 48])
    st.plotly_chart(fig_cmp, use_container_width=True)
 
    st.markdown('<p class="section-title">📋 Tabla resumen</p>', unsafe_allow_html=True)
    df_tabla = pd.DataFrame({
        "Año": AÑOS,
        "TGP (%)": tgp,
        "TO (%)":  to_,
        "TD — Desempleo (%)": tdd,
        "Pobreza monetaria (%)": mon_nac,
        "Pobreza extrema (%)":  ext_nac,
    }).set_index("Año")
    st.dataframe(
        df_tabla.style
            .highlight_max(axis=0, color="#FADBD8")
            .highlight_min(axis=0, color="#D5F5E3")
            .format("{:.1f}"),
        use_container_width=True,
    )
    st.caption("🔴 Máximo del periodo &nbsp;|&nbsp; 🟢 Mínimo del periodo")
 
    st.markdown("""
    <div class="analysis-box">
    <strong>Síntesis:</strong> Los dos indicadores muestran una correlación positiva clara:
    cuando el desempleo sube, la pobreza monetaria también lo hace, con 2020 como el año de
    mayor deterioro simultáneo. El mercado laboral es el canal de transmisión más directo entre
    la actividad económica y el bienestar de los hogares. La recuperación post-pandemia fue
    más rápida en términos de crecimiento económico (PIB) que en términos de empleo y pobreza,
    lo que evidencia una <strong>recuperación asimétrica</strong> que benefició más a los hogares
    de mayores ingresos.
    </div>
    """, unsafe_allow_html=True)
 
# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
<strong style="color:#FDFEFE;">📚 Fuentes</strong><br>
• DANE (2023). <em>Gran Encuesta Integrada de Hogares (GEIH) — Series históricas.</em> Bogotá: DANE.<br>
• DANE (2023). <em>Pobreza monetaria y desigualdad — Boletines técnicos 2017–2023.</em> Bogotá: DANE.<br>
<span style="color:#7FB3D3; font-size:0.78rem;">Seminario de Desigualdad, Exclusión y Pobreza · Indicadores Colombia 2017–2023</span>
</div>
""", unsafe_allow_html=True)