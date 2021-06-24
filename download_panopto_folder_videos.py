import requests
import sys
import json
import re
from tqdm import tqdm

if len(sys.argv) != 2:
    print("Please give one folder ID")
    exit()

# COPY YOUR IMPERIAL LOGIN COOKIE HERE:
cookies = {
    '_ga': '<FILL THIS>',
    '_gid': '<FILL THIS>',
    '.ASPXAUTH': '<FILL THIS>',
    'UserSettings': '<FILL THIS>',
    'ic.ac.uk\\<USERNAME>': '<FILL THIS>',
    'sandboxCookie': '<FILL THIS>',
    'csrfToken': '<FILL THIS>',
    '_gat': '<FILL THIS>',
    '_gat_customerTracker': '<FILL THIS>',
}

headers = {
    'authority': 'imperial.cloud.panopto.eu',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'content-type': 'application/json; charset=UTF-8',
    'accept': '*/*',
    'origin': 'https://imperial.cloud.panopto.eu',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://imperial.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx',
    'accept-language': 'en-US,en;q=0.9,el;q=0.8,ko;q=0.7,fr;q=0.6',
}

data = {'queryParameters': {'query': None, 'sortColumn': 1, 'sortAscending': False, 'maxResults': 50, 'page': 0, 'startDate': None, 'endDate': None,
                            'folderID': str(sys.argv[1]), 'bookmarked': False, 'getFolderData': True, 'isSharedWithMe': False, 'isSubscriptionsPage': False, 'includePlaylists': True}}

response = requests.post('https://imperial.cloud.panopto.eu/Panopto/Services/Data.svc/GetSessions',
                         headers=headers, cookies=cookies, data=json.dumps(data))

out = json.loads(response.text)


ids = [re.findall("id=.*", o['ViewerUrl'])[0][3:] for o in out['d']['Results']]

# print(ids)

for id in tqdm(ids):
    headers = {
        'authority': 'imperial.cloud.panopto.eu',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': f"https://imperial.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id={id}",
        'accept-language': 'en-US,en;q=0.9,el;q=0.8,ko;q=0.7,fr;q=0.6',
    }

    params = (
        ('mediaTargetType', 'videoPodcast'),
    )

    with requests.get(f"https://imperial.cloud.panopto.eu/Panopto/Podcast/Download/{id}.mp4", headers=headers, params=params, cookies=cookies, stream=True) as r:
        r.raise_for_status()
        name = r.headers['Content-Disposition'][21:-1]
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB', unit_scale=True, leave=False)
        progress_bar.set_description(name)
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
