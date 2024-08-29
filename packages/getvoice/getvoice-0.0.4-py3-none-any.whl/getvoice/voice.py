from gtts import gTTS
async def voice():
    c = client
    m = message    
    Language= "hi"
    name = await client.ask(message.chat.id, text="text_to_speech")
    Text = f"{name.text}"
    speech = gTTS(text = Text , lang = Language, slow = False)
    speech.save("q.mp3")
    await message.reply_audio("q.mp3")
