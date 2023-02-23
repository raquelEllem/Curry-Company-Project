import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine 
import folium

import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(page_title='Visão Entregadores', layout='wide')

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


            
def top_delivers(df1, top_asc):
    """ 
    1. Recebe o dataset e o top_asc (ver 3.)
    2. Retorna os 10 entregadores mais lentos ou rápidos por cidade
    3. O top_asc define o ascending, se for False pega os últimos (ou seja, os entregadores que possuem os maiores tempos de entrega, que são os mais lentos). Se for True, pega os com o menor tempo (mais rápidos)   
    """
    
    df2 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby( ['City', 'Delivery_person_ID'] ).max().sort_values(['City', 'Time_taken(min)'], ascending=top_asc).reset_index()

    #encontra os top 10 de cada cidade
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    #concatena os top10 de cada cidade em uma única tabela
    df3 =  pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index(drop=True)

    return df3




#--------------- Início da Estrtutura Lógica do Código ----------------
  
#---------------------------------
# Import Dataset
#---------------------------------    
    
df = pd.read_csv('train.csv')

#---------------------------------
# Limpando os dados
#---------------------------------

df1 = clean_code(df)




## VISÃO - EMPRESA

#=====================================
#    Barra Lateral --- no Streamlit

#=====================================
st.header('Markeplace - Visão Entregadores')

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


tab1, tab2, tab3 = st.tabs(['Visão Gerencial', ' ', ' '])

with tab1:
    with st.container():
        st.markdown('## Overall Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:
            # A Maior idade entre os entregadores         
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)
            
            
        with col2:
            #A Menor idade entre os entregadores            
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)

        
        with col3:
            # Veiculo com melhor condição
            melhor_condicao_veiculo = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao_veiculo)
            
        
        with col4:
            # Veiculo com pior condição
            pior_condicao_veiculo = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao_veiculo)
            
    
    with st.container():
        st.sidebar.markdown("""----""")
        st.markdown('## Avaliações')
        
        
        col1, col2 = st.columns(2)
        with col1:            
            st.markdown('##### Avaliação média por entregador')
            
            avaliacao_media_entregador = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby( ['Delivery_person_ID'] ).mean().reset_index())
            
            st.dataframe(avaliacao_media_entregador)

            
            
        with col2:
          
            st.markdown('##### Avaliação média por trânsito')
            
            df_agg_rating_by_trafic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby( 'Road_traffic_density' ).agg( {'Delivery_person_Ratings' : ['mean', 'std']} ) )

            #mudança de nome das colunas
            df_agg_rating_by_trafic.columns = ['Delivery_mean', 'Delivery_std']

            #reset index
            df_agg_rating_by_trafic.reset_index()
            
            st.dataframe(df_agg_rating_by_trafic)
                      
            st.markdown('##### Avaliação média por clima')
            df_agg_weather = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby( 'Weatherconditions' ).agg( {'Delivery_person_Ratings' : ['mean', 'std']} ) )
            #mudança de nome das colunas
            df_agg_weather.columns = ['Weather_mean', 'Weather_std']
            #reset index
            df_agg_weather.reset_index()
            
            st.dataframe(df_agg_weather)
            
            
            
    with st.container():
        st.sidebar.markdown("""----""")
        st.markdown('## Velocidade de Entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            df3 = top_delivers(df1, top_asc=True)
            st.markdown('##### Top entregadores mais rápidos')
            st.dataframe(df3)

            
        with col2:
            df3 = top_delivers(df1, top_asc=False)
            st.markdown('##### Top entregadores mais lentos')         
            st.dataframe(df3)