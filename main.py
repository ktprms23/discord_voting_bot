import discord
import asyncio
import requests
import json
import configparser
import random

token = ''
registeredChannel = 0
serviceStart = False
votingEndTime = 0




commandList = [ '--help', '--start', '--vote' ]
commandDescription = ['I am a Vote Bot.\nMention me with --help for more info\nMention me with following commands for voting service:\n\t--start Target Option1-Option2-Option3_...-OptionN EndInMinutes \n\t--vote Option\t\t\t', ' ']


#service_task

vote_result = []
vote_result_count = []
vote_result_list = []

client = discord.Client()

def readConfigFile():

    global token

    configFile = configparser.ConfigParser()
    configFile.read('config.ini', encoding='utf-8')
    
    
    token = configFile['bot_config']['bot_token']

    print(token)

async def background_update_voting_result():

    global serviceStart
    global votingEndTime
    print('DEBUG, start process')
    await client.wait_until_ready()
    print('DEBUG, start process 1')


    print('DEBUG, start waiting {} minute'.format(int(votingEndTime)))
    await asyncio.sleep(int(votingEndTime)*60)
    print('DEBUG, start process 2')
    
    serviceStart = False
    
    maxResultIndex = 0
    maxResult = 0

    if len(vote_result_count) == 0:
        await registeredChannel.send('The vote is failed')
        return

    for c in range(1, len(vote_result_count)):
        if vote_result_count[c] > maxResult:
            maxResult = vote_result_count[c] 
            maxResultIndex = c

    
  
    await registeredChannel.send('The vote result is {}'.format(vote_result[maxResultIndex]))
    await registeredChannel.send('The vote result list is {}'.format(vote_result_list))



@client.event 
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(client.user)
    print('------')

@client.event
async def on_message(message):

    global serviceStart
    global registeredKeyword
    global registeredChannel
    global service_task
    global auto_response_list
    global votingEndTime
    #global commandList
    #global commandDescription

    print(message.author)
    print(message.content)

    if message.content == '':
        return

    # Voting Bot Command
    if any( client.user == mention for mention in message.mentions ):
        print(message.content)
        if message.content.find(commandList[0]) >= 0:
            
            await message.channel.send(commandDescription[0])

        elif message.content.find(commandList[1]) >= 0:
            if serviceStart == True:
                await message.channel.send('Vote has been already started.')
            else:
                serviceStart = True
                registeredChannel = message.channel
                split_voting_content = message.content.split(' ')
                votingEndTime = split_voting_content[4]
                _loop = asyncio.get_event_loop()
                service_task = _loop.create_task(background_update_voting_result())

                validOption = split_voting_content[3].split("-")

                await message.channel.send('Vote is starting.\nThe vote Target is {}\n And valid option are {} \nPlease mention me with --vote OptionNumber to vote.\nVote will be stopped in {} minutes.'.format( split_voting_content[2], validOption, split_voting_content[4]))
    
        elif message.content.find(commandList[2]) >= 0:
            if serviceStart == False:
                await message.channel.send('Vote has been already stopped.')
            else:
                '''
                service_task.cancel()
                try:
                    await service_task
                except asyncio.CancelledError:
                    print("on_message(): service_task is cancelled now")
                '''
                # --vote option
                split_voting_content = message.content.split(' ')

                if split_voting_content[2] in vote_result:
                    vote_result_count[vote_result.index(split_voting_content[2])] += 1
                    vote_result_list.append(split_voting_content[2]+"_"+str(message.author.name))
                else:
                    vote_result.append(split_voting_content[2])
                    vote_result_count.append(0) 
                    
                    vote_result_list.append(split_voting_content[2]+"_"+str(message.author.name))  
                
                

                await message.channel.send('{} vote {}'.format( str(message.author.name), split_voting_content[2]))  

def main():

    global service_task

    readConfigFile()
    if token == '':
        print( 'No bot token. Please check your config file.' )
        exit()
       
    #service_task = client.loop.create_task(background_update_news())
    client.run(token)
    


if __name__ == '__main__':
    main()


