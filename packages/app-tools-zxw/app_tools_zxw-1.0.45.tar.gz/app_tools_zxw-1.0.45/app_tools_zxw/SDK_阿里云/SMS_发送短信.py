from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json

userID = 'sms@.onaliyun.com'
accessKeyId = ''
accessSecret = ''
#
client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')


def 发送短信验证码SMS(手机号: str, 验证码):
    """
    return: {'Message': '触发小时级流控Permits:5', 'RequestId': 'E3F11903-3F92-4245-8FDD-407BAE980FCA', 'Code': 'isv.BUSINESS_LIMIT_CONTROL'}
    """
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', 手机号)
    request.add_query_param('SignName', "景募")
    request.add_query_param('TemplateCode', "SMS_168725021")
    request.add_query_param('TemplateParam', "{\"code\":%s}" % 验证码)

    response = client.do_action_with_exception(request)
    #
    re = json.loads(response.decode('utf-8'), encoding='utf-8')
    #
    return re


if __name__ == '__main__':
    re = 发送短信验证码SMS('15050560029', 12345)
    print(re)
