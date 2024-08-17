import asyncio

from telebot.asyncio_filters import ForwardFilter
from telebot.asyncio_filters import IsDigitFilter
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import StateFilter

from Bot.Handlers.EditAccountActionsHandler import _sendAddAdvChatText
from Bot.Handlers.EditAccountActionsHandler import _sendChangeAccountMessageText
from Bot.Handlers.EditAccountActionsHandler import _sendChangePromptText
from Bot.Handlers.EditAccountActionsHandler import _sendChangeStatusMenu
from Bot.Handlers.EditAccountActionsHandler import _sendChangeTargetChannelText
from Bot.Handlers.EditAccountActionsHandler import _sendDeleteAccountText
from Bot.Handlers.EditAccountActionsHandler import _sendReloadYandexGPTMessageText
from Bot.Handlers.EditAccountActionsHandler import _sendRemoveAdvChatText
from Bot.Handlers.EditAccountActionsHandler import _set_status_off
from Bot.Handlers.EditAccountActionsHandler import _set_status_on
from Bot.Handlers.EditAccountActionsHandler import _sendChangeDelayText

from Bot.Handlers.ServiceMenuHandler import _serviceMenu

from Bot.Handlers.EditAccountVisualMenuHandler import _visualConfig
from Bot.Handlers.EditAccountVisualMenuHandler import _accountSessionsList
from Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeFirstNameText
from Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeLastNameText
from Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeUsernameText
from Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeProfilePictureText
from Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeAccountDescriptionText

from Bot.Handlers.SpamTgHandler import _spamTg
from Bot.Handlers.SpamInstHandler import _spamInst

from Bot.Handlers.StoriesMenuHandler import _stories
from Bot.Handlers.StoriesMenuHandler import _showAccountStories
from Bot.Handlers.StoriesMenuHandler import _aioschedulerStoriesMenu
from Bot.Handlers.StoriesActionsHandler import _sendAddTargetChatText
from Bot.Handlers.StoriesActionsHandler import _sendDeleteTargetChatText
from Bot.Handlers.StoriesActionsHandler import _launchStories
from Bot.Handlers.StoriesActionsHandler import _setDelayForAioschedulerText
from Bot.Handlers.StoriesActionsHandler import _changeStatusForAioscheduler
from Bot.Handlers.StoriesActionsHandler import _errorNoTargetChannels

from Bot.Handlers.EditAccountsMenuHandler import _editAccountsMenu
from Bot.Handlers.EditAccountsMenuHandler import _showAccountActions
from Bot.Handlers.EditAccountsInstMenuHandler import _editAccountsInstMenu
from Bot.Handlers.EditAccountsInstMenuHandler import _showAccountInstActions

from Bot.Handlers.EditAccountInstActionsHandler import _sendUpdateMessageText
from Bot.Handlers.EditAccountInstActionsHandler import _sendAddTargetChannelText
from Bot.Handlers.EditAccountInstActionsHandler import _sendRemoveTargetChannelText
from Bot.Handlers.EditAccountInstActionsHandler import _sendDeleteAccountInstText
from Bot.Handlers.EditAccountInstActionsHandler import _changeStatusAccountInst
from Bot.Handlers.EditAccountInstActionsHandler import _errorNoTargetInstChannels
from Bot.Handlers.EditAccountInstActionsHandler import _sendAddProxyText
from Bot.Handlers.EditAccountInstActionsHandler import _setDelayForInstText
from Bot.Handlers.EditAccountInstActionsHandler import _updateReelsLinkText
from Bot.Handlers.EditAccountInstActionsHandler import _errorInsufficientAmountOfProxies
from Bot.Handlers.EditAccountInstActionsHandler import _errorNoMessageAndNoReels
from Bot.Handlers.EditAccountInstActionsHandler import _sendDeleteProxyText

from Bot.Handlers.NewAccountHandler import _newAccountMenu
from Bot.Handlers.NewAccountInstHandler import _getInstAccountLogin
from Bot.Handlers.NewAccountInstHandler import _getInstAccountPassword
from Bot.Handlers.NewAccountInstHandler import _getProxyAddress

from Bot.Markups import MarkupBuilder  # noqa
from Bot.Middlewares import FloodingMiddleware
from Config import account_context
from Config import bot
from Config import message_context_manager
from Config import REDQUIRED_AMOUNT_OF_PROXIES
from Config import singleton
from Database.DAL.AccountTgDAL import AccountDAL
from Database.DAL.AccountStoriesDAL import AccountStoriesDAL
from Database.session import async_session
from Database.DAL.AccountInstDAL import AccountInstDAL
from Database.DAL.ProxyDAL import ProxyAddressDAL
from Database.AlembicWrapper import asyncInitializeDatabase
from Database.AlembicWrapper import initializeDatabase


@singleton
class Bot:

    bot.add_custom_filter(StateFilter(bot))

    def __init__(self):
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.add_custom_filter(IsDigitFilter())
        bot.setup_middleware(FloodingMiddleware(1))

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def HandlerInlineMiddleware(call):
        # ------------------menu----------------------

        if call.data == "back_to_service_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _serviceMenu(message=call.message)

        if call.data == "new_account_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _newAccountMenu(call.message)

        if call.data == "spam_tg" or call.data == "back_to_spam_tg":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _spamTg(message=call.message)
        
        if call.data == "acc_edit" or call.data == "back_to_acc_edit":
            
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _editAccountsMenu(message=call.message)
        
        if "edit_account" in call.data or "back_to_edit_menu" in call.data:
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _showAccountActions(message=call.message, account_name=account_name)

        if call.data == "vis_cfg": 
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _accountSessionsList(message=call.message)
        
        if call.data == "back_to_vis_cfg":
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            await _accountSessionsList(message=call.message)


        if "viscfg_account" in call.data or "back_to_viscfg_account" in call.data:
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            
            await _visualConfig(account_name=account_name, message=call.message)

        # ------------------stories------------------

        if call.data == "stories_menu" or call.data == "back_to_stories_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            
            await _showAccountStories(message=call.message)

        if "look_stories" in call.data or "back_to_look_stories" in call.data:
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _stories(account_name=account_name, message=call.message)
        

        # --------------stories actions--------------
        
        if "add_trgt_chnl" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendAddTargetChatText(message=call.message)
        
        if "delete_trgt_chnl" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendDeleteTargetChatText(message=call.message)
        
        if "stories_service" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
  
            await _launchStories(message=call.message)
        
        if "aiosheduler_stories" in call.data or "back_to_aiosheduler_stories" in call.data:
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
  
            await _aioschedulerStoriesMenu(message=call.message)

        if "chng_delay" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
  
            await _setDelayForAioschedulerText(message=call.message)
        
        if "chng_status" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            async with async_session() as session:
                account_stories_dal = AccountStoriesDAL(session)
                account = await account_stories_dal.getAccountBySessionName(
                    session_name=account_name
                )
                if (account.target_channels == None):
                    await _errorNoTargetChannels(call.message)
                elif (len(account.target_channels) == 0):
                    await _errorNoTargetChannels(call.message)
                else:
                    new_status = (False if account.aioscheduler_status else True)
                    await account_stories_dal.updateStatus(
                        session_name=account_name,
                        new_status=new_status
                    )
    
                    await _changeStatusForAioscheduler(message=call.message, status=new_status)

        # -------editing visual account config-------
    
        if "chng_first_name" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeFirstNameText(message=call.message)

        if "chng_last_name" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeLastNameText(message=call.message)        
        
        if "chng_username" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeUsernameText(message=call.message)   
        
        if "chng_pfp" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeProfilePictureText(message=call.message)   
        
        if "chng_profile_desc" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeAccountDescriptionText(message=call.message)   

        # ---------------bot editing-----------------
            
        if "change_acc_msg" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendChangeAccountMessageText(call.message)

        if "change_prompt" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendChangePromptText(call.message)

        if "change_delay" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendChangeDelayText(call.message)

        if "add_adv_chat" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendAddAdvChatText(call.message)

        if "remove_adv_chat" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendRemoveAdvChatText(call.message)

        if "change_target_channel" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendChangeTargetChannelText(call.message)

        if "change_status" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendChangeStatusMenu(call.message)

        if "reload_chatgpt_message" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendReloadYandexGPTMessageText(call.message)

        if "delete_account" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendDeleteAccountText(call.message)

        if "set_status_on" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            async with async_session() as session:
                account_dal = AccountDAL(session)
                await account_dal.updateStatus(session_name=account_name, status=True)

            await _set_status_on(call.message)

        if "set_status_off" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            async with async_session() as session:
                account_dal = AccountDAL(session)
                await account_dal.updateStatus(session_name=account_name, status=False)

            await _set_status_off(call.message)

        # ---------------inst menu-----------------
        
        if call.data == "spam_inst" or call.data == "back_to_spam_inst":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _spamInst(message=call.message)

        if call.data == "logging_in_inst" or call.data == "back_to_logging_in_inst":
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _getInstAccountLogin(message=call.message)
        
        if call.data == "back_to_get_password":
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _getInstAccountPassword(message=call.message)
        
        if call.data == "back_to_get_proxy":
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _getProxyAddress(message=call.message)
        
        if call.data == "inst_acc_edit" or call.data == "back_to_inst_acc_edit":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )

            await _editAccountsInstMenu(message=call.message)

        if "edit_inst_account" in call.data or "back_to_edit_inst_account" in call.data:
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _showAccountInstActions(message=call.message, account_name=account_name)
        
        if "change_acc_inst_msg" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendUpdateMessageText(message=call.message)

        if "add_target_chat" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendAddTargetChannelText(message=call.message)
        
        if "remove_target_chat" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendRemoveTargetChannelText(message=call.message)
        
        if "delete_inst_account" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendDeleteAccountInstText(message=call.message)
        
        if "chng_inst_status" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            async with async_session() as session:
                account_inst_dal = AccountInstDAL(session)
                proxy_dal = ProxyAddressDAL(session)
                account = await account_inst_dal.getAccountBySessionName(
                    session_name=account_name
                )
                proxies = await proxy_dal.getProxyAddressById(
                    account_inst_id=account.id
                )
                amount_of_proxies = len(proxies)
                if (amount_of_proxies < REDQUIRED_AMOUNT_OF_PROXIES):
                    await _errorInsufficientAmountOfProxies(call.message, amount_of_proxies)
                elif (account.target_channels == None):
                    await _errorNoTargetInstChannels(call.message)
                elif (len(account.target_channels) == 0):
                    await _errorNoTargetInstChannels(call.message)
                elif (account.message == "Не указано" and account.reels_link == "Не указана"):
                    await _errorNoMessageAndNoReels(call.message)
                else:
                    new_status = (False if account.status else True)
                    await account_inst_dal.updateStatus(
                        session_name=account_name,
                        new_status=new_status
                    )
                    await _changeStatusAccountInst(message=call.message, status=new_status)
        
        if "add_proxy" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendAddProxyText(message=call.message)
        
        if "delete_proxy" in call.data:
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendDeleteProxyText(message=call.message)
        
        if "chng_inst_delay" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
  
            await _setDelayForInstText(message=call.message)
        
        if "add_reels_link" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
  
            await _updateReelsLinkText(message=call.message)
        

        

            
    @staticmethod
    async def polling():
        task1 = asyncio.create_task(bot.infinity_polling())
        await task1


if __name__ == "__main__":
    b = Bot()
    loop = asyncio.get_event_loop()
    
    initializeDatabase()

    try:
        loop.run_until_complete(b.polling())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
