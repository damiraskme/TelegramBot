import logging
import os
from aiogram import types
from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext
import basic_func

from bot_states import note_states, function_form


bot = basic_func.bot
dp = basic_func.dp

async def note_choice(message: types.Message, state: FSMContext):
    await function_form.note.set()
    await message.reply("What do you want to do?\nYou can clear notes with /clear\nOr add note with /add\nAlso you can view all your notes with /view")


async def note_clear(message: types.Message, state: FSMContext):
    with open(f"note/{message.from_user.mention}.txt", "w", encoding="utf-8"):
        pass
    await function_form.note.set()
    await message.answer("Notes are cleaned!")
    await message.answer("Want to do something else?\nYou can clear notes with /clear\nOr add note with /add\nAlso you can view all your notes with /view")


async def note_view(message: types.Message, state: FSMContext):
    if (os.stat(f"note/{message.from_user.mention}.txt").st_size == 0):
        await function_form.note.set()
        await message.reply("Notes are empty")
        await message.answer("Want to do something else?\nYou can clear notes with /clear\nOr add note with /add\nAlso you can view all your notes with /view")
    else:
        with open(f"note/{message.from_user.mention}.txt", "r", encoding="utf-8") as read_note:
            note_read = read_note.read()
        await function_form.note.set()
        await message.answer(note_read, disable_web_page_preview=True)
        await message.answer("Want to do something else?\nYou can clear notes with /clear\nOr add note with /add\nAlso you can view all your notes with /view")

async def note_first(message: types.Message, state: FSMContext):
    await note_states.note_add_1.set()
    await message.answer("Send name for note")

async def note_name_remember(message: types.Message, state: FSMContext):
    with open(f"note/{message.from_user.mention}.txt", "a", encoding="utf-8") as note_write:
        note_write.write(f"{str(message.text)}: ")
    await note_states.note_add_2.set()
    await message.answer("Now send additional information for note")

async def note_second(message: types.Message, state: FSMContext):
    with open(f"note/{message.from_user.mention}.txt", "a", encoding="utf-8") as note_write:
        note_write.write(str(message.text))
        note_write.write("\n")
    await function_form.note.set()
    await message.answer("Note added!\nWant to do something else?\nYou can clear notes with /clear\nOr add note with /add\nAlso you can view all your notes with /view")
    
def setup(dp: Dispatcher):
    dp.register_message_handler(note_choice, state=function_form.function_choice, commands=["note"])
    dp.register_message_handler(note_clear, state=function_form.note, commands=["clear"])
    dp.register_message_handler(note_view, state=function_form.note, commands=["view"])

    dp.register_message_handler(note_first, state=function_form.note, commands=["add"])
    dp.register_message_handler(note_name_remember, state=note_states.note_add_1)
    dp.register_message_handler(note_second, state=note_states.note_add_2)