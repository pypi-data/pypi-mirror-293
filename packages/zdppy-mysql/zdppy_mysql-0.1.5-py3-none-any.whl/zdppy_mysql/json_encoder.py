import json
import decimal
from datetime import datetime, date


class JsonEncoder(json.JSONEncoder):
    """
    decimal解析器
    """

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):  # 将decimal类型转换为float类型
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        super(JsonEncoder, self).default(obj)
