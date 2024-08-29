from gtts import gTTS

from pyrogram import Client

from pyrogram.types import Message

async def voice(c: Client, m: Message):    
    Language= "hi"
    name = await client.ask(message.chat.id, text="text_to_speech")
    Text = f"{name.text}"
    speech = gTTS(text = Text , lang = Language, slow = False)
    speech.save("q.mp3")
    await m.reply_audio("q.mp3")
