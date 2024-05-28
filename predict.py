import matplotlib.pyplot as plt
import pandas as pd 
from prophet import Prophet
import matplotlib.font_manager as fm
import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
from prophet.plot import plot_plotly
from utils import load_data

total_df = load_data()


def about_house_type(period):
    path = 'BMHANNAPro.ttf'
    fontprop = fm.FontProperties(fname=path, size=12)

    total_df = pd.read_csv('seoul_real_estate.csv')
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'],format='%Y-%m-%d')

    types = list(total_df['HOUSE_TYPE'].unique())

    fig,ax = plt.subplots(figsize=(10,6),sharex=True, ncols=2,nrows=2)

    for i in range(len(types)):
        model = Prophet()
        total_df2 = total_df.loc[total_df['HOUSE_TYPE'] == types[i],['DEAL_YMD','OBJ_AMT']]

        summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
        summary_df = summary_df.rename(columns={'DEAL_YMD':'ds','OBJ_AMT':'y'})

        model.fit(summary_df)

        future1 = model.make_future_dataframe(periods=period)
        forecast1 = model.predict(future1)

        x = i // 2
        y = i % 2

        fig = model.plot(forecast1, uncertainty=True, ax=ax[x,y])
        ax[x,y].set_title(f'서울시 {types[i]} 평균 가격 예측 시나리오 {period}일간',fontproperties=fontprop)
        ax[x,y].set_xlabel(f'날짜',fontproperties=fontprop)
        ax[x,y].set_ylabel(f'평균가격(만원)',fontproperties=fontprop)

        for tick in ax[x,y].get_xticklabels():
            tick.set_rotation(30)

    plt.tight_layout()
    st.pyplot(fig)

def about_sgg_type(period):
    path = 'BMHANNAPro.ttf'
    fontprop = fm.FontProperties(fname=path, size=12)

    total_df = pd.read_csv('seoul_real_estate.csv')
    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'],format='%Y-%m-%d')

    total_df = total_df[total_df['HOUSE_TYPE'] == '아파트']
    sgg_nms = list(total_df['SGG_NM'].unique())

    sgg_nms = [x for x in sgg_nms if x is not np.nan]

    fig,ax = plt.subplots(figsize=(30,20),sharex=True, ncols=5,nrows=5)

    loop = 0

    for sgg in sgg_nms:
        model = Prophet()
        total_df2 = total_df.loc[total_df['SGG_NM'] == sgg,['DEAL_YMD','OBJ_AMT']]

        summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
        summary_df = summary_df.rename(columns={'DEAL_YMD':'ds','OBJ_AMT':'y'})

        model.fit(summary_df)

        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)

        x = sgg_nms.index(sgg) // 5
        y = loop % 5
        loop = loop + 1

        fig = model.plot(forecast, uncertainty=True, ax=ax[x,y])
        ax[x,y].set_title(f'서울시 {sgg} 평균 가격 예측 시나리오 {period}일간',fontproperties=fontprop)
        ax[x,y].set_xlabel(f'날짜',fontproperties=fontprop)
        ax[x,y].set_ylabel(f'평균가격(만원)',fontproperties=fontprop)

        for tick in ax[x,y].get_xticklabels():
            tick.set_rotation(30)

    plt.tight_layout()
    st.pyplot(fig)

def reportMain(total_df):
    sgg_nm = st.sidebar.selectbox('자치구',total_df['SGG_NM'].unique())
    periods = int(st.number_input('예측 기간',min_value = 1, max_value = 30,
                  step=1))
    
    model = Prophet()

    total_df2 = total_df.loc[total_df['SGG_NM'] == sgg_nm, ['DEAL_YMD','OBJ_AMT']]
    summary_df = total_df2.groupby('DEAL_YMD')['OBJ_AMT'].agg('mean').reset_index()
    summary_df = summary_df.rename(columns={'DEAL_YMD':'ds','OBJ_AMT':'y'})

    model.fit(summary_df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    csv = forecast.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button('결과 다운로드(csv)', csv, 
                               f'{sgg_nm} 아파트 평균 예측 {periods}일간.csv','text/csv',key='download_csv')

    fig = plot_plotly(model, forecast)
    fig.update_layout(title=dict(text = f'{sgg_nm} 아파트 평균 예측 {periods}일간',
                                 font = dict(size=20),
                                 yref='paper'),
                      xaxis_title='날짜',
                      yaxis_title='아파트 평균값(만원)',
                      autosize=False,
                      width=700,height=800)
    fig.update_yaxes(tickformat='000')
    st.plotly_chart(fig)


def all_predict():
    st.markdown('기계학습 예측 페이지입니다.\n'
                '사용 알고리즘 : meta의 prophet')
    selected = option_menu(None, ['Home','주거형태별',
                                  '자치구역별','보고서'],
                icons=['house','bar-chart','file-spreadsheet',
                       'map'],
                menu_icon='cast',default_index=0,
                orientation='horizontal',
                
                styles={'container':{
                    'padding':'0!important',
                    'background-color':'#808080'
                },
                'icon':{
                    'color':'orange',
                    'font-size':'25px'
                },'nav-link':{
                    'font-size':'15px',
                    'text-align':'left',
                    'margin':'0px',
                    '--hover-color':'#eee'
                },
                'nav-link-selected':{
                    'background-color':'green'
                }})

    if selected == 'Home':
        st.markdown('- 가구당 평균 가격 예측 그래프 추세\n'
                '- 자치구별 평균 가격 예측 그래프 추세\n'
                '- 사용한 알고리즘 : meta의 prophet')
    elif selected == '주거형태별':
        period = st.number_input('예측 기간',min_value=10,max_value=100)
        about_house_type(period)
    elif selected == '자치구역별':
        period = st.number_input('예측 기간',min_value=10,max_value=100)
        about_sgg_type(period)
    elif selected == '보고서':
        reportMain(total_df)