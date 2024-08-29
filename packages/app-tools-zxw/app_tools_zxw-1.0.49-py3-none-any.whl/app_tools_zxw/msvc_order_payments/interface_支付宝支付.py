"""
# File       : interface_支付宝支付.py
# Time       ：2024/8/29 上午10:47
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
import httpx
from typing import Optional
from app_tools_zxw.models_payment import OrderStatus, PaymentMethod
from app_tools_zxw.Errors.api_errors import HTTPException_AppToolsSZXW
from app_tools_zxw.msvc_order_payments.schemas_微信支付宝支付 import (
    请求_支付宝url_创建订单,
    返回_支付宝url_订单信息,
    请求_支付宝url_发起支付,
    返回_支付宝url_支付信息
)
from app_tools_zxw.msvc_order_payments.__interface通用方法__ import 验证请求异常sync

BASE_URL = "http://127.0.0.1:8002"  # Replace with the actual base URL


async def 创建订单_alipay_pay_qr_create_order__post(
        amount: float,
        user_id: str,
        product_id: int,
        app_id: str
) -> 返回_支付宝url_订单信息:
    url = f"{BASE_URL}/alipay/pay_qr/create_order/"
    payload = 请求_支付宝url_创建订单(
        amount=amount,
        user_id=user_id,
        product_id=product_id,
        app_id=app_id
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload.dict())
        验证请求异常sync(response)
        res = response.json()
        print("创建订单_alipay_pay_qr_create_order__post", res)
        return 返回_支付宝url_订单信息(**res)


async def 发起支付_alipay_pay_qr_pay__post(
        order_number: str,
        callback_url: str
) -> 返回_支付宝url_支付信息:
    url = f"{BASE_URL}/alipay/pay_qr/pay/"
    payload = 请求_支付宝url_发起支付(
        order_number=order_number,
        callback_url=callback_url
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload.dict())
        验证请求异常sync(response)
        return 返回_支付宝url_支付信息(**response.json())


async def 查询支付状态_alipay_pay_qr_payment_status__transaction_id__get(
        transaction_id: str
) -> 返回_支付宝url_支付信息:
    url = f"{BASE_URL}/alipay/pay_qr/payment_status/{transaction_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        验证请求异常sync(response)
        return 返回_支付宝url_支付信息(**response.json())
