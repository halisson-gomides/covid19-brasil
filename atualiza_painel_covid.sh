#!/bin/bash
######################################################################################################
# SCRIPT QUE ORQUESTRA A ATUALIZAÇAO DOS GRAFICOS
# E INDICADORES QUE COMPOEM O PAINEL COVID
# URL: https://sistema7hom.presidencia.gov.br/painel/login.php
# 
# Autor: Halisson Souza Gomides
# <halisson.gomides@gmail.com>
# Data: 26/05/2021
######################################################################################################


# SETA VARIAVEIS
###############################################
CAMINHO_ARQS_SCRIPT='/home/halissonsmb/painel-covid/graficos'
CAMINHO_ARQS_PAINEL='/var/www/html/sistema8dev/desenvolvedores/halissonsmb/painelcovid'
CAMINHO_SCRIPT_PYTHON='/home/halissonsmb/painel-covid'

# EXECUCAO DO SCRIPT PYTHON QUE GERA OS COMPONENTES DO PAINEL
###############################################
export PYTHON_BUILD_ARIA2_OPTS="-x 10 -k 1M"
export PATH="/home/halissonsmb/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
source /home/halissonsmb/.pyenv/versions/miniconda3-latest/etc/profile.d/conda.sh
conda activate covid
RESULTADO_EXECUCAO=`python $CAMINHO_SCRIPT_PYTHON/graph_updates_covid19.py`

if [ "$RESULTADO_EXECUCAO" != "OK!" ];
then
	echo -e '\033[41;10;1;4m Ocorreu um erro na execucao do script python \033[m'
	echo -e '\033[40;40;1;6m favor verificar o arquivo gera_graficos_covid.log para maiores detalhes \033[m'
	exit 1
fi

######################################################################################################
# COPIA OS ARQUIVOS GERADOS PELO SCRIPT PYTHON PARA O DIRETÓRIO DOS AQUIVOS QUE IRÃO PARA A APLICAÇÃO
######################################################################################################
cp $CAMINHO_ARQS_SCRIPT/mapa* $CAMINHO_ARQS_PAINEL/graficos/
cp $CAMINHO_ARQS_SCRIPT/leg-int/* $CAMINHO_ARQS_PAINEL/graficos/leg-int/
cp $CAMINHO_ARQS_SCRIPT/../dt-atualizacao-painel-covid.json $CAMINHO_ARQS_PAINEL

######################################################################################################
# ATUALIZANDO OS INDICADORES QUE VÃO PARA O PAINEL
######################################################################################################

# TEMPO DE VACINACAO
###############################################

# CAPTURA O VALOR ATUALIZADO DA NOVA IMAGEM GERADA
KPI_TEMPO_VAC="`grep -o '>\([0-9]\{3,\}\)<' $CAMINHO_ARQS_SCRIPT/indicadores/ind-tempo-vacinacao.svg | awk -F">|<" '{print $2}'`"

# SUBSTITUI O VALOR ATUALIZADO NA IMAGEM QUE VAI PRO PAINEL
sed -i 's/>\([0-9]\{3,\}\)</>'"$KPI_TEMPO_VAC"'</' $CAMINHO_ARQS_PAINEL/graficos/indicadores/ind-tempo-vacinacao.svg

# QTD TOTAL DE VACINAS
###############################################

# CAPTURA O VALOR ATUALIZADO DA NOVA IMAGEM GERADA
KPI_QTD_VAC="`grep -o '>\([0-9]\{2,\}\.[0-9]\{1,\}.\)<' $CAMINHO_ARQS_SCRIPT/indicadores/ind-qtd-vacinas.svg | awk -F">|<" '{print $2}'`"

# SUBSTITUI O VALOR ATUALIZADO NA IMAGEM QUE VAI PRO PAINEL
sed -i 's/>\([0-9]\{2,\}\.[0-9]\{1,\}.\)</>'"$KPI_QTD_VAC"'</' $CAMINHO_ARQS_PAINEL/graficos/indicadores/ind-qtd-vacinas.svg


# 1a DOSE
###############################################

# CAPTURA O VALOR ATUALIZADO DA NOVA IMAGEM GERADA - TOTAL
KPI_1DOSE=(`grep -oe '>\([0-9]\{2,\}\.[0-9]\{1,\}.\)<' -e '>▲\([0-9]\{1,\}\.[0-9]\{1,\}.\)<' $CAMINHO_ARQS_SCRIPT/indicadores/ind-qtd-1dose.svg | awk -F">|<" '{print $2}'`)

# SUBSTITUI OS VALORES ATUALIZADOS NA IMAGEM QUE VAI PRO PAINEL
sed -i 's/>\([0-9]\{2,\}\.[0-9]\{1,\}.\)</>'"${KPI_1DOSE[0]}"'</; s/>▲\([0-9]\{1,\}\.[0-9]\{1,\}.\)</>'"${KPI_1DOSE[1]}"'</' $CAMINHO_ARQS_PAINEL/graficos/indicadores/ind-qtd-1dose.svg


# 2a DOSE
###############################################

# CAPTURA O VALOR ATUALIZADO DA NOVA IMAGEM GERADA - TOTAL
KPI_2DOSE=(`grep -oe '>\([0-9]\{2,\}\.[0-9]\{1,\}.\)<' -e '>▲\([0-9]\{1,\}\.[0-9]\{1,\}.\)<' $CAMINHO_ARQS_SCRIPT/indicadores/ind-qtd-2dose.svg | awk -F">|<" '{print $2}'`)

# SUBSTITUI OS VALORES ATUALIZADOS NA IMAGEM QUE VAI PRO PAINEL
sed -i 's/>\([0-9]\{2,\}\.[0-9]\{1,\}.\)</>'"${KPI_2DOSE[0]}"'</; s/>▲\([0-9]\{1,\}\.[0-9]\{1,\}.\)</>'"${KPI_2DOSE[1]}"'</' $CAMINHO_ARQS_PAINEL/graficos/indicadores/ind-qtd-2dose.svg
