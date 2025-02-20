import interactions
from interactions import slash_command, listen, SlashContext
import google.generativeai as genai

intents = interactions.Intents.ALL
intents.message_content = True
bot = interactions.Client(intents=intents)

# 請登入 https://discord.com/developers/applications，創建機器人，取得 Token 並填入此處
DISCORD_TOKEN = "YOUR_DISCORD_TOKEN_HERE" 

# 請到 https://aistudio.google.com/，按下 Get API Key 取得 API Key 並填入此處
GENAI_API_KEY = "YOUR_AI_STUDIO_API_KEY_HERE" 
genai.configure(api_key=GENAI_API_KEY)

"""
這裡是系統提示，這是讓 AI 能夠正確運作的重要部分。
這將定義 AI 的角色、行為和任務，並確保 AI 能夠符合使用者的要求。
範例的系統提示並不完整也不一定是最好的，請根據您的需求進行修改。

Example: 
你是一名 Google Developer Groups On Campus 的核心成員，專注於協助學生使用 Flutter 以及 GCP 進行開發，擁有豐富的專案開發經驗。

你可以參考這個連結來了解更多：
https://github.com/google-gemini/cookbook/blob/main/quickstarts/System_instructions.ipynb
"""
system_prompt = [
    "你是一名 AI 助理，",
    "你喜歡且會盡可能地幫助使用者解決任何程式開發相關的問題。",
    "你全程都必須使用繁體中文溝通",
]


"""
這裡可以調整模型參數，如果你想套用這些參數，請查看下方註解。
"""
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

"""
這段程式碼將列出可用的模型
"""

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

"""
如果你想使用不同的模型，請修改 model_name="" 這行。

你可以自行決定要使用哪個版本的模型，

注意：若要進一步了解頻率限制和模型功能，請參考 Gemini 模型

此段程式碼來源：(https://ai.google.dev/gemini-api/docs/get-started/tutorial?lang=python)
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_prompt,
    generation_config=generation_config,
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

"""
定義一個斜線指令，根據使用者的 prompt 生成回應
指令使用方法：/ask <prompt>
"""
@slash_command(name = "ask",
        description="與機器人聊天",
        options=[
            interactions.SlashCommandOption( # 定義指令選項
            name="prompt", # 選項名稱，注意：必須與下方定義函數的參數名稱相同，如果你想使用不同的參數名稱，請在 @slash_command() 裡使用 argument_name 參數
            description="輸入你想要對機器人說的話", # 選項的描述
            type=3, # 這個參數型別是字串
            required=True # True 表示這個參數必填
            )
        ]
) # 新增一個叫做 ask 的 command
async def chat(ctx: SlashContext, prompt: str):
    # 因為 Discord Bot 若沒有回應超過五秒就會 Timeout，因此需要使用 defer() 告訴 Discord 需要等待
    await ctx.defer() 
    # 設定使用者的 prompt
    content = [
        {
            "role": "user",
            "parts": prompt
        }
    ]
    try:
        response = model.generate_content(content)
        if response.text:
            await ctx.send(response.text)
        else:
            await ctx.send("目前機器人無法回應，請稍後再試")
    except Exception as e:
        await ctx.send("目前機器人無法回應，請稍後再試: " + str(e))
  
    return

if __name__ == '__main__':
    bot.start(DISCORD_TOKEN)