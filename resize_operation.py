import boto3
import io
import re
import sys
import traceback
from PIL import Image

s3 = boto3.resource('s3')
s3client = boto3.client('s3')


def create_thumbnail_image(backet, org_key):
    try:
        org_image = s3client.get_object(Bucket=backet, Key=org_key)
        img_bin = io.BytesIO(org_image['Body'].read())
        pil_img = Image.open(img_bin)

        extention_type = 'JPEG'
        if re.match(r'.*png$', org_key):
            extention_type = 'PNG'

        if extention_type == 'JPEG' and pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")

        pil_img.thumbnail((250, 250), Image.ANTIALIAS)
        img = io.BytesIO()
        pil_img.save(img, extention_type)
        thumb_img = img.getvalue()
        s3obj = s3.Object(backet, org_key + '.thumb.jpg')
        s3obj.put(Body=thumb_img)
    except Exception:
        print(traceback.format_exc())
        print('Failed to create thumbnail image of "{}/{}".'.format(backet, org_key))
        return False


def lambda_handler(event, context):
    if 'debug' in event and event['debug'] == 'True':
        # for test
        print('for debug')
        create_thumbnail_image(event['backet'], event['key'])
    else:
        # Parse job parameters
        jobId = event['job']['id']
        invocationId = event['invocationId']
        invocationSchemaVersion = event['invocationSchemaVersion']

        # Process the task
        task = event['tasks'][0]
        taskId = task['taskId']
        s3Key = task['s3Key']
        s3VersionId = task['s3VersionId']
        s3BucketArn = task['s3BucketArn']
        s3Bucket = s3BucketArn.split(':')[-1]
        print('BatchProcessObject(' + s3Bucket + "/" + s3Key + ')')

        create_thumbnail_image(s3Bucket, s3Key)

        results = [{
            'taskId': taskId,
            'resultCode': 'Succeeded',
            'resultString': 'Succeeded'
        }]

        return {
            'invocationSchemaVersion': invocationSchemaVersion,
            'treatMissingKeysAs': 'PermanentFailure',
            'invocationId': invocationId,
            'results': results
        }


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print('First argument for backet, and second argument for key are required.')
        quit()

    create_thumbnail_image(args[1], args[2])
