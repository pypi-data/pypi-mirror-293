"""
# File       : test_interface_支付宝支付.py
# Time       ：2024/8/29 上午10:51
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：使用真实服务器请求的支付宝支付接口测试
"""
import pytest
from app_tools_zxw.models_payment import OrderStatus, PaymentMethod
from app_tools_zxw.msvc_order_payments.schemas_微信支付宝支付 import (
    请求_支付宝url_创建订单,
    返回_支付宝url_订单信息,
    请求_支付宝url_发起支付,
    返回_支付宝url_支付信息,
)
from app_tools_zxw.msvc_order_payments.interface_支付宝支付 import (
    创建订单_alipay_pay_qr_create_order__post,
    发起支付_alipay_pay_qr_pay__post,
    查询支付状态_alipay_pay_qr_payment_status__transaction_id__get,
)

# 使用正确的测试环境URL和凭证
# BASE_URL = "http://127.0.0.1:8002"  # 替换为实际的测试环境URL
APP_ID = "test_app_id"  # 替换为实际的测试应用ID
Product_ID = 1  # 替换为实际的测试商品ID


@pytest.mark.asyncio
async def test_创建订单_alipay_pay_qr_create_order__post():
    request = 请求_支付宝url_创建订单(
        amount=0.01,  # 使用小额进行测试
        user_id="test_user",
        product_id=Product_ID,
        app_id=APP_ID
    )

    result = await 创建订单_alipay_pay_qr_create_order__post(**request.model_dump())

    assert isinstance(result, 返回_支付宝url_订单信息)
    assert result.user_id == "test_user"
    assert result.total_amount == 0.01
    assert result.status == OrderStatus.PENDING

    # 保存订单号以供后续测试使用
    global test_order_number
    test_order_number = result.order_number


@pytest.mark.asyncio
async def test_发起支付_alipay_pay_qr_pay__post():
    request = 请求_支付宝url_发起支付(
        order_number=test_order_number,
        callback_url="http://test-callback.example.com"
    )

    result = await 发起支付_alipay_pay_qr_pay__post(**request.model_dump())

    assert isinstance(result, 返回_支付宝url_支付信息)
    assert result.amount == 0.01
    assert result.payment_status in ["pending", "processing"]  # 根据实际情况调整
    assert result.qr_uri is not None

    # 保存交易ID以供后续测试使用
    global test_transaction_id
    test_transaction_id = result.transaction_id


@pytest.mark.asyncio
async def test_查询支付状态_alipay_pay_qr_payment_status__transaction_id__get():
    result = await 查询支付状态_alipay_pay_qr_payment_status__transaction_id__get(test_transaction_id)

    assert isinstance(result, 返回_支付宝url_支付信息)
    assert result.transaction_id == test_transaction_id
    assert result.amount == 0.01


if __name__ == "__main__":
    pytest.main(["-v", "test_interface_支付宝支付.py"])
