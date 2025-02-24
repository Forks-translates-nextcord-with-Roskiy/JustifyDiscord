import sys
import os
import aiohttp
import requests
from typing import Any, Union
import datetime
import subprocess
import random

from aeval import aeval
from textwrap3 import wrap
from .paginator import JustifyPaginatorInterface
import nextcord as disnake
from disnake.ext import commands


class JustifyUtils:

    __version__ = 'justify-1.0'

    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot

    async def eval_code(self, ctx: commands.Context, code: str) -> Any | None:
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'commands': commands,
            'disnake': disnake,
            '__import__': __import__,
            'sys': sys,
            'os': os,
            'aiohttp': aiohttp,
            'requests': requests,
            'datetime': datetime,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'subprocess': subprocess,
            'channel': ctx.channel,
            'random': random
        }
        
        return await aeval(self.remove_token_references(code), env, {})


    def remove_token_references(self, text: str):
        return text.replace(self.bot.http.token, "'token omitted'")
    

    async def _python_handler_result(self, ctx: commands.Context, result: str, prefix='', suffix='', length=2000):
        paginator = None

        if isinstance(result, disnake.Message):
            return await ctx.reply(f'Message({result.jump_url})')

        if not isinstance(result, str):
            result = repr(result)
        
        if len(result) >= 2000:
            paginator = JustifyPaginatorInterface(pages := [f"```{p}```" for p in wrap(result, length)])
            result = pages[0]

        await ctx.reply(f'{prefix}\n{result}{suffix}', view=paginator)


    async def shell_reader(self, ctx, commands: str) -> str:
        cmds = commands.split()
        byte_to_str = subprocess.check_output(cmds).decode('utf-8')
        result = '$ ' + "\n".join(cmds) + '\n\n' + byte_to_str

        return await self._python_handler_result(ctx, result, length=1900)
