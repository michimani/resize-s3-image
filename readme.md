# resize-s3-image

This is an AWS Lambda function that resizes the image in Amazon S3. This function is supposed to be called by Amazon S3 Batch Operations.  

## feature
- resize a image to 250px x 250px
- file type of resized image is JPEG

## for deploy

```
sh archive.sh
```

The zip file `upload.zip` will be generated. So, you upload this zip file to AWS Lambda function.

In this shell script, `docker-compose` command is called. So you need docker for local machine.  

### Why use docker ?
The Pillow library has parts dependent on the installed OS. In order to run on AWS Lambda, you need the Pillow library installed in the Amazon Linux 2 environment. Therefore, it is necessary to include the Pillow library installed with docker image of Amazon Linux 2 in the zip file to be uploaded to AWS Lambda.

## run at local

It is needed to install the following python libraries.

- boto3
- Pillow

```
pip3 install -r ./deploy/requirements_local.txt
```

Although omitted, configuration of AWS CLI is also needed.


```
python3 resize_operation.py s3_backet_name key_for_image_file
```