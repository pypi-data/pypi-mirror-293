import requests


def send(message, token, *args, **kwargs):
    # 提取platform参数, 如果没有从kwargs传入, 则从args中提取第一个参数作为platform
    if kwargs.get("platform", None):
        platform = kwargs["platform"]
    elif len(args) > 0:
        args = list(args)
        platform = args.pop(0).lower()
    else:
        raise ValueError(f"API Platform Not Found.")
    # 调用platform对应的函数
    if platform in globals() and callable(globals()[platform]):
        return globals()[platform](message, token, *args, **kwargs)
    raise ValueError(f"Not Support API Platform {platform}")


def telegram(message: str, token: str, host="api.telegram.org", mono=False, **kwargs):
    # 从token中提取bot_id和chat_id
    bot_id, chat_id = token.split("|")[0], token.split("|")[1]
    # 生成url
    url = f"https://{host}/bot{bot_id}/sendMessage"
    # 设置字体为等宽字体
    text = message
    if mono and "parse_mode" not in kwargs:
        text = f"<pre>{message}</pre>"
        kwargs["parse_mode"] = "HTML"
    # 消息格式
    data = {
        "chat_id": chat_id,
        "text": text,
        **kwargs,
    }
    # 发送请求
    response = None
    try:
        response = requests.get(url, params=data, timeout=1)
        resp_json = response.json()
        return resp_json
    except Exception as e:
        if response is None:
            print(f"Telegram API response ({text}): {e} ")
        else:
            print(f"Telegram API response ({text}): {e} -> {response.text}")
        if kwargs.get("raise_error", False):
            raise ValueError(f"Telegram API Error. {e}")


def pushplus(message, token, title="default", template="html", **kwargs):
    url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={message}&template={template}"
    return requests.get(url=url).text
