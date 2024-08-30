import os
import time
import json
import uuid
import zipfile
import tempfile
import boto3
import requests
import shutil
from .utils import wait_for_lambda_function_active

def deploy_lambda_function(user_code_zip, trigger_conf=None, overwrite=False, ondemand=False):
    """Deploy user code with a Lambda handler."""
    print("####################### Starting deployment process... ########################")

    # 에러 메시지 추가: trigger_conf가 없고 ondemand가 False일 때
    if trigger_conf is None and not ondemand:
        print("Error: trigger.conf is required when not deploying as an on-demand function.")
        print("example: lum0x deploy your_code.zip trigger.conf")
        return

    if not os.path.exists('.lum0x_session'):
        print("Error: No valid session found. Please run `lum0x credential` first.")
        return

    with open('.lum0x_session', 'r') as session_file:
        session_data = json.load(session_file)

    print("AWS session loaded.")

    sts_client = boto3.client(
        'sts',
        aws_access_key_id=session_data['aws_access_key_id'],
        aws_secret_access_key=session_data['aws_secret_access_key'],
        region_name=session_data['aws_region']
    )

    try:
        identity = sts_client.get_caller_identity()
        print(f"Authenticated as: {identity['Arn']}")
    except Exception as e:
        print(f"Error in AWS authentication: {e}")
        return

    user_id = session_data['farcasterFid']
    print(f"Using user ID (farcasterFid): {user_id}")

    # 임시 디렉토리 생성
    with tempfile.TemporaryDirectory() as tempdir:
        # 원래의 .zip 파일을 임시 디렉토리로 추출
        with zipfile.ZipFile(user_code_zip, 'r') as zip_ref:
            zip_ref.extractall(tempdir)
        print(f"User code extracted to {tempdir}")

        # handler.js 파일을 직접 생성하여 추가
        handler_code = """
import { main } from './index.js';

export async function lum0xhandler(event) {
  let result;

  if (event.triggerType === 'on-demand') {
    const parameters = event.parameters || {}; // 사용자가 지정한 파라미터
    result = await main(parameters);
  } else {
    const limit = event.limit || 250; // 기본값을 주기적 실행 시 사용하는 경우
    result = await main(limit);
  }

  return {
    statusCode: 200,
    body: JSON.stringify(result),
  };
}
"""
        handler_file_path = os.path.join(tempdir, 'handler.js')
        with open(handler_file_path, 'w') as handler_file:
            handler_file.write(handler_code)
        print(f"Lambda handler added to {handler_file_path}")

        # 새로 압축할 .zip 파일의 경로 설정 (원래의 .zip 파일 제외)
        modified_zip_file = os.path.join(tempdir, f"{user_id}_{os.path.basename(user_code_zip)}")
        with zipfile.ZipFile(modified_zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zip_ref:
            for foldername, subfolders, filenames in os.walk(tempdir):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    if filepath != user_code_zip:  # 원래의 .zip 파일을 제외
                        arcname = os.path.relpath(filepath, tempdir)
                        zip_ref.write(filepath, arcname)
        print(f"Created modified ZIP: {modified_zip_file}")

        s3_client = boto3.client(
            's3',
            aws_access_key_id=session_data['aws_access_key_id'],
            aws_secret_access_key=session_data['aws_secret_access_key'],
            region_name=session_data['aws_region']
        )

        bucket_name = 'lum0x-buildathon'
        s3_prefix = f"{user_id}/"

        if not overwrite:
            timestamp = time.strftime('%Y%m%dT%H%M%S', time.gmtime())
            s3_key = f"{s3_prefix}{os.path.splitext(os.path.basename(modified_zip_file))[0]}-{timestamp}.zip"
            function_name = f"{os.path.splitext(os.path.basename(modified_zip_file))[0]}-{timestamp}"
        else:
            s3_key = f"{s3_prefix}{os.path.basename(modified_zip_file)}"
            function_name = os.path.splitext(s3_key.replace(f"{user_id}/", ''))[0]

        try:
            s3_client.upload_file(modified_zip_file, bucket_name, s3_key)
            print(f"Uploaded {modified_zip_file} to S3 bucket {bucket_name} with key {s3_key}.")

            lambda_client = boto3.client(
                'lambda',
                aws_access_key_id=session_data['aws_access_key_id'],
                aws_secret_access_key=session_data['aws_secret_access_key'],
                region_name=session_data['aws_region']
            )

            created_at = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

            try:
                # Check if the function already exists
                lambda_client.get_function(FunctionName=function_name)

                # If the function exists and overwrite is true, update the function code
                response = lambda_client.update_function_code(
                    FunctionName=function_name,
                    S3Bucket=bucket_name,
                    S3Key=s3_key,
                )
                print(f"Lambda function {function_name} updated successfully.")
            except lambda_client.exceptions.ResourceNotFoundException:
                # If the function does not exist, create a new one
                response = lambda_client.create_function(
                    FunctionName=function_name,
                    Runtime='nodejs20.x',
                    Role=session_data['aws_lambda_role_arn'],
                    Handler='handler.lum0xhandler',
                    Code={'S3Bucket': bucket_name, 'S3Key': s3_key},
                    Timeout=300,
                    MemorySize=128,
                )
                print(f"Lambda function {function_name} created successfully.")

            wait_for_lambda_function_active(lambda_client, function_name)

            try:
                function_url_response = lambda_client.create_function_url_config(
                    FunctionName=function_name,
                    AuthType='NONE',
                )
                function_url = function_url_response['FunctionUrl']
                print(f"Function URL created: {function_url}")
            except lambda_client.exceptions.ResourceConflictException:
                function_url_response = lambda_client.get_function_url_config(
                    FunctionName=function_name
                )
                function_url = function_url_response['FunctionUrl']
                print(f"Function URL already exists: {function_url}")

            try:
                lambda_client.add_permission(
                    FunctionName=function_name,
                    StatementId='AllowPublicAccessViaFunctionURL',
                    Action='lambda:InvokeFunctionUrl',
                    Principal='*',
                    FunctionUrlAuthType='NONE'
                )
                print("Permission added for public access via Function URL.")
            except lambda_client.exceptions.ResourceConflictException:
                print("Permission already exists for public access.")

            function_uuid = str(uuid.uuid4())
            print(f"Your Function ID: {function_uuid}")

            # 스케줄 표현식 설정
            schedule_expression = None
            if not ondemand and trigger_conf:
                with open(trigger_conf, 'r') as f:
                    schedule_expression = f.read().strip()

            if overwrite:
                # 기존 메타데이터를 업데이트
                metadata_update_payload = {
                    "functionId": function_uuid,
                    "uploadedAt": created_at,
                    "trigger": schedule_expression if schedule_expression else "on-demand",
                }

                metadata_update_response = requests.put(
                    f"https://testnetapi.lum0x.com/function/metadata/overwrite",
                    json=metadata_update_payload
                )

                if metadata_update_response.status_code in [200, 201]:
                    print("Function metadata updated successfully.")
                else:
                    print(f"Failed to update function metadata: {metadata_update_response.status_code} {metadata_update_response.text}")

            else:
                # 새 메타데이터 생성
                metadata_payload = {
                    "functionId": function_uuid,
                    "awsFunctionArn": response['FunctionArn'],
                    "functionName": function_name,
                    "farcasterId": session_data['farcasterFid'],
                    "createdAt": created_at,
                    "uploadedAt": created_at,
                    "trigger": schedule_expression if not ondemand else "on-demand",
                    "functionURL": function_url
                }

                metadata_response = requests.post(
                    "https://testnetapi.lum0x.com/function/metadata",
                    json=metadata_payload
                )

                if metadata_response.status_code in [200, 201]:
                    print("Function metadata stored successfully.")
                else:
                    print(f"Failed to store function metadata: {metadata_response.status_code} {metadata_response.text}")

            if not ondemand:
                if trigger_conf is None:
                    print("Error: trigger_conf is required for non-ondemand deployment.")
                    return

                events_client = boto3.client(
                    'events',
                    aws_access_key_id=session_data['aws_access_key_id'],
                    aws_secret_access_key=session_data['aws_secret_access_key'],
                    region_name=session_data['aws_region']
                )

                with open(trigger_conf, 'r') as f:
                    schedule_expression = f.read().strip()

                rule_name = f"{function_name}-trigger-rule"
                try:
                    events_client.put_rule(
                        Name=rule_name,
                        ScheduleExpression=schedule_expression,
                        State='ENABLED'
                    )
                    print(f"Trigger set with schedule: {schedule_expression}")
                except events_client.exceptions.ResourceAlreadyExistsException:
                    events_client.put_rule(
                        Name=rule_name,
                        ScheduleExpression=schedule_expression,
                        State='ENABLED'
                    )
                    print(f"Existing rule updated with schedule: {schedule_expression}")

                events_client.put_targets(
                    Rule=rule_name,
                    Targets=[
                        {
                            'Id': function_name,
                            'Arn': response['FunctionArn']
                        }
                    ]
                )
                print(f"Function URL before saving metadata: {function_url}")
                print(f"Function ARN before saving metadata: {response['FunctionArn']}")

        except Exception as e:
            print(f"An error occurred: {e}")
