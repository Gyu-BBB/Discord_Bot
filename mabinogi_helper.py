import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz  
import os
import json
import re
import yaml
import math
from discord import File
from Token import Token
from datetime import date

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
    file_path = get_datafile_path(os.path.join('colors', image_file_name))
    
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


@bot.command(name='경매장쿠폰최신화')
async def modify_coupon_command(ctx, price_10:int=None, price_20:int=None, price_30:int=None, price_50:int=None, price_100:int=None):
    #!빠진 입력이 있는 경우
    if price_10 is None or price_20 is None or price_30 is None or price_50 is None or price_100 is None:
        message = "다음과 같은 형식으로 기입해주세요. \n"
        message += "!경매장쿠폰최신화 [10%쿠폰비용(숫자)] [20%쿠폰비용(숫자)] [30%쿠폰비용(숫자)] [50%쿠폰비용(숫자)] [100%쿠폰비용(숫자)]\n"
        message += "예) !경매장쿠폰최신화 11500 65000 390000 19999999 29230000"
        await ctx.send(message)
    pdate_date,coupon_10,coupon_20,coupon_30,coupon_50,coupon_100 = modify_coupon_price(price_10, price_20, price_30, price_50, price_100)
    
    message = f" 쿠폰 가격 갱신\n"
    message += f"```"
    message += f" 10% 할인쿠폰 : {coupon_10:,}\n"
    message += f" 20% 할인쿠폰 : {coupon_20:,}\n"
    message += f" 30% 할인쿠폰 : {coupon_30:,}\n"
    message += f" 50% 할인쿠폰 : {coupon_50:,}\n"
    message += f"100% 할인쿠폰 : {coupon_100:,}\n"
    message += f"*updated by {update_date}*\n\n"
    message += f"```"
    message += f"갱신 완료되었습니다."
    await ctx.send(message)

@bot.command(name='경매장')
async def auction_command(ctx, price:int=None, premium:str=None):    
    #!경매장 만 입력한경우
    if price is None or premium is None:
        # 누락된 인자가 있을 시 사용자에게 양식 제공
        message = "다음과 같은 형식으로 기입해주세요. \n"
        message += "!경매장 [판매가(숫자)] [프리미엄멤버십 또는 프리시즌 여부(y/n)]\n"
        message += "예) !경매장 5000000 y"
        await ctx.send(message)
    
    result, sales_commission,sales_commission_percent, discount_10, discount_20, discount_30, discount_50, discount_100 = calculate_auction(price, premium)
    
    global update_date, coupon_10, coupon_20, coupon_30, coupon_50, coupon_100
    load_coupon_prices_from_yaml() 

    
    auction_dic = {'10%':discount_10-coupon_10, 
                   '20%':discount_20-coupon_20, 
                   '30%':discount_30-coupon_30,
                   '50%':discount_50-coupon_50, 
                   '100%':discount_100-coupon_100}
                   
    actual_received_amount = {'10%':result+(discount_10-coupon_10),
                              '20%':result+(discount_20-coupon_20), 
                              '30%':result+(discount_30-coupon_30),
                              '50%':result+(discount_50-coupon_50), 
                              '100%':result+(discount_100-coupon_100)}

    
    #최고 효율을 내는 값 찾기
    max_profit_key = max(auction_dic, key=auction_dic.get)
    max_profit_value = auction_dic[max_profit_key]
    
    message = f"판매가: {price:,.0f}\n"
    message += f"적용 수수료율: {sales_commission_percent*100}%"
    if sales_commission_percent == 0.04 :
        message += f" (프리미엄 멤버십 적용)"
    else :
        message += f" (프리미엄 멤버십 미적용)"
    message += f"\n"
    message += f"수수료: {sales_commission:,.0f}\n"
    message += f"수령 금액: {result:,.0f}\n\n"
    
    message += f"**==할인 쿠폰 사용시 수익==**\n"
    message += f"10% : {actual_received_amount['10%']:,.0f}\n"
    message += f"20% : {actual_received_amount['20%']:,.0f}\n"
    message += f"30% : {actual_received_amount['30%']:,.0f}\n"
    message += f"50% : {actual_received_amount['50%']:,.0f}\n"
    message += f"100%: {actual_received_amount['100%']:,.0f}\n"
    if max_profit_value > 0 :
        message += f"\n**💡최고 효율을 내는 수수료할인쿠폰은 [{max_profit_key}할인쿠폰] 입니다.💡**\n\n"
    else :
        message += f"\n**💡경매장 수수료할인쿠폰을 사용하지 않는 것이 좋습니다.💡**\n\n"
    
    message += f"```"
    message += f"==할인 쿠폰 금액==\n"
    message += f" 10% : {coupon_10:,}\n"
    message += f" 20% : {coupon_20:,}\n"
    message += f" 30% : {coupon_30:,}\n"
    message += f" 50% : {coupon_50:,}\n"
    message += f"100% : {coupon_100:,}\n"
    message += f"*updated by {update_date}*"
    # message += f"\n\n!경매장쿠폰최신화 1000 2000 3000 4000 5000"
    
    message += f"```"


    await ctx.send(message)

def calculate_auction(price, premium):
    # 프리미엄 여부에 따라 수수료율 결정
    sales_commission_percent = 0.04 if premium.lower() == 'y' else 0.05
    # 판매수수료 계산
    sales_commission = int(price * sales_commission_percent)
    #수수료 할인쿠폰 없이 수령할 금액
    result = price - sales_commission
    
    # 수수료 할인쿠폰 계산
    discount_10 = sales_commission * 0.1
    discount_20 = sales_commission * 0.2
    discount_30 = sales_commission * 0.3
    discount_50 = sales_commission * 0.5
    discount_100 = sales_commission * 1

    
    return result, sales_commission, sales_commission_percent, discount_10, discount_20, discount_30, discount_50, discount_100

def load_coupon_prices_from_yaml():
    global update_date, coupon_10, coupon_20, coupon_30, coupon_50, coupon_100
    try:
        with open(get_datafile_path('Discount_Ticket_Price.yaml'), 'r') as file:
            coupon_data = yaml.safe_load(file)
            update_date = coupon_data['update_date']
            coupon_10 = coupon_data['coupon_10']
            coupon_20 = coupon_data['coupon_20']
            coupon_30 = coupon_data['coupon_30']
            coupon_50 = coupon_data['coupon_50']
            coupon_100 = coupon_data['coupon_100']
    except FileNotFoundError:
        update_date = date.today().isoformat()
        coupon_10 = 0
        coupon_20 = 0
        coupon_30 = 0
        coupon_50 = 0
        coupon_100 = 0
        save_coupon_prices_to_yaml()
        
# 쿠폰값 업데이트 및 YAML 저장
def modify_coupon_price(modify_10, modify_20, modify_30, modify_50, modify_100):
    global update_date, coupon_10, coupon_20, coupon_30, coupon_50, coupon_100
    update_date = date.today().isoformat()
    coupon_10 = modify_10
    coupon_20 = modify_20
    coupon_30 = modify_30
    coupon_50 = modify_50
    coupon_100 = modify_100
    save_coupon_prices_to_yaml()
    return update_date, coupon_10, coupon_20, coupon_30, coupon_50, coupon_100

def save_coupon_prices_to_yaml():
    coupon_data = {
        'update_date': update_date,
        'coupon_10': coupon_10,
        'coupon_20': coupon_20,
        'coupon_30': coupon_30,
        'coupon_50': coupon_50,
        'coupon_100': coupon_100
    }
    with open(get_datafile_path('Discount_Ticket_Price.yaml'), 'w') as file:
        yaml.safe_dump(coupon_data, file)

# 현재 요일을 확인하는 함수
def get_current_day():
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    today = datetime.now(pytz.timezone('Asia/Seoul')).weekday()
    return days[today]

# 어드템 확인
@bot.command()
async def 어드(ctx):
    current_day = get_current_day()
    data_file = get_datafile_path("Advanced_Item.yaml")
    with open(data_file, 'r', encoding='utf-8') as file:
        schedule = yaml.safe_load(file)
        if current_day in schedule:
            content = "\n".join(schedule[current_day])
            await ctx.send(f"## 오늘의 어드벤스드 아이템\n{content}")
        else:
            await ctx.send(f"제대로 입력해")

@bot.command()
async def 어드전체(ctx):
    data_file = get_datafile_path("Advanced_Item.yaml")
    with open(data_file, 'r', encoding='utf-8') as file:
        schedule = yaml.safe_load(file)
        message = []
        for day, items in schedule.items():
            day_items = f"{day}\n" + "\n".join(items)
            message.append(day_items)
        formatted_message = "```" + "\n\n".join(message) + "```"
        await ctx.send(formatted_message)

@bot.command()
async def 전체어드(ctx):
    data_file = get_datafile_path("Advanced_Item.yaml")
    with open(data_file, 'r', encoding='utf-8') as file:
        schedule = yaml.safe_load(file)
        message = []
        for day, items in schedule.items():
            day_items = f"{day}\n" + "\n".join(items)
            message.append(day_items)
        formatted_message = "```" + "\n\n".join(message) + "```"
        await ctx.send(formatted_message)

bot.run(Token)