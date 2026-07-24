# GB Eng_bot

> Telegram bot for interactive English learning with games. MVP version

## Features

At the moment, the bot can:
- Create and delete lessons
- Edit previously created lessons
- Show the list of lessons and the list of words in the current lesson

## Usage

The following commands are currently available for working with lessons:

- `/start` — displays the welcome message
- `/show_lessons` — shows all previously created lessons
- `/show_words [Lesson name]` — shows all words in the specified lesson
- `/delete_lesson [Lesson name]` — deletes the lesson
- `/cancel` — cancels delete or create operations
- `/edit [Lesson name]` — switches to edit mode
- `/add <word1, word2, ...>` — adds new words (only in edit mode)
- `/remove <word1, word2, ...>` — removes words (only in edit mode)
- `/show` — shows all words in the lesson (only in edit mode)
