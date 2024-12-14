import discord
import google.generativeai as genai

intents = discord.Intents.all()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

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
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

"""
如果你想啟用調整模型參數，請取消註解 generation_config=generation_config 這行。
如果你想使用不同的模型，請修改 model_name="" 這行。

請注意，如果你的 Request/Token 數量太多或者選到需要付費的模型，可能會被收錢。

截至目前(2024/12/15)，你可以使用的模型有：
- "gemini-1.5-pro"
- "gemini-1.5-flash"
- "gemini-1.5-8b"
- "gemini-2.0-flash-exp"
- "gemini-exp-1206" (Preview)
- "gemini-exp-1121" (Preview)
- "learnlm-1.5-pro-experimental"
- "gemma-2-2b-it"
- "gemma-2-9b-it"
- "gemma-2-27b-it"

請參考 https://aistudio.google.com/ 右側模型列表來選擇適合的模型。
"""
model = genai.GenerativeModel(
    model_name="MODEL_NAME_HERE",
    system_instruction=system_prompt,
    # generation_config=generation_config,
)

@bot.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {bot.user}')

"""
定義一個斜線指令，根據使用者的 prompt 生成回應
指令使用方法：/ask <prompt>
"""
@tree.command(name="ask", description="Ask a question to the AI assistant.")
async def ask(interaction: discord.Integration, *, user_prompt: str):
    try:
        prompts = [
            {"role": "user", "parts": user_prompt}
        ]
        response = model.generate_content(prompts)
        if response.text:
            await interaction.response.send_message(response.text)
        else:
            await interaction.response.send_message("發生錯誤，請再試一次")
    except Exception as e:
        await interaction.response.send_message(f"發生錯誤: {e}")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)