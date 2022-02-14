import discord
from discord.ext import menus

class MyMenuPages(menus.MenuPages, inherit_buttons=False):
    @menus.button("<:before_check:754948796487565332>", position=menus.First(1))
    async def go_before(self, payload):
        """Goes to the previous page."""
        await self.show_checked_page(self.current_page - 1)

    @menus.button("<:next_check:754948796361736213>", position=menus.Last(0))
    async def go_after(self, payload):
        """Goes to the next page."""
        await self.show_checked_page(self.current_page + 1)

    @menus.button("<:before_fast_check:754948796139569224>", position=menus.First(0))
    async def go_first(self, payload):
        """Goes to the first page."""
        await self.show_page(0)

    @menus.button("<:next_fast_check:754948796391227442>", position=menus.Last(1))
    async def go_last(self, payload):
        """Goes to the last page."""
        await self.show_page(self._source.get_max_pages() - 1)
    
    @menus.button("<:stop_check:754948796365930517>", position=menus.First(2))
    async def go_stop(self, payload):
        """Remove this message."""
        self.stop()
