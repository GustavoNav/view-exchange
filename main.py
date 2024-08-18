import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from export.transformed_data.data import df_general_financials, df_historic
from utils.format import format_number

def set_page_config():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)
    
def display_side_bar():
    st.sidebar.header("Filtros")
    
    company_code_unique = st.sidebar.selectbox(
        'Selecione a Empresa:', df_historic['company_code'].unique(), index=0)
    
    start_date = pd.Timestamp(st.sidebar.date_input(
        "Data inicial", 
        value=df_historic['date_information'].min().date(),
        min_value=df_historic['date_information'].min().date(),
        max_value=df_historic['date_information'].max().date()
    ))
    
    end_date = pd.Timestamp(st.sidebar.date_input(
        "Data final", 
        value=df_historic['date_information'].max().date(),
        min_value=df_historic['date_information'].min().date(),
        max_value=df_historic['date_information'].max().date()
    ))

    st.sidebar.markdown('---')
    st.sidebar.write('Escolha Empresas para Comparar')
    company_codes = st.sidebar.multiselect(
        'Selecione as Empresas:', df_historic['company_code'].unique(), default=[df_historic['company_code'].unique()[0]]
    )

    st.sidebar.markdown('---')
    st.sidebar.markdown('**Links:**')
    st.sidebar.markdown('[GitHub](https://github.com/GustavoNav)')
    st.sidebar.markdown('[LinkedIn](https://www.linkedin.com/in/gustavo-navarro-felix/)')

    return company_code_unique, start_date, end_date, company_codes

def display_charts(company_code, start_date, end_date):

    start_date = pd.Timestamp(start_date).tz_localize('UTC')
    end_date = pd.Timestamp(end_date).tz_localize('UTC')
    
    filtered_df = df_historic[
        (df_historic['company_code'] == company_code) &
        (df_historic['date_information'] >= start_date) &
        (df_historic['date_information'] <= end_date)
    ]
    
    fig = px.area(
        filtered_df, 
        x='date_information', 
        y='open', 
        title="Valor de Abertura ao Longo do Tempo",
        labels={'open': 'Valor de Abertura', 'date_information': 'Data'},
        width=900, 
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

def display_charts_multiple(company_codes, start_date, end_date):
    st.markdown('---')
    st.write('Compararação entre Empresas')

    start_date = pd.Timestamp(start_date).tz_localize('UTC')
    end_date = pd.Timestamp(end_date).tz_localize('UTC')

    filtered_df = df_historic[
        (df_historic['company_code'].isin(company_codes)) &
        (df_historic['date_information'] >= start_date) &
        (df_historic['date_information'] <= end_date)
    ]

    col1, col2 = st.columns([4,6])

    with col1:
        volume_by_company = filtered_df.groupby('company_code')['volume'].sum().reset_index()

        fig_pie = px.pie(
            volume_by_company, 
            values='volume', 
            names='company_code',
            title='Distribuição de Volume por Empresa',
            width=300,
            height=500
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        last_7_days_start = datetime.now() - timedelta(days=7)
        last_7_days_start = pd.Timestamp(last_7_days_start).tz_localize('UTC')
        
        recent_df = filtered_df[
            filtered_df['date_information'] >= last_7_days_start
        ]
        
        volume_last_7_days = recent_df.groupby('company_code')['volume'].sum().reset_index()
        
        fig_bar = px.bar(
            volume_last_7_days,
            x='company_code',
            y='volume',
            title='Volume Total por Empresa nos Últimos 7 Dias',
            labels={'company_code': 'Empresa', 'volume': 'Volume Total'},
            width=300,
            height=460
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    fig_area = px.area(
        filtered_df, 
        x='date_information', 
        y='open', 
        color='company_code',  
        title="Valor de Abertura ao Longo do Tempo",
        labels={'open': 'Valor de Abertura', 'date_information': 'Data'},
        width=500, 
        height=00
    )

    st.plotly_chart(fig_area, use_container_width=True)

def show_metrics(company_code):
    df_general_financials_filtred = df_general_financials[df_general_financials['company_code'] == company_code]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('Receita Líquida', format_number(df_general_financials_filtred['net_sales'].values[0]))
        
    with col2:
        st.metric('Lucro Líquido', format_number(df_general_financials_filtred['net_income'].values[0]))

    with col3:
        st.metric('Ebitda', format_number(df_general_financials_filtred['ebitda'].values[0]))

def main():
    company_code_unique, start_date, end_date, company_codes = display_side_bar()

    show_metrics(company_code_unique)
    display_charts(company_code_unique, start_date, end_date)
    display_charts_multiple(company_codes, start_date, end_date)
    
    
if __name__ == "__main__":
    main()