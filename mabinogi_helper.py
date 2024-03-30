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

@bot.command()
async def hello(ctx):
    await ctx.send('Hi!')

@bot.command(name='크롬')
async def calculate_command(ctx, *, arg):
    result, equation = calculate_expression_with_equation(arg)
    await ctx.send(f'계산 결과: {result}')

@bot.command(name='분배')
async def calculate_command(ctx, *, arg):
    result, equation = calculate_expression_with_equation(arg)
    await ctx.send(f'계산 결과: {result}')

@bot.command(name='루루')
async def lulu(ctx):
    await ctx.send('Hi!')

bot.run(Token)

