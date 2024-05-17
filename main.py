import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from data import db_session
from data.task import Task

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
BOT_TOKEN = '6407358949:AAFkKp52Oj2So8-pA7R92baOJH4NUTrIpqw'


async def start(update, context):
    await update.message.reply_text('Начнём работу!')


async def add(update, context):
    await update.message.reply_text("Пожалуйста, напишите задачу. Для отмены введите /stop")
    return 'get_task'


async def get_task(update, context):
    text = update.message.text
    db_sess = db_session.create_session()
    if text:
        task = Task(
            task=text
        )
        db_sess.add(task)
        db_sess.commit()
        await update.message.reply_text('Задача успешно добавлена!')
        return ConversationHandler.END
    else:
        await update.message.reply_text('Я не понимаю вас :(')


async def tsk(update, context):
    db_sess = db_session.create_session()
    all_tasks = db_sess.query(Task).all()
    for elem in all_tasks:
        await update.message.reply_text(f"Задача №{elem.id}\n{elem.task}")


async def stop(update, context):
    await update.message.reply_text('Действие отменено')
    return ConversationHandler.END


def main():
    db_session.global_init("tg_db")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("tsk", tsk))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add)],
        states={'get_task': [MessageHandler(filters.TEXT & ~filters.COMMAND, get_task)]},
        fallbacks=[CommandHandler("stop", stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
