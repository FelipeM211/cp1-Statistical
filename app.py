"""
PROJETO: Dashboard Profissional - Currículo & Estudo de Mercado
DISCIPLINA: Data Science and Statistical Computing (CP1)
ALUNO: Felipe Balbino Murad
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ============================================================
# 1. CARREGAMENTO E TRATAMENTO DOS DADOS
# ============================================================

def load_data():
    """Carrega salaries.csv com fallback de nomes de colunas."""
    try:
        df = pd.read_csv("salaries.csv")

        # Fallbacks: aceita variações de nome das colunas
        colunas = {
            "work_year": ["work_year", "year", "ano"],
            "experience_level": ["experience_level", "exp_level", "nivel_experiencia"],
            "job_title": ["job_title", "role", "cargo"],
            "salary_in_usd": ["salary_in_usd", "salary_usd", "salario_usd"],
            "company_size": ["company_size", "size", "tamanho_empresa"],
        }
        for alvo, opcoes in colunas.items():
            for op in opcoes:
                if op in df.columns and op != alvo:
                    df.rename(columns={op: alvo}, inplace=True)

        df = df.dropna(subset=["salary_in_usd", "experience_level"])

        # Nomes amigáveis para os níveis de experiência
        exp_map = {
            "EN": "Entry / Junior",
            "MI": "Mid-level / Pleno",
            "SE": "Senior / Expert",
            "EX": "Executive / Direção",
        }
        df["experience_level"] = df["experience_level"].replace(exp_map)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(
            columns=["work_year", "experience_level", "job_title", "salary_in_usd"]
        )

df = load_data()

# ============================================================
# 2. LAYOUT DO DASHBOARD
# ============================================================

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Felipe Murad | Dashboard Profissional"

CARD = {"box-shadow": "0 4px 8px rgba(0,0,0,0.2)", "border-radius": "10px", "padding": "15px"}

# ----- ABA 1: QUEM SOU EU -----
tab_quem_sou = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                # ESPAÇO PARA FOTO: salve sua imagem como assets/foto.png
                html.Img(src="/assets/foto.png", className="img-fluid rounded-circle",
                         style={"width": "250px", "height": "250px",
                                "object-fit": "cover", "border": "5px solid #2c3e50"}),
                html.H2("Felipe Balbino Murad", className="mt-3"),
                html.P("Estudante de Engenharia de Software - FIAP", className="lead"),
                html.Hr(),
                html.P([html.Strong("Email: "), "felipebmurad@gmail.com"]),
                html.P([html.Strong("Telefone: "), "+55 11 96392-2503"]),
                html.P([html.Strong("Local: "), "São Paulo, SP"]),
                dbc.Button("LinkedIn", href="https://www.linkedin.com/in/felipebmurad/",
                           target="_blank", color="primary", className="me-2"),
                dbc.Button("GitHub", href="https://github.com/FelipeM211",
                           target="_blank", color="dark"),
            ], width=4, className="text-center border-end"),
            dbc.Col([
                html.H3("Minibio Profissional"),
                html.P("""Entusiasta de tecnologia com forte interesse em Segurança da Informação.
                    Cursando Engenharia de Software na FIAP, busco constantemente aprender sobre a
                    área por conta própria. Tenho experiência em projetos acadêmicos e em parceria
                    com empresas reais (TOTVS, Passa a Bola), desenvolvendo soluções com Python,
                    Java, JavaScript e boas práticas de programação. Vivência internacional e
                    fluência em inglês.""", style={"text-align": "justify"}),
                html.H4("Objetivo", className="mt-4"),
                html.P("Iniciar minha carreira na área de Segurança da Informação, aplicando os "
                       "conhecimentos desenvolvidos na graduação e adquirindo experiência prática "
                       "para continuar evoluindo na área."),
                html.H4("Diferenciais", className="mt-4"),
                html.Ul([
                    html.Li("Inglês fluente (intercâmbio no Canadá - 2023)"),
                    html.Li("Design Thinking aplicado a projetos reais"),
                    html.Li("Experiência com prototipação em Figma e UX Research"),
                ]),
            ], width=8, className="ps-4"),
        ])
    ]), className="mt-3", style=CARD
)

# ----- ABA 2: QUALIFICAÇÕES -----
tab_qualificacoes = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H4("Educação Acadêmica"),
                html.Ul([
                    html.Li([html.Strong("FIAP (Aclimação): "),
                             "Engenharia de Software (Jan/2025 - Cursando)"]),
                    html.Li([html.Strong("Colégio Dante Alighieri: "),
                             "Ensino Médio completo (2024)"]),
                    html.Li([html.Strong("Kildonan East Collegiate (Canadá): "),
                             "Intercâmbio Grade 11 (2023)"]),
                ]),
                html.H4("Formação Complementar", className="mt-4"),
                html.Ul([
                    html.Li("Nano Course Design Thinking - FIAP"),
                    html.Li("Curso Python na Prática - By Learn"),
                ]),
            ], width=6),
            dbc.Col([
                html.H4("Experiências & Projetos Reais"),
                dbc.Accordion([
                    dbc.AccordionItem(
                        [
                            html.P("Solução desenvolvida em equipe em parceria com a TOTVS, "
                                   "utilizando Inteligência Artificial para analisar transcrições "
                                   "de reuniões e identificar pontos que poderiam passar "
                                   "despercebidos pelos participantes."),
                            html.P([html.Strong("Tecnologias: "),
                                    "JavaScript, HTML, CSS e Python."], className="mb-0"),
                        ],
                        title="Projeto TOTVS - Análise de Reuniões com IA (2026)",
                    ),
                    dbc.AccordionItem(
                        [
                            html.P("Protótipo de aplicativo/site desenvolvido em Figma, com "
                                   "pesquisa de campo e metodologia de Design Centrado no Usuário. "
                                   "Foco em resolver gargalos operacionais e melhorar a experiência "
                                   "dos usuários."),
                            html.P([html.Strong("Resultado: "),
                                    "80% de feedback positivo dos usuários testadores."],
                                   className="mb-0"),
                        ],
                        title="Projeto Passa a Bola (Mai-Jun 2025)",
                    ),
                    dbc.AccordionItem(
                        [
                            html.P("Período de estudos em Winnipeg, Canadá, que contribuiu para o "
                                   "desenvolvimento pessoal e para a fluência em inglês técnico e "
                                   "acadêmico."),
                        ],
                        title="Intercâmbio Cultural e Acadêmico (2023)",
                    ),
                ]),
            ], width=6),
        ])
    ]), className="mt-3", style=CARD
)

# ----- ABA 3: SKILLS -----
tab_skills = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H4("Hard Skills"),
                html.P("Python (Intermediário)"),
                dbc.Progress(value=70, color="success", className="mb-3"),
                html.P("Java (Intermediário)"),
                dbc.Progress(value=60, color="info", className="mb-3"),
                html.P("HTML / CSS / JavaScript"),
                dbc.Progress(value=75, color="warning", className="mb-3"),
                html.P("Arduino / C++"),
                dbc.Progress(value=55, color="danger", className="mb-3"),
            ], width=6),
            dbc.Col([
                html.H4("Soft Skills & Idiomas"),
                html.P("Inglês Fluente (B2/C1)"),
                dbc.Progress(value=90, color="primary", className="mb-3"),
                html.H5("Competências Comportamentais", className="mt-4"),
                dbc.Badge("Design Thinking", color="secondary", className="me-1 p-2 mb-1"),
                dbc.Badge("Resolução de Problemas", color="success", className="me-1 p-2 mb-1"),
                dbc.Badge("Trabalho em Equipe", color="info", className="me-1 p-2 mb-1"),
                dbc.Badge("Comunicação", color="warning", className="me-1 p-2 mb-1"),
                dbc.Badge("Proatividade", color="danger", className="me-1 p-2 mb-1"),
            ], width=6),
        ])
    ]), className="mt-3", style=CARD
)

# ----- ABA 4: ANÁLISE DE DADOS (ESTUDO DE MERCADO) -----
tab_analise = html.Div([
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H6("Total de Registros", className="text-muted"),
            html.H3(f"{len(df):,}".replace(",", "."))
        ], body=True, style=CARD), width=3),
        dbc.Col(dbc.Card([
            html.H6("Salário Médio (USD)", className="text-muted"),
            html.H3(f"${df['salary_in_usd'].mean():,.0f}" if not df.empty else "-")
        ], body=True, style=CARD), width=3),
        dbc.Col(dbc.Card([
            html.H6("Salário Mediano (USD)", className="text-muted"),
            html.H3(f"${df['salary_in_usd'].median():,.0f}" if not df.empty else "-")
        ], body=True, style=CARD), width=3),
        dbc.Col(dbc.Card([
            html.H6("Maior Salário (USD)", className="text-muted"),
            html.H3(f"${df['salary_in_usd'].max():,.0f}" if not df.empty else "-")
        ], body=True, style=CARD), width=3),
    ], className="mb-4 mt-3"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Label("Filtrar por Nível de Experiência:"),
                dcc.Dropdown(
                    id="exp-filter",
                    options=[{"label": i, "value": i} for i in df["experience_level"].unique()],
                    value=df["experience_level"].unique().tolist(),
                    multi=True,
                ),
                dcc.Graph(id="graph-jobs", className="mt-3"),
            ], body=True, style=CARD)
        ], width=8),
        dbc.Col([
            dbc.Card([
                html.H5("Insights do Mercado"),
                html.Div(id="text-insights", style={"font-size": "14px", "text-align": "justify"})
            ], body=True, style=CARD)
        ], width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([dcc.Graph(id="graph-exp")], body=True, style=CARD), width=6),
        dbc.Col(dbc.Card([dcc.Graph(id="graph-evolution")], body=True, style=CARD), width=6),
    ]),
])

# ----- LAYOUT PRINCIPAL -----
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard Profissional | Felipe Murad",
                        className="text-center my-4 text-primary"), width=12)
    ]),
    dcc.Tabs([
        dcc.Tab(label="Quem sou eu", children=[tab_quem_sou]),
        dcc.Tab(label="Minhas qualificações", children=[tab_qualificacoes]),
        dcc.Tab(label="Skills", children=[tab_skills]),
        dcc.Tab(label="Análise de Mercado (InfoSec)", children=[tab_analise]),
    ]),
], fluid=True)

# ============================================================
# 3. CALLBACKS (INTERATIVIDADE)
# ============================================================

@app.callback(
    [Output("graph-jobs", "figure"),
     Output("graph-exp", "figure"),
     Output("graph-evolution", "figure"),
     Output("text-insights", "children")],
    [Input("exp-filter", "value")]
)
def update_graphs(selected_exp):
    """Atualiza os gráficos e insights conforme o filtro selecionado."""
    if not selected_exp:
        selected_exp = df["experience_level"].unique().tolist()
    filtrado = df[df["experience_level"].isin(selected_exp)]

    # 1) Top 10 cargos por salário médio
    top_jobs = (filtrado.groupby("job_title")["salary_in_usd"]
                .mean().sort_values(ascending=False).head(10).reset_index())
    fig_jobs = px.bar(top_jobs, x="salary_in_usd", y="job_title", orientation="h",
                      title="Top 10 Cargos por Média Salarial (USD)",
                      labels={"salary_in_usd": "Salário Médio", "job_title": "Cargo"},
                      color="salary_in_usd", color_continuous_scale="Viridis")
    fig_jobs.update_layout(yaxis={"categoryorder": "total ascending"}, title_x=0.5)

    # 2) Boxplot: distribuição salarial por nível
    fig_exp = px.box(filtrado, x="experience_level", y="salary_in_usd",
                     title="Distribuição Salarial por Nível de Experiência",
                     color="experience_level", points="all")
    fig_exp.update_layout(title_x=0.5, showlegend=False)

    # 3) Evolução temporal do salário médio
    evolucao = filtrado.groupby("work_year")["salary_in_usd"].mean().reset_index()
    fig_evo = px.line(evolucao, x="work_year", y="salary_in_usd", markers=True,
                      title="Evolução do Salário Médio (USD) por Ano",
                      labels={"work_year": "Ano", "salary_in_usd": "Média USD"})
    fig_evo.update_layout(title_x=0.5)

        # 4) Insights dinâmicos (sem tags HTML literais)
    insights = [
        html.P([
            "• Cargo com maior remuneração média no filtro atual: ",
            html.Span(top_jobs.iloc[0]["job_title"], style={"fontWeight": "bold"}),
            ".",
        ]),
        html.P([
            "• Média salarial geral: ",
            html.Span(f"${filtrado['salary_in_usd'].mean():,.2f}", style={"fontWeight": "bold"}),
            " e mediana de ",
            html.Span(f"${filtrado['salary_in_usd'].median():,.2f}", style={"fontWeight": "bold"}),
            ".",
        ]),
        html.P("• A diferença entre níveis Junior e Senior tende a dobrar a remuneração, "
               "reforçando o valor de certificações e experiência prática."),
        html.P("• A tendência de crescimento dos salários de InfoSec reflete a alta demanda "
               "por profissionais de segurança da informação no mercado global."),
    ]

    return fig_jobs, fig_exp, fig_evo, insights


server = app.server

if __name__ == "__main__":
    app.run(debug=True)