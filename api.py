from typing import Optional
from fastapi import FastAPI
from numpy.random.mtrand import random
from sqlalchemy import create_engine
from model import Vasicek
from pydantic import BaseModel
from starlette.responses import JSONResponse
from random import randrange

engine = create_engine('sqlite:///./db.db', echo=False)
app = FastAPI()

@app.get('/')
def read_root():
  return {"Hello": "World"}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: Optional[str] = None):
  return {'item_id': item_id, 'q': q}

@app.get('/int_rate/{year}')
def get_int_rate(year: int) -> str:
  data = engine.execute(f"""
    SELECT BASE_DATE,
          MATURITY,
          VALUE
      FROM INT_RATE
      WHERE BOND_TYPE="KTB"
        AND substr(BASE_DATE, 1, 4)='{year}'
    """).fetchall()
  result = [{'BASE_DATE': d[0], 'MATURITY': d[1], 'VALUE': d[2]} for d in data]
  return result

class VasicekConfig(BaseModel):
  dt: float
  a: float
  b: float
  sigma: float
  r0: float
  t: float
  n: int

@app.post('/model/vasicek/scen')
def get_vasicek_scen(config: VasicekConfig):
  vas = Vasicek()
  vas.set_param(config.dt, config.a, config.b, config.sigma)
  # scen = vas.gen_scen(config.r0, config.n, config.t)
  scen = vas.gen_scen(config.r0, config.n, config.t, random_state=randrange(100))
  # result = {i+1: list(scen[:, i]) for i in range(scen.shape[1])}
  result = [list(scen[:, i]) for i in range(scen.shape[1])]
  return JSONResponse(result)