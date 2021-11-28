import json
import requests
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

st.write("""
# 금리 모형
Vasicek, CIR, Hull-White 등 다양한 금리모형을 시뮬레이션할 수 있습니다.
""")

with st.form('vasicek_config'):
  st.write('Vasicek 모델 시나리오 설정')
  dt = 1/12
  with st.expander('모델 매개변수'):
    a = st.slider('a', min_value=0.01, max_value=1., value=0.1, step=0.001)
    b = st.slider('b', min_value=0., max_value=1., value=0.02, step=0.001)
    sigma = st.slider('sigma', min_value=0., max_value=1., value=0.1, step=0.001)
  with st.expander('시나리오 설정'):
    r0 = st.slider('r0', min_value=0., max_value=1., value=0.05, step=0.001)
    t = st.slider('t', min_value=1, max_value=100, value=20, step=1)
    n = st.slider('n', min_value=1, max_value=200, value=10, step=1)

  submitted = st.form_submit_button('시나리오 생성')
  if submitted:
    headers = {'Content-Type': 'application/json; charset=utf-8', 'accept': 'application/json'}
    config = {'dt': dt, 'a': a, 'b': b, 'sigma': sigma, 'r0': r0, 't': t, 'n': n}
    scen = requests.post('http://127.0.0.1:8000/model/vasicek/scen',
      headers=headers, data=json.dumps(config)).json()
    
    fig = go.Figure(data=[go.Scattergl(x=np.arange(0, t+dt, dt), y=scen[i], line=dict(width=1), hovertemplate='금리: %{y:,.2%}<br>시점: %{x:,.2f}년<extra></extra>') for i in range(n)])
    fig.update_layout({
      'width': 675,
      'height': 250,
      'title': '<b>시나리오 생성결과 (Vasicek 모델)</b>',
      'title_font_size': 20,
      'title_x': 0.524,
      'paper_bgcolor': '#fff',
      'plot_bgcolor': '#fff',
      'margin': dict(l=20, r=20, t=50, b=20),
      'showlegend': False,
      'xaxis_title': '시점(년)',
      'yaxis_title': '금리',
      'yaxis_range': [-1., 1.],
      # 'xaxis_linecolor': 'black',
      # 'xaxis_linewidth': 1,
      'font': dict(
        family='Malgun Gothic',
        size=8,
        color='#7f7f7f',
      )
    })
    st.plotly_chart(fig)

if submitted:
  scen_df = pd.DataFrame(scen)
  now = datetime.now().strftime('%Y%m%d%H%M%S')
  download_btn = st.download_button('시나리오 다운', data=scen_df.to_csv(index=False, header=False),
    file_name=f'vasicek_scen_{now}.csv', mime='text/csv')