import smtplib
import ssl
import time
from datetime import datetime, timedelta

import pytz
import requests

print('Starting League of Legend Watchman')

sender_email = ''
password = ''
receiver_emails = ['']

message = """\
Subject: X has started a game

Hi my name is x and I have started a game of League of Legends"""

player_name = ''
region = 'euw'
port = 465

already_playing = False
number_of_games = 0
total_game_duration = 0
last_game_start_ts = None

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
    server.login(sender_email, password)

    while True:
        print('Checking for new games...')
        tz_LSB = pytz.timezone('Europe/Lisbon')
        current_time = datetime.now(tz_LSB)

        if 9 >= current_time.hour <= 18:
            response = requests.get(
                'https://{}.op.gg/summoner/ajax/spectateStatus/summonerName={}'.format(region, player_name))

            if 'status' in response.json():
                if not already_playing:
                    print("New Game Started")
                    number_of_games += 1
                    last_game_start_ts = current_time
                    for email in receiver_emails:
                        print('Sending email notification to ' + email)
                        message += '\n\nThis is my {}th game today\nTotal time wasted: {} minutes'.format(
                            number_of_games, total_game_duration)
                        server.sendmail(sender_email, email, message)

                    already_playing = True

            else:
                if already_playing:
                    total_game_duration = ((current_time - last_game_start_ts).total_seconds() / 60.0)
                    print('Game Finished')
                already_playing = False

            time.sleep(10)
        else:
            wakeup_time = (current_time + timedelta(days=1)).replace(hour=9, minute=0, second=0)
            print('Outside of work hours, sleeping until {}'.format(wakeup_time))
            time.sleep((wakeup_time - current_time).seconds)
            # Reset Vars
            already_playing = False
            number_of_games = 0
            total_game_duration = 0
            last_game_start_ts = None

