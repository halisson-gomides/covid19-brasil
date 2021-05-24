########################################
# @author: HALISSON SOUZA GOMIDES
# halisson.gomides@gmail.com
# ver: 1.0  21/05/2021
########################################

import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import json
import time


# --------------------------------------------------------------------------------------------
# Função de carga de dados
# --------------------------------------------------------------------------------------------
def load_data(data_url: str, tipo: str = 'csv', date_f: list = [], **kwargs) -> 'DataFrame':
    '''
    Função para carregar um conjunto de dados
    :rtype: pd.Dataframe
    :param data_url: caminho completo do arquivo a ser carregado
    :param tipo: tipo de arquivo: csv|xls|xlsx|json etc
    :param date_f: lista com os nomes dos campos a ser convertidos para datetime
    :param kwargs: argumentos especificos para a carga do arquivo, conforme o parametro 'tipo'
    :return: Pandas DataFrame
    '''

    if tipo == 'csv':

        if 'chunksize' in kwargs:

            kwargs['iterator'] = True
            data = pd.DataFrame()
            _df_chunked = pd.read_csv(data_url, **kwargs)
            for _df in _df_chunked:
                data = data.append(_df)
        else:
            data = pd.read_csv(data_url, **kwargs)

    elif tipo == 'xls' or tipo == 'xlsx':

        data = pd.read_excel(data_url, **kwargs)

    elif tipo == 'json':

        import json

        with open(data_url) as f:
            data = json.load(f)

        return data

    else:
        if 'chunksize' in kwargs:

            kwargs['iterator'] = True
            data = pd.DataFrame()
            _df_chunked = pd.read_table(data_url, **kwargs)
            for _df in _df_chunked:
                data = data.append(_df)
        else:
            data = pd.read_table(data_url, **kwargs)

    for dt_field in date_f:
        data[dt_field] = pd.to_datetime(data[dt_field])

    return data


# --------------------------------------------------------------------------------------------
# Funções de Transformação dos dados
# --------------------------------------------------------------------------------------------
async def transform_dfbr(df, cols: list = []) -> 'DataFrame':
    '''
    Função para transformar o DataFrame df_br, filtra os dados para o Brasil, seleciona colunas especificadas
    e adiciona novas colunas
    :param df: dataframe com dados sobre a covid do Brasil
    :param cols: lista com os nomes das colunas que deverão conter no DataFrame de retorno. Não sendo informado,
    retorna todas as colunas do DataFrame.
    :return: Pandas DataFrame
    '''

    colunas = cols if len(cols) > 0 else df.columns.to_list()

    # Filtra os dados para o Brasil e seleciona colunas específicas
    _df_BR = df.query("state == 'TOTAL'")[colunas]

    # cria novas colunas
    _df_BR['activeCases'] = _df_BR['totalCases'] - _df_BR['deaths'] - _df_BR['recovered']
    _df_BR['activeCasesMS'] = _df_BR['totalCasesMS'] - _df_BR['deathsMS'] - _df_BR['recovered']
    _df_BR['activeCasesDiff'] = _df_BR['activeCases'] - _df_BR['activeCasesMS']
    _df_BR['deathsDiff'] = _df_BR['deaths'] - _df_BR['deathsMS']
    _df_BR['newVaccinated'] = _df_BR['vaccinated'].diff()
    _df_BR['newVaccinated_second'] = _df_BR['vaccinated_second'].diff()

    return _df_BR


async def transform_popuf(df_munic) -> 'DataFrame':
    '''
    Função para transformar o DataFrame df_popmunic, trata o dado de POPULAÇÃO ESTIMADA e retonar outro dataframe
    agregado por UF
    :param df_munic: dataframe com dados populacionais dos municípios
    :return: Pandas DataFrame
    '''

    df_munic['POPULAÇÃO ESTIMADA'] = df_munic['POPULAÇÃO ESTIMADA'].apply(lambda x: str(x).split('(')[0])
    df_munic['POPULAÇÃO ESTIMADA'] = df_munic['POPULAÇÃO ESTIMADA'].astype(int)
    _popuf = df_munic[['UF', 'POPULAÇÃO ESTIMADA']].groupby('UF').sum().reset_index()

    return _popuf


async def transform_dfcities(df_cities, df_gps_cities) -> 'DataFrame':
    '''
    Função para transformar o DataFrame df_cities, acrescentando informações de latitude e longitude a partir do df_gps_cities
    :param df_cities: dataframe com dados de covid por município
    :param df_gps_cities: dataframe com dados de coordenadas geográficas dos municípios
    :return: Pandas DataFrame
    '''

    # filtra pela data mais recente
    _df = df_cities.query('date == @df_cities.date.max()').copy()

    # removendo as linhas cujo campo ibgeID está faltando
    _df_gps = df_gps_cities.dropna(subset=['ibgeID']).copy()

    # convertendo o tipo da coluna ibeID do df_gps_cities para o mesmo tipo da coluna ibgeID do df_cities
    _df_gps.loc[:, 'ibgeID'] = _df_gps['ibgeID'].astype(int)

    # definindo as colunas 'lat' e 'lon' no df_cities com base no 'ibgeID' do df_gps_cities
    _df['lat'] = _df.loc[:, 'ibgeID'].map(_df_gps.set_index('ibgeID').loc[:, 'lat'])
    _df['lon'] = _df.loc[:, 'ibgeID'].map(_df_gps.set_index('ibgeID').loc[:, 'lon'])

    return _df


async def transform_dfuf(df, df_popuf) -> 'DataFrame':
    '''
    Função para transformar o DataFrame df_br, filtra os dados por UF e adiciona nova coluna de percentual
    da população vacinada de cada UF com base na informação de população do df_popuf
    :param df: dataframe com dados sobre a covid do Brasil
    :param df_popuf: dataframe com dados sobre a população estimada por UF
    :return: Pandas DataFrame
    '''

    # Filtra os dados para as UFs e para a data mais recente
    _df_UF = df.query("state != 'TOTAL' and date == @df['date'].max()").copy()

    # cria nova coluna de percentual de vacinados
    _df_UF['perc_vac'] = (_df_UF.loc[:, 'vaccinated'] / _df_UF.loc[:, 'state'].map(
        df_popuf.set_index('UF').loc[:, 'POPULAÇÃO ESTIMADA'])) * 100

    return _df_UF


# --------------------------------------------------------------------------------------------
# Função para retornar os dataframes carregados e transformados
# --------------------------------------------------------------------------------------------
async def fetch_dataframes(url_br, url_cities, url_popmunic, url_gpscities, url_geojson_br, chunk_size, logger):
    '''

    :param url_br: caminho do conjunto de dados sobre a covid referente ao Brasil e aos estados brasileiros
    :param url_cities: caminho do conjunto de dados sobre a covid nos municípios brasileiros
    :param url_popmunic: caminho do conjunto de dados sobre a população estimada dos municípios brasileiros
    :param url_gpscities: caminho do conjunto de dados contendo informações geográficas de latitude e longitude dos municípios brasileiros
    :param url_geojson_br: caminho do arquivo geojson do mapa geográfico brasileiro, dividido por UF
    :param chunk_size: quantidade de linhas por parte, usado para particionar o carregamento de DataFrames muito grandes
    :param logger: biblioteca para registrar os passos dos processamentos dos DatFrames
    :return: df_br,     -> DataFrame com dados de covid no Brasil transformado
            df_cities,  -> DataFrame com dados de covid nos municípios brasileiros transformado
            df_popuf,   -> DataFrame com dados populacionais por UF
            df_uf       -> DataFrame com dados de covid agregados por UF e com percentual de vacinados por UF
    '''

    # Dicionário cuja chave é o nome do Dataframe a ser carregado e o valor são os parâmetros a serem
    # passados para a função que irá carregar o DataFrame - load_data
    D_ARGS = {
        'df_br': dict(data_url=url_br, date_f=['date']),
        'df_cities': dict(data_url=url_cities, date_f=['date'], compression='gzip', chunksize=chunk_size),
        'df_popmunic': dict(data_url=url_popmunic, tipo='xls', sheet_name='Municípios', skiprows=1, skipfooter=16),
        'df_gpscities': dict(data_url=url_gpscities),
        'gj_br': dict(data_url=url_geojson_br, tipo='json'),
    }

    # Inicializa o Dicionário que irá conter os DataFrames carregados
    datasets = {}

    logger.info('Iniciando carga de dados...')

    # Marca o tempo de início da execução da carga
    start = time.perf_counter()

    # Execução paralela da carga de dados
    with ThreadPoolExecutor() as executor:

        # Inicia as tarefas de carga e atribui a cada tarefa o nome da chave correspondente a cada conjunto de dados
        future_data_loader = {executor.submit(load_data, **valor): chave for chave, valor in D_ARGS.items()}

        for task in as_completed(future_data_loader):

            try:
                datasets[future_data_loader[task]] = task.result()
            except Exception as exc:

                logger.error(f'{future_data_loader[task]} generated an exception: {exc}')
            else:
                print(f'dataset {future_data_loader[task]} carregado - {len(datasets[future_data_loader[task]])} linhas')
                logger.info(f'dataset {future_data_loader[task]} carregado - {len(datasets[future_data_loader[task]])} linhas')

    logger.info(f'Carga de dados finalizada. Tempo de execução: {time.perf_counter() - start} ')

    logger.info('Iniciando tratamento dos dados...')

    # Marca o tempo de início da transformação dos dados
    start = time.perf_counter()

    df_br, df_cities, df_popuf = await asyncio.gather(
        transform_dfbr(datasets['df_br'],
                       cols=['date', 'state', 'newDeaths', 'deaths', 'deathsMS', 'newCases', 'totalCases',
                             'totalCasesMS', 'recovered', 'tests', 'vaccinated', 'vaccinated_second']),
        transform_dfcities(datasets['df_cities'], datasets['df_gpscities']),
        transform_popuf(datasets['df_popmunic']),
    )
    df_uf = await transform_dfuf(datasets['df_br'], df_popuf)

    logger.info(f'Tratamento os dados finalizada. Tempo de execução: {time.perf_counter() - start} ')

    return df_br, df_cities, df_popuf, df_uf, datasets['gj_br']
