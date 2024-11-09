import discord
from datetime import timedelta
import asyncio
import unicodedata
import random
import json

# CREATE A CONFIG.JSON TO PUT YOUR TOKEN AND YOUR PREFIX
with open('./config.json', 'r') as f:
    config = json.load(f)
        
# ------ Defs ------ 
def remove_caracters(text):
    normalized_text = unicodedata.normalize('NFD', text)
    return ''.join(caracter for caracter in normalized_text if unicodedata.category(caracter) != 'Mn').lower()

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged as {client.user}")

    #Looping Status
    while True:
        presence1 = discord.Game("digite .help para todos os comandos!")
        await client.change_presence(status=discord.Status.idle, activity=presence1)
        await asyncio.sleep(4)
        presence2 = discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servidores")
        await client.change_presence(status=discord.Status.idle, activity=presence2)
        await asyncio.sleep(4)
        
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == f"<@{client.user.id}>":
        await message.channel.send(f"Olá, digite `{config["prefix"]}ajuda` para mais ajuda")

# ------ Async Defs ------ 
    async def create_embed(title, description=None, imageUrl=None, url=None):
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.dark_purple(),
            url=url
        )
        embed.set_image(url=imageUrl)

        if message.author.avatar:
            embed.set_footer(text=f"Requested by {message.author}", icon_url=message.author.avatar.url)
        else:
            embed.set_footer(text=f"Requested by {message.author}", icon_url=message.author.default_avatar.url)

        return embed
# ------ Responses ------ 
    if isinstance(message.channel, discord.DMChannel):
        return

    if message.content.startswith(f"{config["prefix"]}"):
        command = message.content[len(config["prefix"]):]
        command = remove_caracters(command)

# ------ User Commands ------
        if command == "help" or command == "ajuda":
            commands = f"""
            **Comandos:**
            .ajuda/help `mostra essa mensagem`
            .ping `retorna a latência do bot`
            .rolar/roll (numero) `rola um dado`
            .moeda/coin `cara ou coroa`
            .warninfo (@user) `mostra o motivo e a quantidade de advertências de um usuário`
            """
            adminCommands = f"""
            **Comandos Admins**
            .say (mensagem) `faz a neeko dizer algo`
            .ban (@user) `bane um usuário mencionado`
            .unban (id) `desbane um usuário por id`
            .kick (@user) `expulsa um usuário mencionado`
            .clear (quantidade) `apaga uma quantidade de mensagens no chat`
            .mute (@user) `muta um usuário mencionado`
            .unmute (@user) `desmuta um usuário mencionado`
            .lock `destrava o canal onde a mensagem foi enviada`
            .unlock `destrava o canal onde a mensagem foi enviada`
            .warn (@user) `aplica uma advertencia a um usuario, caso ele leve 3 advertencias, e banido`
            .removewarn (@user) `remove a advertencia de um usuario`
            .timeout (@user) `deixa um usuario de castigo`
            """
            if message.author.guild_permissions.administrator:
                embed = await create_embed("Ajuda", commands + adminCommands)
            else: 
                embed = await create_embed("Ajuda", commands)
            await message.channel.send(embed=embed)
        if command == "ping" or command == "latencia":
            latency = f"Latência de {int((client.ws.latency*1000))}ms"
            embed = await create_embed("Ping!", latency)
            await message.reply(embed=embed)
        if command.startswith(("roll", "rolar")):
            try:
                number = int(command[len("rolar"):].strip())
                if number <= 1:
                    embed = await create_embed("Roll", "O número para rolar deve ser maior que 1")
                    await message.reply(embed=embed)
                    return
                result = random.randint(1, number)
                await message.channel.send(f"{message.author.mention} rolou um **d{number}**... e conseguiu... {result}!. :game_die: ")
            except (IndexError, ValueError):
                embed = await create_embed("Roll", "Escolha um número para rolar")
                await message.reply(embed=embed)
            except:
                embed = await create_embed("Roll", "Erro ao executar comando")
                await message.reply(embed=embed)
        if command == "coin" or command == "moeda":
            result = random.randint(0, 1)
            if result == 1:
                msg = await message.reply("🪙")
                await asyncio.sleep(0.4)
                await msg.edit(content="👑")
                await asyncio.sleep(0.4)
                await msg.edit(content="🪙")
                await asyncio.sleep(0.4)
                await msg.edit(content="Deu Cara! 🪙")
            elif result == 0:
                msg = await message.reply("🪙")
                await asyncio.sleep(0.4)
                await msg.edit(content="👑")
                await asyncio.sleep(0.4)
                await msg.edit(content="🪙")
                await asyncio.sleep(0.4)
                await msg.edit(content="Deu Coroa! 👑")
        if command.startswith("avatar"):
            try:
                msg = command[len("avatar"):].strip().split(maxsplit=1)
                target_id = msg[0].strip("<@>")
                target_id = int(target_id)
                target = message.guild.get_member(target_id)
                
                if target.display_avatar:
                    url = target.display_avatar.url
                    embed = await create_embed(f"Clique aqui para baixar", imageUrl=url, url=url)
                    await message.reply(embed=embed)

            except (IndexError, ValueError):
                embed = await create_embed(f"Mencione um Usuário.")
                await message.reply(embed=embed)
        

# ------ Admin Commands ------
        if command.startswith("say"):
            if not message.author.guild_permissions.manage_messages:
                await message.channel.send(f"{message.author.mention} Você precisa de um cargo com `Gerenciar Mensagens` para executar esse comando!")
                return
            await message.channel.send(command[len("say"):].strip())
            await message.delete()
        if command.startswith("clear"):
            try:
                amount = int(message.content.split()[1])
                if not message.author.guild_permissions.manage_messages:
                    embed = await create_embed("Sem Permissão", f"{message.author.mention} Você não tem permissão para executar esse comando!")
                    await message.reply(embed=embed)
                    return
                if amount < 1:
                    embed = await create_embed("Clear", f"{message.author.mention} A quantidade de mensagens para excluir deve ser no mínimo 1")
                    await message.reply(embed=embed)
                    return
                if amount > 99:
                    embed = await create_embed("Clear", f"{message.author.mention} A quantidade de mensagens para excluir deve ser no máximo 99")
                    await message.reply(embed=embed)
                    return

                deleted = await message.channel.purge(limit=amount)
                embed = await create_embed(f"{len(deleted)} mensagens excluidas")
                await message.channel.send(embed=embed)

            except (IndexError, ValueError):
                await message.channel.send(f"{message.author.mention} Forneça um número válido de mensagens para excluir.")
        if command.startswith("ban"):
            if not message.author.guild_permissions.ban_members:
                embed = await create_embed("Você não tem permissão para fazer isso!")
                await message.reply(embed=embed)
                return
            try:
                msg = command[len("ban"):].strip().split(maxsplit=1)
                target_id = int(msg[0].strip("<@>"))
                if len(msg) < 2: reason = "Nenhum"
                else: reason = str(msg[1])
                
                authorid = message.author.id
                target = message.guild.get_member(target_id)
                
                async def cancel_callback(interaction):
                    if interaction.user.id != authorid:   
                        return
                    embed = await create_embed("Banimento cancelado.", f"O banimento de {target} foi cancelado!")
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                async def ban(interaction):
                    url="https://media1.tenor.com/m/TbfChfHKkOUAAAAd/ban-button.gif"
                    if interaction.user.id != authorid:   
                        return
                    await message.guild.ban(target, reason=reason)
                    embed = await create_embed("Banido!", f"{target.mention} foi banido com sucesso. Motivo: `{reason}`", url)
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                button1 = discord.ui.Button(label="Sim", style=discord.ButtonStyle.red)
                button1.callback = ban
                button2 = discord.ui.Button(label="Cancelar", style=discord.ButtonStyle.green)
                button2.callback = cancel_callback

                view = discord.ui.View()
                view.add_item(button1)
                view.add_item(button2)

                embed = await create_embed("Confirmar", f"Tem certeza que quer banir {target.mention}?")
                confirm_msg = await message.reply(embed=embed, view=view)

            except (IndexError, ValueError):
                embed = await create_embed(f"Mencione um Usuário para banir.")
                await message.reply(embed=embed)
        if command.startswith("unban"):
            if not message.author.guild_permissions.ban_members:
                    embed = await create_embed("Você não tem permissão para fazer isso!")
                    await message.reply(embed=embed)
                    return
            try:
                msg = command[len("unban"):].strip().split(maxsplit=1)
                if len(msg) < 1: target_id = int(msg[0])

                target = None
                async for ban_entry in message.guild.bans():
                    if ban_entry.user.id == target_id:
                        target = ban_entry
                        break

                if target is None:
                    embed = await create_embed("Erro", "Usuário não encontrado na lista de banidos.")
                    await message.reply(embed=embed)
                    return

                url = "https://media1.tenor.com/m/Ami1cSjr1NoAAAAd/saul-goodman3d-ok-saul-goodman.gif"
                embed = await create_embed("Desbanido", f"{target.user} foi desbanido do servidor.", url)

                await message.guild.unban(target.user)
                await message.reply(embed=embed)
            except (IndexError, ValueError):
                embed = await create_embed(f"Informe um ID para desbanir.")
                await message.reply(embed=embed)
        if command.startswith("kick"):
            if not message.author.guild_permissions.kick_members:
                embed = await create_embed("Você não tem permissão para fazer isso!")
                await message.reply(embed=embed)
                return
            try:
                msg = command[len("kick"):].strip().split(maxsplit=1)
                target_id = int(msg[0].strip("<@>"))
                if len(msg) < 2: reason = "Nenhum"
                else: reason = str(msg[1])
                
                authorid = message.author.id
                target = message.guild.get_member(target_id)
                
                async def cancel_callback(interaction):
                    if interaction.user.id != authorid:   
                        return
                    embed = await create_embed("Expulsão cancelada.", f"A expulsão de {target} foi cancelada!")
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                async def kick(interaction):
                    url="https://media1.tenor.com/m/esCHs7tm78UAAAAd/spongebob-squarepants-get-out.gif"
                    if interaction.user.id != authorid:   
                        return
                    await message.guild.kick(target, reason=reason)
                    embed = await create_embed("Expulso!", f"{target.mention} foi expulso com sucesso. Motivo: `{reason}`", url)
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                button1 = discord.ui.Button(label="Sim", style=discord.ButtonStyle.red)
                button1.callback = kick
                button2 = discord.ui.Button(label="Cancelar", style=discord.ButtonStyle.green)
                button2.callback = cancel_callback

                view = discord.ui.View()
                view.add_item(button1)
                view.add_item(button2)

                embed = await create_embed("Confirmar", f"Tem certeza que quer expulsar {target.mention}?")
                confirm_msg = await message.reply(embed=embed, view=view)

            except (IndexError, ValueError):
                embed = await create_embed(f"Mencione um Usuário para expulsar.")
                await message.reply(embed=embed)
        if command.startswith("mute"):
            try:
                role_name = "Penalizado"

                if not message.author.guild_permissions.manage_roles:
                    embed = await create_embed("Você não tem permissão para fazer isso!")
                    await message.reply(embed=embed)
                    return

                msg = command[len("mute"):].strip().split(maxsplit=1)
                target_id = msg[0].strip("<@>")
                target_id = int(target_id)
                target = message.guild.get_member(target_id)

                if target_id == client.user.id:
                    embed = await create_embed("Você não pode me mutar!")
                    await message.reply(embed=embed)
                    return

                authorid = message.author.id
                role = discord.utils.get(message.guild.roles, name=role_name)
                if role is None:
                    embed = await create_embed(f"Cargo '{role_name}' não encontrado!")
                    await message.reply(embed=embed)
                    return

                async def cancel_callback(interaction):
                    if interaction.user.id != authorid:   
                        return
                    embed = await create_embed("Mute cancelado.", f"O mute de {target} foi cancelado!")
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                async def mute(interaction):
                    url="https://media.tenor.com/f9jcZAy3gToAAAAj/mute-muted.gif"
                    if interaction.user.id != authorid:   
                        return
                    await target.add_roles(role)
                    embed = await create_embed("Mutado!", f"{target.mention} foi mutado com sucesso.", url)
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                button1 = discord.ui.Button(label="Sim", style=discord.ButtonStyle.red)
                button1.callback = mute
                button2 = discord.ui.Button(label="Cancelar", style=discord.ButtonStyle.green)
                button2.callback = cancel_callback

                view = discord.ui.View()
                view.add_item(button1)
                view.add_item(button2)

                embed = await create_embed("Confirmar", f"Tem certeza que quer mutar {target.mention}?")
                confirm_msg = await message.reply(embed=embed, view=view)
            except (IndexError, ValueError):
                    embed = await create_embed(f"Mencione um Usuário para mutar.")
                    await message.reply(embed=embed)
        if command.startswith("unmute"):
            role_name = "Penalizado"

            try:
                if not message.author.guild_permissions.manage_roles:
                    embed = await create_embed("Você não tem permissão para fazer isso!")
                    await message.reply(embed=embed)
                    return
            
                msg = command[len("unmute"):].strip().split(maxsplit=1)
                target_id = msg[0].strip("<@>")
                target_id = int(target_id)
                target = message.guild.get_member(target_id)

                role = discord.utils.get(message.guild.roles, name=role_name)
                if role is None:
                    embed = await create_embed(f"Cargo '{role_name}' não encontrado!")
                    await message.reply(embed=embed)
                    return

                await target.remove_roles(role)
                embed = await create_embed("Desmutado!", f"{target.mention} foi desmutado com sucesso.")
                await message.reply(embed=embed)
            except (IndexError, ValueError):
                    embed = await create_embed(f"Mencione um Usuário para mutar.")
                    await message.reply(embed=embed)
        if command.startswith("lock"):
            try:
                if not message.author.guild_permissions.manage_channels:
                    embed = await create_embed("Você não tem permissão para fazer isso!")
                    await message.reply(embed=embed)
                    return
            
                await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                embed = await create_embed("🔒 Canal Trancado 🔒")
                await message.reply(embed=embed)
            except:
                await message.reply("Erro ao executar o comando")
        if command.startswith("unlock"):
            try:
                if not message.author.guild_permissions.manage_channels:
                    embed = await create_embed("Você não tem permissão para fazer isso!")
                    await message.reply(embed=embed)
                    return
                
                await message.channel.set_permissions(message.guild.default_role, send_messages=True)
                embed = await create_embed("🔓 Canal Destrancado 🔓")
                await message.reply(embed=embed)
            except:
                await message.reply("Erro ao executar o comando")
        if command.startswith("warn") and not command.startswith("warninfo"):
            if not message.author.guild_permissions.ban_members:
                embed = await create_embed("Você não tem permissão para fazer isso!")
                await message.reply(embed=embed)
                return
            
            try:
                msg = command[len("warn"):].strip().split(maxsplit=1)
                target_id = msg[0].strip("<@>")

                target_id = int(target_id)
                max_warns = 3

                if len(msg) < 2:
                    embed = await create_embed("Você precisa informar o motivo da advertência!")
                    await message.reply(embed=embed)
                    return
                else:
                    reason = str(msg[1])

                authorid = message.author.id
                target = message.guild.get_member(target_id)

                if target:
                    guild = str(message.guild.id)
                    id = str(target.id)
                    with open('warned_users.json', 'r') as f:
                        warned_users = json.load(f)

                    if guild not in warned_users:
                        warned_users[guild] = {}

                    if id in warned_users[guild]:
                        warn = warned_users[guild][id].get("warns", 0)
                        warned_users[guild][id]["warns"] = warn + 1
                        warned_users[guild][id]["reason"] = reason
                        warned_users[guild][id]["author"] = message.author.id

                        if warned_users[guild][id]["warns"] >= max_warns:
                            url = "https://media1.tenor.com/m/TbfChfHKkOUAAAAd/ban-button.gif"
                            await message.guild.ban(target, reason="O usuário recebeu o limite de advertências.")
                            embed = await create_embed("Banido!", f"{target.mention} foi banido após atingir o limite de advertências no servidor.", url)
                            await message.reply(embed=embed)
                            return

                        url = "https://media1.tenor.com/m/mZuCRpWtld4AAAAC/be-doo-be-doo-minion.gif"
                        embed = await create_embed(f"Advertido! {warn}/{max_warns}", f"{target.mention} Você tomou uma advertência! Tome mais cuidado, caso atinja o limite de advertências você será banido na hora.", url)
                        await message.reply(embed=embed)
                        await target.timeout(timedelta(minutes=30), reason="Warned")
                        
                        
                    else:
                        warned_users[guild][id] = {
                            "warns": 1,
                            "reason": reason,
                            "author": message.author.id
                        }
                        warn = warned_users[guild][id].get("warns", 0)
                        url = "https://media1.tenor.com/m/mZuCRpWtld4AAAAC/be-doo-be-doo-minion.gif"
                        embed = await create_embed(f"Advertido! {warn}/{max_warns}", f"{target.mention} Você tomou uma advertência! Tome mais cuidado, caso atinja o limite de advertências você será banido na hora.", url)
                        await message.reply(embed=embed)

                    with open('warned_users.json', 'w') as f:
                        json.dump(warned_users, f, indent=4)
            except (IndexError, ValueError):
                    embed = await create_embed(f"Mencione um Usuário para advertir.")
                    await message.reply(embed=embed)
        if command.startswith("removewarn"):
            if not message.author.guild_permissions.ban_members:
                embed = await create_embed("Você não tem permissão para fazer isso!")
                await message.reply(embed=embed)
                return
            
            try:
                msg = command[len("removewarn"):].strip().split(maxsplit=1)
                target_id = msg[0].strip("<@>")
                target_id = int(target_id)
                target = message.guild.get_member(target_id)

                with open('warned_users.json', 'r') as f:
                    warned_users = json.load(f)

                guild = str(target.guild.id)
                id = str(target_id)

                if guild in warned_users and id in warned_users[guild]:
                    del warned_users[guild][id]
                    
                    if not warned_users[guild]:
                        del warned_users[guild]

                    with open('warned_users.json', 'w') as f:
                        json.dump(warned_users, f, indent=4)
                    
                    embed = await create_embed("Parabéns!", "Sua advertência foi removida, tome mais cuidado na próxima vez!")
                    await message.reply(embed=embed)
                else:
                    embed = await create_embed("Este usuário não tem advertências.")
                    await message.reply(embed=embed)

            except (IndexError, ValueError):
                embed = await create_embed(f"Mencione um usuário para remover a advertência.")
                await message.reply(embed=embed)
        if command.startswith("warninfo"):
            try:
                msg = command[len("warninfo"):].strip().split(maxsplit=1)
                target_id = msg[0].strip("<@>")
                target_id = int(target_id)
                target = message.guild.get_member(target_id)

                guild = str(message.guild.id)
                id = str(target.id)

                with open('warned_users.json', 'r') as f:
                    warned_users = json.load(f)

                warn = warned_users[guild][id]["warns"]
                reason = warned_users[guild][id]["reason"]
                author = warned_users[guild][id]["author"]
                embed = await create_embed(f"Warn Info {target}", f"{warn}/3 Advertências\nMotivo: {reason}\nAutor: <@{author}>")
                await message.reply(embed=embed)
            except (IndexError, ValueError):
                embed = await create_embed(f"Mencione um usuário para remover a advertência.")
                await message.reply(embed=embed)
        if command.startswith("timeout"):
            if not message.author.guild_permissions.ban_members:
                embed = await create_embed("Você não tem permissão para fazer isso!")
                await message.reply(embed=embed)
                return
            try:
                msg = command[len("timeout"):].strip().split(maxsplit=2)
                target_id = msg[0].strip("<@>")

                target_id = int(target_id)
                max_warns = 3

                if len(msg) < 2:
                    embed = await create_embed("Você precisa informar o tempo do timout (minutos)")
                    await message.reply(embed=embed)
                    return
                if len(msg) < 3:
                    embed = await create_embed("Você precisa informar o motivo do timeout!")
                    await message.reply(embed=embed)
                    return
                else:
                    reason = str(msg[2])
                    time = int(msg[1])

                authorid = message.author.id
                target = message.guild.get_member(target_id)

                async def cancel_callback(interaction):
                    if interaction.user.id != authorid:   
                        return
                    embed = await create_embed("Timeout cancelado.", f"O timeout de {target} foi cancelado!")
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                async def timeout(interaction):
                    url="https://media1.tenor.com/m/TbfChfHKkOUAAAAd/ban-button.gif"
                    if interaction.user.id != authorid:   
                        return
                    embed = await create_embed("Timeout!", f"{target.mention} tomou timeout por {time} minutos.\nMotivo: {reason}")
                    try:
                        await target.timeout(timedelta(minutes=time), reason=reason)
                    except (discord.errors.Forbidden):
                        await message.reply("Não tenho permissões para castigar este membro!")
                        await confirm_msg.delete()
                        return
                    await interaction.response.send_message(embed=embed)
                    await confirm_msg.delete()

                button1 = discord.ui.Button(label="Sim", style=discord.ButtonStyle.red)
                button1.callback = timeout
                button2 = discord.ui.Button(label="Cancelar", style=discord.ButtonStyle.green)
                button2.callback = cancel_callback

                view = discord.ui.View()
                view.add_item(button1)
                view.add_item(button2)

                embed = await create_embed("Confirmar", f"Tem certeza que quer dar timeout em {target.mention}?")
                confirm_msg = await message.reply(embed=embed, view=view)
            except (IndexError, ValueError):
                embed = await create_embed(f"Mencione um usuário para remover a advertência.")
                await message.reply(embed=embed)


client.run(config.json["prefix"])