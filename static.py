import streamlit as st
import pandas as pd 
from plotly.subplots import make_subplots
import plotly.express as px
from pingouin import ttest
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg 
import matplotlib.font_manager as fm

def twoMeans(total_df, sgg_nm):
    st.markdown(f'### 서울시 2,3월 아파트 평균 가격 차이 검증')

    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2,3]))]

    dec_df = apt_df[apt_df['month'] == 2]
    nov_df = apt_df[apt_df['month'] == 3]

    st.markdown('2월 아파트 평균 가격(만원) : {}'.format(dec_df['OBJ_AMT'].mean().round(0)))
    st.markdown('3월 아파트 평균 가격(만원) : {}'.format(nov_df['OBJ_AMT'].mean().round(0)))

    result = ttest(dec_df['OBJ_AMT'],nov_df['OBJ_AMT'], paired=False)

    st.dataframe(result, use_container_width=True)

    if result['p-val'].values[0] > 0.05:
        st.markdown('p-val값이 0.05초과로 서울시 2,3월 아파트 평균 가격의 차이는 없다.')
    else:
        st.markdown('p-val값이 0.05미만으로 서울시 2,3월 아파트 평균 가격의 차이는 있다.')

    st.markdown('<br><br>',unsafe_allow_html=True)

    st.markdown(f'### 서울시 {sgg_nm} 2,3월 아파트 평균 가격 차이 검증')

    total_df['month'] = total_df['DEAL_YMD'].dt.month
    total_df = total_df[total_df['SGG_NM'] == sgg_nm]
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2,3]))]

    dec_df = apt_df[apt_df['month'] == 2]
    nov_df = apt_df[apt_df['month'] == 3]

    st.markdown('2월 아파트 평균 가격(만원) : {}'.format(dec_df['OBJ_AMT'].mean().round(0)))
    st.markdown('3월 아파트 평균 가격(만원) : {}'.format(nov_df['OBJ_AMT'].mean().round(0)))

    result = ttest(dec_df['OBJ_AMT'],nov_df['OBJ_AMT'], paired=False)

    st.dataframe(result, use_container_width=True)

    if result['p-val'].values[0] > 0.05:
        st.markdown('p-val값이 0.05초과로 서울시 2,3월 아파트 평균 가격의 차이는 없다.')
    else:
        st.markdown('p-val값이 0.05미만으로 서울시 2,3월 아파트 평균 가격의 차이는 있다.')

def corrRealtion(total_df, sgg_nm):
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2,3]))]

    st.markdown('### 상관관계 분석 데이터 확인'
                '- 건물 면적과 거래금액의 상관관계 분석'
                '- 먼저 추출한 데이터 확인')

    corr_df = apt_df[['DEAL_YMD','OBJ_AMT', 'BLDG_AREA','SGG_NM','month']].reset_index(drop=True)
    st.dataframe(corr_df.head())

    st.markdown('### 상관관계 분석 시각화\n'
                '- 상관관계 시각화(산포도)\n')
    
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x='BLDG_AREA',y='OBJ_AMT', data=corr_df, ax=ax)
    
    st.pyplot(fig)

    # 상관계수 확인

    st.markdown('### 서울시 상관관계 계수 및 검정\n'
                '상관관계 계수를 확인')
    
    st.dataframe(pg.corr(corr_df['BLDG_AREA'],corr_df['OBJ_AMT']).round(3), use_container_width=False)
    corr_r = pg.corr(corr_df['BLDG_AREA'],corr_df['OBJ_AMT']).round(3)['r']

    st.write(corr_r.item())

    if corr_r.item() > 0.5:
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적 증가 시 금액도 증가하는 경향을 보임')
    elif corr_r.item() < -0.5:
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적 증가 시 금액은 감소하는 경향을 보임')
    else:
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적과 금액의 관계성은 비교적 작다.')

    st.markdown(f'### 서울시 {sgg_nm} 2, 3월 아파트 가격 - 건물면적 상관관계 분석\n')
    sgg_df = corr_df[corr_df['SGG_NM'] == sgg_nm]
    corr_coef = pg.corr(sgg_df['BLDG_AREA'], sgg_df['OBJ_AMT'])
    st.dataframe(corr_coef, use_container_width=False)

    path = 'BMHANNAPro.ttf'
    fontprop = fm.FontProperties(fname = path, size=12)

    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x='BLDG_AREA',y='OBJ_AMT', data=sgg_df)
    ax.text(0.95, 0.05, f'Pearson Correlation : {corr_coef["r"].values[0]:.2f}',transform = ax.transAxes, ha='right', fontsize=12)
    ax.set_title(f'{sgg_nm} 피어슨 상관계수',fontproperties=fontprop,fontsize=20)
    
    st.pyplot(fig)

def task(total_df, sgg_nm):
    total_df = total_df[total_df['SGG_NM'] == sgg_nm]
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    apt_df = total_df[(total_df['HOUSE_TYPE'] == '아파트') & (total_df['month'].isin([2,3]))]

    mean_size = apt_df.groupby('DEAL_YMD')['OBJ_AMT'].agg(['mean','size']).reset_index()

    st.markdown('### 서울시 구별 거래 건수와 아파트 가격의 상관관계')

    st.dataframe(pg.corr(mean_size['mean'],mean_size['size']).round(3), use_container_width=False)
    corr_r = pg.corr(mean_size['mean'],mean_size['size']).round(3)['r']

    if corr_r.item() > 0.5:
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적 증가 시 금액도 증가하는 경향을 보임')
    elif corr_r.item() < -0.5:
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적 증가 시 금액은 감소하는 경향을 보임')
    else:
        st.markdown(f'상관계수는 {corr_r.item()}이며, 건물 면적과 금액의 관계성은 비교적 작다.')

    path = 'BMHANNAPro.ttf'
    fontprop = fm.FontProperties(fname = path, size=12)

    corr_coef = pg.corr(mean_size['mean'],mean_size['size'])

    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x='mean',y='size', data=mean_size)
    ax.text(0.95, 0.05, f'Pearson Correlation : {corr_coef["r"].values[0]:.2f}',transform = ax.transAxes, ha='right', fontsize=12)
    ax.set_title(f'{sgg_nm} 피어슨 상관계수',fontproperties=fontprop,fontsize=20)
    
    st.pyplot(fig)


def showStat(total_df):
    analysis_nm = st.sidebar.selectbox('분석 메뉴',['두 집단 간 차이 검정','상관분석','구별 거래건수 상관관계'])
    sgg_nm = st.sidebar.selectbox('자치구명',total_df['SGG_NM'].unique())

    if analysis_nm == '두 집단 간 차이 검정':
        twoMeans(total_df, sgg_nm)
    elif analysis_nm == '상관분석':
        corrRealtion(total_df, sgg_nm)
    elif analysis_nm == '구별 거래건수 상관관계':
        task(total_df,sgg_nm)
    else:
        st.warning('Error')