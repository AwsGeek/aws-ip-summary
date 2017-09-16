# aws-ip-summary
Recieve a sumary notification via SNS each time ther is a change to the AWS IP ranges

1. Create the IAM role. Permissions to SNS Publish
2. Create the SNS topic and subscribe to it
3. Create the Lambda function
4. Subscribe to the AWS IP Range SNS topic, target Lambda function
5. Create the Lambda trigger
