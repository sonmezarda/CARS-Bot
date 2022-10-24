import discord
import json

def create_task_embed(task_name,tasks_path='./bin/tasks.json'):
    with open(tasks_path, 'r', encoding='utf-8') as task_file:
        tasks = json.load(task_file)
    task = tasks[task_name]
    color = int(task["color"], 16)
    print(color)
    embed = discord.Embed(title=task["title"], color=color)
    for field in task["fields"]:
        expected_files = '\n🔹' +'\n🔹'.join(field['expected_files'])
        field_msg = f"\n:bookmark_tabs: **Ödev açıklaması:**\n\n {field['desc']}\nBeklenen Dosyalar:{expected_files}"
        embed.add_field(name=field["name"], value=field_msg)
    embed.set_footer(text=task["footer"])
    return embed

def get_task(task_name, tasks_path='./bin/tasks.json'):
    with open(tasks_path, 'r', encoding='utf-8') as task_file:
        tasks = json.load(task_file)
    task = tasks[task_name]
    return task