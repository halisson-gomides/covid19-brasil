########################################
# @author: HALISSON SOUZA GOMIDES
# halisson.gomides@gmail.com
# ver: 1.0  21/05/2021
########################################

import asyncio
from data_functions import fetch_dataframes
import logging
from plotly.graph_objs import Figure
from graph_functions import (
graph_active_cases_cum, graph_deaths_cum,
graph_confirmed_cases_by_month, graph_deaths_by_month,
graph_vaccines_doses_cum, graph_vaccination_by_day,
kpi_total_doses, kpi_total_1dose,
kpi_total_2dose
)
import plotly.io as pio
pio.kaleido.scope.default_format = "svg"
pio.kaleido.scope.default_width = 300
pio.kaleido.scope.default_height = 200
pio.kaleido.scope.default_scale = 1



# Setando variáveis
url_br = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
url_cities = "https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time.csv.gz?raw=true"
url_popmunic = 'datasets/originais/populacao_2020.xls'
url_gpscities = "https://raw.githubusercontent.com/wcota/covid19br/master/gps_cities.csv"
url_geojson_br = 'geojson/brasil-uf-compressed.json'
chunk_size = 50000
graphs_path = 'graficos/leg-int'
ind_path = 'graficos/indicadores'

if __name__ == "__main__":
    # seta o arquivo que armazenará os logs e as configurações básicas de log
    logging.basicConfig(filename='gera_graficos_covid.log',
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S')

    # Instancia o objeto de Log
    logger = logging.getLogger()

    # Fazendo a carga dos dados atualizados e tratamento dos mesmos
    logger.info('Iniciando carga de dados...')
    df_br, df_cities, df_popuf, df_uf = asyncio.run(fetch_dataframes(url_br, url_cities, url_popmunic, url_gpscities, url_geojson_br, chunk_size, logger))

    # gerando os gráficos atualizados
    fig_casos_ativos_cum = Figure(graph_active_cases_cum(df_br))
    fig_casos_ativos_cum.write_html(graphs_path+'/casos-ativos_x_consorcio.html')