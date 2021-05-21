########################################
# @author: HALISSON SOUZA GOMIDES
# halisson.gomides@gmail.com
# ver: 1.0  21/05/2021
########################################

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def graph_active_cases_cum(data_BR):
    """
    Gera gráfico da evolução de casos ativos de covid-19 no Brasil - Acumulado
    :param data_BR: Pandas DataFrame com os dados de casos de covid-19 no Brasil acumulados
    :return: Plotly Fig object
    """

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=data_BR['date'],
            y=data_BR['activeCases'],
            line=dict(width=3),
            name='Casos Ativos',
            text=data_BR['date'],
            hoverinfo='text',
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data_BR['date'],
            y=data_BR['activeCasesMS'],
            line=dict(width=3),
            name='Casos Ativos - MS',
            text=data_BR['date'],
            hoverinfo='text',
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(
            x=data_BR['date'],
            y=data_BR['activeCasesDiff'],
            name='diferença',
            text=data_BR['date'],
            hoverinfo='text',
        ),
        secondary_y=True,
    )

    # customizações de layout
    fig.update_layout(
        title=dict(
            text='<b>Casos Ativos - MS x SES</b>',
            xref='paper',
            pad=dict(l=150),
        ),
        xaxis_tickformat='%d/%m/%Y',
        hovermode='x unified',
        separators=',.',
        plot_bgcolor='#fafafa',
        legend=dict(
            x=0.01,
            y=0.9,
            traceorder='normal',
            font=dict(size=10)
        ),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    fig.update_traces(hovertemplate='%{y:,.0f}')

    # Anotações
    fig.add_annotation(x=data_BR.loc[data_BR['activeCasesDiff'].idxmax(), 'date'], y=data_BR['activeCasesDiff'].max(),
                       yref='y2',
                       text="> " + str(round(data_BR['activeCasesDiff'].max(), -3)),
                       font=dict(size=10),
                       showarrow=True,
                       arrowhead=1)

    # Set x-axis title
    # fig.update_xaxes(title_text="Data")

    # Set y-axes titles
    fig.update_yaxes(title_text="Casos Confirmados", secondary_y=False)
    fig.update_yaxes(title_text="Diferença", secondary_y=True)

    return fig


def graph_confirmed_cases_by_month(p_mes):
    """
    Gera gráfico de casos de covid-19 confirmados por mês no Brasil, desde o início dos registros
    :param p_mes: Pandas DataFrame df_br agrupado por mês
    :return: Plotly Fig object
    """

    fig = go.Figure(
        data=[
            go.Bar(
                x=p_mes.index,
                y=p_mes['newCases'],
                name='Casos',
            ),
        ]
    )

    fig.update_layout(
        title=dict(
            text='<b>Casos Confirmados por mês - COVID-19</b>',
            xref='paper',
            pad=dict(l=150),
        ),
        legend=dict(
            x=0.01,
            y=0.9,
            traceorder='normal',
            font=dict(size=10),
        ),
        hovermode='x unified',
        separators=',.',
        plot_bgcolor='#fafafa',
        xaxis_tickformat='%m/%Y',
        margin=dict(l=0, r=0, t=30, b=0),
    )
    fig.update_xaxes(nticks=p_mes.shape[0])

    fig.update_traces(
        hovertemplate='%{y:,.0f}',
        marker_color='goldenrod',
    )

    return fig


def graph_deaths_cum(data_BR):
    """
    Gera gráfico da evolução de óbitos por covid-19 no Brasil - Acumulado
    :param data_BR: Pandas DataFrame com os dados de óbitos por covid-19 acumulados
    :return: Plotly Fig object
    """

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=data_BR['date'],
            y=data_BR['deaths'],
            line=dict(width=3, color='orange'),
            name='Óbitos',
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=data_BR['date'],
            y=data_BR['deathsMS'],
            line=dict(width=3, color='blue'),
            name='Óbitos - MS',
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(
            x=data_BR['date'],
            y=data_BR['deathsDiff'],
            name='diferença',
        ),
        secondary_y=True,
    )

    # customização do layout
    fig.update_layout(
        title=dict(
            text='<b>Óbitos - Acumulado - MS x SES</b>',
            xref='paper',
            pad=dict(l=150),
        ),
        xaxis_tickformat='%d/%m/%Y',
        hovermode='x unified',
        separators=',.',
        plot_bgcolor='#fafafa',
        legend=dict(
            x=0.01,
            y=0.9,
            traceorder='normal',
            font=dict(size=10)
        ),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    fig.update_traces(hovertemplate='%{y:,.0f}')

    # Anotações
    fig.add_annotation(x=data_BR.loc[data_BR['deathsDiff'].idxmax(), 'date'], y=data_BR['deathsDiff'].max(),
                       yref='y2',
                       text="> " + str(round(data_BR['deathsDiff'].max(), -2)),
                       font=dict(size=10),
                       showarrow=True,
                       arrowhead=1)

    # Set x-axis title
    # fig.update_xaxes(title_text="Data")

    # Set y-axes titles
    fig.update_yaxes(title_text="Óbitos Confirmados", secondary_y=False)
    fig.update_yaxes(title_text="Diferença", secondary_y=True)

    return fig


def graph_deaths_by_month(p_mes):
    """
    Gera gráfico de óbitos por covid-19 no Brasil, por mês, desde o início dos registros
    :param p_mes: Pandas DataFrame df_br agrupado por mês
    :return: Plotly Fig object
    """

    fig = go.Figure(
        data=[
            go.Bar(
                x=p_mes.index,
                y=p_mes['newDeaths'],
                name='Óbitos',
            ),
        ]
    )

    fig.update_layout(
        title=dict(
            text='<b>Óbitos registrados por mês - COVID-19</b>',
            xref='paper',
            pad=dict(l=150),
        ),
        legend=dict(
            x=0.01,
            y=0.9,
            traceorder='normal',
            font=dict(size=10),
        ),
        hovermode='x unified',
        separators=',.',
        plot_bgcolor='#fafafa',
        xaxis_tickformat='%m/%Y',
        margin=dict(l=0, r=0, t=30, b=0),
    )
    fig.update_xaxes(nticks=p_mes.shape[0])

    fig.update_traces(
        hovertemplate='%{y:,.0f}',
        marker_color='firebrick',
    )

    return fig


def graph_vaccines_doses_cum(df_vac, df_50M, dias_50M):
    """
    Gera gráfico da evolução da vacinação contra a covid-19 no Brasil desde o início dos registros - Acumulado
    :param df_vac: recorte do DataFrame data_BR contendo apenas os registros a partir do início da vacinação, e que contém dados de doses de vacina aplicadas - acumulados
    :param df_50M: recorte do DataFrame data_BR contendo apenas o registro da data em que o Brasil alcançou a marca de 50 milhões de doses aplicadas
    :param dias_50M: número de dias de vacinação que o Brasil levou para alcançar a marca de 50 milhões de doses aplicadas
    :return: Plotly Fig object
    """

    fig = go.Figure(go.Scatter(
        x=df_vac['date'],
        y=df_vac['vaccinated'],
        line=dict(color='MediumPurple', width=3),
        fill='tonexty',
        name='primeira dose'

    ))

    fig.add_trace(go.Scatter(
        x=df_vac['date'],
        y=df_vac['vaccinated_second'],
        line=dict(color='Coral', width=3),
        fill='tozeroy',
        name='segunda dose'
    ))

    fig.update_layout(
        title=dict(
            text='<b>Evolução da vacinação - COVID-19</b>',
            xref='paper',
            pad=dict(l=150),
        ),
        xaxis_tickformat='%d/%m/%Y',
        legend=dict(
            x=0.01,
            y=0.9,
            traceorder='normal',
            font=dict(size=10)
        ),
        hovermode='x unified',
        separators=',.',
        plot_bgcolor='#fafafa',
        margin=dict(l=0, r=0, t=30, b=0),
    )

    fig.update_traces(hovertemplate='%{y:,.0f}')

    fig.add_vline(
        x=df_50M['date'],
        line_width=3,
        line_dash="dash",
        line_color="green",
    )

    # Anotações
    fig.add_annotation(
        x=df_50M['date'],
        y=df_50M['vaccinated'] + 100000,
        text=f"50M em {dias_50M} dias",
        font=dict(size=10, color='white'),
        showarrow=False,
        xref="x",
        yref="y",
        yshift=-100,
        xshift=-50,
        align="left",
        borderpad=4,
        bgcolor="ForestGreen",
    )

    return fig


def graph_vaccination_by_day(df_vac):
    """
    Gera gráfico de doses de vacinas contra a covid-19 aplicadas por dia no Brasil desde o início dos registros,
    além das médias móveis de 07 dias para a primeira e segunda doses
    :param df_vac: recorte do DataFrame data_BR contendo apenas os registros a partir do início da vacinação, e que contém dados de doses de vacina aplicadas
    :return: Plotly Fig object
    """

    df_vac['1_dose_7d'] = df_vac['newVaccinated'].rolling(7).mean()
    df_vac['2_dose_7d'] = df_vac['newVaccinated_second'].rolling(7).mean()

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_vac['date'],
                y=df_vac['newVaccinated'],
                name='primeira dose',
                opacity=0.5
            ),
            go.Bar(
                x=df_vac['date'],
                y=df_vac['newVaccinated_second'],
                name='segunda dose',
            ),
            go.Scatter(
                x=df_vac['date'],
                y=df_vac['1_dose_7d'],
                line=dict(color='MediumPurple', width=5),
                name='média móvel 1ª dose'
            ),
            go.Scatter(
                x=df_vac['date'],
                y=df_vac['2_dose_7d'],
                line=dict(color='Coral', width=5),
                name='média móvel 2ª dose'
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text='<b>Vacinação por dia - COVID-19</b>',
            xref='paper',
            pad=dict(l=150),
        ),
        xaxis_tickformat='%d/%m/%Y',
        barmode='stack',
        legend=dict(
            x=0.01,
            y=0.9,
            traceorder='normal',
            font=dict(size=10)
        ),
        margin=dict(l=0, r=0, t=30, b=0),
    )
    fig.update_traces(
        hovertemplate='%{y:,.0f}',
        marker_color='DarkGray',
    )
    fig.update_layout(hovermode='x unified', separators=',.', plot_bgcolor='#fafafa')

    return fig


def kpi_total_doses(data_BR):
    """
    Gera o indicador do número total de doses de vacinas contra covid-19 aplicadas até o momento no Brasil
    :param data_BR: Pandas DataFrame com os dados de doses de vacinas contra covid-19 aplicadas no Brasil - acumulado
    :return: Plotly Fig object
    """

    fig = go.Figure()

    total_vacinados = data_BR['vaccinated'].iloc[-1] + data_BR['vaccinated_second'].iloc[-1]

    fig.add_trace(go.Indicator(
        mode="number",
        value=total_vacinados,
        number={'valueformat': ',.4s', },
        title={'text': 'Doses aplicadas'},
        domain={'x': [0.15, 0], 'y': [0.001, 0]}
    )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig


def kpi_total_1dose(data_BR):
    """
    Gera o indicador do número total da primeira dose da vacina contra covid-19 aplicada até o momento no Brasil
    :param data_BR: Pandas DataFrame com os dados de doses de vacinas contra covid-19 aplicadas no Brasil - acumulado
    :return: Plotly Fig object
    """

    fig = go.Figure()

    total_vacinados = data_BR['vaccinated'].iloc[-1]
    crescimento = data_BR['vaccinated'].iloc[-2]

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=total_vacinados,
        number={'valueformat': ',.4s', },
        delta={'reference': crescimento, 'relative': False, 'valueformat': ',.5s'},
        title={'text': '1ª Dose'},
        domain={'x': [0.15, 0], 'y': [0.001, 0]}
    )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig


def kpi_total_2dose(data_BR):
    """
    Gera o indicador do número total da segunda dose da vacina contra covid-19 aplicada até o momento no Brasil
    :param data_BR: Pandas DataFrame com os dados de doses de vacinas contra covid-19 aplicadas no Brasil - acumulado
    :return: Plotly Fig object
    """

    fig = go.Figure()

    total_vacinados = data_BR['vaccinated_second'].iloc[-1]
    crescimento = data_BR['vaccinated_second'].iloc[-2]

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=total_vacinados,
        number={'valueformat': ',.4s', },
        delta={'reference': crescimento, 'relative': False, 'valueformat': ',.5s'},
        title={'text': '2ª Dose'},
        domain={'x': [0.15, 0], 'y': [0.001, 0]}
    )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig
