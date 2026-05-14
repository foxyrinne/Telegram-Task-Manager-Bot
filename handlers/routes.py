from aiogram import Router, F
from aiogram.types import Message

from db import add_task, get_tasks, get_task_id_by_index, mark_task_done, delete_task


router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message) -> None:
    """Handler for the /start command."""
    await message.answer("Hello! I'm your task manager bot. You can add tasks by sending me a message, and I'll keep track of them for you.\n\nCommands:\n/add <task description> - Add a new task\n/tasks - List all your tasks\n/done <task number> - Mark a task as done\n/delete <task number> - Delete a task")


@router.message(F.text.startswith("/add"))
async def add_task_handler(message: Message) -> None:
    """Handler for adding a new task."""
    description = message.text[4:].strip()
    if not description:
        await message.answer("Please provide a task description after the /add command. Example: /add Buy groceries")
        return

    await add_task(message.from_user.id, description)
    await message.answer(f"Task added: {description}")


@router.message(F.text == "/tasks")
async def list_tasks_handler(message: Message) -> None:
    """Handler for listing all tasks."""
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("You have no tasks.")
        return

    response = "Your tasks:\n"
    for index, (_, description, is_done) in enumerate(tasks, start=1):
        status = "✅" if is_done else "❌"
        response += f"{index}. {status} {description}\n"

    response += "\nUse /done <number> или /delete <number>."
    await message.answer(response)


@router.message(F.text.startswith("/done"))
async def mark_task_done_handler(message: Message) -> None:
    """Handler for marking a task as done by user-specific task number."""
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer("Please provide a task number after the /done command. Example: /done 1")
        return

    try:
        task_index = int(args[1].strip())
    except ValueError:
        await message.answer("Please provide a valid task number after the /done command. Example: /done 1")
        return

    task_id = await get_task_id_by_index(message.from_user.id, task_index)
    if task_id is None:
        await message.answer("Task number not found. Use /tasks to see your task numbers. Example: /done 1")
        return

    await mark_task_done(task_id)
    await message.answer(f"Task #{task_index} marked as done.")


@router.message(F.text.startswith("/delete"))
async def delete_task_handler(message: Message) -> None:
    """Handler for deleting a task by user-specific task number."""
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer("Please provide a task number after the /delete command. Example: /delete 1")
        return

    try:
        task_index = int(args[1].strip())
    except ValueError:
        await message.answer("Please provide a valid task number after the /delete command. Example: /delete 1")
        return

    task_id = await get_task_id_by_index(message.from_user.id, task_index)
    if task_id is None:
        await message.answer("Task number not found. Use /tasks to see your task numbers. Example: /delete 1")
        return

    await delete_task(task_id)
    await message.answer(f"Task #{task_index} has been deleted.")