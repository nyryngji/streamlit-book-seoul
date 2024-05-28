import streamlit as st 
from streamlit_option_menu import option_menu
import func

def main():
    with st.sidebar:
        selected = option_menu('대시보드 메뉴',['홈','탐색적 자료분석','부동산'],
                               icons=['house','file-bar-graph','graph-up-arrow'],
                               default_index=0,menu_icon='cast')
    if selected in ['홈','부동산']:
        pass
    elif selected == '탐색적 자료분석':
        func.run_home()
    else:
        print('error') 
    
if __name__ == '__main__':
    main()