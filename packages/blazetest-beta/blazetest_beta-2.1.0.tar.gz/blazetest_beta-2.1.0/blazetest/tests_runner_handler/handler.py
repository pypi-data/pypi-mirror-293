import json
import logging
import os
from typing import List, Dict

import boto3
import pytest

PWD = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(format="%(process)d-%(levelname)s-%(message)s", level=logging.INFO)


class S3Upload:
    def __init__(self, region):
        self.client = boto3.client(
            "s3",
            region_name=region,
        )

    def upload_file_to_s3_bucket(
        self,
        filepath: str,
        timestamp: str,
        s3_bucket: str,
        session_uuid: str,
        retry: bool,
    ) -> str:
        filename = os.path.basename(filepath)
        dst_folder = os.path.join(session_uuid, f"{timestamp}/target/junitxml")
        dst_filepath = os.path.join(dst_folder, filename)

        if retry:
            dst_filepath = os.path.join(dst_folder, f"flaky-{filename}")

        with open(filepath, "rb") as f:
            self.client.put_object(
                Body=f,
                Bucket=s3_bucket,
                Key=dst_filepath,
            )

        return dst_filepath


def execute_tests(args: List[str]):
    return pytest.main(args)


def run_tests(event, context=None) -> Dict:  # noqa
    setup_logging()

    pytest_args: List[str] = event["pytest_args"]
    node_id: str = event["node_id"]
    report_path: str = event["report_path"]
    region: str = event["region"]
    session_uuid: str = event["session_uuid"]
    timestamp: str = event["start_timestamp"]
    retry: bool = event["retry"]

    logger.info(f"Invoking test: {node_id} with pytest args: {pytest_args}")

    s3_bucket = os.environ.get("S3_BUCKET")

    args = [node_id, f"--junitxml={report_path}"] + pytest_args

    exit_code = execute_tests(args=args)
    test_result = True if exit_code == 0 else False

    logger.info(f"Test result: {'passed' if test_result else 'failed'}")

    s3 = S3Upload(region=region)
    s3_path = s3.upload_file_to_s3_bucket(
        filepath=report_path,
        session_uuid=session_uuid,
        s3_bucket=s3_bucket,
        timestamp=timestamp,
        retry=retry,
    )

    test_result = {
        "test_result": test_result,
        "report_path": s3_path,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(test_result),
    }

    logger.info(f"Response: {response}")

    return response
