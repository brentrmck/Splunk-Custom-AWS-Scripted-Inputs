import socket
import time

ENDPOINTS = [
	"ec2.us-east-1.amazonaws.com",
	"ec2.us-west-2.amazonaws.com",
	"s3.us-east-1.amazonaws.com",
	"s3.us-west-2.amazonaws.com"
]

for endpoint in ENDPOINTS:
	start = time.time()
	try:
		socket.getaddrinfo(endpoint, 443, proto=socket.IPPROTO_TCP)
		latency_ms = round((time.time() - start) * 1000,2)
		success = 1.0
	except socket.gaierror:
		latency_ms = 0.0
		success = 0.0

	print(f"aws.dns.success:{success}|g|#dns_endpoint:{endpoint}")
	print(f"aws.dns.latency_ms:{latency_ms}|g|#dns_endpoint:{endpoint}")