# Análise do Mercado Cripto 2020
<p>
  <a href="https://www.linkedin.com/in/luanhteixeira/">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/800px-LinkedIn_logo_initials.png" alt="LinkedIn" width="30" height="30" style="vertical-align: middle;"/>
  </a>
  &nbsp;&nbsp; 
  <a href="PlaceHolder" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" alt="YouTube" width="30" height="30" style="vertical-align: middle;"/>
  </a>
</p>

### Visão Geral

Esse projeto de análise de dados tem como objetivo fornecer insights sobre o mercado de criptomoedas. Atráves da análise de diversos pontos cruciais para o mercado cripto, busquei identificar padrões e fornecer de forma clara um melhor entendimento do mercado. 

O arquivo com o relatório completo no PowerBI pode ser encontrado [aqui](https://github.com/LuanHott/Analise_MercadoCripto2020/blob/main/power_bi/Crypto_Historical_Analysis.pbix)

![Primeira página](Imagens/Página1.png)
![Segunda página](Imagens/Página2.png)

### Fonte de dados

[Coin_Raw](https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory/data): O data set primário do projeto, contendo informações detalhadas de 23 das principais moedas do mercado de 2020 como preço, data, market cap e volume.

[Calendar_Raw](https://www.kaggle.com/datasets/devorvant/economic-calendar/data?select=D2019-21.csv): O data set de apoio usado primariamente na primeira página do relatório, contendo o nome dos anúncios fiscais, países, volatilidade esperada e data.

### Ferramentas

- Python(Pandas) - Limpeza inicial dos datasets
- PowerBI - Limpeza dos dados, modelagem dos dados, criação dos cálculos lógicos e visualização interativa.

### Limpeza e preparação dos dados

Na fase inicial do projeto foram seguidas as seguintes etapas:

- Limpeza inicial dos .csv utilizando pandas para fazer a primeira seleção de colunas e valores conforme escopo do projeto.

  - Utilizando um notebook python [Calendar_cleanup](https://github.com/LuanHott/Analise_MercadoCripto2020/blob/main/notebooks/calendar_cleanup.py) , realizei a limpeza selecionando apenas o nome e a data dos anúncios fiscais realizados no ano de 2020, que possuiam alta volatilidade esperada e foram realizados nos EUA. O resultado pode ser encontrado [aqui](https://github.com/LuanHott/Analise_MercadoCripto2020/blob/main/data/Calendar_Clean/calendar_clean.csv)
  - Utilizando de uma lógica similar [Coin_cleanup](https://github.com/LuanHott/Analise_MercadoCripto2020/blob/main/notebooks/coin_cleanup.py), realizei a limpeza das tabelas selecionando apenas as colunas relevantes para o escopo, que foram Nome, Data, Volume, Marketcap e o preço.

- O restante da preparação de dados foi feita através do PowerQuery do PowerBI, essa etapa consistiu em formatar os dados, realizar um append das 23 tabelas de moeda em uma só e assegurar o tipo de dado correto para cada coluna e por fim a criação do relacionamento entre ambas as colunas de data, criando um relacionamento many to many pois ambas continham duplicatas necessárias para o processo.

### Análise exploratória de dados

A AED consistiu em explorar padrões em ambas as tabelas de dados para responder algumas perguntas chaves como:

1. Qual anúncio fiscal tem o maior impacto sobre o mercado cripto (preço, volume, marketcap)? E sobre uma moeda específica?
2. Quais as moedas que sofrem mais impacto dos anúncios fiscais em seu respectivo âmbito (preço, volume, marketcap)?
3. Qual foi o movimento do mercado em 2020, ele cresceu? O volume de dinheiro aportado e movimentado, cresceu?
4. Quais são as moedas mais voláteis? Consequentemente as melhores moedas para traders.
5. Existe uma correlação da mudança dos preços das moedas em relação a mudança da principal moeda, o bitcoin? Qual o tamanho dessa correlação?

### Análise de dados

A parte mais complicada foi pensar em uma lógica para comparar a mudança no preço das criptos referentes as datas do anúncio. A conclusão foi:

MudançaRelativa = Preço na data posterior ao anúncio - Preço na data do anúncio
MudançaReal = (MudançaRelativa / Valor atual) * 100

Que também pode ser representado pelos códigos usados nas Medidas DAX:
```
PrecoData = 
VAR CurrentDate = 'Coin_Clean'[Data]
Var CurrentNome = 'Coin_Clean'[Nome]
RETURN
CALCULATE(
    MAX('Coin_Clean'[Preco]),
    FILTER(
        'Coin_Clean',
        'Coin_Clean'[Data] = CurrentDate &&
        'Coin_Clean'[Nome] = CurrentNome
    )
)
```
```
PrecoDataPosterior = 
VAR CurrentDate = 'Coin_Clean'[Data]
VAR PostDate = CurrentDate + 1
Var CurrentNome = 'Coin_Clean'[Nome]
RETURN
CALCULATE(
    MAX('Coin_Clean'[Preco]),
    FILTER(
        'Coin_Clean',
        'Coin_Clean'[Data] = PostDate &&
        'Coin_Clean'[Nome] = CurrentNome
    )
)
```
```
% Mudança preço = 
VAR ValorAtual = 'Coin_Clean'[PrecoData]
VAR ValorPosterior = 'Coin_Clean'[PrecoDataPosterior]
VAR MudancaRelativa = ValorPosterior - ValorAtual
VAR MudancaReal = 
    IF(
        ISBLANK(ValorPosterior),
        BLANK(),
        DIVIDE(MudancaRelativa, ValorAtual)
    )
RETURN
    IF(
        ISBLANK(MudancaReal),
        0,
        ABS(MudancaReal * 100)
    )

```
Que são encontrados dentro da pasta respectiva no arquivo .pbix do repositório.

### Resultados/Descobertas

O resultado das análises podem ser resumidos em:

- O PPI é o anúncio fiscal que mais impactou no preço do mercado como um todo, mas cada moeda é impactada de uma forma única.
- O EIA Short-Term Energy Outlook foi o anúncio fiscal que mais impactou o volume do mercado como um todo, mas cada moeda é impacatada de uma forma única.
- O Sesc Kashkari Speaks foi o anúncio fiscal que mais trouxe acúmulo de capital pro mercado, porém a diferença entre os 5 que mais impactaram não é muito grande, e novamente cada moeda é impactada de forma única.
- O preço, o marketcap e o volume do mercado de 2020 tiveram uma alta constante desde o ínicio ao fim do ano, o que nos leva a acreditar que tudo estaria pronto para 2021 ser um grande ano no mercado cripto (e foi).
- A melhor moeda para trade foi a Solana, que possuiu uma volatilidade de quase 6% acima da média.
- A solana também é a moeda que mais tenta imitar os movimentos do bitcoin de forma mais precisa, possuindo uma alta correlação no preço de ambas.







