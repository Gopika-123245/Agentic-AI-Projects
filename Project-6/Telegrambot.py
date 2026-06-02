import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

from autogen import AssistantAgent

# LOAD ENV VARIABLES
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# GROQ LLM CONFIG
llm_config = {
    "config_list": [
        {
            "model": "llama-3.1-8b-instant",
            "api_key": GROQ_API_KEY,
            "base_url": "https://api.groq.com/openai/v1",
            "price": [0, 0]
        }
    ],
    "temperature": 0.7
}

# THINKER AGENT
thinker = AssistantAgent(
    name="Thinker",
    llm_config=llm_config,
    system_message="Understand the user message briefly."
)

# WRITER AGENT
writer = AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="Reply shortly in max 10 lines."
)

# CHATBOT FUNCTION
async def chatbot(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # user message
    user_message = update.message.text

    print("👤 USER MESSAGE:")
    print(user_message)

    # thinker agent
    analysis = thinker.generate_reply(
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    print("\n🧠 THINKER AGENT:")
    print(analysis)

    # writer agent
    reply = writer.generate_reply(
        messages=[
            {
                "role": "user",
                "content": f"""
                User: {user_message}

                Analysis: {analysis}
                """
            }
        ]
    )

    print("\n✍️ WRITER AGENT:")
    print(reply)


    # telegram reply
    await update.message.reply_text(
        str(reply)
    )

# TELEGRAM APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chatbot
    )
)

print("🚀 Bot Running...")

app.run_polling()
