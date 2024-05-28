import streamlit as st 
from streamlit_option_menu import option_menu
from utils import load_data
from home3 import run_home3
from eda import run_eda_home
from predict import *

def main():
    total_df = load_data()

    with st.sidebar:
        selected = option_menu('대시보드 메뉴',['홈','탐색적 자료분석','부동산 예측'],
                               icons=['house','file-bar-graph','graph-up-arrow'],
                               menu_icon='cast',default_index=0)
    
    if selected == '홈':
        run_home3(total_df)
    elif selected == '탐색적 자료분석':
        run_eda_home()
    elif selected == '부동산 예측':
        st.markdown('### 기계학습 예측 개요')
        all_predict()
    else:
        print('error')
    
if __name__ == "__main__":
    main()