from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.client import ClientConfig
from app.services.scenario import detect_scenario
from app.services.cisco import CiscoGenerator
from app.services.dlink import DLinkGenerator


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="Switch Configurator",
    version="0.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


cisco_generator = CiscoGenerator()
dlink_generator = DLinkGenerator()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.post("/api/config")
def generate_config(config: ClientConfig):
    try:
        scenario = detect_scenario(config)

        cisco = cisco_generator.generate(
            config,
            scenario,
        )

        dlink = dlink_generator.generate(
            config,
            scenario,
        )

        return {
            "scenario": scenario,
            "cisco": cisco,
            "dlink": dlink,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )