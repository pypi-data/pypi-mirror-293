from app_tools_zxw.SDK_苹果内购验证 import responseModel订阅, responseModel非订阅
import asyncio
import datetime
import time
import itunesiap

url_production = "https://buy.itunes.apple.com/verifyReceipt"
url_sandbox = "https://sandbox.itunes.apple.com/verifyReceipt"
共享密钥 = "d30f0080cbba428892fd494d6fa8b855"  # 为非自动订阅式购买必传

错误码 = {
    0: "成功",
    21000: "App Store无法读取你提供的JSON数据",
    21002: "收据数据不符合格式",
    21003: "收据无法被验证",
    21004: "你提供的共享密钥和账户的共享密钥不一致",
    21005: "收据服务器当前不可用",
    21006: "收据是有效的，但订阅服务已经过期。当收到这个信息时，解码后的收据信息也包含在返回内容中",
    21007: "收据信息是测试用（sandbox），但却被发送到产品环境中验证",
    21008: "收据信息是产品环境中使用，但却被发送到测试环境中验证"
}


async def check购买(recipt, is订阅=True):
    try:
        response = await itunesiap.aioverify(recipt, password=共享密钥,
                                             env=itunesiap.env.review)
        resDict = response.__dict__["_"]
        if is订阅:
            resPYD = responseModel订阅.response_data(**resDict)
        else:
            resPYD = responseModel非订阅.response_data(**resDict)
        return [True, resPYD]

    except itunesiap.exc.InvalidReceipt as e:
        tmp = e.__dict__["_"]
        if tmp.get("status", None) is not None:
            res = 错误码.get(tmp["status"], tmp["status"])
        else:
            res = str(e)
        return [False, res]


async def 非订阅校验(recipt, transaction_id) -> bool:
    # 服务器请求
    res = await check购买(recipt, is订阅=False)
    if res[0] is False:
        return False
    else:
        appleRes = res[1]

    # 校验返回值
    is购买 = False
    for item in appleRes.receipt.in_app:
        if item.transaction_id == transaction_id:
            is购买 = True
            break
    return is购买


async def 订阅校验(appleRes: responseModel订阅.response_data, transaction_id) -> float:
    # 校验订阅是否到期
    now = time.time() * 1000
    订阅到期时间 = now - 2 * 60 * 60 * 1000

    # # 1. 先查latest_receipt_info
    print("先查latest_receipt_info")
    for item in appleRes.latest_receipt_info:
        if item.original_transaction_id == transaction_id:
            # print("id相等：", item.expires_date, " --- ", datetime.datetime.fromtimestamp(item.expires_date_ms / 1000))
            if item.expires_date_ms > 订阅到期时间:
                print("此条记录为未过期记录，", datetime.datetime.fromtimestamp(item.expires_date_ms / 1000))
                订阅到期时间 = item.expires_date_ms

    if 订阅到期时间 > now:
        return 订阅到期时间 / 1000

    # # 2.latest_receipt_info不存在时,查询in_app
    print("latest_receipt_info不存在时,查询in_app")
    for item in appleRes.receipt.in_app:
        if item.original_transaction_id == transaction_id:
            # print("id相等：", item.expires_date, " --- ", datetime.datetime.fromtimestamp(item.expires_date_ms / 1000))
            if item.expires_date_ms > 订阅到期时间:
                print("此条记录为未过期记录，", datetime.datetime.fromtimestamp(item.expires_date_ms / 1000))
                订阅到期时间 = item.expires_date_ms

    return 订阅到期时间 / 1000


if __name__ == '__main__':
    recipt = "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"
    transaction_id = "1000000694853763"
    originalTransactionIdentifierIOS = "1000000694851733"


    async def tmp():
        rex = await check购买(recipt,is订阅=True)
        rs = await 订阅校验(rex[1], originalTransactionIdentifierIOS)
        x = datetime.datetime.fromtimestamp(rs)
        print(x)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(tmp())
