import os
import sys
import json
import random
import time
import datetime
import discord
from discord.flags import MessageFlags
import qrcode
import requests
import logging
import urllib.request
from datetime import timedelta
from discord import user
from discord.ext import commands
from discord import app_commands, message
from dotenv import load_dotenv

client = discord.Client(intents=discord.Intents.all())

async def log(content):
  print(content)
  await discord.Webhook.from_url(os.environ['DISCORD_WEBHOOK'], client=client).send(content)

bot = commands.Bot(command_prefix="ky!", intents=discord.Intents.all())

tree = app_commands.CommandTree(client)

intent = discord.Intents.default()
intent.messages = True

#保存系

nickcmd_users = []

freeze_nick = {}

Developers = [1189807997669609552,1153623987906154507]

brackserver = [1165118279044579358]

brackusers = [1158390588836696124]

#buttonclassだよ


class DeleteButton(discord.ui.Button):

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_modal(ModalName())


#words一覧

omikuji = ['大凶','凶','末吉','吉','小吉','中吉','大吉']

banned_users = []

GLOBALCHAT = ("kyonshi-gc")

ngwords = ['010509']

kitanaiwords = ['010409']

aisatu = ['おはよう', 'おやすみ', 'こんばんは', 'やぁ!', 'よぉ!', 'よお!', 'よう!', 'よぅ!', 'やぁ！', 'やあ！','よぉ！', 'よお！', 'よう！', 'よぅ！', 'おはよう!', 'おは', 'こん','おはよ','こん','こんちゃ','よっ','おは！','おは!']

owa = ['がこおわ', 'ふろおわ', '風呂おわ', 'めしおわ', '飯おわ','学校おわ']

oti = ['風呂落ち', 'ふろおち', '飯落ち', 'めしおち', 'めし落ち', 'ふろ落ち']

say = ["言わそうとしてきたぞ"]

mentions = ["@everyone", "@here"]

links = ["discord.gg", "discord.com/invite","discordapp.com/invite"]

Developers = [1189807997669609552,1153623987906154507]

yamadas = ["やまだ","山田","ヤマダ","yamada","Yamada","YAMADA"]

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

getpoll = discord.Embed()


class ModalName(discord.ui.Modal):
  input = discord.ui.TextInput(label="CONTEXT",
                               style=discord.TextStyle.short,
                               placeholder="内容")

  def __init__(self):
    super().__init__(title="回答", timeout=None)

  async def on_submit(self, interaction: discord.Interaction):
    getpollmoto = (getpoll.description)
    getpoll.add_field(name="", value=f"\n{self.input.value}", inline=False)
    await interaction.response.edit_message(embed=getpoll)

#/cmdだよ 自分でもよくわかってないよ

@tree.command(name="redirect", description="指定したURLのリダイレクト先を調べて表示します。")
async def redirectcommand(interaction: discord.Interaction, url: str):
    try:
      response = requests.get(url, allow_redirects=True)
      embed = discord.Embed(title="結果", description="")
      embed.add_field(name="元URL",value=f"```{url}```",inline=False)
      embed.add_field(name="リダイレクト先",value=f"```{response.url}```",inline=False)
      await interaction.response.send_message(embed=embed)
    except Exception as e:
      print(e)
      await interaction.response.send_message("処理中にエラーが発生しました。")

@tree.command(name="qrcode", description="qrcodeを作成します。")
async def qrcodecommand(interaction: discord.Interaction, text: str):
      qr = qrcode.QRCode(version=1, box_size=10, border=5)
      qr.add_data(text)
      qr.make(fit=True)
      img = qr.make_image(fill_color="black", back_color="white")
      img.save("qrcode.png")
      file = discord.File("qrcode.png", filename="image.png")
      embed = discord.Embed(title="QRコード", description="```"+text+"```")
      embed.set_image(url="attachment://image.png")
      await interaction.response.send_message(file=file, embed=embed)

@tree.command(name="timeout", description="指定したユーザーをタイムアウトします。(timeは分で指定します)")
async def timeoutcmd(interaction: discord.Interaction, member: discord.Member, time: int, reason: str = (f"理由は指定されていません。")):
      duration = datetime.timedelta(minutes=time)
      if interaction.user == member:
          await interaction.response.send_message("❌自分自身をタイムアウトすることはできません。")
          return
      elif member.guild_permissions.administrator:
          await interaction.response.send_message("❌管理者をタイムアウトすることはできません。")
          return
      elif member.id == 1190912307790872637:
          await interaction.response.send_message("❌このbotをタイムアウトすることはできません。")
          return
      elif interaction.user.guild_permissions.moderate_members:
          await member.timeout(duration,reason=reason)
          await interaction.response.send_message(f"✅{member.mention} をタイムアウトしました！")
      else:
          await interaction.response.send_message(f"❌{interaction.user.mention}はタイムアウト権限を持っていません。")

@tree.command(name="kick", description="指定したユーザーをキックします。")
async def kickcmd(interaction: discord.Interaction, member: discord.Member, reason: str = ("理由は指定されていません")):
      if interaction.user == member:
          await interaction.response.send_message("❌自分自身をキックすることはできません。")
          return
      elif member.guild_permissions.administrator:
          await interaction.response.send_message("❌管理者をキックすることはできません。")
          return
      elif member.id == 1190912307790872637:
          await interaction.response.send_message(f"❌このbotをキックすることはできません。")
      elif interaction.user.guild_permissions.kick_members:
          await member.kick(reason=reason)
          await interaction.response.send_message(f"✅{member.mention} をキックしました！")
      else:
          await interaction.response.send_message(f"❌{interaction.user.mention}はその権限を持っていません。")

@tree.command(name="ban", description="指定したユーザーをBANします。")
async def bancmd(interaction: discord.Interaction, member: discord.Member, reason: str = ("理由は指定されていません")):
      if interaction.user == member:
        await interaction.response.send_message("❌自分自身をBANすることはできません。")
        return
      elif member.guild_permissions.administrator:
        await interaction.response.send_message("❌管理者をBANすることはできません。")
        return
      elif member.id == 1190912307790872637:
        await interaction.response.send_message("❌このbotをBANすることはできません。")
      elif interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"✅{member.mention} をBANしました！")
      else:
        await interaction.response.send_message(f"❌{interaction.user.mention}はその権限を持っていません。")

@tree.command(name="unban", description="指定したユーザーのBANを解除します。")
async def unbancomd(interaction: discord.Interaction, member: int, reason: str = ("理由は指定されていません")):
      if interaction.user.guild_permissions.ban_members:
        members = await client.fetch_user(member)
        await interaction.guild.unban(members, reason=reason)
        await interaction.response.send_message(f"✅{member.mention} のBANを解除しました。")
      else:
        await interaction.response.send_message(f"❌{interaction.user.mention}はその権限を持っていません。")

@tree.command(name="wpoll", description="調整中")
async def poll(interaction: discord.Interaction, title: str):
  getpoll.clear_fields()
  getpoll.title = title  #embedのタイトルがgoodbyeに書き変わる
  getpoll.description = "**回答**"
  view = discord.ui.View()
  delete_button = DeleteButton(label='回答する', style=discord.ButtonStyle.red)
  view.add_item(delete_button)  # 作ったボタンを view に追加
  await interaction.response.send_message("作成完了", ephemeral=True)
  await interaction.channel.send(embed=getpoll, view=view)


@tree.command(name='avatar', description='ユーザーのアイコンを取得します。')
async def get_user_avatar(inter: discord.Interaction, member: discord.Member):
  embed = discord.Embed(title=f'{member.display_name} さんのアイコン',
                        colour=discord.Colour.teal(),
                        type='image')
  embed.set_image(url=member.display_avatar.url)
  await inter.response.send_message(embed=embed)
  return


@tree.command(name='test', description='testです')
async def m_test(interaction: discord.Interaction):
  await interaction.response.send_modal(
      ModalName())  ### ModalNameは上のclassで決めた名前に置き換えてください


@tree.command(name='ping', description='ping!')
async def get_ping(interaction: discord.Interaction):
  raw_ping = client.latency

  ping = round(raw_ping * 1000)

  await interaction.response.send_message(f"Pong!\nBotのPing値は{ping}msだよ。")


@tree.command(name='random',description='乱数を生成します。デフォルトでは0~100の数値からランダムに一つ選びます')
async def get_random(interaction: discord.Interaction,min: int = 0,max: int = 100):
  raodom = random.randint(min, max)
  raodomembed = discord.Embed(title='乱数',
                              description=raodom,
                              color=discord.Color.blue())
  await interaction.response.send_message(embed=raodomembed)


@tree.command(name='time', description='現在の時刻を表示します')
async def get_time(interaction: discord.Interaction):
  now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  await interaction.response.send_message(
      f"現在時刻は{now.hour}時{now.minute}分{now.second}秒です")


@tree.command(name='say', description='指定した内容を送信します')
async def sey(interaction: discord.Interaction, text: str):
  if ' '.join(say) in text:
    await interaction.response.send_message("それは言わせないよ", ephemeral=True)
    await interaction.channel.send(
        f"{interaction.user.display_name}さん！！人に濡れ衣着せようとするのやめようね！！m9(^Д^)")
    saylog = {interaction.user.display_name}
    for channel in client.get_guild(1191687272035270666).channels:
      if channel.id == 1191691984889446421:
        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9)))
        say_bad_m = discord.Embed(
            title='濡れ衣検出',
            description=
            (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が```{text}```を言わせようとして拒否したよ"
             ),
            color=discord.Color.purple())
        await channel.send(embed=say_bad_m)
    return
  for ngword in ngwords:
    if ngword in text:
      await interaction.response.send_message("止めてね", ephemeral=True)
      await interaction.channel.send(
          f"みんな{interaction.user.display_name}が{text}って私に言わそうとしてきたぞ")
      saylog = {interaction.user.display_name}
      for channel in client.get_guild(1191687272035270666).channels:
        if channel.id == 1191691984889446421:
          now = datetime.datetime.now(
              datetime.timezone(datetime.timedelta(hours=9)))
          say_bad_n = discord.Embed(
              title='NGワード検出',
              description=
              (f"みんな{interaction.user.display_name}が{text}って私に言わそうとしてきたぞ"
               ),
              color=discord.Color.orange())
          await channel.send(embed=say_bad_n)
      return
  for mention in mentions:
    if mention in text:
      await interaction.response.send_message("everyoneメンションまたはhereメンションを検知しました。", ephemeral=True)
      saylog = {interaction.user.display_name}
      for channel in client.get_guild(1191687272035270666).channels:
        if channel.id == 1191691984889446421:
          now = datetime.datetime.now(
              datetime.timezone(datetime.timedelta(hours=9)))
          say_bad_g = discord.Embed(
              title='NGmention検出',
              description=
              (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が```{text}```を言わせようとして拒否したよ"
               ),
              color=discord.Color.red())
          await channel.send(embed=say_bad_g)
      return
  for kitanaiword in kitanaiwords:
    if kitanaiword in text:
      await interaction.response.send_message("きっしょ", ephemeral=True)
      await interaction.channel.send(
          f"みんな{interaction.user.display_name}が卑猥なこと私に言わそうとしてきたぞ")
      saylog = {interaction.user.display_name}
      for channel in client.get_guild(1191687272035270666).channels:
        if channel.id == 1191691984889446421:
          now = datetime.datetime.now(
              datetime.timezone(datetime.timedelta(hours=9)))
          say_bad_h = discord.Embed(
              title='卑猥ワード検出',
              description=
              (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が```{text}```を言わせようとして拒否したよ"
               ),
              color=discord.Color.orange())
          await channel.send(embed=say_bad_h)
      return 
  for link in links:
    if link in text:
       await interaction.response.send_message("招待リンクを検知しました。", ephemeral=True)
       saylog = {interaction.user.display_name}
       for channel in client.get_guild(1191687272035270666).channels:
         if channel.id == 1191691984889446421:
           now = datetime.datetime.now(
               datetime.timezone(datetime.timedelta(hours=9)))
           say_bad_discord = discord.Embed(
             title='serverlink検出',
             description=
            (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が```{text}```を言わせようとして拒否したよ"
             ),
            color=discord.Color.red())
           await channel.send(embed=say_bad_discord)
       return
  for yamada in yamadas:
    if yamada in text:
       await interaction.response.send_message("私は山田じゃない")
       saylog = {interaction.user.display_name}
       for channel in client.get_guild(1191687272035270666).channels:
         if channel.id == 1191691984889446421:
           now = datetime.datetime.now(
               datetime.timezone(datetime.timedelta(hours=9)))
           say_bad_y = discord.Embed(
             title='山田検出',
             description=
            (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が```{text}```を言わせようとして拒否したよ"
             ),
            color=discord.Color.yellow())
           await channel.send(embed=say_bad_y)
       return
  nomention = discord.AllowedMentions(roles=False)
  await interaction.response.send_message("送信しました", ephemeral=True)
  await interaction.channel.send(text, allowed_mentions=nomention)
  saylog = {interaction.user.display_name}
  for channel in client.get_guild(1191687272035270666).channels:
    if channel.id == 1191691984889446421:
      now = datetime.datetime.now(
          datetime.timezone(datetime.timedelta(hours=9)))
      say_ok = discord.Embed(
            title='発言',
            description=
            (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が```{text}```を言わせようとしたよ"
             ),
        color=discord.Color.blue())
      await channel.send(embed=say_ok)
  return


#起動時のデバッグだよ


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online,
                               activity=discord.Game(f"ky!help"))

  for channel in client.get_guild(1191687272035270666).channels:
    if channel.id == 1191687272903475302:
      now = datetime.datetime.now(
          datetime.timezone(datetime.timedelta(hours=9)))
      kidou = discord.Embed(
          title='bot起動',
          description=(f"{now.hour}時{now.minute}分{now.second}秒にbotが起動しました"),
          color=discord.Color.blue())
      await channel.send(embed=kidou)
  await tree.sync()

  print('ログインしました')

#serverに導入された時の処理

@client.event
async def on_guild_join(guild):
  if guild.id in brackserver:
    m = discord.Embed(title=f'{guild.name} joined.',description='このサーバーがブラックリストに登録されているため、脱退しました。', color=discord.Color.red())
    await guild.leave()
    for channel in client.get_guild(1191687272035270666).channels:
      if channel.id == 1205101611702165504:
        await channel.send(embed=m)
        break
  else:
    for channel in client.get_guild(1191687272035270666).channels:
      if channel.id == 1205101611702165504:
        joinem = discord.Embed(title=f'{guild.name} joined.',description='サーバーに参加しました。', color=discord.Color.blue())
        await channel.send(embed=joinem)
        break

#serverから退出された時の処理

@client.event
async def on_guild_remove(guild):
  for channel in client.get_guild(1191687272035270666).channels:
    if channel.id == 1205101696825434152:
      leavem = discord.Embed(title=f'{guild.name} left.',description='このサーバーからbotが脱退しました。', color=discord.Color.yellow())
      await channel.send(embed=leavem)
      break

#山田じゃない

@client.event
async def on_member_update(before, after):
  if before.nick != after.nick:
      # ニックネームが変更された場合
      if after.id == client.user.id:
          # 自分のニックネームが変更された場合
          if any(name in after.nick.lower() for name in yamadas):
              await after.edit(nick='kyonshi_bot')

  if str(before.id) in freeze_nick:
    if before.nick != after.nick:
      await after.edit(nick=freeze_nick[str(after.id)])


@client.event
async def on_message(message):
  global brackusers

  global nickcmd_users

  global freeze_nick

  global Developers

  global brackserver

  if message.author.id in brackusers:
    return

  if message.author.bot:
    return

  usr = message.author

  #ky!admincmd

  if message.content.startswith('ky!jsondump'):
    if usr.id in Developers:
      try:
        file = str(message.content.split(' ')[2])
        with open(f'/ex/kyon/kyonshi_bot/data/{file}', 'r') as f:
          json_data = json.load(f)
          key = str(message.content.split(' ')[3])
          if message.content.split(' ')[1] == 'add':
            value = str(message.content.split(' ')[4])
            json_data[key] = value
            await message.channel.send(f'{file}に{key},{value}を追加しました。')
          elif message.content.split(' ')[1] == 'remove':
            json_data.pop(str(message.content.split(' ')[3]))
            await message.channel.send(f'{file}から{key}を削除しました。')
        with open(f'/ex/kyon/kyonshi_bot/data/{file}', 'w') as f:
          json.dump(json_data, f,indent=2,ensure_ascii=False)
      except Exception as e:
        error = discord.Embed(title='エラー',description=e)
        await message.channel.send(embed=error)
    return

  if message.content.startswith('ky!jsonview'):
    if usr.id in Developers:
      try:
        await message.channel.send(file=discord.File(f'/ex/kyon/kyonshi_bot/data/{str(message.content.split(" ")[1])}'))
      except Exception as e:
        error = discord.Embed(title='エラー',description=e)
        await message.channel.send(embed=error)

  if message.content.startswith('ky!exec'):
    if usr.id == 1189807997669609552:
      try:
        exec(message.content.split(" ")[1])
        await message.channel.send('実行しました。')
      except Exception as e:
        em = discord.Embed(title='エラー',description=e)
        await message.channel.send(embed=em)

  if message.content.startswith('ky!debug_server_leave'):
    if usr.id in Developers:
      target_server = discord.utils.get(client.guilds, id=int(message.content.split(' ')[1]))
      if target_server:
        await target_server.leave()
        await message.channel.send(f'{target_server}から脱退しました。')
        return
      else:
        await message.channel.send('サーバーが見つかりませんでした。')

  if message.content.startswith('ky!brackservers'):
    if usr.id in Developers:
      bserembed = ("")
      for bserver in brackserver:
        bservers = client.get_guild(bserver)
        bserembed += (f"{bserver}\n")
      else:
        bsem = discord.Embed(title="ブラックリスト一覧", description=bserembed, color=discord.Color.red())
        await message.channel.send(embed=bsem)
    else:
      await message.channel.send('そのコマンドを実行する権限がありません。')
      return

  if message.content.startswith('ky!brackserver+'):
    if usr.id in Developers:
      if len(message.content.split(' ')) == 1:
        await message.channel.send('サーバーを指定してください。')
        return
      elif not message.content.split(' ')[1].isdecimal():
        await message.channel.send('IDが正しくありません。')
        return
      elif not int(message.content.split(' ')[1]) in brackserver:
        try:
          brackguild = client.get_guild(int(message.content.split(' ')[1]))
          brackserver.append(int(message.content.split(' ')[1]))
          a = message.content.split(' ')[1]
          await message.channel.send(f'{a}をブラックリストに追加しました。')
        except Exception as e:
          await message.channel.send('そのサーバーは存在しません。')
          return
      else:
        await message.channel.send('そのサーバーは既にブラックリストに登録されています。')
    else:
      await message.channel.send('このコマンドは開発者専用です。')
      return

  if message.content.startswith('ky!brackserver-'):
    if usr.id in Developers:
      if len(message.content.split(' ')) == 1:
        await message.channel.send('サーバーを指定してください。')
        return
      elif not message.content.split(' ')[1].isdecimal():
        await message.channel.send('IDが正しくありません。')
        return
      elif int(message.content.split(' ')[1]) in brackserver:
        brackserver.remove(int(message.content.split(' ')[1]))
        removebser = client.get_guild(int(message.content.split(' ')[1]))
        await message.channel.send(f'{removebser}をブラックリストから削除しました。')
      else:
        await message.channel.send('そのサーバーはブラックリストに登録されていません。')
    else:
      await message.channel.send('このコマンドは開発者専用です。')
      return

  if message.content.startswith('ky!brackusers'):
    if usr.id in Developers:
      bues = ("")
      for bue in brackusers:
        devuser = await client.fetch_user(bue)
        bues += (f"{devuser}\n")
      else:
        devem = discord.Embed(title="ブラックリスト", description=bues, color=discord.Color.red())
        await message.channel.send(embed=devem)
    else:
      await message.channel.send('そのコマンドを実行する権限がありません。')
      return

  if message.content.startswith('ky!brackuser-'):
    if usr.id in Developers:
      if len(message.content.split(' ')) == 1:
        await message.channel.send('ユーザーを指定してください。')
        return
      elif not message.content.split(' ')[1].isdecimal():
        await message.channel.send('IDが正しくありません。')
        return
      elif int(message.content.split(' ')[1]) in brackusers:
        brackusers.remove(int(message.content.split(' ')[1]))
        removeuser = await client.fetch_user(int(message.content.split(' ')[1]))
        await message.channel.send(f'{removeuser.name}をブラックリストから削除しました。')
      else:
        await message.channel.send('そのユーザーはブラックリストに登録されていません。')
    else:
      await message.channel.send('このコマンドは開発者専用です。')
      return

  if message.content.startswith('ky!brackuser+'):
    if usr.id in Developers:
      if len(message.content.split(' ')) == 1:
        await message.channel.send('ユーザーを指定してください。')
        return
      elif not message.content.split(' ')[1].isdecimal():
        await message.channel.send('IDが正しくありません。')
        return
      elif not int(message.content.split(' ')[1]) in brackusers:
        try:
          brackuser = await client.fetch_user(int(message.content.split(' ')[1]))
          brackusers.append(int(message.content.split(' ')[1]))
          if brackuser.id in Developers:
            Developers.remove(brackuser.id)
            await message.channel.send(f'{brackuser.name}を開発者一覧から削除しました。')
          await message.channel.send(f'{brackuser.name}をブラックリストに登録しました。')
        except Exception as e:
          await message.channel.send('そのユーザーは存在しません。')
          return
      else:
        await message.channel.send('そのユーザーはすでにブラックリストに登録されています。')
    else:
      await message.channel.send('このコマンドは開発者専用です。')
      return

  if message.content.startswith('ky!developers'):
    if usr.id in Developers:
      devs = ("")
      for dev in Developers:
        devuser = await client.fetch_user(dev)
        devs += (f"{devuser}\n")
      else:
        devem = discord.Embed(title="開発者一覧", description=devs, color=discord.Color.blue())
        await message.channel.send(embed=devem)
    else:
      await message.channel.send('そのコマンドを実行する権限がありません。')
      return

  if message.content.startswith('ky!developer-'):
    if usr.id == 1189807997669609552:
      if len(message.content.split(' ')) == 1:
        await message.channel.send('ユーザーを指定してください。')
        return
      elif not message.content.split(' ')[1].isdecimal():
        await message.channel.send('IDが正しくありません。')
        return
      elif int(message.content.split(' ')[1]) in Developers:
        Developers.remove(int(message.content.split(' ')[1]))
        removedev = await client.fetch_user(int(message.content.split(' ')[1]))
        await message.channel.send(f'{removedev.name}を開発者一覧から削除しました。')
      else:
        await message.channel.send('そのユーザーは開発者ではありません。')
    else:
      await message.channel.send('このコマンドは制作者専用です。')
      return

  if message.content.startswith('ky!developer+'):
    if usr.id == 1189807997669609552:
      if len(message.content.split(' ')) == 1:
        await message.channel.send('ユーザーを指定してください。')
        return
      elif not message.content.split(' ')[1].isdecimal():
        await message.channel.send('IDが正しくありません。')
        return
      elif not int(message.content.split(' ')[1]) in Developers:
        try:
          dev = await client.fetch_user(int(message.content.split(' ')[1]))
          Developers.append(int(message.content.split(' ')[1]))
          await message.channel.send(f'{dev.name}を開発者一覧に追加しました。')
        except Exception as e:
          await message.channel.send('そのユーザーは存在しません。')
          return
      else:
        await message.channel.send('そのユーザーはすでに開発者です。')
    else:
      await message.channel.send('このコマンドは制作者専用です。')
      return

  if message.content.split(' ')[0] == 'ky!addnick':
    if message.author.id in Developers:
      nickmem = message.guild.get_member(int(message.content.split(' ')[1]))
      nickname = message.content.split(' ')[2]
      try:
        await nickmem.edit(nick=nickname)
        nickcmd_users.append(message.content.split(' ')[1])
        freeze_nick[str(nickmem.id)] = nickname
        await message.channel.send(f'ニックネームを変更しました。')
      except Exception as e:
        await message.channel.send("権限不足もしくは何らかの例外が発生しました。")
    else:
      await message.channel.send("そのコマンドを実行する権限がありません。")
      return

  if message.content.split(' ')[0] == f'ky!debug_linkget':
    if message.author.id in Developers:
      guild = client.get_guild(int(message.content.split(' ')[1]))
      text = guild.text_channels
      if text:
        text_id = text[0].id
        channel = client.get_channel(text_id)
        invite = await channel.create_invite(max_uses=1,unique=False)
        await message.channel.send(f"作成しました。\n{invite.url}")
      else:
        await message.channel.send(f'見つかりませんでした。')
        return
    else:
      await message.channel.send("そのコマンドを実行する権限がありません。")
      return

  if message.content == "ky!debug_server":
    if not message.author.id in Developers:
      await message.channel.send("そのコマンドを実行する権限がありません。")
      return
    if message.author.id in Developers:
     guildlist = client.guilds
     server_info = ""
     serveritiran = discord.Embed(title="kyonshi_bot参加サーバー一覧",description="参加サーバーの一覧を表示します\n",color=discord.Color.blue())
     for server in guildlist:
         server_info += f" {server.name}, : {server.id}\n"
         serveritiran.description = server_info
     await message.channel.send(embed=serveritiran)

  if message.content.startswith("ky!debug_global.ban"):
    if message.author.id == 1189807997669609552:
      split_message = message.content.split(" ")
      if len(split_message) > 2:
        await message.channel.send("ユーザーIDが指定されていません。")
        return
      if len(message.mentions) == 1:
        await message.channel.send("ユーザーを選択してください")
        return
      else:
        banuser = split_message[1]
        gbanuser = await client.fetch_user(banuser)
        banned_users.append(banuser)
        for server in client.guilds:
          try:
            await server.ban(user = gbanuser , reason = "開発者が危険なユーザーとしてglobal.banコマンドを実行しました。" , delete_message_days = 1)
            await message.channel.send(f"{gbanuser}を{server.name}からBANしました")
          except Exception as e:
            print(e)
            await message.channel.send(f"{gbanuser}を{server.name}からBANできませんでした。権限不足または何らかの例外が発生しました。")
    else:
      await message.channel.send("このコマンドは制作者専用です。")
      return

  if message.content== 'ky!reload':
    if message.author.id == 1189807997669609552:
      await message.channel.send("再起動します")
      await client.close()
      sys.exit()
    else:
      await message.channel.send("このコマンドは制作者専用です。")

  #ky!globalcommand

  if message.content.startswith('ky!events'):
    today = ('false')
    time_data = ('null')
    if len(message.content.split(' ')) == 1:
      japan_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
      month = japan_time.month
      day = japan_time.day
      time_data = (f"{month}/{day}")
      today = ('true')
    elif len(message.content.split(' ')) == 2:
      if message.content.split(' ')[1] in ("/"):
        time_data = str(message.content.split(' ')[1])
    elif len(message.content.split(' ')) == 3:
      months = message.content.split(' ')[1]
      days = message.content.split(' ')[2]
      time_data = (f'{months}/{days}')
    else:
      await message.channel.send("引数が不正です。")
      return
    with open('/ex/kyon/kyonshi_bot/data/event.json', 'r') as f:
      try:
        event = json.load(f)
        event_data = event[str(time_data)]
        event_title = event_data.split("_")[0]
        event_description = event_data.split("_")[1]
        event_embed = discord.Embed(title=event_title, description=event_description)
        await message.channel.send(embed=event_embed)
      except Exception as e:
        if today == 'true':
          await message.channel.send("今日のイベントはありません。")
        else:
          await message.channel.send("その日のイベントはありません。")
      return

  if message.content.startswith("ky!check_permissions"):
    if len(message.mentions) != 1:
      await message.reply("ユーザーを指定してください。")
    else:
      member = message.mentions[0]
      perms = member.guild_permissions
      embed = discord.Embed(title=f"Permissions for {member}", color=0x00ff00)
      embed.add_field(name="administrator", value=perms.administrator)
      embed.add_field(name="kick members", value=perms.kick_members)
      embed.add_field(name="ban members", value=perms.ban_members)
      embed.add_field(name="manage channels", value=perms.manage_channels)
      embed.add_field(name="manage roles", value=perms.manage_roles)
      embed.add_field(name="manage messages", value=perms.manage_messages)
      await message.channel.send(embed=embed)

  if message.content == 'ky!invite':
    await message.reply('[botのリンクだよ](<https://discord.com/oauth2/authorize?client_id=1190912307790872637&permissions=67061618699863&scope=bot>)')
    
  if message.content == 'ky!time':
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    await message.reply(f"現在時刻は{now.hour}時{now.minute}分{now.second}秒です")

  if message.content == "ky!ping":
    raw_ping = client.latency
    ping = round(raw_ping * 1000)
    await message.reply(f"Pong!\nBotのPing値は{ping}msだよ。")

  if message.content == 'ky!server':
    await message.reply(f'今は {len(client.guilds)} サーバーに参加してるよ')

  if message.content == 'ky!help':
    test = discord.Embed(
        title='ヘルプ',
        description=
        '/cmdは自分で見てね\nprefixはky!でping,server,time,random,help.inviteが多分使えるよ\nあとはこいつにメンションして、「～って言って」って言うと言ってくれるよ\n「がこおわ」とか「やぁ」とか「おはよう」とか、あとは卑猥な言葉とか酷い言葉を言うと反応するよ\n多分こんくらいだよ',
        color=discord.Color.blue())
    await message.channel.send(embed=test)

  if message.content == 'ky!random':
    ramdom = random.randint(0, 100)
    ramdomembed = discord.Embed(title='乱数',
                                description=ramdom,
                                color=discord.Color.blue())
    await message.reply(embed=ramdomembed)

  if message.content == 'ky!special_thanks':
    print('実行確認')
    special = discord.Embed(
        title='Special Thanks!!',
        description=
        '**nr.nell** bot開発を進めてくれて、bot開発に協力してくれた\n\n**akku**    サーバーを貸してくれた \n\n**音猫**    たまにサポートしてくれた\n\n**先輩,たけとら**    botの下ネタ対策testに図らずも協力してくれた\n\n**Suger** 同じくtestに協力してくれた\n\n**🪐**   modal等pythonのコードで分からない所を教えてくれた。',
        color=discord.Color.blue())
    await message.channel.send(embed=special)

  if message.content == 'ky!omikuji':
    if message.author.id == 1189807997669609552:
      ms = 6
    else:
      ms = random.randint(0, 6)
    mikuji = discord.Embed(title='おみくじ', description=omikuji[ms], color=discord.Color.blue())
    await message.channel.send(embed=mikuji)

  #messageに反応する奴らだよ

  if message.content == '<@1190912307790872637>':
    if message.author.id == 1189807997669609552:
     await message.channel.send('どうかなさいましたかkyonshi様')
     return
    else:
     await message.channel.send("なんすか")

  if message.content == 'kyonshi':
    await message.channel.send('が開発したbotです')

  if message.content == 'やあ':
    await message.channel.send('やぁ')

  for i in ngwords:
    if i in message.content:
      if '<@1190912307790872637>' in message.content:
        await message.reply('うるせぇぶち殺すぞ')
      else:
        if i == message.content:
          await message.reply('酷いなぁ')
        else:
          return
      break

  for i in kitanaiwords:
    if i in message.content:
      if '<@1190912307790872637>' in message.content:
        await message.reply('きっしょ')
      else:
        await message.reply('帰れ')
      break

  for i in owa:
    if i in message.content:
      if '<@1190912307790872637>' in message.content:
        await message.reply('何でいちいちメンションして言ったんだ　必要なくね')
      else:
        if i == message.content:
          await message.reply('おつ')
        else:
          return
      break
  for i in aisatu:
    if i == message.content:
      response = message.content
      await message.reply(response)
      break

  for i in oti:
    if i in message.content:
      if '<@1190912307790872637>' in message.content:
        await message.reply('何でいちいちメンションして言ったんだ　必要なくね')
      else:
        if i == message.content:
          await message.reply('行ってら')
        else:
          return
      break

  if message.author == client.user:
    return

  if client.user in message.mentions and 'って言って' in message.content:
    response = message.content.split('って言って')[0]
    if '<@1190912307790872637>' in response:
      response = response.replace('<@1190912307790872637>', '')
    elif any(ngword in message.content for ngword in ngwords):
      return
    elif any(kitanaiword in message.content for kitanaiword in kitanaiwords):
      return
    elif any(mention in message.content for mention in mentions):
      await message.channel.send("everyoneメンションまたはhereメンションを検知しました。 ")
      return
    elif any(link in message.content for link in links):
      await message.channel.send("招待リンクを検知しました。 ")
      return
    elif any(yamada in message.content for yamada in yamadas):
      await message.channel.send("山田じゃねぇよ")
      return
    response = response.replace("@", "＠")
    await message.channel.send(response)

  if message.author.id == client.user.id:
    return
  if not message.channel.name == GLOBALCHAT:
    return
  text = (f"```{message.content}```")
  embed = discord.Embed(description=text)
  embed.set_author(name=message.author, icon_url=message.author.avatar)

  if message.attachments:
      embed.set_image(url=message.attachments[0].url)

  for channel in client.get_all_channels():
    if channel.name == GLOBALCHAT:
        if channel.id == message.channel.id:
            await message.delete()

        await channel.send(embed=embed)

class Client(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.all())
    self.tree = discord.CommandTree(client=self)

  async def setup_hook(self) -> None:
    self.tree.add_command(kickcmd)
    await self.tree.sync()

class DiscordWebHookHandler(logging.Handler):
  webhook:str
  console:logging.StreamHandler
  def __init__(self):
    self.webhook = os.environ['DISCORD_WEBHOOK']
    self.console = logging.StreamHandler()
    super().__init__()

  def emit(self, record):
    try:
      self.console.emit(record)
      urllib.request.urlopen(urllib.request.Request(
        self.webhook,
        data=json.dumps({
          "content": "```js\n"+self.format(record)+"\n```"
        }).encode(),
        headers={
          "Content-Type": "application/json",
          "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
        },
      )).close()
    except Exception:
      self.handleError(record)

#bot起動

my_secret = os.environ['TOKEN']
def run():
  client.run(my_secret, log_handler=DiscordWebHookHandler())