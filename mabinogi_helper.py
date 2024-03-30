import discord
from discord.ext import commands
import re
from Token import Token

# Define intents
intents = discord.Intents.default()

# Initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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

@bot.command(name='도움')
async def help(ctx):
    await ctx.send('# 명령어 \n!계산 - 분배, 크롬계산을 도와드립니다. (예시: 80 44 22 +* or 2500/4)\n')

    # await ctx.send("!계산 - 분배, 크롬계산을 도와드립니다. (예시: 80 44 22 +* or 2500/4)")

@bot.command(name='계산')
async def calculate_command(ctx, *, arg):
    result, equation = calculate_expression_with_equation(arg)
    await ctx.send(f'계산 결과: {result}')


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
    valid_colors = ['빨강', '파랑', '노랑', '초록', '핑크']
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

bot.run(Token)

