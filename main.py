import json
import sys
import argparse
import csv
import requests
import warnings

warnings.filterwarnings("ignore")

def main(args) -> int:
    """Echo CSV file with players stats."""
    headers = ['personId', 'licence', 'lastname', 'firstname', 'sex', 'simpleRate', 'simpleSubLevel', 'doubleRate', 'doubleSubLevel', 'mixteRate', 'mixteSubLevel', 'clubSimpleRank', 'clubMixteRank', 'clubDoubleRank']
    output = [','.join([str(elem) for elem in headers])]
    with open(args.filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            info = []
            licence_number = row[0]
            req = requests.get('https://myffbad.fr/api/person/' + licence_number + '/informationsLicence/undefined', verify=False, headers= {
                'referer': 'https://myffbad.fr/joueur/' + licence_number,
                'verify-token': '5dcc4eeb56f8e63a7d06d429ed077ff647ff0e5966f952ab5bc9764988837dfa.1667039942558',
                'caller-url': '/api/person/'
            })
            if req.status_code == 200:
                licence_info = json.loads(req.text)
                info.extend((licence_info['personId'], licence_info['licence'], licence_info['lastName'], licence_info['firstName'], licence_info['sex']))
                req2 = requests.get('https://myffbad.fr/api/person/' + str(licence_info['personId']) + '/rankings', verify=False, headers= {
                    'referer': 'https://myffbad.fr/joueur/' + licence_number,
                    'verify-token': '5dcc4eeb56f8e63a7d06d429ed077ff647ff0e5966f952ab5bc9764988837dfa.1667039942558',
                    'caller-url': '/api/person/'
                })
                if req2.status_code == 200 and len(req2.text) > 2:
                    ranking_info = json.loads(req2.text)
                    info.extend((ranking_info['simpleRate'], ranking_info['simpleSubLevel'], ranking_info['doubleRate'], ranking_info['doubleSubLevel'], ranking_info['mixteRate'], ranking_info['mixteSubLevel'], ranking_info['clubSimpleRank'], ranking_info['clubMixteRank'], ranking_info['clubDoubleRank']))
                
                output.append(','.join([str(elem) for elem in info]))
    
    for row in output:
        print(row)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch user stats from FFBAD website.')
    parser.add_argument('filename', help='input CSV file with licence number as first column')
    args = parser.parse_args()
    sys.exit(main(args))