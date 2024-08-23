import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# To use this script: Run, and open the link to view the dashboard.
# Para usar esse script: Rode-o e abra o link para ver o dashboard.

# Load public dataset (COVID-19 data in this case)
# Carrega o conjunto de dados público (dados de COVID-19)
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
data = pd.read_csv(url)

# Preprocess the data
# Pré-processa os dados
data = data.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"], var_name="Date", value_name="Confirmed")

# Specify the date format explicitly to avoid warnings
# Especifica o formato da data explicitamente para evitar avisos
data["Date"] = pd.to_datetime(data["Date"], format='%m/%d/%y')

# Create a Dash app
# Cria um aplicativo Dash
app = dash.Dash(__name__)

# Layout of the dashboard
# Layout do dashboard
app.layout = html.Div([
    html.H1("COVID-19 Global Dashboard"),

    dcc.Dropdown(
        id='country-filter',
        options=[{'label': country, 'value': country} for country in data['Country/Region'].unique()],
        value='United States',
        placeholder="Select a Country"
        # USA as default value, select another country in the dropdown
        # Valor padrão como Estados Unidos, selecione outro país no dropdown
    ),

    dcc.Graph(id='confirmed-cases-chart')
])


# Callback to update the chart based on the selected country
# Função callback para atualizar o gráfico com base no país selecionado
@app.callback(
    Output('confirmed-cases-chart', 'figure'),
    [Input('country-filter', 'value')]
)
def update_chart(selected_country):
    # Filter data for the selected country
    # Filtra os dados para o país selecionado
    filtered_data = data[data['Country/Region'] == selected_country]

    # Create a line chart showing the trend of confirmed cases
    # Cria um gráfico de linha mostrando a tendência dos casos confirmados
    fig = px.line(filtered_data, x='Date', y='Confirmed', title=f'COVID-19 Confirmed Cases in {selected_country}')
    return fig


# Run the app
# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
