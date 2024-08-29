from fastapi import FastAPI
from loguru import logger

from plurally.models.flow import Flow


def get_plurally_app(flow: Flow) -> FastAPI:
    app = FastAPI()

    @app.post("/run")
    def run_flow():
        logger.info("Running flow")
        return flow.name

    @app.get("/health")
    def read_root():
        return {"status": "ok"}

    return app
