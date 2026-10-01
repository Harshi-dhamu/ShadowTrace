from fastapi import FastAPI

app = FastAPI(
    title="ShadowTrace",
    description="Attack Reconstruction & Security Investigation Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "ShadowTrace",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }