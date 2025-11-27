"""統一的 API 回應格式工具"""


def success_response(data, status_code=200):
    """成功回應格式"""
    return {"success": True, "data": data}, status_code


def error_response(message, error_code, status_code=400):
    """錯誤回應格式"""
    return {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
        },
    }, status_code
