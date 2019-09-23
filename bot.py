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

# ================================================MAIN===========================================================================
if __name__ == "__main__":
    bot.run()