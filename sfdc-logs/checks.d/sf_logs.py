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
        base_url = "https://{}".format(instance["url"])
        sf_url = "{}{}".format(base_url, "asdf")
        query = {"q": "SELECT+Id,EventType,LogDate,CreatedDate+FROM+EventLogFile+WHERE+CreatedDate>={}+AND+Interval='Hourly'+ORDER+BY+CreatedDate+LIMIT+1000".format(formatted_date_string)}
        sf_request = requests.get(url=sf_url, params=query, auth=(instance["username"], instance["password"]), headers=[])
        print(sf_request.status_code)
        sf_logs = sf_request.json()["records"]
        for log in sf_logs:
            r = requests.get(url="http://winterolympicsmedals.com/medals.csv")
            with open("out.csv", 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            with open('out.csv', newline='\n') as csvfile:
                keys = []
                line_count = 0
                for row in csvfile:
                    if line_count == 0:
                        for key in row.split(","):
                            keys.append(key.strip("\n"))
                    else:
                        json_payload = {}
                        values = row.split(",")
                        for value in values:
                            json_payload[keys[values.index(value)]]=value.strip("\n")
                        print(json_payload)
                        with open('log.txt', 'a') as log_file:
                            log_file.write("{}\n".format(json_payload))
                    line_count += 1
