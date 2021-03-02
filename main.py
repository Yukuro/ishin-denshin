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

bot.run(os.environ["DISCORD_BOT_TOKEN"])