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

        # Create a node - `phone` and store `username` & 'total_attempt' to "user" key in REDIS DB. This is bcoz in botogram, can't set global_variable.
        r.hset(phoneno, "user", json.dumps(dict(
            username= message.sender.username, 
            total_attempt=0)))
        # Create a node - `phone` and store nested dicts:`correct` & 'incorrect' and 'score' keys in REDIS DB. This is bcoz in botogram, can't set global_variable.
        r.hset(phoneno, "correct", json.dumps(dict(count= 0)))
        r.hset(phoneno, "incorrect", json.dumps(dict(count= 0)))
        r.hset(phoneno, "score", 0)

        # find the root phoneno. if username is available in REDIS DB
        key_phone = ""
        keys_list = r.keys()
        keys_list.remove(b'quiz')   # list of users (with phone nos.)
        for k in keys_list:
            # chat.send(k.decode('utf-8'))
            dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "user"))
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
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    keys_list = r.keys()
    keys_list.remove(b'quiz')   # list of users (with phone nos.)
    for k in keys_list:
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "user"))
        if dict_nested2_val2['username'] == message.sender.username:
            key_phone = k.decode('utf-8')


    if key_phone != "":
        total_attempt = json.loads(r.hget(key_phone, "user"))['total_attempt']       # -1 indicates 'no quiz played'
        curr_ques_no = total_attempt + 1

        if curr_ques_no >= 0 and curr_ques_no <= 9:   # from 0 to 9
            btns = botogram.Buttons()
            
            btns[0].callback("A - {option_a}".format(option_a= json.loads(r.hget("quiz", str(curr_ques_no)))['a']), "option_a")     # button - Option A
            btns[1].callback("B - {option_b}".format(option_b= json.loads(r.hget("quiz", str(curr_ques_no)))['b']), "option_b")     # button - Option B
            btns[2].callback("C - {option_c}".format(option_c= json.loads(r.hget("quiz", str(curr_ques_no)))['c']), "option_c")     # button - Option C
            btns[3].callback("D - {option_d}".format(option_d= json.loads(r.hget("quiz", str(curr_ques_no)))['d']), "option_d")     # button - Option D

            chat.send(json.loads(r.hget("quiz", str(curr_ques_no)))['que'], attach= btns)
        else:
             # TODO: set the curr_ques_no to zero
             chat.send('Invalid Question no.') 
    else:
        chat.send("Please, share the phone no. first via /sharephone")

# ================================================Option button callbacks===========================================================================
@bot.callback("option_a")
def option_a_callback(query, chat, message):
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    keys_list = r.keys()
    keys_list.remove(b'quiz')   # list of users (with phone nos.)
    for k in keys_list:
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "user"))
        if dict_nested2_val2['username'] == query.sender.username:
            key_phone = k.decode('utf-8')

    if key_phone != "":
        total_attempt = json.loads(r.hget(key_phone, "user"))['total_attempt']

        # Increase the total_attempt
        curr_ques_no = total_attempt + 1
        curr_ques_ans = json.loads(r.hget("quiz", str(curr_ques_no)))['ans']
        curr_ques_ans_initial = curr_ques_ans[0]

        correct_count = json.loads(r.hget(key_phone, "correct"))['count']
        incorrect_count = json.loads(r.hget(key_phone, "incorrect"))['count']
        score = json.loads(r.hget(key_phone, "score"))

        
        # check if ans is correct or not
        if curr_ques_ans_initial == 'A':
            correct_count = correct_count + 1
            r.hset(key_phone, "correct", json.dumps(dict(count= correct_count)))
            chat.send("Good! correct answer.")
        else:
            incorrect_count = incorrect_count + 1
            r.hset(key_phone, "incorrect", json.dumps(dict(count= incorrect_count)))
            chat.send("Sorry! the correct answer is: {0}".format(curr_ques_ans))

        # update the score
        if (correct_count + incorrect_count) != 0:
            score = correct_count + incorrect_count

        r.hset(key_phone, "score", score)
        r.hset(key_phone, "user", json.dumps(dict(username= query.sender.username, total_attempt= total_attempt + 1)))
        chat.send('Play more via /play')

    else:
        chat.send("Please, share the phone no. first via /sharephone")

@bot.callback("option_b")
def option_b_callback(query, chat, message):
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    keys_list = r.keys()
    keys_list.remove(b'quiz')   # list of users (with phone nos.)
    for k in keys_list:
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "user"))
        if dict_nested2_val2['username'] == query.sender.username:
            key_phone = k.decode('utf-8')

    if key_phone != "":
        total_attempt = json.loads(r.hget(key_phone, "user"))['total_attempt']

        # Increase the total_attempt
        curr_ques_no = total_attempt + 1
        curr_ques_ans = json.loads(r.hget("quiz", str(curr_ques_no)))['ans']
        curr_ques_ans_initial = curr_ques_ans[0]

        correct_count = json.loads(r.hget(key_phone, "correct"))['count']
        incorrect_count = json.loads(r.hget(key_phone, "incorrect"))['count']
        score = json.loads(r.hget(key_phone, "score"))

        
        # check if ans is correct or not
        if curr_ques_ans_initial == 'B':
            correct_count = correct_count + 1
            r.hset(key_phone, "correct", json.dumps(dict(count= correct_count)))
            chat.send("Good! correct answer.")
        else:
            incorrect_count = incorrect_count + 1
            r.hset(key_phone, "incorrect", json.dumps(dict(count= incorrect_count)))
            chat.send("Sorry! the correct answer is: {0}".format(curr_ques_ans))

        # update the score
        if (correct_count + incorrect_count) != 0:
            score = (correct_count/(correct_count + incorrect_count)) * 100

        r.hset(key_phone, "score", score)
        r.hset(key_phone, "user", json.dumps(dict(username= query.sender.username, total_attempt= total_attempt + 1)))
        chat.send('Play more via /play')

    else:
        chat.send("Please, share the phone no. first via /sharephone")

@bot.callback("option_c")
def option_c_callback(query, chat, message):
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    keys_list = r.keys()
    keys_list.remove(b'quiz')   # list of users (with phone nos.)
    for k in keys_list:
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "user"))
        if dict_nested2_val2['username'] == query.sender.username:
            key_phone = k.decode('utf-8')

    if key_phone != "":
        total_attempt = json.loads(r.hget(key_phone, "user"))['total_attempt']

        # Increase the total_attempt
        curr_ques_no = total_attempt + 1
        curr_ques_ans = json.loads(r.hget("quiz", str(curr_ques_no)))['ans']
        curr_ques_ans_initial = curr_ques_ans[0]

        correct_count = json.loads(r.hget(key_phone, "correct"))['count']
        incorrect_count = json.loads(r.hget(key_phone, "incorrect"))['count']
        score = json.loads(r.hget(key_phone, "score"))

        
        # check if ans is correct or not
        if curr_ques_ans_initial == 'C':
            correct_count = correct_count + 1
            r.hset(key_phone, "correct", json.dumps(dict(count= correct_count)))
            chat.send("Good! correct answer.")
        else:
            incorrect_count = incorrect_count + 1
            r.hset(key_phone, "incorrect", json.dumps(dict(count= incorrect_count)))
            chat.send("Sorry! the correct answer is: {0}".format(curr_ques_ans))

        # update the score
        if (correct_count + incorrect_count) != 0:
            score = correct_count + incorrect_count

        r.hset(key_phone, "score", score)
        r.hset(key_phone, "user", json.dumps(dict(username= query.sender.username, total_attempt= total_attempt + 1)))
        chat.send('Play more via /play')

    else:
        chat.send("Please, share the phone no. first via /sharephone")

@bot.callback("option_d")
def option_d_callback(query, chat, message):
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    keys_list = r.keys()
    keys_list.remove(b'quiz')   # list of users (with phone nos.)
    for k in keys_list:
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "user"))
        if dict_nested2_val2['username'] == query.sender.username:
            key_phone = k.decode('utf-8')

    if key_phone != "":
        total_attempt = json.loads(r.hget(key_phone, "user"))['total_attempt']

        # Increase the total_attempt
        curr_ques_no = total_attempt + 1
        curr_ques_ans = json.loads(r.hget("quiz", str(curr_ques_no)))['ans']
        curr_ques_ans_initial = curr_ques_ans[0]

        correct_count = json.loads(r.hget(key_phone, "correct"))['count']
        incorrect_count = json.loads(r.hget(key_phone, "incorrect"))['count']
        score = json.loads(r.hget(key_phone, "score"))

        
        # check if ans is correct or not
        if curr_ques_ans_initial == 'D':
            correct_count = correct_count + 1
            r.hset(key_phone, "correct", json.dumps(dict(count= correct_count)))
            chat.send("Good! correct answer.")
        else:
            incorrect_count = incorrect_count + 1
            r.hset(key_phone, "incorrect", json.dumps(dict(count= incorrect_count)))
            chat.send("Sorry! the correct answer is: {0}".format(curr_ques_ans))

        # update the score
        if (correct_count + incorrect_count) != 0:
            score = correct_count + incorrect_count

        r.hset(key_phone, "score", score)
        r.hset(key_phone, "user", json.dumps(dict(username= query.sender.username, total_attempt= total_attempt + 1)))
        chat.send('Play more via /play')

    else:
        chat.send("Please, share the phone no. first via /sharephone")

# ===================================================Stats command=================================================================
@bot.command("stats")
def stats_command(chat, message, args):
    """Check the score of the quiz so far"""
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    keys_list = r.keys()
    keys_list.remove(b'quiz')   # list of users (with phone nos.)
    for k in keys_list:
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.hget(k.decode('utf-8'), "user"))
        if dict_nested2_val2['username'] == message.sender.username:
            key_phone = k.decode('utf-8')


    if key_phone != "":
        # define the vars: score, total_attempt, correct, incorrect
        score = json.loads(r.hget(key_phone, "score"))
        total_attempt = json.loads(r.hget(key_phone, "user"))['total_attempt']
        correct = json.loads(r.hget(key_phone, "correct"))['count']
        incorrect = json.loads(r.hget(key_phone, "incorrect"))['count']

        chat.send('The score of the quiz so far is:\nScore: {0} % \nTotal attempts: {1} \nCorrect: {2}, \nIncorrect: {3}'.format(
            score,
            total_attempt,
            correct,
            incorrect))
    else:
        chat.send("Please, share the phone no. first via /sharephone")

# ================================================MAIN===========================================================================
if __name__ == "__main__":
    bot.run()