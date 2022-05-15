import time
from typing import Union
import sys

import disnake
from .services.utils import JustifyUtils
from disnake.ext import commands


class JustifyCog(commands.Cog):
    """Loads justify cog."""
    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot
        self.justify = JustifyUtils(bot)

    @commands.group(name='justify', aliases=['jst'], invoke_without_command=True)
    async def jst(self, ctx: commands.Context):
        text = (
            f'{self.justify.__version__}, disnake-{disnake.__version__}, {sys.version}.\n',
            f'Guilds: **{len(self.bot.guilds)}**, users: **{len(self.bot.users)}**',
            f'Cached messages: **{len(self.bot.cached_messages)}**\n',
            f'```py\nEnabled intents: {", ".join([i[0] for i in self.bot.intents if i[-1]])}```\n'
        )

        if isinstance(self.bot, commands.AutoShardedBot):
            text.append(f'Shards: ' + ', '.join(list(f"{i[0]} - {i[-1]}" for i in self.bot.latencies)))

        await ctx.reply(text)

    @jst.command(name='eval', aliases=['py'])
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, text: str):
        code = text.strip("\n").strip("```").lstrip("\n").lstrip("py").replace(self.bot.http.token, 'token deleted from code') if text.startswith("```py") else text.replace(self.bot.http.token, 'token deleted from code') # Колбаска ^-^
        start = time.time()
        
        try:
            result = str(await self.justify.eval_code(ctx, code))
            
        except Exception as exception:
            result = f"# An error occurred while executing the code :: \n{exception.__class__}: {exception}"
        
        finally:
            execution_time = (time.time() - start)
            await ctx.send(f"Completed for **{execution_time} seconds.**\n```py\n{result}\n```")
        

def setup(bot):
    bot.add_cog(JustifyCog(bot))
