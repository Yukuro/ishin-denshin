import discord
import line_notify
import os
from discord.ext import commands

global g_vc

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_voice_state_update(member, before, after):
    print("member:{} before:{} after:{}".format(member, before, after))

    if before.channel == None: #Entered
        out = "\n"
        out += "{}に{}が入室しました\n".format(after.channel.name, member.display_name)
        for member in after.channel.members:
            if len(member.activities) == 0:
                tp = "{}は何もプレイしていません\n".format(member.display_name)
            else:
                tp = "{}は{}をプレイ中\n".format(member.display_name, member.activities[0].name)
            out += tp

        # for test
        targetChannel: discord.TextChannel
        for ch in after.channel.guild.text_channels:
            if ch.name == "bot-test":
                targetChannel = ch

        print(out)
        await targetChannel.send(out)

        line_notify.notify(out[:-1], os.environ["LINE_NOTIFY_TOKEN"])

    if after.channel == None: #Exit
        pass

@bot.command()
async def tellme(ctx, channelName):
    targetVc: discord.VoiceChannel
    for vc in ctx.guild.voice_channels:
        if channelName == vc.name:
            targetVc = vc

    out = ""
    out += "{}には{}人います！\n".format(targetVc.name, len(targetVc.members))

    for member in targetVc.members:
        if len(member.activities) == 0:
            tp = "{}は何もプレイしていません\n".format(member.display_name)
        else:
            tp = "{}は{}をプレイ中\n".format(member.display_name, member.activities[0].name)
        out += tp

    print(out)
    await ctx.send(out)

@bot.command()
async def konya(ctx, *args):
    res = "\nこんや～\n"

    if len(args) == 0:
        return

    if args[0] != "": # game name
        res += args[0]
    if args[1] != "": # time
        if args[1] == "now":
            res += " 今から\n"
        else:
            res += " {}～\n".format(args[1])

    print(res)
    line_notify.notify(res, os.environ["LINE_NOTIFY_TOKEN"])

@bot.command()
async def invite(ctx, name):
    res = "\n{}は{}をゲームに誘っています!\n".format(ctx.author.display_name, name)
    res += "一緒にゲームをしませんか？\n"

    print(res)
    line_notify.notify(res, os.environ["LINE_NOTIFY_TOKEN"])

bot.run(os.environ["DISCORD_BOT_TOKEN"])