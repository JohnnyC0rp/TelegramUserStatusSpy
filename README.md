# Telegram users status spy
This python script uses pyrogram to login to your account and monitor all satus changes of people you have ever chat
It connects to 2 accounts: 
- 1 Spy(main) - this account will be monitoring changes
- 2 Informator(second) - this account will be sending you gathered information

To connect api keys, create **api_info.py**:
~~~ python 
api_id = ""
api_hash = ""

informer_api_id = ""
informer_api_hash = ""

main_acc_username = ""

restricted_usernames = ["", "", ""]

~~~ 

Fill this file with your data, restricted usernames will not be tracked, put there usernames of all your accounts
