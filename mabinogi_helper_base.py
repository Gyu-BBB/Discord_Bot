import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz  # 시간대 처리를 위해 pytz 모듈을 사용
import os
import json
import re
import yaml
import math
from discord import File
from Token import Token

# Define intents
intents = discord.Intents.default()

# Initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# data파일 절대경로 설정
def get_datafile_path(file_name):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', file_name)
    return file_path

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user}')

bot.run(Token)

