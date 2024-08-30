from .tobase64 import get_base64
from .validate import is_captcha


def captcha(api, cache, num=4, expire=60):
    """
    :param cache: 缓存对象
    :param num: 验证码的个数
    :param expire: 验证码的过期时间，默认1分钟
    """

    async def get_captcha(req):
        """
        获取zdppy_api生成验证码的接口
        :param success: api.resp.success 是zdppy_api框架中统一返回成功结果的方法
        :return:
        """
        key, code, img = get_base64(num)
        try:
            cache.set(key, code, expire)
            return api.resp.success({
                "key": key,
                "img": img,
            })
        except Exception as e:
            pass
            return api.resp.error_500(str(e))

    async def validate(req):
        """
        校验验证码
        """
        # 用户的验证码
        data = await api.req.get_json(req)
        key = data.get("key")
        code = data.get("code")
        if not key or not code:
            return api.resp.error_400("key或者code不能为空")

        # 校验
        v1 = is_captcha(cache, key, code)
        return api.resp.success({"key": key, "code": code, "ok": v1})

    return [
        api.resp.get("/zdppy_captcha", get_captcha),
        api.resp.post("/zdppy_captcha", validate),
    ]
