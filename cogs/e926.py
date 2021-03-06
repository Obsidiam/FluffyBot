import aiohttp
import discord
from collections import defaultdict
from discord.ext import commands


class E926(object):
    def __init__(self, bot):
        self.bot = bot
        self.search_link = 'http://e926.net/post/index.json?tags='
        self.original_link = 'http://e926.net/post/show/'
        self.keys = ['file_url', 'author', 'score', 'id']
        self.entries = defaultdict(list)

    @commands.command()
    async def e9(self, ctx, *, arg: str):
        if arg.lower() != 'original':
            split_message = arg.split()

            amount = int(split_message[-1]) if split_message[-1].isdigit() and int(split_message[-1]) > 0 else 1
            query = '+'.join(split_message) if not split_message[-1].isdigit() else '+'.join(split_message[:-1])

            self.entries.clear()
            await self.make_req(query, amount)

            for entry in self.entries[self.keys[0]]:
                author = self.entries[self.keys[1]][0]
                score = self.entries[self.keys[2]][0]
                await ctx.send(embed=discord.Embed(description='Author: {a}, Score: {s}'.format(a=author, s=score)).set_image(url=entry))
        else:
            await ctx.send("Original -> {l}".format(l='{ol}{id}'.format(ol=self.original_link, id = self.entries[self.keys[3]][0])))


    async def make_req(self, query, amount):
        async with aiohttp.ClientSession() as cs:
            req_mess = '{l}{q}{li}{a}'.format(l=self.search_link, q=query, li='&limit=', a=str(amount))
            async with cs.get(req_mess) as r:
                entries = await r.json()
                for entry in entries:
                    for key in self.keys:
                        self.entries[key].append(entry[key])


def setup(bot):
    print('added E9 module')
    bot.add_cog(E926(bot))
