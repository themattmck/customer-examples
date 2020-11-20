from datadog_checks.base import AgentCheck
from datetime import datetime, timedelta
import requests
__version__ = "1.0.0"

class SFDCLogs(AgentCheck):
    def check(self, instance):
        # Get one hour ago in UTC
        last_hour = datetime.utcnow() - timedelta(hours=1)
        # Format the time to YYYY-MM-DDTHH:00:00.00+0000
        formatted_date_string = last_hour.strftime("%Y-%m-%dT%H:00:00.000+0000")

        # Format the URL based on the instance identifier and date
        sf_url = "https://{}/services/data/v48.0/query".format(instance["url"])
        query = {"q": "SELECT+Id,EventType,LogDate,CreatedDate+FROM+EventLogFile+WHERE+CreatedDate>={}+AND+Interval='Hourly'+ORDER+BY+CreatedDate+LIMIT+1000".format(formatted_date_string)}
        sf_request = requests.get(url=sf_url, params=query, auth=(instance["username"], instance["password"]), headers=[])
        print(sf_request.status_code)
        sf_logs = sf_request.json()["records"]
        dd_headers = {
            "DD-API-KEY": instance["api-key"],
            "Content-Type": "application/json"
        }
        dd_url = "https://http-intake.logs.datadoghq.com/v1/input"
        for log in sf_logs:
            log["ddsource"]=instance["source"]
            log["service"]=instance["service"]
            log["ddtags"]="env:{}".format(instance["env"])
            log["timestamp"]=log["LogDate"].split("+")[0]
            r = requests.post(url=dd_url,headers=dd_headers,json=log)
            print(r.status_code)
            print(log)
