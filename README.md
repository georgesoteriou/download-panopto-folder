# Download Panopto folders

## SETUP
1. Go to panopto and login with your imperial account
2. Open your cookies and copy them in the code you need both Panopto and imperial cookies:
   
    ```
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
    ```
3. Go to the folder in panopto and get folder id from URL:
     - Example: DoC folder is `https://imperial.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID="e2584204-079a-46ea-922a-908294c29ad4"`
     - You want this: `e2584204-079a-46ea-922a-908294c29ad4`


## RUN 

```
cd folder_to_save_results
python download_panopto_folder_videos.py <folder_ID>
```