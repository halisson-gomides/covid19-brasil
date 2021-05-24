########################################
# @author: HALISSON SOUZA GOMIDES
# halisson.gomides@gmail.com
# ver: 1.0  21/05/2021
########################################

import asyncio
from data_functions import fetch_dataframes
import logging
logging.root.handlers
import graph_functions as gf
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
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level=logging.INFO)

    # Instancia o objeto de Log
    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)

    # Fazendo a carga dos dados atualizados e tratamento dos mesmos
    logging.info('Iniciando carga de dados...')
    print('Iniciando carga de dados...')
    df_br, df_cities, df_popuf, df_uf, gj_uf_br = asyncio.run(fetch_dataframes(url_br, url_cities, url_popmunic, url_gpscities, url_geojson_br, chunk_size, logging))

    #---------------------------------------------------------------------------------------------
    # gerando os gráficos atualizados
    # ---------------------------------------------------------------------------------------------

    # KPI's
    logging.info('Gerando os KPIs...')
    kpi_doses_aplicadas = gf.kpi_total_doses(df_br)
    kpi_doses_aplicadas.write_image(ind_path+'/ind-qtd-vacinas.svg')

    kpi_1a_dose = gf.kpi_total_1dose(df_br)
    kpi_1a_dose.write_image(ind_path+'/ind-qtd-1dose.svg')

    kpi_2a_dose = gf.kpi_total_2dose(df_br)
    kpi_2a_dose.write_image(ind_path + '/ind-qtd-2dose.svg')

    # Vacinas
    logging.info('Gerando o gráfico de evolução da vacinação')
    dv = df_br[~df_br['vaccinated'].isna()]     # recorte contendo apenas os registros a partir do início da vacinação
    dt_inicio_vac = dv['date'].min()            # data de inicio da vacinação no Brasil
    df_50M = df_br.loc[(df_br['vaccinated'] + df_br['vaccinated_second']) > 49999999].iloc[0] # dados do primeiro dia em que o Brasil alcançou a marca de 50M de doses aplicadas
    dias_50M = df_50M['date'] - dt_inicio_vac
    dias_50M = int(str(dias_50M).split()[0]) # número de dias que demorou para alcançar a marca de 50M de doses aplicadas no Brasil
    fig_evol_vac = gf.graph_vaccines_doses_cum(df_vac=dv, df_50M=df_50M, dias_50M=dias_50M)
    fig_evol_vac.write_html(graphs_path+'/casos-ativos_x_consorcio.html')
    
    logging.info('Gerando o gráfico de casos ativos...')
    fig_casos_ativos_cum = gf.graph_active_cases_cum(df_br)
    fig_casos_ativos_cum.write_html(graphs_path+'/evolucao-vacinacao.html')

