from fastapi import FastAPI, Response, HTTPException, status

app = FastAPI()


@app.get("/")
def health_check():
    return {"health": "ok"}
