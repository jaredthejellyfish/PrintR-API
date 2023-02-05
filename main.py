import os
import PIL
import uvicorn
from urllib.parse import unquote
from PrintWrapper import PrintManager
from fastapi.responses import JSONResponse
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request, status
from slowapi.errors import RateLimitExceeded
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_SECRET = os.environ.get("API_SECRET")

@app.get("/")
async def root():
    return {"response": f"Hello, welcome to this receipt printing API! {API_SECRET}"}


@app.exception_handler(RequestValidationError)
@limiter.limit("2/minute")
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/print")
@limiter.limit("2/minute")
async def print(request: Request, text: str, cut: bool = False):
    text = unquote(text)
    p = PrintManager(0x04b8, 0x0202)
    my_header = request.headers.get('x-PrintRAPI-key')
    if my_header != API_SECRET:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "unauthorized"}))

    if len(text) > 2000:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"error": "text too long"}))

    print_status = "ok"

    p.println(text, cut)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"text": text, "status": print_status}))


@app.get("/pmarkdown")
@limiter.limit("2/minute")
async def pmarkdown(request: Request, doc: str):
    my_header = request.headers.get('x-PrintRAPI-key')
    p = PrintManager(0x04b8, 0x0202)
    if my_header != API_SECRET:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "unauthorized"}))
    if len(doc) > 2000:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"error": "text too long"}))

    print_status = "ok"
    document = unquote(doc)

    p.pdocument(document=document)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"text": document, "status": print_status}))


@app.get("/part")
@limiter.limit("2/minute")
async def part(request: Request, doc: str):
    my_header = request.headers.get('x-PrintRAPI-key')
    p = PrintManager(0x04b8, 0x0202)
    if my_header != API_SECRET:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "unauthorized"}))
    print_status = "ok"

    p.part(document=doc)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"text": doc, "status": print_status}))


@app.get("/cut")
@limiter.limit("2/minute")
async def cut(request: Request, ):
    my_header = request.headers.get('x-PrintRAPI-key')
    p = PrintManager(0x04b8, 0x0202)
    if my_header != API_SECRET:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "unauthorized"}))

    p.p.cut()

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"status": "ok"}))

@app.get("/image")
@limiter.limit("2/minute")
async def image(request: Request, ):
    my_header = request.headers.get('x-PrintRAPI-key')
    p = PrintManager(0x04b8, 0x0202)
    if my_header != API_SECRET:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "unauthorized"}))
    img = PIL.Image.open("image.png")
    p.p.image(img_source=img)
    p.p.cut()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"status": "ok"}))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8899, log_level="info")
