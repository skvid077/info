import asyncio

from database.config import settings

from aiobotocore.session import get_session


class S3Client:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key_id: str, endpoint_url: str, bucket_name: str):
        self.config = {
            'aws_access_key_id': aws_access_key_id,
            'aws_secret_access_key': aws_secret_access_key_id,
            'endpoint_url': endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    async def upload_file(self, file_path: str):
        object_name = file_path.split('/')[-1]
        async with self.session.create_client('s3', **self.config) as client:
            with open(file=file_path, mode='rb') as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )

    async def download_file(self, file_path: str, file_url: str):
        async with self.session.create_client('s3', **self.config) as client:
            with open(file=file_path, mode='wb') as file:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=file_url,
                )
                async with response['Body'] as stream:
                    content = await stream.read()
                    file.write(content)

    async def delete_file(self, file_url: str):
        async with self.session.create_client('s3', **self.config) as client:
            await client.delete_object(
                Bucket=self.bucket_name,
                Key=file_url,
            )


async def main():
    from database.queries import Task, Variant
    for num in await Task.nums():
        await s3_client.delete_file(file_url=f'{num}_task.zip')
    for num in await Variant.nums():
        await s3_client.delete_file(file_url=f'{num}_variant.zip')


s3_client = S3Client(
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key_id=settings.aws_secret_access_key_id,
    endpoint_url='https://s3.storage.selcloud.ru',
    bucket_name='info',
)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
