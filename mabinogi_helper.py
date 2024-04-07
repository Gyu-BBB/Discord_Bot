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
# intents.guild_voice_states = True  # 음성 상태 변경 인텐트 활성화

# Initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# 음성 채널 ID와 이름 매핑
voice_channel_ids = {
    "1202655269818204180": "전망대",
    "1202655302890160178": "땃지",
    "1202655087202271232": "노는방",
    "1202655142395121675": "지하감옥",
}

# 입장 메시지를 나타낼 채팅방의 ID
text_channel_id = 1225476401889804379

def calculate_expression_with_equation(text):
    # 정규표현식을 사용하여 숫자와 연산자를 추출
    numbers = re.findall(r'\d+', text)
    operators = re.findall(r'[-+*/]', text)
    
    # 문자열에서 공백 제거
    numbers = [int(num) for num in numbers]
    operators = [op for op in operators if op.strip()]
    
    # 결과 및 식 초기화
    result = str(numbers[0])
    equation = str(numbers[0])
    
    for i in range(1, len(numbers)):
        equation += operators[i - 1] + str(numbers[i])
        if operators[i - 1] == '+':
            result += ' + ' + str(numbers[i])
        elif operators[i - 1] == '-':
            result += ' - ' + str(numbers[i])
        elif operators[i - 1] == '*':
            result += ' * ' + str(numbers[i])
        elif operators[i - 1] == '/':
            result += ' / ' + str(numbers[i])
    
    # 결과 계산
    result = eval(equation)
    
    return result, equation

# data파일 절대경로 설정
def get_datafile_path(file_name):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', file_name)
    return file_path

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user}')

# 음성채팅방 입퇴장 알림
@bot.event
async def on_voice_state_update(member, before, after):
    # print(f"Voice state updated for {member}: {before.channel} -> {after.channel}")

    tz = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    channel = bot.get_channel(text_channel_id)
    # 사용자가 음성 채널에 입장한 경우
    if before.channel is None and after.channel is not None:
        channel_name = voice_channel_ids.get(str(after.channel.id))
        if channel_name and channel:  # 채널 이름이 매핑에 있고, 텍스트 채널이 유효한 경우
            await channel.send(f"'{member.display_name}'님이 '{channel_name}'에 입장했습니다. ({current_time})")
    # 사용자가 음성 채널에서 퇴장한 경우
    elif before.channel is not None and after.channel is None:
        channel_name = voice_channel_ids.get(str(before.channel.id))
        if channel_name and channel:  # 채널 이름이 매핑에 있고, 텍스트 채널이 유효한 경우
            await channel.send(f"'{member.display_name}'님이 '{channel_name}'에서 퇴장했습니다. ({current_time})")
    # 사용자가 음성 채널을 변경한 경우
    elif before.channel is not None and after.channel is not None:
        before_channel_name = voice_channel_ids.get(str(before.channel.id))
        after_channel_name = voice_channel_ids.get(str(after.channel.id))
        if before_channel_name and after_channel_name and channel:
            if before_channel_name == after_channel_name:
                pass
            else:
                await channel.send(f"'{member.display_name}'님이 '{before_channel_name}' > '{after_channel_name}'으로 옮기셨습니다. ({current_time})")

# 도움말 부르기
@bot.command(name='도움')
async def help(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'manual.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)
@bot.command(name='명령어')
async def help(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'manual.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)

# 빅 이모티콘 
@bot.command(name='땃지')
async def help(ctx):
    await ctx.send('https://cdn.discordapp.com/emojis/1209645978140020747.webp?size=240&quality=lossless')
@bot.command(name='뚯지')
async def help(ctx):
    await ctx.send('https://cdn.discordapp.com/emojis/1209645978140020747.webp?size=240&quality=lossless')

# 계산기
@bot.command(name='계산')
async def calculate_command(ctx, *, arg):
    result, equation = calculate_expression_with_equation(arg)
    await ctx.send(f'계산 결과: {result}')
@bot.command(name='분배')
async def calculate_command(ctx, *, arg):
    result, equation = calculate_expression_with_equation(arg)
    await ctx.send(f'계산 결과: {result}')

# 역할관련
@bot.command(name='프팩')
async def premium(ctx):
    # '프팩' 역할 찾기
    role = discord.utils.get(ctx.guild.roles, name='프팩')
    if not role:
        # 역할이 없는 경우 메시지 전송
        await ctx.send('서버에 "프팩" 역할이 존재하지 않습니다.')
        return
    
    # 해당 역할을 명령어 사용자에게 추가
    try:
        await ctx.author.add_roles(role)
        await ctx.send(f'축하합니다! "{ctx.author.name}"님께 "프팩" 역할이 부여되었습니다.')
    except Exception as e:
        await ctx.send(f'역할을 추가하는 동안 오류가 발생했습니다: {e}')
@bot.command(name='색깔')
async def assign_color_role(ctx, *, color_name):
    # 정의된 색깔 이름을 역할 이름으로 사용
    valid_colors = ['빨강', '파랑', '노랑', '초록', '핑크', '보라', '검정']
    color_name = color_name.strip()

    # 유효한 색깔 이름인지 확인
    if color_name not in valid_colors:
        await ctx.send(f'유효하지 않은 색깔 이름입니다. 사용 가능한 색깔: {", ".join(valid_colors)}')
        return

    # 현재 사용자가 가진 색깔 역할 삭제
    current_roles = ctx.author.roles
    for role in current_roles:
        if role.name in valid_colors:
            try:
                await ctx.author.remove_roles(role)
            except Exception as e:
                await ctx.send(f'오류가 발생했습니다.: {e}')
                return

    # 새 색깔 역할 찾기 및 부여
    new_role = discord.utils.get(ctx.guild.roles, name=color_name)
    if not new_role:
        await ctx.send(f'"{color_name}" 색깔을 찾을 수 없습니다.')
        return

    try:
        await ctx.author.add_roles(new_role)
        await ctx.send(f'"{ctx.author.name}"님께 "{color_name}" 색깔이 부여되었습니다.')
    except Exception as e:
        await ctx.send(f'색깔을 추가하는 동안 오류가 발생했습니다: {e}')
@bot.command(name='색깔삭제')
async def remove_all_color_roles(ctx):
    valid_colors = ['빨강', '파랑', '노랑', '초록', '핑크', '보라', '검정']
    roles_to_remove = [discord.utils.get(ctx.guild.roles, name=color) for color in valid_colors]

    # 사용자가 가진 역할 중에서 유효한 색깔 역할이 있는지 확인하고, 해당하는 모든 역할을 제거
    removed_colors = []
    for role in roles_to_remove:
        if role and role in ctx.author.roles:
            try:
                await ctx.author.remove_roles(role)
                removed_colors.append(role.name)
            except Exception as e:
                await ctx.send(f'오류가 발생했습니다: {e}')
                return

    # 삭제된 색깔 역할이 있을 경우, 삭제된 역할 목록을 사용자에게 알림
    if removed_colors:
        await ctx.send(f'"{ctx.author.name}"님의 색깔이 삭제되었습니다.')
    else:
        await ctx.send('삭제할 색깔이 없습니다.')

# 공략관련
@bot.command(name='크롬')
async def send_chrome_bath(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'Chrome_Bath.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)
@bot.command(name='크롬30')
async def send_chrome_bath(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'Chrome_Bath30.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)
@bot.command(name='크롬50')
async def send_chrome_bath(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'Chrome_Bath50.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)
@bot.command(name='크롬100')
async def send_chrome_bath(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'Chrome_Bath100.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)
@bot.command(name='글렌')
async def send_chrome_bath(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'Glenn_Bearna.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)
@bot.command(name='글렌낮')
async def send_chrome_bath(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'Glenn_Bearna_day.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)
@bot.command(name='글렌밤')
async def send_chrome_bath(ctx):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'data', 'Glenn_Bearna_night.md')
    with open(file_path, 'r', encoding='utf-8') as file:
        message = file.read()
    await ctx.send(message)



# 오늘의 베테랑 찾기
# 베테랑 데이터 로드
def load_veteran_data():
    file_path = get_datafile_path('veteran_dungeon.yaml')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        for item in data:
            if '베테랑' in item:
                return item['베테랑']
    return [] 
# 오늘의 베테랑 선택
def select_veteran_for_today(veterans_list):
    start_date = datetime(2024, 4, 5)
    now = datetime.now()
    
    if now.hour < 7:
        today = now.date() - timedelta(days=1)
    else:
        today = now.date()
    
    delta = (today - start_date.date()).days
    
    index = delta % len(veterans_list)
    return veterans_list[index]

@bot.command()
async def 오테랑(ctx):
    veterans = load_veteran_data()
    today_veteran = select_veteran_for_today(veterans)
    await ctx.send(f'오늘의 베테랑 던전은 "{today_veteran}던전" 입니다.')
@bot.command()
async def 베테랑(ctx):
    veterans = load_veteran_data()
    today_veteran = select_veteran_for_today(veterans)
    await ctx.send(f'오늘의 베테랑 던전은 "{today_veteran}던전" 입니다.')
@bot.command()
async def 오늘의베테랑(ctx):
    veterans = load_veteran_data()
    today_veteran = select_veteran_for_today(veterans)
    await ctx.send(f'오늘의 베테랑 던전은 "{today_veteran}던전" 입니다.')
# 베테랑 : [페카, 알비, 키아, 라비, 마스, 피오드, 바리, 코일, 룬다]

# 염색
def find_nearest_color(rgb_values):
    file_path = get_datafile_path('dye_converted.yaml')
    
    with open(file_path, 'r', encoding='utf-8') as file:
        colors = yaml.safe_load(file)
    
    nearest_color_name = None
    nearest_color_rgb = None
    min_distance = float('inf')
    
    for color in colors:
        distance = math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb_values, color['rgb'])))
        if distance < min_distance:
            min_distance = distance
            nearest_color_name = color['name']
            nearest_color_rgb = color['rgb']
    
    return nearest_color_name, nearest_color_rgb

async def send_color_image(ctx, rgb):
    """해당 RGB 값을 가진 이미지 파일을 디스코드 채널에 전송합니다."""
    # 이미지 파일 이름을 "r,g,b.png" 형식으로 생성
    image_file_name = f"{rgb[0]},{rgb[1]},{rgb[2]}.png"
    # get_datafile_path 함수를 사용해 파일의 절대 경로를 구성
    file_path = get_datafile_path(os.path.join('color', image_file_name))
    
    if os.path.exists(file_path):
        await ctx.send(file=File(file_path))
    else:
        await ctx.send("해당 RGB 값에 맞는 이미지 파일이 없습니다.")

# 색상 이름으로 RGB 값을 찾는 함수
def find_rgb_by_name(color_name):
    file_path = get_datafile_path('dye_converted.yaml')
    
    with open(file_path, 'r', encoding='utf-8') as file:
        colors = yaml.safe_load(file)
    
    for color in colors:
        if color['name'] == color_name:
            return color['rgb']
    return None

def find_rgb(rgb_values):
    """Find the color name corresponding to the given RGB values."""
    file_path = get_datafile_path('dye_converted.yaml')

    with open(file_path, 'r', encoding='utf-8') as file:
        colors = yaml.safe_load(file)
    
    for color in colors:
        if color['rgb'] == rgb_values:
            return color['name']
    
    return None

@bot.command()
async def 지염(ctx, *args):
    # 기존 코드는 유지하고, 마지막에 이미지 전송 부분을 추가합니다.
    
    input_str = " ".join(args)
    if all(char.isdigit() or char in [',', ' '] for char in input_str):
        rgb_values = [int(val) for val in re.findall(r'\d+', input_str)]

        if len(rgb_values) == 3 and all(0 <= val <= 255 for val in rgb_values):
            exact_match_name = find_rgb(rgb_values)
            if exact_match_name:
                await ctx.send(f'해당 RGB 값 ({",".join(map(str, rgb_values))})에 대한 색상 이름은 "{exact_match_name}"입니다.')
                await send_color_image(ctx, rgb_values)
                return
            
            nearest_color_name, nearest_rgb = find_nearest_color(rgb_values)
            if nearest_color_name:
                await ctx.send(f'해당 RGB 값 ({",".join(map(str, rgb_values))})과 일치하는 색상이 없습니다.\n해당값과 가장 비슷한 색상은 {nearest_color_name}({",".join(map(str, nearest_rgb))})입니다.')
                await send_color_image(ctx, rgb_values)
                await send_color_image(ctx, nearest_rgb)
            else:
                await ctx.send("가장 비슷한 색상을 찾을 수 없습니다.")
        else:
            await ctx.send("올바른 RGB 형식으로 입력해주세요. 예) !지염 255,255,255")
    else:
        rgb_values = find_rgb_by_name(input_str)
        if rgb_values:
            await ctx.send(f'{input_str}에 일치하는 RGB값은 ({",".join(map(str, rgb_values))})입니다.')
            await send_color_image(ctx, rgb_values)
        else:
            await ctx.send(f'{input_str}에 일치하는 색상이 없습니다.')

bot.run(Token)

