import streamlit as st

def run_home():
    st.markdown('## 대시보드 개요 \n''본 프로젝트는 서울시 부동산 실거래가를 알려주는 대시보드입니다.'
                '여기에 추가하고 싶은 내용을 추가하면 됩니다.')
    sgg_nm = st.sidebar.selectbox('자치구',['구로구','영등포구','관악구'])
    acc_year = st.sidebar.selectbox('연도',[2023,2024])
    month_dic = {}
    for i in range(1,13):
        month_dic['{}월'.format(i)] = i
    selected_month = st.sidebar.radio('확인하고 싶은 월을 선택하시오',list(month_dic.keys()))
    st.markdown('<hr>',unsafe_allow_html=True)
    st.subheader(f'{sgg_nm} {acc_year}년 {selected_month} 아파트 가격 개요')
    st.markdown('자치구와 월을 클릭하면 자동으로 각 지역구에서 거래된 **최소가격**, **최대가격**을 확인할 수 있습니다.')