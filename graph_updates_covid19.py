########################################
# @author: HALISSON SOUZA GOMIDES
# halisson.gomides@gmail.com
# ver: 1.0  21/05/2021
########################################

import asyncio
import os
import json
from datetime import datetime
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
url_geojson_br = 'geojson/brasil-uf-compressed-utf8.json'
chunk_size = 50000
maps_path = 'graficos'
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
    df_br, df_cities, df_popuf, df_uf, gj_uf_br = asyncio.run(fetch_dataframes(url_br, url_cities, url_popmunic, url_gpscities, url_geojson_br, chunk_size, logging))

    #---------------------------------------------------------------------------------------------
    # gerando os gráficos atualizados
    # ---------------------------------------------------------------------------------------------

    # KPI's
    logging.info('Gerando os KPIs...')
    kpi_doses_aplicadas = gf.kpi_total_doses(df_br)
    kpi_doses_aplicadas.write_image(os.path.join(ind_path, 'ind-qtd-vacinas.svg'))

    kpi_1a_dose = gf.kpi_total_1dose(df_br)
    kpi_1a_dose.write_image(os.path.join(ind_path, 'ind-qtd-1dose.svg'))

    kpi_2a_dose = gf.kpi_total_2dose(df_br)
    kpi_2a_dose.write_image(os.path.join(ind_path, 'ind-qtd-2dose.svg'))

    kpi_dias_doinicio = gf.kpi_qtd_dias_vac(data_BR=df_br)
    kpi_dias_doinicio.write_image(os.path.join(ind_path, 'ind-tempo-vacinacao.svg'))

    # VACINAS
    logging.info('Gerando o gráfico de evolução da vacinação')
    dv = df_br[~df_br['vaccinated'].isna()]     # recorte contendo apenas os registros a partir do início da vacinação
    dt_inicio_vac = dv['date'].min()            # data de inicio da vacinação no Brasil
    df_50M = df_br.loc[(df_br['vaccinated'] + df_br['vaccinated_second']) > 49999999].iloc[0] # dados do primeiro dia em que o Brasil alcançou a marca de 50M de doses aplicadas
    dias_50M = df_50M['date'] - dt_inicio_vac
    dias_50M = int(str(dias_50M).split()[0]) # número de dias até alcançar a marca de 50M de doses aplicadas no Brasil
    fig_evol_vac = gf.graph_vaccines_doses_cum(df_vac=dv, df_50M=df_50M, dias_50M=dias_50M)
    fig_evol_vac.write_html(os.path.join(graphs_path, 'evolucao-vacinacao.html'))

    logging.info('Gerando o gráfico de vacinação por dia')
    fig_vac_pdia = gf.graph_vaccination_by_day(df_vac=dv)
    fig_vac_pdia.write_html(os.path.join(graphs_path, 'vacinacao-por-dia.html'))

    # MAPAS
    logging.info('Gerando gráficos de mapa')
    map_perc_vacinados = gf.mapbox_cloropleth_percvac(data_UF=df_uf, geo_UF=gj_uf_br)
    map_perc_vacinados.write_html(os.path.join(maps_path, 'mapa_vacinacao.html'))

    map_casos_p100k = gf.mapbox_cases_p100k(df_cities=df_cities)
    map_casos_p100k.write_html(os.path.join(maps_path, 'mapa-casos-p-100k-h.html'))

    # CASOS
    logging.info('Gerando gráfico de casos ativos e confirmados...')
    fig_casos_ativos_cum = gf.graph_active_cases_cum(df_br)
    fig_casos_ativos_cum.write_html(os.path.join(graphs_path, 'casos-ativos_x_consorcio.html'))

    per = df_br['date'].dt.to_period('M')
    agg_mes = df_br.groupby(per).agg({
        'newDeaths': 'sum',
        'newCases': 'sum'}).to_timestamp()
    fig_casos_confirmados  = gf.graph_confirmed_cases_by_month(p_mes=agg_mes)
    fig_casos_confirmados.write_html(os.path.join(graphs_path, 'casos-p-mes.html'))

    # OBITOS
    logging.info('Gerando gráfico de óbitos acumulados e por mês...')
    fig_obitos_acumulados = gf.graph_deaths_cum(data_BR=df_br)
    fig_obitos_acumulados.write_html(os.path.join(graphs_path, 'obitos_x_consorcio.html'))

    fig_obitos_pmes = gf.graph_deaths_by_month(p_mes=agg_mes)
    fig_obitos_pmes.write_html(os.path.join(graphs_path, 'obitos-p-mes.html'))

    logging.info('FIM')
    record = {'app': 'painel-covid', 'dt_atualizacao': '{:%d/%m/%Y %H:%M}'.format(datetime.now())}
    with open('dt-atualizacao-painel-covid.json', 'w') as atualizacao:
        json.dump(record, atualizacao)

    print('OK!')

