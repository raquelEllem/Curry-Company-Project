import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine 
import folium

import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(page_title='Visão Empresa', layout='wide')


#---------------------------------
# Funções
#---------------------------------
def clean_code(df1):
    """  Esta função tem a responsabilidade de limpar o dataframe
    
    Tipos de limpeza: 
    1. Remoção dos dados NaN
    2. Mudança do tipo da coluna de dados
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
    
    Input: Dataframe
    Output: Dataframe       
    
    """
    # Excluir as linhas com a idade dos entregadores vazia
    linhas_vazias = df['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]


    # Excluir as linhas com a trafego  vazia
    # ( Conceitos de seleção condicional )
    linhas_vazias = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]


    # Excluir as linhas com a cidade  vazia
    linhas_vazias = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]


    # Excluir as linhas com o Festival  vazia
    linhas_vazias = df['Festival'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    
    # Remove as linhas da culuna multiple_deliveries igual a 'NaN '
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :]
    
    # Limpando a coluna de time_taken (min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )


    # Conversao de texto/categoria/string para numeros inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    # Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    # Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )


    # Remover spaco da string
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip() 
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip() 
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip() 
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip() 
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip() 
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip() 

    return df1


def order_metric(df1):
    """
    Recebe o dataframe, executa, gera uma figura e retorna a figura
    
    1. Gera gráfico de BARRAS
    2. Total de pedidos por dia
    """
    #seleção de colunas
    cols = ['ID', 'Order_Date']
    #seleção de linhas
    df_aux = df1.loc[:, cols].groupby(['Order_Date']).count().reset_index()

    #desenhando gráfico barras
    fig = px.bar(df_aux, x='Order_Date', y='ID')

    return fig


def traffic_order_share(df1):
    """
    Recebe o dataframe, executa, gera uma figura e retorna a figura
    
    1. Gera gráfico Pizza
    2. Total de pedidos por densidade de tráfego
    
    """
    cols = ['ID', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['Road_traffic_density']).count().reset_index()
    #cria uma nova coluna para armazenar a porcentagem de entrega
    df_aux['Delivery_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    #desenhando gráfico pizza
    fig = px.pie(df_aux, values='Delivery_perc', names='Road_traffic_density')
    return fig



def traffic_order_city(df1):
    """
    Recebe o dataframe, executa, gera uma figura e retorna a figura
    
    1. Gera gráfico com Pontos
    2. Total de pedidos por cidade e por densidade de tráfego
    
    """
    cols = ['ID', 'City', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).count().reset_index()
    #desenhando gráfico 
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig



def order_by_week(df1):
    """
    Recebe o dataframe, executa, gera uma figura e retorna a figura
    
    1. Gera gráfico de Linhas
    2. Cria uma coluna com os pedidios por semana (separando o ano em 52 semanas)  
    3. Total de pedidos por semana
    
    """
    #Criar a coluna da semana
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID', 'Week_of_year']].groupby( 'Week_of_year').count().reset_index()
    #desenhando gráfico linhas
    fig = px.line(df_aux, x='Week_of_year', y='ID')
    return fig


def order_share_by_week(df1):
    """
    Recebe o dataframe, executa, gera uma figura e retorna a figura
    
    1. Gera gráfico de Linhas
    2. Total de pedidos por entregador por semana
    
    """
    
    df_aux01 = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby('Week_of_year').nunique().reset_index()

    df_aux = pd.merge( df_aux01, df_aux02, how='inner')
    df_aux['Order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='Week_of_year', y='Order_by_delivery')
    
    return fig


def country_maps(df1):
    """
    Recebe o dataframe, executa, gera um mapa
    
    1. Gera um mapa
    2. Localização central de cada cidade por tipo de tráfego.
    
    """
    
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to(map)
    
    folium_static(map, width=1024, height=600)


#--------------- Início da Estrtutura Lógica do Código ----------------
  
#---------------------------------
# Import Dataset
#---------------------------------    
    
df = pd.read_csv('train.csv')

#---------------------------------
# Limpando os dados
#---------------------------------

df1 = clean_code(df)

#====================================
#    Barra Lateral --- no Streamlit
#====================================

st.header('Markeplace - Visão Cliente')

image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""----""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider('Até qual valor?',
                                value=pd.datetime(2022, 4, 13),
                                min_value=pd.datetime(2022, 2, 11),
                                max_value=pd.datetime(2022, 4, 6),
                                format='DD-MM-YYYY')

st.sidebar.markdown("""----""")


traffic_options = st.sidebar.multiselect(
                        'Quais as condições do trânsito?',
                        ['Low', 'Medium', 'High', 'Jam'],
                        default=['Low', 'Medium', 'High', 'Jam'])


st.sidebar.markdown("""----""")
st.sidebar.markdown('### Powered by DS')


# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]





#=========================================================================

#    Layout

#=========================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    #Order Metric
    with st.container():
        fig = order_metric(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart(fig, use_container_width=True)
           
    with st.container():
        col1, col2 = st.columns(2)
       
        with col1:
            fig = traffic_order_share(df1)
            st.markdown('# Trafic Order Share')
            st.plotly_chart(fig, use_container_width=True)
       
        with col2:
            fig = traffic_order_city(df1)
            st.markdown('# Trafic Order City')
            st.plotly_chart(fig, use_container_width=True)   

    
with tab2:
    with st.container():        
        fig = order_by_week(df1)
        st.markdown('# Order by Week')       
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():        
        fig = order_share_by_week(df1)
        st.markdown('# Order Share by Week')
        st.plotly_chart(fig, use_container_width=True)

    
with tab3:
    country_maps(df1)
    st.markdown('# Country Maps')
    


