import re
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import save_lesson
from database import save_lesson, lesson_exists
router = Router()

class CreateLessonForm(StatesGroup):
    """Class for managing states of the lesson creation form."""
    waiting_for_lesson_name = State() # State of waiting for lesson name input
    waiting_for_lesson_words = State() # State of waiting for lesson words input

# Handler for the /start command
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hi, {message.from_user.first_name}! 👋\n"
        "Ready to tackle some new English words today?"
    )

@router.message(Command("create_lesson"))
async def cmd_create_lesson(message: types.Message, state: FSMContext):
    """Handler for the /create_lesson command to create a new lesson."""
    await message.answer("Please enter the name of the lesson:")
    await state.set_state(CreateLessonForm.waiting_for_lesson_name)

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
