Collection of scripts to generate high level metrics on uptime/availability of AWS.

NO AUTH REQUIRED

aws_health_check.py:
This script iterates through a subset of AWS services in the public GovCloud Health Status dashboard.
The script returns status based on RSS feed response, then formats as a metric data point for Splunk ingest.

aws_dns_check.py:
Checks DNS resolution (not connectivity) for static list of AWS endpoints from the host running this script, emitting per-endpoint success/failure and resolver latency as metrics on stdout.

Reflects only the local resolver's path to AWS's public DNS (not AWS's DNS health globally). It does not verify port/service reachability & no explicit timeout, so hung lookups won't register as failures.

Requires a downstream collector (Splunk Universal Forwarder) to route metrics into Splunk or another metrics store — this script does not transmit data itself. Built for a scripted input on a splunk forwarder, to log to a metrics based index.