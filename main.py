from MeowerBot import Bot 
from os import environ as env 
import traceback

counting = Bot()

with open("count.txt", "r") as f:
	current_count = int(f.read())

last_sender = ""




@counting.command()
def count(ctx):
	counting.wss.sendPacket({"cmd": "direct", "val":  { "cmd": "add_to_chat", "val": {"chatid": env["counting_chat"], "username": ctx.message.user.username} } })
	ctx.reply("added to the GC ")

#Start counting
def on_message(msg, bot=counting):
	try:
		if msg.data.startswith(bot.prefix):
			msg.data = msg.data.split(bot.prefix, 1)[1]
			bot.run_command(msg)
	except: traceback.print_exc()
  
	if msg.chat != env["counting_chat"]: return 
	if msg.user.username == env["MEOWER_USERNAME"]: return 
	print(f"{msg.user.username}: {str(msg)}")
	global current_count
	global last_sender
	
	if not int(str(msg).split()[0]) == current_count+1:
		counting.send_msg("1 You counted wrong", to=env["counting_chat"])
		current_count = 0
	
	if last_sender == msg.user.username:
		counting.send_msg("1 You cant count twice in a row", to=env["counting_chat"])
		current_count = 0
	
	current_count+=1
	last_sender = msg.user.username if not current_count==1 else ""
	
	with open("count.txt", "w") as f:
		f.write(str(current_count))

def on_login(bot=counting):
	bot.send_msg(str(current_count), to=env["counting_chat"])
	bot.send_msg(f"Run @{env['MEOWER_USERNAME']} count, to join the bot GC")

counting.callback(on_message, "message")
counting.callback(on_login, "login")

# Login to the bot
if __name__ == "__main__":
	counting.run(env["MEOWER_USERNAME"], env["MEOWER_PASSWORD"])
