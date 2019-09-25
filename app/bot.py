import botogram
import redis
import json

from input import *


# -------------------------------------------------------About Bot--------------------------------------------------------------------
bot = botogram.create(API_key)
bot.about = "This is a GOT FAQ Bot."
bot.owner = "@abhi3700"

# -------------------------------------------------------Redis DB------------------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

# =======================================================Share phone via keyboard===========================================================================
@bot.command("sharephone")
def sharephone_command(chat, message, args):
    """Share your phone no. via clicking the keyboard below."""    
    bot.api.call('sendMessage', {
        'chat_id': chat.id,
        'text': 'Please click on \'Phone no.\' button below to share your phone no.',
        'reply_markup': json.dumps({
            'keyboard': [
                [
                    {
                        'text': 'Phone no.',
                        'request_contact': True,
                    },
                ],
            ],
            # These 3 parameters below are optional
            # See https://core.telegram.org/bots/api#replykeyboardmarkup
            'resize_keyboard': True,
            'one_time_keyboard': True,
            'selective': True,
        }),
    })

# =======================================================Process messages===========================================================================
@bot.process_message
def button_messages_are_like_normal_messages(chat, message):
    if message.contact:
        phoneno = message.contact.phone_number
        phoneno = phoneno.replace("+", "")      # '+91343242343' --> '91343242343'Unlike phone app, in Telegram desktop app, it's '+' sign in phone no.

        # Create a node - `phone` and store `username` in REDIS DB. This is bcoz in botogram, can't set global_variable.
        r.set(phoneno, json.dumps(dict(
            username= message.sender.username, 
            correct_count=0, 
            incorrect_count=0, 
            total_attempt=0, 
            score=0)))

        # find the root phoneno. if username is available in REDIS DB
        key_phone = ""
        keys_list = r.keys()
        keys_list.remove(b'quiz')   # list of users (with phone nos.)
        for k in keys_list:
            # chat.send(k.decode('utf-8'))
            dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
            if dict_nested2_val2['username'] == message.sender.username:
                key_phone = k.decode('utf-8')

        chat.send('You choose to send your contact no.: \'{phone}\''.format(phone= key_phone))
        chat.send("Now, you can play quiz via /play command.\nPress /removekeyboard to remove the annoying keyboard")

# ===================================================remove keyboard(s)=================================================================
@bot.command("removekeyboard")
def removekeyboard_command(chat, message):
    """removes the keyboard appearing below"""
    bot.api.call('sendMessage', {
        'chat_id': chat.id,
        'reply_to_message': message.id,
        'text': 'keyboards removed.',
        'reply_markup': json.dumps({
            'remove_keyboard': True,
            # This 1 parameter below is optional
            # See https://core.telegram.org/bots/api#replykeyboardremove
            'selective': True,
        })
    })

# ===================================================Play command=================================================================
@bot.command("play")
def show_command(chat, message, args):
    """Play quiz on \"Game of Thrones (GOT)\" TV series"""
    key_phone = ""
    keys_list = r.keys()
    keys_list.remove(b'quiz')   # list of users (with phone nos.)
    for k in keys_list:
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
        if dict_nested2_val2['username'] == message.sender.username:
            key_phone = k.decode('utf-8')

    if key_phone != "":
        total_attempt = json.loads(r.get(key_phone))['total_attempt']
        if total_attempt < 10:
            curr_ques_no = total_attempt + 1 
            chat.send(json.loads(r.hget("quiz", str(curr_ques_no)))['que'])

        else:
             # set the total_attempt to zero 
    else:
        chat.send("Please, share the phone no. first via /sharephone")

# ================================================MAIN===========================================================================
if __name__ == "__main__":
    bot.run()