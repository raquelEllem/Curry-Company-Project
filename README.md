# 1. Problema de negócio
A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas.

Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Cury Company.

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores e etc. Apesar da entrega estar crescendo, em termos de entregas, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

Você foi contratado como um Cientista de Dados para criar soluções de dados para entrega, mas antes de treinar algoritmos, a necessidade da empresa é ter um os principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes.

A Cury Company possui um modelo de negócio chamado Marketplace, que faz o intermédio do negócio entre três clientes principais: Restaurantes, entregadores e pessoas compradoras. Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:


### Do lado da empresa:
Quantidade de pedidos por dia.

Quantidade de pedidos por semana.

Distribuição dos pedidos por tipo de tráfego.

Comparação do volume de pedidos por cidade e tipo de tráfego.

A quantidade de pedidos por entregador por semana.

A localização central de cada cidade por tipo de tráfego.


### Do lado do entregador:
A menor e maior idade dos entregadores.

A pior e a melhor condição de veículos.

A avaliação médida por entregador.

A avaliação média e o desvio padrão por tipo de tráfego.

A avaliação média e o desvio padrão por condições climáticas.

Os 10 entregadores mais rápidos por cidade.

Os 10 entregadores mais lentos por cidade.


### Do lado do restaurantes:
A quantidade de entregadores únicos.

A distância média dos resturantes e dos locais de entrega.

O tempo médio e o desvio padrão de entrega por cidade.

O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.

O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.

O tempo médio de entrega durantes os Festivais.

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.


# 2. Premissas assumidas para a análise
A análise foi realizada com dados entre 17/02/2023 e 22/02/2023.

Marketplace foi o modelo de negócio assumido.

Os 3 principais visões do negócio foram: Visão transação de pedidos, visão restaurante e visão entregadores.

# 3. Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:

  -Visão do crescimento da empresa
  
  -Visão do crescimento dos restaurantes
  
  -Visão do crescimento dos entregadores

Cada visão é representada pelo seguinte conjunto de métricas.


### Visão do crescimento da empresa
Pedidos por dia.

Porcentagem de pedidos por condições de trânsito.

Quantidade de pedidos por tipo e por cidade.

Pedidos por semana.

Quantidade de pedidos por tipo de entrega.

Quantidade de pedidos por condições de trânsito e tipo de cidade.


### Visão do crescimento dos restaurantes
Quantidade de pedidos únicos.

Distância média percorrida.

Tempo médio de entrega durante festival e dias normais.

Desvio padrão do tempo de entrega durante festivais e dias normais.

Tempo de entrega médio por cidade.

Distribuição do tempo médio de entrega por cidade.

Tempo médio de entrega por tipo de pedido.


### Visão do crescimento dos entregadores
Idade do entregador mais velho e do mais novo.

Avaliação do melhor e do pior veículo.

Avaliação média por entregador.

Avaliação média por condições de trânsito.

Avaliação média por condições climáticas.

Tempo médido do entregador mais rápido.

Tempo médio do entregador mais rápido por cidade.



# 4. Top 3 Insights de dados
  -A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais.
  
  -As cidades do tipo Semi-Urban não possuem condições baixas de trânsito.
  
  -As maiores variações no tempo de entrega, acontecem durante o clima ensoladao.


# 5. O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: https://raquel-projects-curry-company.streamlit.app


# 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.
Da visão da Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022.


# 7. Próximo passos
Reduzir o número de métricas.

Criar novos filtros.

Adicionar novas visões de negócio.
