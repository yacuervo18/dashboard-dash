import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import unicodedata
import numpy as np


#Bases de datos
youtube_df = pd.read_csv(
    "https://raw.githubusercontent.com/yacuervo18/BasesDeDatos/01630ab19085d4e2d14e82acd15f0a1e8927b2ff/youtube_candidatos.csv"
)
google_df = pd.read_csv(
    "https://raw.githubusercontent.com/yacuervo18/BasesDeDatos/01630ab19085d4e2d14e82acd15f0a1e8927b2ff/google_trends_candidatos.csv"
)

#Variables requeridas para las funciones

youtube_df["fecha_publicacion"] = pd.to_datetime(youtube_df["fecha_publicacion"])
youtube_df["mes"] = youtube_df["fecha_publicacion"].dt.month
youtube_df["año"] = youtube_df["fecha_publicacion"].dt.year
youtube_df["semana"] = youtube_df["fecha_publicacion"].dt.isocalendar().week
youtube_df["mes_nombre"] = youtube_df["fecha_publicacion"].dt.strftime("%B").str.capitalize()

google_df["date"] = pd.to_datetime(google_df["date"])
google_df["año"] = google_df["date"].dt.year
google_df["semana"] = google_df["date"].dt.isocalendar().week


#Dashboard
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)


app.layout = dbc.Container(
    fluid=True,
    style={"backgroundColor": "white"},   # ← Fondo general del dashboard
    children=[


    html.H1(
    "Análisis Digital de precandidatos 2024-2025",
    style={
        "textAlign": "center",
        "marginTop": "20px",
        "marginBottom": "20px",
        "fontFamily": "Poppins, sans-serif",   # tipo de letra
        "color": "#4B1075",                    # morado oscuro
        "fontWeight": "700"                    # más grueso (opcional)
    }
),

    # Banner con la foto de los candidatos
    dbc.Row([
        dbc.Col(
            html.A(
                html.Div([
                    html.Img(
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcST2wJasThqQZfL-TJ2Q8LbpdF5J2lV1kmpdQ&s",
                        style={"width": "90px", "border-radius": "50%", "margin-bottom": "10px"}
                    ),
                    html.H5("Vicky Dávila", style={"margin": "0", "font-weight": "bold"}),
                    html.P("333k Suscriptores", style={"font-size": "14px", "margin": "0"})
                ], style={"text-align": "center"}),
                href="https://www.youtube.com/@vickydaviladigital",
                target="_blank",
                style={"text-decoration": "none", "color": "black"}
            ), md=4
        ),

        dbc.Col(
            html.A(
                html.Div([
                    html.Img(
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfCWE8X6yg_o4ibH6JWHsLuQhWlKrbkKFnow&s",
                        style={"width": "90px", "border-radius": "50%", "margin-bottom": "10px"}
                    ),
                    html.H5("Gustavo Bolívar", style={"margin": "0", "font-weight": "bold"}),
                    html.P("259k Suscriptores", style={"font-size": "14px", "margin": "0"})
                ], style={"text-align": "center"}),
                href="https://www.youtube.com/@BolivarGustavo",
                target="_blank",
                style={"text-decoration": "none", "color": "black"}
            ), md=4
        ),

        dbc.Col(
            html.A(
                html.Div([
                    html.Img(
                        src="https://upload.wikimedia.org/wikipedia/commons/a/a0/Claudia_L%C3%B3pez.png",
                        style={"width": "90px", "border-radius": "50%", "margin-bottom": "10px"}
                    ),
                    html.H5("Claudia López", style={"margin": "0", "font-weight": "bold"}),
                    html.P("26.7k Suscriptores", style={"font-size": "14px", "margin": "0"})
                ], style={"text-align": "center"}),
                href="https://www.youtube.com/c/ClaudiaL%C3%B3pezCL",
                target="_blank",
                style={"text-decoration": "none", "color": "black"}
            ), md=4
        ),
    ],
        style={"padding": "15px", "background": "#ECE9ED", "border-radius": "8px",
               "margin-bottom": "20px", "margin-top": "2px"}
    ),
    html.Div(
    style={
        "width": "100%",
        "height": "4px",
        "margin-top": "-18px",
        "margin-bottom": "20px",
        "border-radius": "4px",
        "background": "linear-gradient(90deg, #FF64E0, #76E4B1, #2C7BDC)"
    }
),
    # Contenido principal
    dbc.Row([
        dbc.Col([
            html.H4("Descubre los resultados"),
            html.P("Panel interactivo para explorar métricas, que permiten conocer el desempeño digital de los precandidatos."),

            dbc.Button("Líneas de tiempo", id="btn-tiempo", color="primary", className="mb-2", style={"width": "100%","background": "#6B46C1", "border": "none"}),
            dbc.Button("Comparaciones", id="btn-comparaciones", color="primary", className="mb-2", style={"width": "100%","background": "#6B46C1", "border": "none"}),

            dbc.Button("Correlación YouTube–Google Trends", id="btn-correlacion",
                       color="primary", className="mb-2", style={"width": "100%","background": "#6B46C1", "border": "none"}),

            dbc.Button("Distribución del engagement", id="btn-engagement",
                       color="primary", className="mb-2", style={"width": "100%","background": "#6B46C1", "border": "none"}),

            # ------------------ AQUI AGREGO EL GRÁFICO DE ANILLO ------------------
            html.Hr(),

            html.H5("Suscriptores por candidato", style={"textAlign": "center"}),

            dcc.Graph(
                id="grafico-suscriptores",
                style={"height": "260px"}
            )
            # ----------------------------------------------------------------------

        ], md=3),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Visualización"),
                dbc.CardBody(id="contenido-dinamico")
            ])
        ], md=9)
    ], align="start")
])


# MENU LATERAL
@app.callback(
    Output("contenido-dinamico", "children"),
    Input("btn-tiempo", "n_clicks"),
    Input("btn-comparaciones", "n_clicks"),
    Input("btn-correlacion", "n_clicks"),
    Input("btn-engagement", "n_clicks")
)
def mostrar_contenido(btn1, btn2, btn3, btn4):

    ctx = dash.callback_context

    if not ctx.triggered:
        return html.P("Seleccione una opción del menú izquierdo.")

    boton = ctx.triggered[0]["prop_id"].split(".")[0]

    # ---------------------- LÍNEAS DE TIEMPO (MODIFICADO) ----------------------
    if boton == "btn-tiempo":
        return [
            html.H5("Seleccione candidatos"),
            dcc.Dropdown(
                id="selector-candidatos",
                options=[{"label": c, "value": c} for c in youtube_df["candidato"].unique()],
                value=[youtube_df["candidato"].unique()[0]],
                multi=True
            ),

            html.H5("Seleccione métrica a graficar", style={"marginTop": "10px"}),
            dcc.Dropdown(
                id="selector-metrica",
                options=[
                    {"label": "Vistas", "value": "vistas"},
                    {"label": "Likes", "value": "likes"},
                    {"label": "Comentarios", "value": "comentarios"},
                    {"label": "Engagement", "value": "engagement"},
                ],
                value="vistas"
            ),

            dcc.Graph(id="grafica-linea-tiempo")
        ]
    # ---------------------------------------------------------------------------

    # Botón Comparaciones
    if boton == "btn-comparaciones":
        return [
            html.H4("Comparación 1: Engagement por 1000 vistas (3 candidatos)"),
            dcc.Dropdown(
                id="cmp1-mes",
                options=[{"label": m, "value": m} for m in youtube_df["mes_nombre"].unique()],
                placeholder="Seleccione un mes"
            ),
            dcc.Dropdown(
                id="cmp1-año",
                options=[{"label": a, "value": a} for a in sorted(youtube_df["año"].unique())],
                placeholder="Seleccione un año"
            ),
            dcc.Graph(id="grafica-comparacion1"),

            html.Hr(),

            html.H4("Comparación 2: Likes promedio (Torta)"),
            dcc.Dropdown(
                id="cmp2-mes",
                options=[{"label": m, "value": m} for m in youtube_df["mes_nombre"].unique()],
                placeholder="Seleccione un mes"
            ),
            dcc.Dropdown(
                id="cmp2-año",
                options=[{"label": a, "value": a} for a in sorted(youtube_df["año"].unique())],
                placeholder="Seleccione un año"
            ),
            dcc.Graph(id="grafica-comparacion2")
        ]

    # Correlación
    if boton == "btn-correlacion":
        return [
            html.H4("Correlación temporal (Lag) entre Google Trends y YouTube"),
            html.P("Identifica si los picos de búsquedas anteceden o siguen los picos de vistas, likes o comentarios."),

            dcc.Dropdown(
                id="corr-metrica",
                options=[
                    {"label": "Vistas", "value": "vistas"},
                    {"label": "Likes", "value": "likes"},
                    {"label": "Comentarios", "value": "comentarios"},
                ],
                value="vistas"
            ),

            dcc.Graph(id="grafica-correlacion")
        ]

    # Engagement
    if boton == "btn-engagement":
        return [
            html.H4("Distribución del Engagement (Anillos)"),
            html.P("Visualización de: Likes / Comentarios / Vistas por cada 1000 suscriptores"),

            html.Div([
                dcc.Dropdown(
                    id="dist-candidatos",
                    options=[{"label": c, "value": c} for c in youtube_df["candidato"].unique()],
                    value=list(youtube_df["candidato"].unique()),
                    multi=True,
                    placeholder="Seleccione candidatos (por defecto: todos)"
                ),
                dcc.Dropdown(
                    id="dist-año",
                    options=[{"label": a, "value": a} for a in sorted(youtube_df["año"].unique())],
                    placeholder="Seleccione año (opcional)",
                    style={"marginTop": "8px"}
                ),
                dcc.Dropdown(
                    id="dist-mes",
                    options=[{"label": m, "value": m} for m in youtube_df["mes_nombre"].unique()],
                    placeholder="Seleccione mes (opcional)",
                    style={"marginTop": "8px"}
                )
            ], style={"marginBottom": "12px"}),

            dcc.Graph(id="graf-engagement")
        ]

    return html.P("Seleccione una opción.")



# ----------------------- CALLBACK: LÍNEAS DE TIEMPO -----------------------
@app.callback(
    Output("grafica-linea-tiempo", "figure"),
    Input("selector-candidatos", "value"),
    Input("selector-metrica", "value")
)
def actualizar_linea_tiempo(lista_candidatos, metrica):

    if not lista_candidatos:
        return px.line(title="Seleccione un candidato")

    df = youtube_df[youtube_df["candidato"].isin(lista_candidatos)].copy()

    if metrica == "engagement":
        df["engagement"] = df["likes"] + df["comentarios"]

    fig = px.line(
        df,
        x="fecha_publicacion",
        y=metrica,
        color="candidato",
        markers=True,
        color_discrete_map={
            "Vicky Dávila": "#FF64E0",
            "Gustavo Bolívar": "#76E4B1",
            "Claudia López": "#2C7BDC"
        },
        title=f"Evolución de {metrica} en el tiempo"
    )

    fig.update_layout(template="plotly_white")
    return fig


#   CALLBACK — COMPARACIÓN 1
@app.callback(
    Output("grafica-comparacion1", "figure"),
    Input("cmp1-mes", "value"),
    Input("cmp1-año", "value")
)
def comparacion1(mes_nombre, año):

    if not mes_nombre or not año:
        return px.bar(title="Seleccione mes y año")

    df = youtube_df[(youtube_df["mes_nombre"] == mes_nombre) & (youtube_df["año"] == año)].copy()

    if df.empty:
        return px.bar(title="No hay datos para esa combinación")

    df["engagement_norm"] = (df["likes"] + df["comentarios"]) / (df["vistas"].replace(0, pd.NA) / 1000)
    resumen = df.groupby("candidato")["engagement_norm"].mean().reset_index()

    fig = px.bar(
        resumen,
        x="engagement_norm",
        y="candidato",
        orientation="h",
        color="candidato",
        color_discrete_sequence=["#2C7BDC","#76E4B1","#FF64E0" ],   # ← AQUÍ ESTABA EL ERROR (faltaba coma)
        title=f"Engagement por 1000 vistas — {mes_nombre} {año}"
    )

    fig.update_layout(template="plotly_white")
    return fig


#   CALLBACK — COMPARACIÓN 2
@app.callback(
    Output("grafica-comparacion2", "figure"),
    Input("cmp2-mes", "value"),
    Input("cmp2-año", "value")
)
def comparacion2(mes_nombre, año):

    if not mes_nombre or not año:
        return px.pie(title="Seleccione mes y año")

    df = youtube_df[(youtube_df["mes_nombre"] == mes_nombre) & (youtube_df["año"] == año)]

    resumen = df.groupby("candidato")["likes"].mean().reset_index()

    # Colores personalizados para cada candidato
    colores = {
        "Vicky Dávila": "#FF64E0",
        "Gustavo Bolívar": "#76E4B1",
        "Claudia López": "#2C7BDC"
    }

    fig = px.pie(
        resumen,
        names="candidato",
        values="likes",
        hole=0.5,
        title=f"Likes promedio — {mes_nombre} {año} (Anillo)",
        color="candidato",
        color_discrete_map=colores
    )

    fig.update_layout(template="plotly_white")
    return fig

#   CALLBACK — CORRELACIÓN TEMPORAL (DISPERSIÓN)
@app.callback(
    Output("grafica-correlacion", "figure"),
    Input("corr-metrica", "value")
)
def correlacion_lag(metrica):

    df_y = youtube_df.groupby(["año", "semana"])[metrica].sum().reset_index()
    df_g = google_df.groupby(["año", "semana"])[["Gustavo Bolívar", "Claudia López", "Vicky Dávila"]].mean().reset_index()

    df = pd.merge(df_y, df_g, on=["año", "semana"], how="inner")

    df["trends"] = df[["Gustavo Bolívar", "Claudia López", "Vicky Dávila"]].mean(axis=1)

    fig = px.scatter(
        df,
        x="trends",
        y=metrica,
        title=f"Relación entre búsquedas en Google Trends y {metrica.capitalize()} en YouTube",
        labels={
            "trends": "Interés promedio en Google Trends",
            metrica: f"{metrica.capitalize()} (YouTube)"
        }
    )

    fig.update_layout(template="plotly_white")
    return fig


#   CALLBACK — ENGAGEMENT ANILLOS
@app.callback(
    Output("graf-engagement", "figure"),
    Input("dist-candidatos", "value"),
    Input("dist-año", "value"),
    Input("dist-mes", "value"),
)
def graficos_engagement(candidatos_sel, año_sel, mes_sel):

    if not candidatos_sel:
        return go.Figure()

    df = youtube_df.copy()
    if año_sel:
        df = df[df["año"] == año_sel]
    if mes_sel:
        df = df[df["mes_nombre"] == mes_sel]

    if df.empty:
        return px.bar(title="No hay datos para la selección")

    resumen = df.groupby("candidato").agg({
        "likes": "sum",
        "comentarios": "sum",
        "vistas": "sum",
        "suscriptores_canal": "mean"
    }).reset_index()

    resumen = resumen[resumen["candidato"].isin(candidatos_sel)].reset_index(drop=True)

    if resumen.empty:
        return px.bar(title="No hay datos para los candidatos seleccionados")

    resumen["subs_1000"] = resumen["suscriptores_canal"].replace(0, np.nan) / 1000.0
    resumen["likes_1000"] = resumen["likes"] / resumen["subs_1000"]
    resumen["comentarios_1000"] = resumen["comentarios"] / resumen["subs_1000"]
    resumen["vistas_1000"] = resumen["vistas"] / resumen["subs_1000"]

    resumen[["likes_1000", "comentarios_1000", "vistas_1000"]] = resumen[["likes_1000", "comentarios_1000", "vistas_1000"]].fillna(0)

    # ----- Conversión a formato largo para barras -----
    resumen_melt = resumen.melt(
        id_vars="candidato",
        value_vars=["likes_1000", "comentarios_1000", "vistas_1000"],
        var_name="metrica",
        value_name="valor"
    )

    nombres_mostrar = {
        "likes_1000": "Likes por 1000 suscriptores",
        "comentarios_1000": "Comentarios por 1000 suscriptores",
        "vistas_1000": "Vistas por 1000 subscriptores"
    }

    resumen_melt["metrica"] = resumen_melt["metrica"].replace(nombres_mostrar)

    # ----- Colores fijos por candidato -----
    colores_candidatos = {
        "Vicky Dávila": "#FF64E0",
        "Gustavo Bolívar": "#76E4B1",
        "Claudia López": "#2C7BDC"
    }

    # ----- Gráfico final -----
    fig = px.bar(
        resumen_melt,
        x="metrica",
        y="valor",
        color="candidato",
        barmode="group",
        color_discrete_map=colores_candidatos,
        title="Engagement normalizado por cada 1000 suscriptores"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Métrica",
        yaxis_title="Valor normalizado",
        legend_title="Candidato"
    )

    return fig



# ------------------ CALLBACK DEL GRÁFICO DE ANILLO NUEVO ------------------
@app.callback(
    Output("grafico-suscriptores", "figure"),
    Input("grafico-suscriptores", "id")
)
def mini_grafico_suscriptores(_):

    data = pd.DataFrame({
        "candidato": ["Vicky Dávila", "Gustavo Bolívar", "Claudia López"],
        "suscriptores": [333000, 259000, 26700]
    })

    fig = px.pie(
        data,
        names="candidato",
        values="suscriptores",
        hole=0.55,
        title="",
        color="candidato",
        color_discrete_sequence=["#FF64E0","#76E4B1", "#2C7BDC"]  
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend_title_text=""
    )

    return fig

# ---------------------------------------------------------------------------

# Para ejecutar
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8000, debug=False)
