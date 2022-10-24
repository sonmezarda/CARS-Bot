import discord
import asyncio
from datetime import datetime
import os
from tools.bot_tools import create_task_embed, get_task

from discord.ext import commands
from discord.ui import Button, View


class TaskHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('TaskHandler Loaded!')

    async def complete_task(self, interaction):
        task = get_task("task1")
        messages = [message async for message in interaction.channel.history(limit=123) if message.author == interaction.user and message.attachments != []]
        for m in messages:
            for file in m.attachments:
                if file.filename in task["expected_files"]:
                    if not os.path.isdir(f'files/{m.author.id}'):
                        os.mkdir(f'files/{m.author.id}')
                    await file.save(f'files/{m.author.id}/{file.filename}')
                    with open(f'files/{m.author.id}/info.txt', 'w', encoding='utf-8') as info_file:
                        now = datetime.now()
                        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")

                        info_file.write(
                            f'id={m.author.id}\nname={m.author.name}\nnick={m.author.nick}\ntime={current_time}')

                    await interaction.channel.send(f"🟩 '{file.filename}' dosyası başarıyla alındı alındı.")
                else:
                    await interaction.channel.send(f"🟥 '{file.filename}' dosyası gönderilmesi gereken dosyalar içerisinde yok.\nLütfen dosya ismini kontrol edin!")

    async def create_task_channel(self, interaction):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(
                read_messages=True)
        }
        task_channel = await interaction.guild.create_text_channel(name="odev_teslim_kanalı", overwrites=overwrites)

        task_complete_button = Button(
            label="❗ Ödevi Gönder ❗", style=discord.ButtonStyle.green)
        task_complete_button.callback = self.complete_task
        view = View()
        view.add_item(task_complete_button)

        task_embed = create_task_embed("task1")

        await task_channel.send('sa', embed=task_embed, view=view)
        await interaction.response.send_message('Ödev kanalını başarıyla oluşturdum!✨', ephemeral=True)

        timer_msg = await task_channel.send(f'Bu kanal x saniye sonra silinecek!')
        for i in range(0, 100):
            await timer_msg.edit(content=f'Bu kanal {100-i} saniye sonra silinecek!')
            await asyncio.sleep(1)
        await timer_msg.edit(content="Kanal siliniyor...")

        await task_channel.delete()

    @commands.command()
    async def tasks(self, ctx):
        button = Button(label="Odev Teslim",
                        style=discord.ButtonStyle.green, emoji="✔")
        button.callback = self.create_task_channel
        view = View()
        view.add_item(button)
        await ctx.send("Deneme", view=view)
