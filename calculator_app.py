from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Union
import uvicorn

app = FastAPI(title="Calculator API", description="A simple calculator API with web interface")

# Pydantic models for request/response
class CalculationRequest(BaseModel):
    a: float
    b: float

class CalculationResponse(BaseModel):
    result: float
    operation: str
    a: float
    b: float

class SingleNumberRequest(BaseModel):
    number: float

# API Routes
@app.post("/add", response_model=CalculationResponse)
async def add(request: CalculationRequest):
    result = request.a + request.b
    return CalculationResponse(result=result, operation="addition", a=request.a, b=request.b)

@app.post("/subtract", response_model=CalculationResponse)
async def subtract(request: CalculationRequest):
    result = request.a - request.b
    return CalculationResponse(result=result, operation="subtraction", a=request.a, b=request.b)

@app.post("/multiply", response_model=CalculationResponse)
async def multiply(request: CalculationRequest):
    result = request.a * request.b
    return CalculationResponse(result=result, operation="multiplication", a=request.a, b=request.b)

@app.post("/divide", response_model=CalculationResponse)
async def divide(request: CalculationRequest):
    if request.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    result = request.a / request.b
    return CalculationResponse(result=result, operation="division", a=request.a, b=request.b)

@app.post("/power", response_model=CalculationResponse)
async def power(request: CalculationRequest):
    result = request.a ** request.b
    return CalculationResponse(result=result, operation="power", a=request.a, b=request.b)

@app.post("/sqrt")
async def square_root(request: SingleNumberRequest):
    if request.number < 0:
        raise HTTPException(status_code=400, detail="Cannot calculate square root of negative number")
    result = request.number ** 0.5
    return {"result": result, "operation": "square_root", "number": request.number}

# Web UI Route
@app.get("/", response_class=HTMLResponse)
async def get_calculator_ui():
    return FileResponse("./index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Calculator API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)