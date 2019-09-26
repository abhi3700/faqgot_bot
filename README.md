# faqgot_bot
A FAQ bot on GOT TV series.

## Modules
### Quiz
* The quiz is on "Game Of Thrones (GOT)" TV Series.
* questions are numbered from `1` to `10`.
* `total_attempt` is set to `0`, which indicates that there has been no attempts so far.
* The entire stats of quiz is seen by `/stats` command.
* Upload the quiz by clicking on the script [upload_quiz.sh](./scripts/upload_quiz.sh) 

### Database
* shown in [redis_db.json](./redis_db.json)
* REDIS is chosen for:
	- fast processing of Quiz questions & answers
	- finding the `phone_no` of a known username (var available in all Botogram functions)
* 2 main root keys: `quiz` & `<contact_no>`
* Inside `<contact_no>` key, 4 sub_keys: `user`, `correct`, `incorrect`, `score`
* Inside `user` key, 2 key, value pairs: `username` & `total_attempt`
* Inside `correct` key, 1 key, value pair: `count`
* Inside `incorrect` key, 1 key, value pair: `count`
* Last, `score` key has value

> NOTE: `correct`, `incorrect`, `score` has been separated with individual keys as this needs to update independently as the quiz progress. 