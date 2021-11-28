from typing import Optional
from fastapi import FastAPI
from numpy.random.mtrand import random
from sqlalchemy import create_engine
from model import Vasicek, CIR
from pydantic import BaseModel
from starlette.responses import JSONResponse
from random import randrange

engine = create_engine('sqlite:///./db.db', echo=False)
app = FastAPI()

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
  scen = vas.gen_scen(config.r0, config.n, config.t)
  result = [list(scen[:, i]) for i in range(scen.shape[1])]
  return JSONResponse(result)

class CIRConfig(BaseModel):
  dt: float
  a: float
  b: float
  sigma: float
  r0: float
  t: float
  n: int

@app.post('/model/cir/scen')
def get_vasicek_scen(config: CIRConfig):
  cir = CIR()
  cir.set_param(config.dt, config.a, config.b, config.sigma)
  scen = cir.gen_scen(config.r0, config.n, config.t)
  result = [list(scen[:, i]) for i in range(scen.shape[1])]
  return JSONResponse(result)