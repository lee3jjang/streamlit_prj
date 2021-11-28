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

selected_model = st.sidebar.selectbox('모형 선택', ['Vasicek', 'CIR', 'Hull-White'], index=1)

if selected_model == 'CIR':
  st.write('CIR Model :')
  st.latex(r"""
    dr_t = a(\theta-r_t)dt+\sigma \sqrt{r_t} dW_t
  """)

  with st.form('cir_config'):
    with st.expander('Parameter'):
      dt = 1/12
      col1, col2, col3 = st.columns(3)
      with col1: a = st.slider('a', min_value=0.01, max_value=1., value=0.1, step=0.001)
      with col2: b = st.slider('θ', min_value=0., max_value=.1, value=0.02, step=0.001)
      with col3: sigma = st.slider('σ', min_value=0., max_value=.5, value=0.1, step=0.001)


    with st.expander('Scenario setting'):
      col1, col2, col3 = st.columns(3)
      with col1: r0 = st.slider('r0', min_value=0., max_value=.1, value=0.001, step=0.001)
      with col2: t = st.slider('t', min_value=1, max_value=100, value=50, step=1)
      with col3: n = st.slider('n', min_value=10, max_value=200, value=10, step=1)

    submitted = st.form_submit_button('Run')
    if submitted:
      if 2*a*b < sigma**2:
        st.warning('2*a*b >= σ^2 조건 위반')
      headers = {'Content-Type': 'application/json; charset=utf-8', 'accept': 'application/json'}
      config = {'dt': dt, 'a': a, 'b': b, 'sigma': sigma, 'r0': r0, 't': t, 'n': n}
      scen = requests.post('http://127.0.0.1:8000/model/cir/scen',
        headers=headers, data=json.dumps(config)).json()

      fig = go.Figure(data=[go.Scattergl(x=np.arange(0, t+dt, dt), y=scen[i], line=dict(width=1), hovertemplate='금리: %{y:,.2%}<br>시점: %{x:,.2f}년<extra></extra>') for i in range(n)])
      fig.update_layout({
        'width': 675,
        'height': 250,
        'title': '<b>시나리오 생성결과 (CIR) 모델)</b>',
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
          size=11,
          color='#7f7f7f',
        )
      })
      st.plotly_chart(fig)

  if submitted:
    scen_df = pd.DataFrame(scen)
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    download_btn = st.download_button('시나리오 다운', data=scen_df.to_csv(index=False, header=False),
      file_name=f'cir_scen_{now}.csv', mime='text/csv')

elif selected_model == 'Vasicek':
  with st.form('vasicek_config'):
    st.write('Vasicek 모델 :')
    st.latex(r"""
      dr_t = a(\theta-r_t)dt+\sigma dW_t
    """)

    with st.expander('모델 매개변수'):
      dt = 1/12
      col1, col2, col3 = st.columns(3)
      with col1: a = st.slider('a', min_value=0.01, max_value=1., value=0.1, step=0.001)
      with col2: b = st.slider('θ', min_value=0., max_value=.1, value=0.02, step=0.001)
      with col3: sigma = st.slider('σ', min_value=0., max_value=.5, value=0.1, step=0.001)

    with st.expander('시나리오 설정'):
      col1, col2, col3 = st.columns(3)
      with col1: r0 = st.slider('r0', min_value=0., max_value=.1, value=0.001, step=0.001)
      with col2: t = st.slider('t', min_value=1, max_value=100, value=50, step=1)
      with col3: n = st.slider('n', min_value=10, max_value=200, value=10, step=1)

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
          size=11,
          color='#7f7f7f',
        )
      })
      st.plotly_chart(fig)

  if submitted:
    scen_df = pd.DataFrame(scen)
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    download_btn = st.download_button('Download', data=scen_df.to_csv(index=False, header=False),
      file_name=f'vasicek_scen_{now}.csv', mime='text/csv')