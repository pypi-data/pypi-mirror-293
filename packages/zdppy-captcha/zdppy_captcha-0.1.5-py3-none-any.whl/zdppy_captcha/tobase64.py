import random
import base64
import uuid
from .image import ImageCaptcha
from .common import base_str


def get_base64(num=4, height=60):
    """
    生成base64格式的随机字符串
    建议校验的时候不区分大小写
    :param num: 字符串中验证码的个数
    :param height: 验证码图片的高度
    :return: 真实值，base64图片字符串
    """
    # 生成随机字符串
    code = random.sample(base_str, num)

    # 生成图片验证码对象
    image = ImageCaptcha(width=40 * num, height=height)

    # 第三种使用方式：生成图片验证码BytesIO
    data = image.generate(code)

    # 转换为base
    base64_str = base64.b64encode(data.getvalue()).decode('utf8')

    # 返回
    key = uuid.uuid4().hex
    code = "".join(code)
    return key, code, base64_str
