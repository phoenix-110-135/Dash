import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df_trends = pd.read_csv("data/Most_Popular_Programming_Languages_2004-2024.csv")
df_info = pd.read_csv("data/Programming_Language_Database.csv")

trend_langs = [
    "Python Worldwide(%)", "JavaScript Worldwide(%)", "Java Worldwide(%)", "C# Worldwide(%)",
    "PhP Worldwide(%)", "Flutter Worldwide(%)", "React Worldwide(%)",
    "Swift Worldwide(%)", "TypeScript Worldwide(%)", "Matlab Worldwide(%)"
]

logos = {
    "Python Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/python/python.png",
    "JavaScript Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/javascript/javascript.png",
    "Java Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/java/java.png",
    "C# Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/csharp/csharp.png",
    "PhP Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/php/php.png",
    "Flutter Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/flutter/flutter.png",
    "React Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/react/react.png",
    "Swift Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/swift/swift.png",
    "TypeScript Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/typescript/typescript.png",
    "Matlab Worldwide(%)": "https://raw.githubusercontent.com/github/explore/main/topics/matlab/matlab.png"
}

app = dash.Dash(__name__)
app.title = "Super Modern Programming Languages Dashboard"

APP_STYLE = {
    "fontFamily": "Arial, sans-serif",
    "backgroundColor": "#0e1621",
    "color": "#e3e3e3",
    "padding": "20px"
}

def line_chart(selected_langs):
    fig = px.line(df_trends, x="Month", y=selected_langs,
                  title="📈 Language Popularity Over Time", template="plotly_dark")
    fig.update_layout(plot_bgcolor="#0e1621", paper_bgcolor="#0e1621", font_color="#e3e3e3",
                      title_font=dict(size=22, color="#00d1ff", family="Arial"), legend_title_text="Languages",
                      hovermode="x unified")
    fig.update_traces(line=dict(width=3))
    return fig

def avg_pop_chart():
    avg = df_trends[trend_langs].mean().sort_values(ascending=False)
    fig = go.Figure([go.Bar(
        x=avg.index.str.replace(" Worldwide(%)", ""),
        y=avg.values,
        text=[f"{v:.2f}%" for v in avg.values],
        textposition="auto",
        marker=dict(color=avg.values, colorscale="Viridis")
    )])
    fig.update_layout(title="🔥 Average Popularity of Languages", template="plotly_dark",
                      plot_bgcolor="#0e1621", paper_bgcolor="#0e1621", font_color="#e3e3e3",
                      xaxis_title="Languages", yaxis_title="Popularity (%)",
                      title_font=dict(size=22, color="#00d1ff"))
    return fig

def pie_last_month(selected_langs):
    last_month = df_trends.iloc[-1]
    values = [last_month[lang] for lang in selected_langs]
    labels = [lang.replace(" Worldwide(%)", "") for lang in selected_langs]
    fig = px.pie(values=values, names=labels, title="🥧 Market Share Last Month", template="plotly_dark")
    fig.update_traces(textinfo='percent+label', pull=[0.05]*len(selected_langs))
    return fig

def treemap_users(selected_langs):
    df_filtered = df_info[df_info['title'].str.lower().isin([lang.replace(" Worldwide(%)","").lower() for lang in selected_langs])]
    if df_filtered.empty:
        return go.Figure()
    fig = px.treemap(df_filtered, path=['title'], values='numberOfUsers', color='rank',
                     color_continuous_scale='Viridis', title="🌳 Number of Users by Language", template="plotly_dark")
    return fig

def bubble_github(selected_langs):
    df_filtered = df_info[df_info['title'].str.lower().isin([lang.replace(" Worldwide(%)","").lower() for lang in selected_langs])]
    if df_filtered.empty:
        return go.Figure()
    df_filtered['exampleCount'] = df_filtered['exampleCount'].fillna(0)
    df_filtered['githubBigQuery.repos'] = df_filtered['githubBigQuery.repos'].fillna(0)
    fig = px.scatter(df_filtered, x='exampleCount', y='githubBigQuery.repos',
                     size='githubBigQuery.repos', color='title',
                     hover_name='title', size_max=60,
                     title="🔵 Examples vs GitHub Repos", template="plotly_dark")
    fig.update_layout(plot_bgcolor="#0e1621", paper_bgcolor="#0e1621", font_color="#e3e3e3")
    return fig

app.layout = html.Div(style=APP_STYLE, children=[
    html.H1("💻 Super Modern Programming Languages Dashboard", style={"textAlign": "center", "color": "#00d1ff"}),
    html.P("Select languages to visualize:", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="lang-selector",
        options=[{"label": lang.replace(" Worldwide(%)",""), "value": lang} for lang in trend_langs],
        value=["Python Worldwide(%)", "JavaScript Worldwide(%)"],
        multi=True,
        style={"backgroundColor": "#1b263b", "color": "#000", "borderRadius": "10px", "padding": "5px"}
    ),
    html.Br(),

    html.Div([
        html.Div(dcc.Graph(id="line-chart"), style={"width": "65%", "display": "inline-block", "verticalAlign": "top"}),
        html.Div(id="language-cards", style={"width": "32%", "display": "inline-block", "verticalAlign": "top", "paddingLeft": "15px"})
    ]),
    html.Br(),

    html.Div([
        html.Div(dcc.Graph(id="avg-bar-chart", figure=avg_pop_chart()), style={"width": "49%", "display": "inline-block"}),
        html.Div(dcc.Graph(id="pie-chart"), style={"width": "49%", "display": "inline-block"})
    ]),

    html.Br(),
    html.Div([
        html.Div(dcc.Graph(id="treemap-chart"), style={"width": "49%", "display": "inline-block"}),
        html.Div(dcc.Graph(id="bubble-chart"), style={"width": "49%", "display": "inline-block"})
    ])
])

@app.callback(
    Output("line-chart", "figure"),
    Output("language-cards", "children"),
    Output("pie-chart", "figure"),
    Output("treemap-chart", "figure"),
    Output("bubble-chart", "figure"),
    Input("lang-selector", "value")
)
def update_dashboard(selected_langs):
    if not selected_langs:
        selected_langs = ["Python Worldwide(%)"]

    fig_line = line_chart(selected_langs)
    fig_pie = pie_last_month(selected_langs)
    fig_treemap = treemap_users(selected_langs)
    fig_bubble = bubble_github(selected_langs)

    # Cards
    cards = []
    for lang in selected_langs:
        info = df_info[df_info['title'].str.lower() == lang.replace(" Worldwide(%)","").lower()]
        if not info.empty:
            info = info.iloc[0]
            title = info['title'] if pd.notna(info['title']) else lang
            appeared = info['appeared'] if pd.notna(info['appeared']) else "Unknown"
            type_ = info['type'] if pd.notna(info['type']) else "Unknown"
            desc = (info['description'][:80] + "...") if pd.notna(info['description']) else "No description"
            github = info['githubRepo'] if pd.notna(info['githubRepo']) else "#"
        else:
            title = lang.replace(" Worldwide(%)","")
            appeared = "Unknown"
            type_ = "Unknown"
            desc = "No description"
            github = "#"

        cards.append(
            html.Div([
                html.Img(src=logos.get(lang,""), style={"width": "60px", "height": "60px", "marginBottom": "5px"}),
                html.H4(title, style={"margin": "5px 0"}),
                html.P(f"Appeared: {appeared}", style={"margin": "2px 0"}),
                html.P(f"Type: {type_}", style={"margin": "2px 0"}),
                html.P(desc, style={"margin": "2px 0", "fontSize":"12px"}),
                html.A("GitHub", href=github, target="_blank", style={"color": "#00d1ff", "fontSize":"13px"})
            ], style={"backgroundColor": "#16213e", "padding": "10px", "borderRadius": "15px", "marginBottom": "15px", "textAlign": "center"})
        )

    return fig_line, cards, fig_pie, fig_treemap, fig_bubble

if __name__ == "__main__":
    app.run(debug=True)
