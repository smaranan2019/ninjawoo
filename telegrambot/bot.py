from operator import index
import os #h
from flask import Flask, request #h

from datetime import datetime, timedelta

import telebot
from telebot import types

import mysql.connector

cnx = mysql.connector.connect(user='b2514fae4958b8', password='16a5852e',
                              host='us-cdbr-east-05.cleardb.net',
                              database='heroku_6d3166f8ecfc76d')

cursor = cnx.cursor()

    
def check_connect():
    if cnx.is_connected():
        return True
    else:
        return False

'''
mysql://b2514fae4958b8:16a5852e@us-cdbr-east-05.cleardb.net/heroku_6d3166f8ecfc76d?reconnect=true

username: b2514fae4958b8
password: 16a5852e
hostname: us-cdbr-east-05.cleardb.net
schema: heroku_6d3166f8ecfc76d

'''
TOKEN = '5112479899:AAEiY7FnX9MQ5HDyZ54NjemgqGXz1Fkxa0w' #ninjavan_jolibeeee_bot

bot = telebot.TeleBot(token=TOKEN)

server = Flask(__name__) #h

@bot.message_handler(commands=['start', 'newdelay']) #answer if command is start
def send_welcome(message):
    userfirstname = message.chat.first_name

    ### connect to db
    cnx = mysql.connector.connect(user='b2514fae4958b8', password='16a5852e',
                                    host='us-cdbr-east-05.cleardb.net',
                                    database='heroku_6d3166f8ecfc76d')



    cursor = cnx.cursor()
    ### finish connecting to db


    #error handling
    user_telegram_handle = message.from_user.username #string
    date_message = message.date #class: integer 
    datetime_user = datetime.fromtimestamp(date_message) + timedelta(hours=8) #SG time is 8 hours faster than UTC (telegram time)
    error_date = datetime_user.strftime('%d %b %Y, %H:%M:%S')
    error = 'New user @{} started the bot on {}.'.format(user_telegram_handle, error_date)
    print(error) #end of error handling

    ### query database to see if user exists (based on telehandle)
    cursor.execute("SELECT * FROM heroku_6d3166f8ecfc76d.driver WHERE driver_tele_handle = '{}'".format(user_telegram_handle))
    row = cursor.fetchone()
    print("PROCESS: query database to see if user exists (based on telehandle)")

    cursor.close()
    cnx.close()

    
    if row is not None:
        print("user reported delay before")
        
        ### SCENARIO 1: if user is reporting 2nd/subsequent driver delay (tele handle is populated in database)
        # return message asking for driver's remark in 1 message
        bot.send_message(message.chat.id, 'Please explain delivery delay.')
        bot.send_message(message.chat.id, 'Limit your problem to 1 message.')


    else:
        print("user is reporting 1st delay")
        ### SCENARIO 2: if user is reporting 1st driver delay (tele handle is not populated)
        # 1) return greeting message and introduce bot and its purpose
        bot.reply_to(message, 'Hello ' + userfirstname + '.\nThis is Ninja Driver bot speaking who will assist you in reporting your delivery delays. ' + u"\U0001F970")
        # 2) return message asking for user's mobile number
        bot.send_message(message.chat.id, 'Please provide your mobile number.')



@bot.message_handler(regexp="Estimated Delay") #will answer when user's input contains Estimated Delay (aka when user submits an Estimated Delay)
def handle_ED(message):
    estimated_delay = message.text

    ### connect to db
    cnx = mysql.connector.connect(user='b2514fae4958b8', password='16a5852e',
                                    host='us-cdbr-east-05.cleardb.net',
                                    database='heroku_6d3166f8ecfc76d')



    cursor = cnx.cursor()
    ### finish connecting to db
     

    estimated_delay_list = estimated_delay.split("\n")
    print("estimated_delay_list:", estimated_delay_list) # see format of list
    ### sample: ['Estimated Delay', 'Day: 1', 'Hour: 2 ', 'Minute: 100']

    for i in range(1,4):
        index_start = estimated_delay_list[i].find(':')
        estimated_delay_list[i] = estimated_delay_list[i] = estimated_delay_list[i][index_start+1:].strip()

    day = int(estimated_delay_list[1])
    hour = int(estimated_delay_list[2])
    minute = int(estimated_delay_list[3])

    print("day: {}, hour: {}, minute: {}".format(day, hour, minute))

    # get problem statement from text file (Driver's Remark)
    user_telegram_handle = message.from_user.username #string

    with open(user_telegram_handle + ".txt",'r',encoding = 'utf-8') as f:
        list_all_lines = f.readlines()
    
    print("list_all_lines (from reading text file):", list_all_lines)
    # sample: ['Wife sick']
    remark_problem_description = list_all_lines[0]



    ### query database to get driver_id based on telegram handle
    cursor.execute("SELECT * FROM heroku_6d3166f8ecfc76d.driver WHERE driver_tele_handle = '{}'".format(user_telegram_handle))
    row = cursor.fetchone()
    print("PROCESS: query database to see if user exists (based on telehandle)")

    driver_id = int(row[0])   

    #remark_id, driver_id, remark_problem_description, estimated_delay_day, estimated_delay_hour, estimated_delay_minute, remark_date_created, remark_date_modified

    
    # insert into database 
    ### - Driver's Remark
    ### - Delay Day
    ### - Delay Hour
    ### - Delay Minute
    ### - Driver Id (from another table)

    cursor.execute("INSERT INTO heroku_6d3166f8ecfc76d.remarks(driver_id, remark_problem_description, estimated_delay_day, estimated_delay_hour, estimated_delay_minute) VALUES({}, '{}', {}, {}, {}) ".format(driver_id, remark_problem_description, day, hour, minute))
    cnx.commit()
    
    cursor.close()
    cnx.close()



    bot.send_message(message.chat.id, u"Thank you, your delivery delay has been recorded. Better luck in your subsequent deliveries! \U0001F697")




@bot.message_handler(regexp= u"Yes \U0001F31A") #will answer if Yes
def handle_yes(message):
    markup = types.ReplyKeyboardRemove() #remove custom keyboard created from asking if user can estimate delay time
    
    bot.reply_to(message, "State estimated delay time in the following format:", reply_markup=markup)    
    bot.send_message(message.chat.id, "Estimated Delay\nDay:\nHour:\nMinute:\n")




@bot.message_handler(regexp= u"No \U0001f97a") #will answer if No
def handle_no(message):

    ### connect to db
    cnx = mysql.connector.connect(user='b2514fae4958b8', password='16a5852e',
                                    host='us-cdbr-east-05.cleardb.net',
                                    database='heroku_6d3166f8ecfc76d')



    cursor = cnx.cursor()
    ### finish connecting to db


    markup = types.ReplyKeyboardRemove() #remove custom keyboard created from asking if user cannot estimate delay time
    
    # get problem statement from text file (Driver's Remark)
    user_telegram_handle = message.from_user.username #string

    with open(user_telegram_handle + ".txt",'r',encoding = 'utf-8') as f:
        list_all_lines = f.readlines()
    
    print("list_all_lines (from reading text file):", list_all_lines)
    # sample: ['Wife sick']
    remark_problem_description = list_all_lines[0]

    

    ### query database to get driver_id based on telegram handle
    cursor.execute("SELECT * FROM heroku_6d3166f8ecfc76d.driver WHERE driver_tele_handle = '{}'".format(user_telegram_handle))
    row = cursor.fetchone()
    print("PROCESS: query database to see if user exists (based on telehandle)")

    driver_id = int(row[0])   


    # insert into database 
    ### - Driver's Remark
    ### - Delay Day = -1
    ### - Delay Hour = -1
    ### - Delay Minute = -1
    ### - Driver Id (from another table)


    
    cursor.execute("INSERT INTO heroku_6d3166f8ecfc76d.remarks(driver_id, remark_problem_description, estimated_delay_day, estimated_delay_hour, estimated_delay_minute) VALUES({}, '{}', {}, {}, {}) ".format(driver_id, remark_problem_description, -1, -1, -1))
    cnx.commit()
    
    cursor.close()
    cnx.close()



    bot.send_message(message.chat.id, u"Thank you, your delivery delay has been recorded. Better luck in your subsequent deliveries! \U0001F697")


@bot.message_handler(func=lambda m: True)
def get_mobilenumber_or_problem(message):
    ### connect to db
    cnx = mysql.connector.connect(user='b2514fae4958b8', password='16a5852e',
                                    host='us-cdbr-east-05.cleardb.net',
                                    database='heroku_6d3166f8ecfc76d')



    cursor = cnx.cursor()
    ### finish connecting to db

     
    user_input = message.text

    #error handling
    date_message = message.date #class: integer 
    datetime_user = datetime.fromtimestamp(date_message) + timedelta(hours=8) #SG time is 8 hours faster than UTC (telegram time)
    error_date = datetime_user.strftime('%d %b %Y, %H:%M:%S')
    error = 'User @{} gave input "{}" on {}.'.format(message.from_user.username, user_input, error_date)
    print(error) #end of error handling

    user_telegram_handle = message.from_user.username #string

    if user_input.isdigit(): #if receive numbers only (assume: user's mobile number)
        print("User @{} provided mobile number.".format(message.from_user.username))
        
        # user is reporting 1st delay and asked to give mobile number
        # query database based on user's mobile number
        # update user's tele handle in database

        number = int(user_input) # convert from str to int
        cursor.execute("UPDATE heroku_6d3166f8ecfc76d.driver SET driver_tele_handle = '{}' WHERE driver_hp = {}".format(user_telegram_handle, number))
        cnx.commit()

        cursor.close()
        cnx.close()


        # return message asking for driver's remark in 1 message
        bot.send_message(message.chat.id, 'Please explain delivery delay.')
        bot.send_message(message.chat.id, 'Limit your problem to 1 message.')

    
    else: # assume: get problem/driver's remark
        # store problem into text file (to be inserted into database with estimated delay later)
        cursor.close()
        cnx.close()



        with open (user_telegram_handle + ".txt", "w", encoding = 'utf-8') as f: #ashley lau feedback, 25 dec 2020: instead of using file to store user data, can CONSIDER cloud relational database
            f.write(user_input) #IF file does not exist, will create a new file. IF file exists, will write over old file with new user_input


        # return message asking user if user can estimate delay time
        # limit user input to Yes or No

        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard=True)
        buttonyes = types.KeyboardButton(u"Yes \U0001F31A")
        buttonno = types.KeyboardButton(u"No \U0001f97a")

        markup.row(buttonyes, buttonno)

        bot.reply_to(message, "Can you estimate delay time?", reply_markup=markup)



#h (from here onwards)
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ninjavan-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))