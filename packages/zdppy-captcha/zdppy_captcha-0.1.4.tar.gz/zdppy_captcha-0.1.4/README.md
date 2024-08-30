# zdppy_captcha

python用于生成图片，声音等验证码的底层框架

## 安装

```bash
pip install zdppy-captcha
```

## 使用教程

### 显示图片验证码

```python
# 生成图片验证码
import random
from zdppy_captcha.image import ImageCaptcha

# 生成随机字符串
code = random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 4)  # 随机选取4个不重复字符串，返回一个列表

# 生成图片验证码对象
image = ImageCaptcha()

# 第一种使用方式：生成图片验证码
im = image.generate_image(code)
im.show()  # 可以直接展示图片
```

### 保存验证码图片

```python
# 生成图片验证码
import random
from zdppy_captcha.image import ImageCaptcha

# 生成随机字符串
code = random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 4)  # 随机选取4个不重复字符串，返回一个列表

# 生成图片验证码对象
image = ImageCaptcha()

# 第二种使用方式：生成图片验证码并保存
image.write(code, 'zdppy_captcha.jpg')
```

### 将验证码转换为bytesio

```python
# 生成图片验证码
import random
from zdppy_captcha.image import ImageCaptcha

# 生成随机字符串
code = random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 4)  # 随机选取4个不重复字符串，返回一个列表

# 生成图片验证码对象
image = ImageCaptcha()

# 第三种使用方式：生成图片验证码BytesIO
data = image.generate(code)
print(data, type(data))
```

### 生成base64图片

```python
import zdppy_captcha as captcha

# 获取验证码以及base64图片
code, img = captcha.get_base64(6)
print(code)
print(img)
```

## 版本历史

### v0.1.0

- 基本用法

### v0.1.2

- get_base64生成key，code和img

### v0.1.3

- 新增zdppy_api.get方法

### v0.1.4

- 支持zdppy低代码开发

