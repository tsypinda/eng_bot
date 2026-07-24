import re
from aiogram import Router, types
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import remove_words, save_lesson, lesson_exists, delete_lesson, add_words, show_words, show_lessons
router = Router()

class CreateLessonForm(StatesGroup):
    """Class for managing states of the lesson creation form."""
    waiting_for_lesson_name = State() # State of waiting for lesson name input
    waiting_for_lesson_words = State() # State of waiting for lesson words input

class EditLessonForm(StatesGroup):
    """Class for managing states of the lesson editing form."""
    editing_active = State() # State of waiting for lesson editing input

class DeleteLessonForm(StatesGroup):
    """Class for managing states of the lesson deletion form."""
    waiting_for_lesson_name = State() # State of waiting for lesson name input

# Handler for the /start command
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hi, {message.from_user.first_name}! 👋\n"
        "Ready to tackle some new English words today?"
    )

@router.message(Command("create_lesson"))
async def cmd_create_lesson(message: types.Message, command: CommandObject, state: FSMContext):
    if command.args:
        lesson_name = command.args.strip()
        if lesson_exists(message.from_user.id, lesson_name):
            await message.answer(f"A lesson with the name '{lesson_name}' already exists. Please choose a different name:")
            return
        await state.update_data(lesson_name=lesson_name)
        await message.answer("Great! Now, please enter the words for the lesson:")
        await state.set_state(CreateLessonForm.waiting_for_lesson_words)
    else:
        await message.answer("Please enter the name of the lesson:")
        await state.set_state(CreateLessonForm.waiting_for_lesson_name)

@router.message(Command('delete_lesson'))
async def cmd_delete_lesson(message: types.Message, command: CommandObject, state: FSMContext):
    if command.args:
        lesson_name = command.args.strip()
        if not lesson_exists(message.from_user.id, lesson_name):
            await message.answer(f"Lesson '{lesson_name}' does not exist.")
            return
        delete_lesson(message.from_user.id, lesson_name)
        await message.answer(f"Lesson '{lesson_name}' has been deleted.")
    else:
        await message.answer("Please enter the name of the lesson to delete:")
        await state.set_state(DeleteLessonForm.waiting_for_lesson_name)

@router.message(Command('cancel'), DeleteLessonForm.waiting_for_lesson_name)
async def cmd_cancel_delete_lesson(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Lesson deletion cancelled.")

@router.message(DeleteLessonForm.waiting_for_lesson_name)
async def process_delete_lesson_name(message: types.Message, state: FSMContext):
    lesson_name = message.text.strip()
    if not lesson_exists(message.from_user.id, lesson_name):
        await message.answer(f"Lesson '{lesson_name}' does not exist.")
        return
    delete_lesson(message.from_user.id, lesson_name)
    await state.clear()
    await message.answer(f"Lesson '{lesson_name}' has been deleted.")

@router.message(Command('cancel'), CreateLessonForm.waiting_for_lesson_name)
async def cmd_cancel_create_lesson(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Lesson creation cancelled.")

@router.message(Command('edit'))
async def cmd_edit_lesson(message: types.Message, command: CommandObject, state: FSMContext):
    if not command.args:
        await message.answer("Please provide the lesson name, Usage: /edit <Lesson Name>")
        return
    lesson_name = command.args.strip()

    if not lesson_exists(message.from_user.id, lesson_name):
        await message.answer(f"Lesson '{lesson_name}' does not exist.")
        return
    
    await state.update_data(lesson_name=lesson_name)
    await state.set_state(EditLessonForm.editing_active)

@router.message(Command('add'), EditLessonForm.editing_active)
async def cmd_add_words(message: types.Message, command: CommandObject, state: FSMContext):
    if not command.args:
        await message.answer("Please provide the words to add, Usage: /add <word1> <word2> ...")
        return
    new_words = command.args.split()
    data = await state.get_data()
    lesson_name = data.get("lesson_name")

    add_words(message.from_user.id, lesson_name, new_words)
    await message.answer(f"Added {len(new_words)} words to lesson '{lesson_name}'.")

@router.message(Command('remove'), EditLessonForm.editing_active)
async def cmd_remove_words(message: types.Message, command: CommandObject, state: FSMContext):
    if not command.args:
        await message.answer("Please provide the words to remove, Usage: /remove <word1> <word2> ...")
        return
    words_to_remove = command.args.split()
    data = await state.get_data()
    lesson_name = data.get("lesson_name")

    remove_words(message.from_user.id, lesson_name, words_to_remove)
    await message.answer(f"Removed {len(words_to_remove)} words from lesson '{lesson_name}'.")

@router.message(Command('exit'), EditLessonForm.editing_active)
async def cmd_exit_editing(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Editing session ended.")

@router.message(Command('show_lessons'))
async def cmd_show_lessons(message: types.Message):
    lessons = show_lessons(message.from_user.id)
    if not lessons:
        await message.answer("You have no lessons yet.")
    else:
        await message.answer(f"Your lessons:\n{chr(10).join(lessons)}")

@router.message(Command('show_words'), EditLessonForm.editing_active)
async def cmd_show_words(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lesson_name = data.get("lesson_name")
    words = show_words(message.from_user.id, lesson_name)
    if not words:
        await message.answer(f"No words found in lesson '{lesson_name}'.")
    else:
        await message.answer(f"Words in lesson '{lesson_name}':\n{chr(10).join(words)}")

@router.message(Command('show_words'))
async def cmd_show_words_no_state(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("Please provide the lesson name, Usage: /show_words <Lesson Name>")
        return
    lesson_name = command.args.strip()
    if not lesson_exists(message.from_user.id, lesson_name):
        await message.answer(f"Lesson '{lesson_name}' does not exist.")
        return
    words = show_words(message.from_user.id, lesson_name)
    if not words:
        await message.answer(f"No words found in lesson '{lesson_name}'.")
    else:
        await message.answer(f"Words in lesson '{lesson_name}':\n{chr(10).join(words)}")

@router.message(CreateLessonForm.waiting_for_lesson_name)
async def process_lesson_name(message: types.Message, state: FSMContext):
    """Handler for processing the lesson name input."""
    lesson_name = message.text.strip()
    if not lesson_name:
        await message.answer("Lesson name cannot be empty. Please enter a valid name:")
        return
    
    if lesson_exists(message.from_user.id, lesson_name):
        await message.answer(f"A lesson with the name '{lesson_name}' already exists. Please choose a different name:")
        return
    
    await state.update_data(lesson_name=lesson_name)
    await message.answer("Great! Now, please enter the words for the lesson:")
    await state.set_state(CreateLessonForm.waiting_for_lesson_words)

@router.message(CreateLessonForm.waiting_for_lesson_words)
async def process_lesson_words(message: types.Message, state: FSMContext):
    """Handler for processing the lesson words input."""
    lesson_words = message.text.strip()
    if not lesson_words:
        await message.answer("Lesson words cannot be empty. Please enter some words:")
        return
    # Extract words from the input, convert to lowercase, and remove duplicates
    words_list = re.findall(r'[a-zA-Z]+', lesson_words.lower())
    unique_words = list(set(words_list))  # Remove duplicates
    if not unique_words:
        await message.answer("No valid words found. Please enter the words again:")
        return
    # Get data from the state
    data = await state.get_data()
    lesson_name = data.get("lesson_name")

    # Save the lesson to the database
    save_lesson(message.from_user.id, lesson_name, unique_words)

    # Complete the state
    await state.clear()

    formatted_words = ', '.join(unique_words)
    await message.answer(f"The lesson '{lesson_name}' is successfully created!\nUnique words: {len(unique_words)}\nWords: {formatted_words}")
