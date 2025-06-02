import asyncio
import re
from telethon import TelegramClient as xgv, events, Button
from telethon.sessions import StringSession as s
from pyrogram import Client as S
from pyrogram.errors import SessionPasswordNeeded as needpass, BadRequest, Unauthorized
from session_converter import SessionManager as ses_mng

apd = 8138160
aph = '1ad2dae5b9fddc7fe7bfee2db9d54ff2'
token = 'توكن بوتك'
Hemo = xgv('cnv', apd, aph)


async def chk_T(ses: str) -> bool:
    try:
        async with xgv(s(ses), apd, aph) as x:  
            await x.connect()
            return await x.is_user_authorized()
    except (ValueError, Exception):
        return False


async def chk_P(ses: str) -> bool:
    client = S("session", api_id=apd, api_hash=aph, session_string=ses, in_memory=True)
    try:
        await client.connect()
        valid = client.is_connected
        await client.disconnect()
        return valid
    except (BadRequest, Unauthorized, needpass, ValueError):
        try:
            await client.disconnect()
        except:
            pass
        return False
    except:
        try:
            await client.disconnect()
        except:
            pass
        return False

        
        
@Hemo.on(events.NewMessage(pattern="/start", func=lambda x: x.is_private))
async def start_CMD(event):
    await event.respond(
        "**• Welcome Boss 😎 \n• i'm string session Convertor 🗳\n\u200f\n• Terminal’s open - drop your commands ⚙**",
        buttons=[
            [
                Button.inline('Telethon → Pyrogram', b'T2P'),
                Button.inline('Pyrogram → Telethon', b'P2T')
            ]
        ]
    )

@Hemo.on(events.CallbackQuery(data=re.compile(b"T2P")))
async def t2p(event):
    await event.answer()
    
    i = event.chat_id        
    try:
        async with Hemo.conversation(i, timeout=300) as conv:
            await conv.send_message("**• دز جلسـة Telethon حـب **🔖")
            res = await conv.get_response()
            
            if not await chk_T(res.text):
                return await conv.send_message('**• جلسة تالفة مـع الاسـف 📂️**')
            
            mng = ses_mng.from_telethon_string_session(res.text)
            Done = mng.pyrogram_string_session(api_id=apd)
            await conv.send_message(f'› تـم التحـويـل, جلسـة PYROGRAM ☑️\n\n`{Done}`', parse_mode='markdown')
    except asyncio.TimeoutError:
        await event.respond("**• خلـص الوقـت لازم تعيـد ⌛️**")
    except Exception as e:
        await event.respond(f"**• اووبـس فيـه مشكله **❗️\n {e}")

@Hemo.on(events.CallbackQuery(data=re.compile(b"P2T")))
async def p2t(event):
    await event.answer()    
    
    i = event.chat_id    
    try:
        async with Hemo.conversation(i, timeout=300) as conv:
            await conv.send_message("**• دز جلسـة Pyrogram حـب **⚙")
            res = await conv.get_response()
            
            if not await chk_P(res.text):
                return await conv.send_message('**• جلسة تالفة مـع الاسـف 📂️**')
            
            mng = ses_mng.from_pyrogram_string_session(res.text)
            Done = mng.telethon_string_session()
            await conv.send_message(f'› تـم التحـويـل, جلسـة TELETHON ☑️\n\n`{Done}`', parse_mode='markdown')
    except asyncio.TimeoutError:
        await event.respond("**• خلـص الوقـت لازم تعيـد ⌛️**")
    except Exception as e:
        await event.respond(f"**• اووبـس فيـه مشكله **❗️\n {e}")


async def Root():
    print('Zero errors, full power 🐾...')
    await Hemo.start(bot_token=token)
    await Hemo.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(Root())
    except KeyboardInterrupt:
        pass 