#streamlit을 활용하여 아파트 매매 거래 지역 [구로구, 영등포구, 양천구]과 년, 월을 선택
# 하면 거래일시, 도로명, 거래금액이 출력되도록 구현해 보세요

import streamlit as st
import requests
from urllib.parse import unquote
import xmltodict
import pandas as pd
import numpy as np

st.title('국토교통부 아파트매매 실거래')
st.write('(˵ ͡~ ͜ʖ ͡°˵)ﾉ')

region_dic = {'구로구':'11530','영등포구':'11560','양천구':'11470'}

with st.sidebar:
    region = st.selectbox('지역',list(region_dic.keys()))
    year = st.selectbox('year',list(range(2020,2025)))
    month = st.selectbox('month',list(range(1,13)))
    btn = st.button('SUBMIT')

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
serviceKey = 'PT7s57yQ6NYjF%2BK4IX03RFJISja7dPlVceXQn7%2Fm2DWnibRv2u9288PJ6m9t4hi6sH2A%2B8fa8AGF3nDiGmeZRw%3D%3D'
api_key = unquote(serviceKey)
params ={'serviceKey' : api_key, 'pageNo' : '1', 'numOfRows' : '10', 'LAWD_CD' : '{}'.format(region_dic[region]), 'DEAL_YMD' : '{}{:02d}'.format(year,month)}

response = requests.get(url, params=params)
contents = xmltodict.parse(response.text)

con = contents['response']['body']['items']['item']
result = pd.DataFrame(con)
result['월'] = np.where(result['월'].astype('int')<10,'0'+result['월'],result['월'])
result['일'] = np.where(result['일'].astype('int')<10,'0'+result['일'],result['일'])
result['거래일시'] = result['년']+result['월']+result['일']
result['거래일시'] = pd.to_datetime(result['거래일시']).dt.date

if btn:
    st.dataframe(result[['거래일시', '도로명', '거래금액']], width=800)