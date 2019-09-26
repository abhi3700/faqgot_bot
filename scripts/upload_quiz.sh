python ../app/upload_quiz.py

# ==============================PAUSE=============================================
#init
function pause() {
    read -p "$*"
}

#....
# call it
printf '\n'		# newline
pause 'Press [Enter] key to continue...'
# rest of the script