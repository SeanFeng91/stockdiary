import requests
from ..config import settings
from fastapi import HTTPException

class StockService:
    @staticmethod
    async def get_stock_info(stock_codes: list[str]):
        results = []
        for code in stock_codes:
            try:
                params = {
                    'key': settings.JUHE_API_KEY,
                    'gid': code,
                }
                response = requests.get(settings.JUHE_API_URL, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if data['error_code'] == 0:
                        stock_data = data['result'][0]['data']
                        # 提取关键信息
                        processed_data = {
                            'name': stock_data['name'],
                            'code': stock_data['gid'],
                            'current_price': stock_data['nowPri'],
                            'change_amount': stock_data['increase'],
                            'change_percent': stock_data['increPer'],
                            'open_price': stock_data['todayStartPri'],
                            'prev_close': stock_data['yestodEndPri'],
                            'high': stock_data['todayMax'],
                            'low': stock_data['todayMin'],
                            'volume': stock_data['traNumber'],
                            'amount': stock_data['traAmount'],
                            'update_time': f"{stock_data['date']} {stock_data['time']}"
                        }
                        results.append(processed_data)
                    else:
                        results.append({
                            'code': code,
                            'error': '获取数据失败'
                        })
            except Exception as e:
                results.append({
                    'code': code,
                    'error': str(e)
                })
                
        return results 