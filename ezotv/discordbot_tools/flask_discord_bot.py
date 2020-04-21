#!/usr/bin/env python3
from flask import current_app, _app_ctx_stack
from .discord_bot import DiscordBot

class FlaskDiscordBot(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):  # Configured by Flask
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'discordbot'):
            del ctx.discordbot

    @property
    def instance(self) -> DiscordBot:
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'discordbot'):
                ctx.discordbot = DiscordBot(current_app.config['DISCORD_BOT_TOKEN'],
                                            current_app.config['DISCORD_GUILD_ID'],
                                            current_app.config['DISCORD_ADMIN_ROLE'],
                                            current_app.config['DISCORD_ADMIN_CHAT'])
            return ctx.discordbot
