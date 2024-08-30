import boto3
import logging
from typing import Any
from pathlib import Path
from cloudpathlib import CloudPath, S3Client


def _make_callback(callback):
    if callback is None:
        return lambda s: s
    return callback


def _make_error_callback(callback):
    if callback is None:
        return lambda s, e: s
    return callback


class TransferEvent:
    def __init__(self, src: str, dst: str, info: Any):
        self.src = src
        self.dst = dst
        self.info = info

class TransferResult:
    def __init__(
        self,
        succeded: list[TransferEvent],
        failed: list[TransferEvent],
    ):
        if succeded is None:
            succeded = []
        self.succeded = succeded
        if failed is None:
            failed = []
        self.failed = failed

    def succeeded_num(self) -> int:
        return len(self.succeeded)

    def failed_num(self) -> int:
        return len(self.failed)

    def total_num(self) -> int:
        return self.succeeded_num() + self.failed_num()

    def add(self, success: bool, event: TransferEvent):
        if success:
            self.succeeded.append(event)
        else:
            self.failed.append(event)


class Datastore:
    def __init__(
        self,
        config: dict[str,str],
        bucket: str,
        download_callback = None,
        download_error_callback = None,
        upload_callback = None,
        upload_error_callback = None
    ):
        self.resource = boto3.resource("s3", **config)
        self.bucket = self.resource.Bucket(bucket)
        self.bucket_name = bucket
        self.bucket_path = CloudPath(
            f"s3://{bucket}",
            client = S3Client(
                 aws_access_key_id = config["aws_access_key_id"],
                 aws_secret_access_key = config["aws_secret_access_key"],
                 endpoint_url = config["endpoint_url"],
            )
        )
        self.download_callback = _make_callback(download_callback)
        self.upload_callback = _make_callback(upload_callback)
        self.download_error_callback = _make_error_callback(download_error_callback)
        self.upload_error_callback = _make_error_callback(upload_error_callback)

    def path(self, *paths) -> CloudPath:
        return self.bucket_path.joinpath(*paths)

    def download(self, key: str|Path) -> bytes|None:
        key_str = str(key)
        self.download_callback(key_str)
        try:
            result = self.resource.Object(self.bucket_name, key_str)["Body"].read()
            return result
        except Exception e:
            self.download_error_callback(key_str, e)
            return None

    def download_to(self, key: str|Path, local_path: str|Path) -> bool:
        key_str = str(key)
        self.download_callback(key_str)
        try:
            self.bucket.download_file(key_str, str(local_path))
            return True
        except Exception e:
            self.download_error_callback(key_str, e)
            return False

    def upload(self, key: str|Path, data: bytes) -> bool:
        key_str = str(key)
        self.upload_callback(key_str)
        try:
            self.bucket.put_object(Key = key_str, Body = data)
            return True
        except Exception e:
            self.upload_error_callback(key_str, e)
            return False

    def upload_from(self, local_path: str|Path, key: str|Path) -> bool:
        key_str = str(key)
        self.upload_callback(key_str)
        try:
            self.bucket.upload_file(str(local_path), key_str)
            return True
        except Exception e:
            self.upload_error_callback(key_str, e)
            return False

    def download_many(self,
        keys: list[str|Path],
        output_dir: str|Path,
        extra_info = list[Any]
    ) -> TransferResult:
        output_path = Path(output_dir)
        result = TransferResult()
        for key, info in zip(keys, extra_info):
            src = key
            dst = output_path.joinpath(key)

            success = self.download_to(src, dst)
            event = TransferEvent(src, dst, info)
            result.add(success, event)

        return result

    def upload_many(self,
        keys: list[str|Path],
        input_dir: str|Path,
        extra_info: list[Any]
    ) -> TransferResult:
        result = TransferResult()
        for key, info in zip(keys, extra_info):
            src = Path(key).relative_to(input_dir)
            dst = key

            success = self.upload_from(src, dst)
            event = TransferEvent(src, dst, info)
            result.add(success, event)

        return result

