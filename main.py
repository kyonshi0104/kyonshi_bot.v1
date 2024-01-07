import os
import random
import time
import datetime
import discord
from discord.ext import commands
from discord import app_commands, message
from dotenv import load_dotenv

load_dotenv()

client = discord.Client(intents=discord.Intents.all())

bot = commands.Bot(command_prefix="ky!", intents=discord.Intents.all())

tree = app_commands.CommandTree(client)

intent = discord.Intents.default()
intent.messages = True

#buttonclassだよ


class DeleteButton(discord.ui.Button):

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_modal(ModalName())


#words一覧

ngwords = ['010509']
kitanaiwords = ['010409']
aisatu = [
    'おはよう', 'おやすみ', 'こんばんは', 'やぁ!', 'よぉ!', 'よお!', 'よう!', 'よぅ!', 'やぁ！', 'やあ！',
    'よぉ！', 'よお！', 'よう！', 'よぅ！', 'おはよう!', 'おは', 'こん'
]
owa = ['がこおわ', 'ふろおわ', '風呂おわ', 'めしおわ', '飯おわ']
oti = ['風呂落ち', 'ふろおち', '飯落ち', 'めしおち', 'めし落ち', 'ふろ落ち']
say = ["言わそうとしてきたぞ"]
mentions = ["@everyone", "@here"]

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

#普通のコマンドのテストだよ

@bot.command()
async def server_list(ctx):
    # サーバーに参加している全てのサーバーの名前とIDを取得する
    server_info = '\n'.join(f'{guild.name} ({guild.id})' for guild in bot.guilds)

    # 名前とIDを一つのメッセージにまとめて表示する
    await ctx.send(f'サーバー名とID:\n{server_info}')

#/cmdだよ 自分でもよくわかってないよ

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


@tree.command(name='random',
              description='乱数を生成します。デフォルトでは0~100の数値からランダムに一つ選びます')
async def get_random(interaction: discord.Interaction,
                     min: int = 0,
                     max: int = 100):
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
            (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が{text}を言わせようとして拒否したよ"
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
              (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が{text}を言わせようとして拒否したよ"
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
              (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が{text}を言わせようとして拒否したよ"
               ),
              color=discord.Color.orange())
          await channel.send(embed=say_bad_h)
      return
  else:
    text = text.replace("@", "＠")
    await interaction.response.send_message("送信しました", ephemeral=True)
    await interaction.channel.send(text)
    saylog = {interaction.user.display_name}
    for channel in client.get_guild(1191687272035270666).channels:
      if channel.id == 1191691984889446421:
        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9)))
        say_ok = discord.Embed(
            title='発言',
            description=
            (f"{now.hour}時{now.minute}分{now.second}秒に{saylog}が{text}を言わせようとしたよ"
             ),
            color=discord.Color.blue())
        await channel.send(embed=say_ok)
    return


#起動時のデバッグだよ


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online,
                               activity=discord.Game(f"test"))

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


@client.event
async def on_message(message):

  if message.author.bot:
    return
  if message.content == "ky!debug_server":
    if message.author.id != 1189807997669609552:
      await message.channel.send("そのコマンドを実行する権限がありません。")
      return
    if message.author.id == 1189807997669609552:
     guildlist = client.guilds
     server_info = ""
     serveritiran = discord.Embed(title="kyonshi_bot参加サーバー一覧",description="参加サーバーの一覧を表示します\n",color=discord.Color.blue())
     for server in guildlist:
         server_info += f" {server.name}, : {server.id}\n"
         serveritiran.description = server_info
     await message.channel.send(embed=serveritiran)

  if message.author.bot:
    return
  if message.content == 'ky!invite':
    await message.reply(
        '[botのリンクだよ](<https://discord.com/oauth2/authorize?client_id=1190912307790872637&permissions=67061618699863&scope=bot>)'
    )

  if message.author.bot:
    return
  if message.content == 'ky!time':
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    await message.reply(f"現在時刻は{now.hour}時{now.minute}分{now.second}秒です")

  if message.content == "ky!ping":

    raw_ping = client.latency

    ping = round(raw_ping * 1000)

    await message.reply(f"Pong!\nBotのPing値は{ping}msだよ。")

  if message.author.bot:
    return
  if message.content == 'ky!server':
    await message.reply(f'今は {len(client.guilds)} サーバーに参加してるよ')

  if message.author.bot:
    return
  if message.content == 'ky!help':
    test = discord.Embed(
        title='ヘルプ',
        description=
        '/cmdは自分で見てね\nprefixはky!でping,server,time,random,help.inviteが多分使えるよ\nあとはこいつにメンションして、「～って言って」って言うと言ってくれるよ\n「がこおわ」とか「やぁ」とか「おはよう」とか、あとは卑猥な言葉とか酷い言葉を言うと反応するよ\n多分こんくらいだよ',
        color=discord.Color.blue())
    await message.channel.send(embed=test)

  if message.author.bot:
    return
  if message.content == 'ky!random':
    ramdom = random.randint(0, 100)
    ramdomembed = discord.Embed(title='乱数',
                                description=ramdom,
                                color=discord.Color.blue())
    await message.reply(embed=ramdomembed)

  if message.author.bot:
    return
  if message.content == 'ky!special_thanks':
    print('実行確認')
    special = discord.Embed(
        title='Special Thanks!!',
        description=
        '**nr.nell** pythonの基礎を教えてくれた\n\n**akku**    サーバーを貸してくれた \n\n**音猫**    たまにサポートしてくれた\n\n**先輩,たけとら**    botの下ネタ対策testに図らずも協力してくれた\n\n**Suger** 同じくtestに協力してくれた\n\n**🪐**   modal等pythonのコードで分からない所を教えてくれた。',
        color=discord.Color.blue())
    await message.channel.send(embed=special)

  #messageに反応する奴らだよ

  if message.author.bot:
    return
  if message.content == '<@1190912307790872637>':
    if message.author.id == 1189807997669609552:
     await message.channel.send('どうかなさいましたかkyonshi様')
     return
    else:
     await message.channel.send("なんすか")

  if message.author.bot:
    return
  if message.content == 'kyonshi':
    await message.channel.send('が開発したbotです')

  if message.author.bot:
    return
  if message.content == 'やぁ':
    await message.channel.send('やぁ')

  if message.author.bot:
    return
  if message.content == 'やあ':
    await message.channel.send('やぁ')

  if message.author.bot:
    return

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

  if message.content == "nsaldigfuijkreawf":
    channel = client.get_channel(1170227909387112588)
    target_message = await channel.fetch_message(1186656441529008219)
    await target_message.channel.send("帰れ")

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
    response = response.replace("@", "＠")
    await message.channel.send(response)


class Client(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.all())
    self.tree = discord.CommandTree(client=self)

  async def setup_hook(self) -> None:
    self.tree.add_command(say)
    await self.tree.sync()


#bot起動

my_secret = os.environ['TOKEN']
def run():
 client.run(my_secret)
print("行けたね")
