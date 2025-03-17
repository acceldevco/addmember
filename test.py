from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel, InputPeerUser
from telethon.errors import PeerFloodError, UserPrivacyRestrictedError
import csv
import time
import os
import sys

# تنظیمات API تلگرام
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'

# لیست کاربران
users = []

# اتصال به تلگرام
client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# دریافت لیست کاربران از یک گروه یا کانال
async def get_users_from_group(group_entity):
    users = []
    async for user in client.iter_participants(group_entity):
        users.append({
            'username': user.username,
            'user_id': user.id,
            'access_hash': user.access_hash
        })
    return users

# اضافه کردن کاربران به گروه یا کانال هدف
async def add_users_to_group(target_group, users):
    n = 0
    added_users = []
    for user in users:
        n += 1
        added_users.append(user)
        if n % 50 == 0:
            print(f'{sleep}{g} Sleep 2 min to prevent possible account ban{rs}')
            time.sleep(120)
        try:
            if user['username'] == "":
                continue
            user_to_add = InputPeerUser(user['user_id'], user['access_hash'])
            await client(InviteToChannelRequest(target_group, [user_to_add]))
            usr_id = user['user_id']
            print(f'{attempt}{g} Adding {usr_id}{rs}')
            print(f'{sleep}{g} Sleep 30s{rs}')
            time.sleep(30)
        except PeerFloodError:
            os.system(f'del {file}')
            sys.exit(f'\n{error}{r} Aborted. Peer Flood Error{rs}')
        except UserPrivacyRestrictedError:
            print(f'{error}{r} User Privacy Restriction{rs}')
            continue
        except KeyboardInterrupt:
            print(f'{error}{r} Aborted. Keyboard Interrupt{rs}')
            update_list(users, added_users)
            if not len(users) == 0:
                print(f'{info}{g} Remaining users logged to {file}')
                logger = Relog(users, file)
                logger.start()
        except:
            print(f'{error}{r} Some Other error in adding{rs}')
            continue

# اجرای توابع
async def main():
    group_entity = await client.get_entity('SOURCE_GROUP_USERNAME_OR_ID')
    target_group = await client.get_entity('TARGET_GROUP_USERNAME_OR_ID')
    
    users = await get_users_from_group(group_entity)
    await add_users_to_group(target_group, users)

with client:
    client.loop.run_until_complete(main())
