import streamlit as st 
import pandas as pd 
from streamlit_option_menu import option_menu
from viz import showViz
from utils import load_data
from static import showStat
from map import *

total_df = load_data()
merge_df = for_merge_df(total_df)

def home():
    st.markdown('### visualization 개요'
                '- 가구당 평균 가격 추이\n'
                '- 가구당 거래 건수 추세\n'
                '- 지역별 평균 가격 막대 그래프\n')
    st.markdown('### Statistics 개요\n')
    st.markdown('### Map 개요')

def run_eda_home():
    st.markdown("### 탐색적 자료 분석 개요\n"
                "탐색적 자료 분석 페이지입니다."
                "여기에 포함하고 싶은 내용을 넣을 수 있습니다")
    
    selected = option_menu(None, ['Home','Visualization',
                                  'Statistics','Map'],
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
        home()
    elif selected == 'Visualization':
        showViz(total_df)
    elif selected == 'Statistics':
        showStat(total_df)
    else:
        showMap(total_df)
        mapMatplotlib(merge_df)