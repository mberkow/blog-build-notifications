
import boto3
import os


def lambda_handler(event, context):

    sns_topic = os.environ.get('SNS_TOPIC_NAME')
    aws_partition = os.environ.get('AWS_PART')
    aws_account = os.environ.get('AWS_ACCID')
    aws_region = os.environ.get('AWS_REGION')

    sns_arn = 'arn:{}:sns:{}:{}:{}'.format(
        aws_partition,
        aws_region,
        aws_account,
        sns_topic
    )

    # Some variables to help with readability
    build_status = event['detail']['build-status']
    project_name = event['detail']['project-name']
    build_id = event['detail']['additional-information']['build-number']
    log_link = event['detail']['additional-information']['logs']['deep-link']
    initiator = event['detail']['additional-information']['initiator']
    build_time = event['detail']['additional-information']['build-start-time']

    subject = "Build for {project_name} {status} on {time}".format(
        project_name=project_name,
        status=build_status,
        time=build_time
    )
    print(subject)

    message = """
    Build completed.

    ------------------------------------------------------------------------------------
    Summary of the build:
    ------------------------------------------------------------------------------------
    {a:<20}:   {project_name}
    {b:<20}:   {status}
    {c:<20}:   {id}
    {d:<20}:   {initiator}
    {e:<20}:   {logs}
    ------------------------------------------------------------------------------------
    """.format(
        a='Project Name',
        b='Build Status',
        c='Build ID',
        d='Initiator',
        e='Logs',
        project_name=project_name,
        status=build_status,
        id=build_id,
        logs=log_link,
        initiator=initiator
    )
    print(message)

    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=sns_arn,
        Message=message,
        Subject=subject
    )
    print(response)
