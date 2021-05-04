import discord
import random
import os

message="""Hello!! This is Bulls and Cows game bot, which can help you kill some time (if you have some to kill obv)
Here are the commands which you can give to me :-\n
        !hello - Greet the bot
        !start - Start playing the game
        !guess <number> - Guess a number in the game
        !help - This is what you get!
        !rules - Rules of the game
        !stop - End the game in between
"""

bull3=["Wow you're guessing it really well !","Bullseye!!","You're almost there !"]
bull0=["Nope, Not even close","Think of something else","Well you can take something from this guess too (I guess)"]
cow3=["Well its something to know","Thats a good number to be honest","Now you've got some thinking to do"]

leavemsg=["Alright I guess you got something important to do","Hmmm alright... I won't judge you (maybe I will)","See you another time then!"]

class Client(discord.Client):
    async def on_ready(self):
        print("Logged in!",self.user)
        self.gameon=False
        self.score=0
        self.orginal=[]
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="you to type !help"))
    
    async def on_message(self,msg):
        # print(msg)
        channel=msg.channel
        if(msg.content.startswith('!')):
            name=str(msg.author).split('#')[0]
            # if len(str(msg.content).split(' '))>1:
            arg=str(msg.content).split(' ')[1:]
            comm=str(msg.content).split(' ')[0]
            if comm=='!hello':
                await channel.send("Hello {}!!\nWant to try the game? Type !help".format(name))
            elif comm=='!help':
                await channel.send(message)
            elif comm=='!stop':
                if self.gameon==False:
                    await channel.send("Come on man! You need to start the game before you can stop it!! (?)")
                else:
                    self.gameon=False
                    self.score=0          
                    await channel.send(random.choice(leavemsg))
            elif comm=='!rules':
                await channel.send("""I'll be thinking of a 4-digit number whose each digits are unique. And you need to guess the number which one is it. I can only give you hints as your guess gives you how many bulls and how many cows.
Having bulls means there are some digits whose position match exactly with my number, while cows means the digit is present in my number, but it is not in the correct position
Try to guess the number in fewest tries! Have fun!""")
            elif comm=='!guess':
                if self.gameon is False:
                    await channel.send("You must start a game first before you make a guess!! Type !start to begin")
                else:
                    guess=[x for x in arg[0]]
                    print(guess)
                    if len(arg)>1 or len(guess)!=4:
                        await channel.send("Please guess a single 4-digit number, for example if I'm guessing 2301, I'd write '!guess 2301'. Oh no, I gave you a hint 😥")
                    else:
                        self.score+=1
                        bull,cows=0,0
                        for i in range(len(self.orginal)):
                            if guess[i] in self.orginal:
                                cows+=1
                            if guess[i]==self.orginal[i]:
                                cows-=1
                                bull+=1
                        print(bull,cows)
                        if bull==len(self.orginal):
                            self.gameon=False
                            await channel.send("Congratulations !! {} guessed the correct number!! You guessed it in {} tries.\nIt's a good score, but you could have done better".format(name,self.score))
                            self.score=0
                        else:
                            newmsg="Hmm..."
                            if cows==3:
                                newmsg=random.choice(cow3)
                            if bull==3:
                                newmsg=random.choice(bull3)
                            elif bull==0:
                                newmsg=random.choice(bull0)
                            await channel.send("You guessed {}\n{}. I can only say that your guess gives you {} bulls and {} cows".format(''.join(guess),newmsg,bull,cows))

            elif comm=='!start':
                if self.gameon==True:
                    await channel.send("The game is already running! To start afresh stop this round (by !stop) and then start it again")
                    return
                await channel.send("Let's play Cows and Bulls!\nI'll think of a 4-digit number and you need to guess it!\nPlease note that all the digits are unique\nI'll keep on informing you about how good is your guess\n\nLet's Begin!!")
                self.orginal=[x for x in str(random.randint(1000,9999))]
                while(len(set(self.orginal))!=4):
                    print("Getting another number")
                    self.orginal=[x for x in str(random.randint(1000,9999))]
                self.gameon=True
                print(self.orginal)
                await channel.send("Alright I have a number in mind. Pick your guess by typing !guess followed by your guess...")
            else:
                await channel.send("Sorry I could not understand this command. Check from the below commands and enter one")
                await channel.send(message)

token=os.getenv("DISCORD_TOKEN")

bot=Client()
bot.run(token)