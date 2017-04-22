# pass in SF: ARN, a sync function, timeout flag
import boto3

def sampleSuccessFunction(input):
    print input
    return '{"foo":"bar"}'

def sampleFailureFunction(input):
    raise Exception("I am failure with %s" %input)

def stepFunctionActivities(region, sfarn, executionFunctions):
    client = boto3.client('stepfunctions', region_name=region)
    workerName = "pythonclient"
    response = client.get_activity_task(activityArn = sfarn, workerName=workerName)
    if response:
        token = response[u'taskToken']
        input = response['input']
        try:
            output = executionFunctions(input)
            client.send_task_success(
                taskToken=token,
                output=output
            )
        except Exception as e:
            print e
            client.send_task_failure(
                taskToken=token,
                error="error",
                cause='i am errored'
            )

if __name__ == "__main__":
    sfarn = 'arn:aws:states:us-east-1:620428855768:activity:get-greeting'
    stepFunctionActivities('us-east-1', sfarn, sampleSuccessFunction)
