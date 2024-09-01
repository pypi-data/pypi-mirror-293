"""
支持平台: AWS, 阿里云

安装: pip install aiobotocore
 aiobotocore==2.14.0
 oss2==2.19.0  - 不需要

使用时,请确保替换以下信息:
    您的AccessKeyId和您的AccessKeySecret
    您的存储桶名称
    要下载的文件名
    保存文件的本地路径

阿里云OSS官网文档: https://help.aliyun.com/zh/oss/developer-reference/use-amazon-s3-sdks-to-access-oss

以中国香港地域为例，
    S3兼容的外网Endpoint格式为s3.oss-cn-hongkong.aliyuncs.com,
    S3兼容的内网Endpoint格式为s3.oss-cn-hongkong-internal.aliyuncs.com。
    如需使用其他地域,请对应替换Endpoint中的Region ID。
    关于Region和Endpoint的对应关系,请参见访问域名和数据中心。
"""
import asyncio
# import oss2
from aiobotocore.session import get_session
from typing import List, Tuple


class AsyncAliyunOSS:
    def __init__(self, access_key_id: str, access_key_secret: str, endpoint: str, bucket_name: str):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.session = get_session()

    async def _get_client(self):
        return await self.session.create_client('s3',
                                                region_name='oss-cn-hangzhou',
                                                endpoint_url=self.endpoint,
                                                aws_access_key_id=self.access_key_id,
                                                aws_secret_access_key=self.access_key_secret)

    async def get_download_url(self, object_key: str, expires: int = 3600) -> str:
        async with await self._get_client() as client:
            url = await client.generate_presigned_url('get_object',
                                                      Params={'Bucket': self.bucket_name, 'Key': object_key},
                                                      ExpiresIn=expires)
            return url

    async def upload_file(self, local_file_path: str, object_key: str) -> bool:
        async with await self._get_client() as client:
            try:
                with open(local_file_path, 'rb') as f:
                    await client.put_object(Bucket=self.bucket_name, Key=object_key, Body=f)
                return True
            except Exception as e:
                print(f"上传文件失败: {e}")
                return False

    async def list_all_files(self) -> List[Tuple[str, str]]:
        async with await self._get_client() as client:
            paginator = client.get_paginator('list_objects_v2')
            file_list = []
            async for page in paginator.paginate(Bucket=self.bucket_name):
                for obj in page.get('Contents', []):
                    file_list.append((obj['Key'], f"https://{self.bucket_name}.{self.endpoint}/{obj['Key']}"))
            return file_list


async def main(access_key_id, access_key_secret,
               bucket_name="your-bucket-name",
               endpoint="oss-cn-hangzhou.aliyuncs.com",
            ):
    # 使用示例
    oss = AsyncAliyunOSS(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
        bucket_name=bucket_name
    )

    # 1. 获取下载链接
    download_url = await oss.get_download_url('example.txt')
    print(f"下载链接: {download_url}")

    # 2. 上传文件
    upload_success = await oss.upload_file('/path/to/local/file.txt', 'remote_file.txt')
    print(f"文件上传{'成功' if upload_success else '失败'}")

    # 3. 列出所有文件
    files = await oss.list_all_files()
    print("所有文件:")
    for file_name, file_url in files:
        print(f"- {file_name}: {file_url}")


if __name__ == "__main__":
    asyncio.run(main(access_key_id="your-access-key-id", access_key_secret="your-access-key-secret"))
