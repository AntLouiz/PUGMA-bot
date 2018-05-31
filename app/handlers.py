from core.pugbot import PugBot
from telegram.ext import CommandHandler, Filters, MessageHandler


def start(bot, update):
    """Mostra um mensagem de apresentação do BOT."""
    message = 'Olá! Sou o Bot do Python User Group - MA (PUGMA)'
    bot.send_message(chat_id=update.message.chat_id, text=message)


def regras(bot, update):
    """Apresenta as regras do grupo."""
    message = PugBot().regras()
    bot.send_message(
        chat_id=update.message.chat_id,
        text=message,
        parse_mode='Markdown'
    )


def generate_hello_msg(username, is_bot):
    msg = ""
    if is_bot:
        msg =(
            '00101100 00100000 01101000 01100101 01101100 '
            '01101100 01101111 00100000 01101101 01111001 '
            '00100000 01100110 01100101 01101100 01101100 '
            '01101111 01110111 00100000 01101101 01100001 '
            '01100011 01101000 01101001 01101110 01100101 '
            '00100000 01100110 01110010 01101001 01100101 '
            '01101110 01100100 00100001'
        )
    else:
        msg = (
            'Seja bem vindo ao Python User Group - MA (PUG-MA). '
            'Um grupo para a galera de Python do Maranhão (ou não) que '
            'queira interagir e ficar por dentro do que está rolando na '
            'cena de Python aqui.'
        )

    if username is not None:
        msg = f'@{username}! ' + msg

    return msg
   

def hello_new_users(bot, update):
    """Recebe um usário novo no chat do grupo."""
    new_chat_members = update.message.new_chat_members

    for member in new_chat_members:
        user_id = member.id

        if user_id != bot.id:
            username, is_bot = member.username, member.is_bot

            message = generate_hello_msg(username, is_bot)

            bot.send_message(
                chat_id=update.message.chat_id,
                text=message
            )

            bot.send_message(
                chat_id=update.message.chat_id,
                text=PugBot().regras(),
                parse_mode='Markdown'
            )


def last_meetup(bot, update):
    """Apresenta o último meetup do PUG."""
    lastMeetup = PugBot().last_event()
    bot.send_photo(
        chat_id=update.message.chat_id,
        caption=lastMeetup['text'],
        photo=lastMeetup['photo']
    )


def meetup(bot, update, args):
    """
    Apresenta um meetup específico do PUG
    baseado no seu número de apresentação.
    """
    index = int(''.join(args))
    meetup = PugBot().event(index)
    bot.send_photo(
        chat_id=update.message.chat_id,
        caption=meetup['text'],
        photo=meetup['photo']
    )


START = CommandHandler('start', start)
NEW_USER = MessageHandler(
    Filters.status_update.new_chat_members,
    hello_new_users
)
LAST_MEETUP = CommandHandler('lastMeetup', last_meetup)
MEETUP = CommandHandler('meetup', meetup, pass_args=True)
RULES = CommandHandler('regras', regras)
