from flask import Flask, redirect, url_for, render_template, request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "bPU_xt5ftColUyTUKBDklnJSM4DJCSioleyJ6qpyxRZE"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/04066c17ad1f4ce8b18c59e43d029679:1dbee128-6dad-4c3a-ae30-61dafecf8e38::"


cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )


app = Flask(__name__)


def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
            print(files_names)
        return files_names

    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))


@app.route('/')
def index():
    files = get_bucket_contents('abinash')
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
