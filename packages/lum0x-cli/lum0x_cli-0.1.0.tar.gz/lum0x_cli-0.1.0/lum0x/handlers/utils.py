import time

def wait_for_lambda_function_active(lambda_client, function_name):
    print(f"Waiting for Lambda function {function_name} to become active...")
    while True:
        response = lambda_client.get_function(FunctionName=function_name)
        status = response['Configuration']['State']
        print(f"Current status: {status}")
        if status == 'Active':
            print("Lambda function is now active.")
            break
        elif status in ['Failed', 'Inactive']:
            raise Exception(f"Lambda function deployment failed with status: {status}")
        time.sleep(5)
