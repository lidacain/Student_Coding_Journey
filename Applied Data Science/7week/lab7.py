import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load the data with the correct separator
df = pd.read_csv('HH_data_DA.csv', sep=';')

# Create Dash app
app = dash.Dash(__name__)

# # Graph 1: Salary comparison between Power BI and Tableau
# fig1 = px.box(df[df['direction'].isin(['Power BI', 'Tableau'])],
#               x='direction',
#               y='salary_net',
#               points="all",
#               title='Salary comparison between Power BI and Tableau')

# График 2: Распределение вакансий по дням недели
df['published_at'] = pd.to_datetime(df['published_at'])
df['day_of_week'] = df['published_at'].dt.day_name()
fig2 = px.bar(df['day_of_week'].value_counts(),
              x=df['day_of_week'].value_counts().index,
              y=df['day_of_week'].value_counts().values,
              title='Распределение вакансий по дням недели')

# График 3: Сравнение количества вакансий летом и осенью
df['season'] = df['published_at'].dt.month.map({1: 'Зима', 2: 'Зима', 3: 'Весна', 4: 'Весна',
                                                5: 'Весна', 6: 'Лето', 7: 'Лето', 8: 'Лето',
                                                9: 'Осень', 10: 'Осень', 11: 'Осень', 12: 'Зима'})
fig3 = px.bar(df['season'].value_counts(),
              x=df['season'].value_counts().index,
              y=df['season'].value_counts().values,
              title='Сравнение количества вакансий летом и осенью')

# График 4: Топ растущих поисковых запросов
top_queries = df['query_string'].value_counts().nlargest(10)
fig4 = px.bar(top_queries,
              x=top_queries.index,
              y=top_queries.values,
              title='Топ растущих поисковых запросов')


# # Graph 5: Vacancies with the highest salary range
# fig5 = px.box(df.nlargest(10, 'salary_to'),
#               x='name',
#               y='salary_to',
#               points="all",
#               title='Vacancies with the Highest Salary Range')

# Layout for Dash app
app.layout = html.Div([
    html.H1("Графики"),

    # # Graph 1
    # dcc.Graph(id='graph1', figure=fig1),

    # Graph 2
    dcc.Graph(id='graph2', figure=fig2),

    # Graph 3
    dcc.Graph(id='graph3', figure=fig3),

    # Graph 4
    dcc.Graph(id='graph4', figure=fig4),

    # # Graph 5
    # dcc.Graph(id='graph5', figure=fig5)
])
if __name__ == '__main__':
    app.run_server(debug=True)
