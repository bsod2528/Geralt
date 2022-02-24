import io
import os
import aiohttp
import disnake
import traceback

from disnake.ext import commands
from disnake.enums import ButtonStyle
from disnake.webhook.async_ import Webhook

from __main__ import CONFIG
import Source.Kernel.Views.Interface as Interface

class ErrorHandler(commands.Cog):
    """Global Error Handling"""
    def __init__(self, bot):
        self.bot        =   bot        
        self.session    =   aiohttp.ClientSession()
        self.webhook    =   Webhook.from_url(CONFIG.get("ERROR"), session = self.session)
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return

        ERROR   =   getattr(error, "original", error)
            
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.DisabledCommand):
            await ctx.trigger_typing()
            return await Interface.Traceback(self.bot, ctx, ERROR).SEND(ctx)
    
        if  isinstance(error, commands.BotMissingPermissions):
            await ctx.trigger_typing()
            return await Interface.Traceback(self.bot, ctx, ERROR).SEND(ctx)
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.trigger_typing()
            return await Interface.Traceback(self.bot, ctx, ERROR).SEND(ctx)

        if isinstance(error, commands.NotOwner):
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.trigger_typing()
            return await Interface.CommandSyntax(self.bot, ctx, ERROR).SEND(ctx)
        
        if isinstance(error, commands.MemberNotFound):
            await ctx.trigger_typing()
            return await Interface.Traceback(self.bot, ctx, ERROR).SEND(ctx)

        if isinstance(error, commands.BadArgument):
            await ctx.trigger_typing()
            return await Interface.Traceback(self.bot, ctx, ERROR).SEND(ctx)
           
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.trigger_typing()
            return await Interface.Traceback(self.bot, ctx, ERROR).SEND(ctx)
        
        else:
            if ctx.guild:
                command_data    =   f"- Occured By    :   {ctx.author} / {ctx.author.id}\n" \
                                    f"- Command Name  :   {ctx.message.content}\n" \
                                    f"- @ Guild       :   {ctx.guild} / {ctx.guild.id}\n" \
                                    f"- @ Channel     :   {ctx.channel} / {ctx.channel.id}"
            else:
                command_data    =   f"- Occured By    :   {ctx.author} /{ctx.author.id}\n" \
                                    f"- Command Name  :   {ctx.message.content}\n" \
                                    f"** Occured in DM's **"
            error_str   =   "".join(traceback.format_exception(type(error), error, error.__traceback__))
            error_emb   =   disnake.Embed(
                title = "Error Boi <:Pain:911261018582306867>",
                description = f"```prolog\n{command_data} \n```\n```py\n {error_str}\n```",
                colour = 0x2F3136)       
            error_emb.timestamp = disnake.utils.utcnow()           
            send_error  =   self.webhook
            if len(error_str) < 2000:
                try:
                    await send_error.send(embed = error_emb)
                    await send_error.send("||Break Point||")
                except(disnake.HTTPException, disnake.Forbidden):
                    await send_error.send(embed = error_emb, file = disnake.File(io.StringIO(error_str), filename = "Traceback.py"))
                    await send_error.send("||Break Point||")
            else:
                await send_error.send(embed = error_emb, file = disnake.File(io.StringIO(error_str), filename = "Traceback.py"))
                await send_error.send("||Break Point||")
        
def setup(bot):
    bot.add_cog(ErrorHandler(bot))