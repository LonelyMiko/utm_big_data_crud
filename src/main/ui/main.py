import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.main.eda.utils import DataAnalysis
from src.main.ui.api.aisles_crud import aisle_router
from src.main.ui.api.departments_crud import departments_router
from src.main.ui.api.orders_crud import router
from src.main.ui.api.products_crud import products_router

app = FastAPI(title="InstaCart CRUD")
app.include_router(router=router)
app.include_router(router=aisle_router)
app.include_router(router=departments_router)
app.include_router(router=products_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Get the directory of the current file
BASE_DIR = Path(__file__).resolve().parent

# Paths to static and templates directories
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(templates_dir))
data_analysis = DataAnalysis(conn_id=os.getenv("DB_CONN"))


@app.get("/orders", response_class=HTMLResponse)
async def orders_ui(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request})


@app.get("/aisles", response_class=HTMLResponse)
async def aisles_ui(request: Request):
    return templates.TemplateResponse("aisles.html", {"request": request})


@app.get("/departments", response_class=HTMLResponse)
async def departments_ui(request: Request):
    return templates.TemplateResponse("departments.html", {"request": request})


@app.get("/products", response_class=HTMLResponse)
async def products_ui(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def index_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/analysis", response_class=HTMLResponse)
async def analysis_ui(request: Request):
    return templates.TemplateResponse("analysis.html", {"request": request})

@app.get("/analysis/hypothesis1", response_class=HTMLResponse)
async def hypothesis1(request: Request):
    result = await data_analysis.analyze_hypothesis1()
    return templates.TemplateResponse("hypothesis1.html", {"request": request, "result": result})


@app.get("/analysis/hypothesis2", response_class=HTMLResponse)
async def hypothesis2(request: Request):
    result = await data_analysis.analyze_hypothesis2()
    return templates.TemplateResponse("hypothesis2.html", {"request": request, "result": result})


@app.get("/analysis/hypothesis3", response_class=HTMLResponse)
async def hypothesis2(request: Request):
    result = await data_analysis.analyze_hypothesis3()
    return templates.TemplateResponse("hypothesis3.html", {"request": request, "result": result})


@app.get("/analysis/hypothesis4", response_class=HTMLResponse)
async def hypothesis2(request: Request):
    result = await data_analysis.analyze_hypothesis4()
    return templates.TemplateResponse("hypothesis4.html", {"request": request, "result": result})


@app.get("/analysis/hypothesis5", response_class=HTMLResponse)
async def hypothesis2(request: Request):
    result = await data_analysis.analyze_hypothesis5()
    return templates.TemplateResponse("hypothesis5.html", {"request": request, "result": result})

