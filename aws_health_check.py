from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET
import socket
 
# This script iterates through a subset of AWS services in the public 
# GovCloud Health Status dashboard. The script returns status based on 
# RSS feed response, then formats as a metric data point for Splunk ingest
 
RSS_BASE = "https://status.amazonaws-us-gov.com/rss/{slug}.rss"
TIMEOUT = 10
 
STATUS_VALUES = {
    "HEALTHY": 1.0,
    "DEGRADED": -1.0,
    "SPLUNK_INTEGRATION_ERROR": 0.0,
}
 
SERVICES = [
    "apigateway-us-gov-east-1",
    "apigateway-us-gov-west-1",
    "dynamodb-us-gov-east-1",
    "dynamodb-us-gov-west-1",
    "ec2-us-gov-east-1",
    "ec2-us-gov-west-1",
    "ecr-us-gov-east-1",
    "ecr-us-gov-west-1",
    "ecs-us-gov-east-1",
    "ecs-us-gov-west-1",
    "rds-us-gov-east-1",
    "rds-us-gov-west-1",
    "route53-us-gov-east-1",
    "route53-us-gov-west-1",
    "sns-us-gov-east-1",
    "sns-us-gov-west-1",
    "sqs-us-gov-east-1",
    "sqs-us-gov-west-1",
    "s3-us-gov-east-1",
    "s3-us-gov-west-1",
    "test-broken-service-gov-west-1",
    "vpc-us-gov-east-1",
    "vpc-us-gov-west-1",
    "iam-us-gov-east-1",
    "iam-us-gov-west-1",
    "kms-us-gov-east-1",
    "kms-us-gov-west-1",
    "lambda-us-gov-east-1",
    "lambda-us-gov-west-1",
    "management-console-us-gov-east-1",
    "management-console-us-gov-west-1",
    "natgateway-us-gov-east-1",
    "natgateway-us-gov-west-1",
    "transitgateway-us-gov-east-1",
    "transitgateway-us-gov-west-1",
]
 
 
def check_feed(slug):
    url = RSS_BASE.format(slug=slug)
    try:
        with urlopen(url, timeout=TIMEOUT) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        items = root.findall("./channel/item")
        if items:
            title = items[0].findtext("title", default="Incident reported")
            return slug, "DEGRADED", title
        return slug, "HEALTHY", "No issues"
    except (HTTPError, URLError, socket.timeout, ET.ParseError) as e:
        return slug, "SPLUNK_INTEGRATION_ERROR", str(e)
 
 
def main():
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_feed, slug): slug for slug in SERVICES}
        for future in as_completed(futures):
            slug, status, message = future.result()
            value = STATUS_VALUES[status]
            clean_message = message.replace("|", " ").replace(",", " ").replace("\n", " ")
            print(f"aws.govcloud.service.status:{value}|g|#service:{slug},status:{status},message:{clean_message}", flush=True)
 
 
if __name__ == "__main__":
    main()