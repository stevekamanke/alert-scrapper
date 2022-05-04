import csv
import json
import os


# Extract alert from panel p within dashboard d
def extract_alert(p: dict, d: str):
    alert = {
        'name': p['alert']['name'],
        'description': p['alert']['message'] if p['alert'].get("message") is not None else '',
        'panel': p['title'],
        'dashboard': d,
        'notifications': p['alert']['notifications']
    }

    # for notification in p['alert']['notifications']:
    #     alert['notifications'].append(notification['uid'])

    return alert


# Get all alerts from dashboard
def load_alerts(root_dir: str, dashboards: list):
    alerts = []

    for dashboard in dashboards:
        with open(f"{root_dir}/{dashboard}") as json_file:
            data = json.load(json_file)
            # Dashboard Panels
            panels = data['panels']

            for panel in panels:
                if "alert" in panel.keys():
                    alerts.append(extract_alert(panel, dashboard))

    return alerts


if __name__ == "__main__":
    # root = input('Enter absolute path to Grafana root directory\n'
    #              'e.g. "/Users/stevekamanke/workspace/superbalist/grafana.office.ohsuper.com"\n\n')

    # path = root + '/src/dashboards'
    results = {}
    path = "/Users/stevekamanke/workspace/superbalist/grafana.office.ohsuper.com/src/dashboards"

    # print(load_alerts())
    for (root, dirs, files) in os.walk(path, topdown=True):
        if files:
            results[os.path.basename(root)] = load_alerts(root, files)

    with open('alerts_scrapper.csv', mode='w') as scrapper_csv:
        fieldnames = ['name', 'description', 'panel', 'dashboard']
        writer = csv.DictWriter(scrapper_csv, fieldnames=fieldnames)
        writer.writeheader()

        # print(type(results))

        for v in results.values():
            for a in v:
                writer.writerow({key: value for key, value in a.items() if key != "notifications"})
