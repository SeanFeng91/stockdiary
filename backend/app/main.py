from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .services.stock_service import StockService

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.pages.dev",  # Cloudflare Pages 域名
        "https://your-custom-domain.com"  # 如果你有自定义域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "股票信息系统API"}

@app.get("/api/stocks")
async def get_stocks(codes: str):
    """
    获取股票信息
    codes: 股票代码列表，用逗号分隔，如 sz002230,sh600519
    """
    try:
        stock_codes = codes.split(',')
        if not stock_codes:
            raise HTTPException(status_code=400, detail="请提供股票代码")
        
        results = await StockService.get_stock_info(stock_codes)
        return {"data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 