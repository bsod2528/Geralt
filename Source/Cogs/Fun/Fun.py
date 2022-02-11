import disnake

from disnake.ext import commands

import Source.Kernel.Utilities.Crucial as CRUCIAL

class Fun(commands.Cog):
    """Simple commands that induce Fun"""
    def __init__(self, bot):
        self.bot            =   bot
        self.DELETE         =   {}  # ---
        self.PRE_EDIT       =   {}  #    |-- > Snipe command related dictionaries
        self.POST_EDIT      =   {}  # --=

    # Listeners for "snipe" command
    @commands.Cog.listener()
    async def on_message_delete(self, MESSAGE):
        self.DELETE[MESSAGE.channel.id] =   (MESSAGE.content, MESSAGE.author, MESSAGE.channel.id, MESSAGE.created_at)

    @commands.Cog.listener()
    async def on_message_edit(self, PRE_EDIT, POST_EDIT):
        self.PRE_EDIT[PRE_EDIT.channel.id] =   (PRE_EDIT.jump_url, PRE_EDIT.content, PRE_EDIT.author, PRE_EDIT.channel.id, PRE_EDIT.created_at)
        self.POST_EDIT[POST_EDIT.channel.id] =   (POST_EDIT.content, POST_EDIT.author, POST_EDIT.channel.id, POST_EDIT.edited_at)

    # Mimics a user by sending a webhook as them.
    @commands.command(
        name    =   "as", 
        brief   =   "Send a Webhook")
    async def echo(self, ctx, USER : disnake.Member, *, MESSAGE):
        """Send a webhook message as the user you mentioned"""
        WBHK = await CRUCIAL.FETCH_WEBHOOK(ctx.channel)
        thread = disnake.utils.MISSING
        if isinstance(ctx.channel, disnake.Thread):
            thread = ctx.channel
        await WBHK.send(
            MESSAGE, 
            avatar_url  =   USER.display_avatar.url, 
            username    =   USER.display_name, 
           thread      =   thread)
        await ctx.message.delete(delay = 0)

    # Snipe command as a group
    @commands.group(
        name    =   "snipe",
        aliases =   ["s"])
    async def snipe(self, ctx):
        """Get edited / deleted messages"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
    
    # Snipes for deleted messages
    @snipe.command(
        name    =   "delete",
        aliases =   ["del", "d"],
        brief   =   "Snipe Deleted Messages")
    async def delete(self, ctx):
        """Get the details of the recently deleted message"""
        try:    
            MESSAGE, AUTHOR, CHANNEL, TIME    =   self.DELETE[ctx.channel.id]    
            DELETE_EMB   =   disnake.Embed(
                title   =   "Sniped Deleted Message",
                description =   f"**<:ReplyContinued:930634770004725821> - [Message Author :]({AUTHOR.display_avatar.url})** {AUTHOR.mention} (`{AUTHOR.id}`)\n**<:ReplyContinued:930634770004725821> - In Channel :** <#{CHANNEL}> (`{CHANNEL}`)\n**<:Reply:930634822865547294> - Message Created At :** {self.bot.DT(TIME)}",
                colour  =   self.bot.colour)
            DELETE_EMB.add_field(
                name    =   "Message Content",
                value   =   f"```prolog\n{MESSAGE}\n```")
            DELETE_EMB.timestamp    =   disnake.utils.utcnow()
            await ctx.reply(embed = DELETE_EMB, allowed_mentions = self.bot.Mention)
        except:
            await ctx.reply("No one has deleted. any messages as of now <a:HumanBro:905748764432662549>", allowed_mentions = self.bot.Mention)

    # Snipes for edited messages
    @snipe.command(
        name    =   "edit",
        aliases =   ["ed", "e"],
        brief   =   "Snipe Edited Messages")
    async def edit(self, ctx):
        """Get the details of the recently edited message"""
        try:    
            URL, MESSAGE, AUTHOR, CHANNEL, PRE_TIME          =   self.PRE_EDIT[ctx.channel.id]    
            POST_MESSAGE, AUTHOR, CHANNEL, POST_TIME    =   self.POST_EDIT[ctx.channel.id]    
            View    =   disnake.ui.View()
            View.add_item(disnake.ui.Button(label = "Jump to Message", style = disnake.ButtonStyle.link, url = URL, emoji = "<a:ChainLink:936158619030941706>"))
            EDIT_EMB   =   disnake.Embed(
                title   =   "Sniped Edited Message",
                description =   f"**<:ReplyContinued:930634770004725821> - [Message Author :]({AUTHOR.display_avatar.url})** {AUTHOR.mention} (`{AUTHOR.id}`)\n**<:ReplyContinued:930634770004725821> - In Channel :** <#{CHANNEL}> (`{CHANNEL}`)\n**<:Reply:930634822865547294> - Message Sent At :** {self.bot.DT(PRE_TIME)}",
                colour  =   self.bot.colour)
            EDIT_EMB.add_field(
                name    =   "Before Edit",
                value   =   f"```prolog\n{MESSAGE}\n```")
            EDIT_EMB.add_field(
                name    =   "After Edit",
                value   =   f"**<:Reply:930634822865547294> - Message Edited at :** {self.bot.DT(POST_TIME)}\n```prolog\n{POST_MESSAGE}\n```",
                inline  =   False)
            await ctx.reply(embed = EDIT_EMB, allowed_mentions = self.bot.Mention, view = View)
        except:
            await ctx.reply("No one has edited any messages as of now <a:BotLurk:905749164355379241>", allowed_mentions = self.bot.Mention)
            
def setup(bot):
    bot.add_cog(Fun(bot))