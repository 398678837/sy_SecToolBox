import requests
import json

class IPLocation:
    def __init__(self):
        self.api_url = "http://ip-api.com/json/{ip}?lang=zh-CN"
    
    def get_location(self, ip):
        try:
            response = requests.get(self.api_url.format(ip=ip), timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "ip": data.get("query"),
                        "country": data.get("country"),
                        "region": data.get("regionName"),
                        "city": data.get("city"),
                        "isp": data.get("isp"),
                        "org": data.get("org"),
                        "as": data.get("as"),
                        "latitude": data.get("lat"),
                        "longitude": data.get("lon"),
                        "timezone": data.get("timezone")
                    }
                else:
                    return {"error": data.get("message", "查询失败")}
            else:
                return {"error": f"API请求失败，状态码：{response.status_code}"}
        except Exception as e:
            return {"error": f"查询过程中发生错误：{str(e)}"}
    
    def batch_query(self, ip_list):
        results = []
        for ip in ip_list:
            result = self.get_location(ip)
            results.append(result)
        return results