import json
import boto3
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):
    # TODO implement



    sns=boto3.resource("sns")
    topic=sns.Topic("arn:aws:sns:ap-southeast-2:812574023636:DeployPortfolio")
    try:
        s3=boto3.resource("s3")
        portfolio_bucket=s3.Bucket("portfolio.bhupendra-jaiswal.info")

        build_bucket=s3.Bucket('portfoliobuil.bhupendrajaiswal.info')


        portfolio_zip=StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild',portfolio_zip)
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj=myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType': 'basestring'})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print("job done")
        topic.publish(Subject="Portfolio Deployed", Message="The Portfolio deployed successfully")
    except:
        topic.publish(Subject="Portfolio Deploy Failed ", Message="The Portfolio was not deployed successfully")
        raise
