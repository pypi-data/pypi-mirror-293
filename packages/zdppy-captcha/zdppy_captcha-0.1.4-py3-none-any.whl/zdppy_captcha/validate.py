def is_captcha(cache_obj, user_key, user_captcha):
    """
    校验验证码是否正确
    :param cache_obj: 这是一个缓存对象，必须有 get 方法，且通过get方法能够获取到真实的验证码
    :param user_key: 验证码的唯一key，用来确保用户输入的验证码的唯一性
    :param user_captcha: 用户输入的验证码，用来校验cache_obj中存储的验证码是否和用户的验证码一致
    """
    # 获取验证码
    cache_captcha = None
    try:
        cache_captcha = cache_obj.get(user_key)
    except:
        return False

    # 验证码不是字符串类型
    if not isinstance(cache_captcha, str):
        return False

    # 比较验证码
    return cache_captcha.lower() == str(user_captcha).lower()
