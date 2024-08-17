import telebot

from Bot.Markups import MarkupBuilder
from Config import bot
from Config import message_context_manager
from Config import sessions_dirPath
from Database.DAL.AccountTgDAL import AccountDAL
from Database.session import async_session

@bot.message_handler(commands=["help", "start"])
async def _serviceMenu(message):

    msg = await bot.send_message(message.chat.id, 
        MarkupBuilder.welcome_text,
        reply_markup=MarkupBuilder.AccountListServices(),
        parse_mode="MarkdownV2"
    )
    
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

