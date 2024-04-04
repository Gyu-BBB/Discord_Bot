import discord
from discord.ext import commands
from datetime import datetime
import pytz  # 시간대 처리를 위해 pytz 모듈을 사용
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
    await ctx.send('# 명령어 \n ## !계산 - 분배, 크롬계산을 도와드립니다.\n(예시: !계산 80 44 22 +* || !계산 2500/4)\n## !색깔 - 닉네임의 색을 변경합니다.\n(가능한 색: 빨강, 파랑, 노랑, 초록, 핑크, 보라, 검정)\n## !색깔삭제 - 자신이 가진 닉네임 색을 삭제합니다.')
@bot.command(name='명령어')
async def help(ctx):
    await ctx.send('# 명령어 \n ## !계산 - 분배, 크롬계산을 도와드립니다.\n(예시: !계산 80 44 22 +* || !계산 2500/4)\n## !색깔 - 닉네임의 색을 변경합니다.\n(가능한 색: 빨강, 파랑, 노랑, 초록, 핑크, 보라, 검정)\n## !색깔삭제 - 자신이 가진 닉네임 색을 삭제합니다.')

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

bot.run(Token)

