import os

# Setup for testing
os.environ['EZOTV_LOCAL_API_KEY'] = 'testkey'
os.environ['EZOTV_LUNA_API_KEY'] = 'testkey'
os.environ['EZOTV_SERVER_NAME'] = 'localhost:5000'
os.environ['EZOTV_DISCORD_OAUTH_CLIENT_ID'] = 'testkey'
os.environ['EZOTV_DISCORD_OAUTH_CLIENT_SECRET'] = 'testkey'
os.environ['EZOTV_DISCORD_BOT_TOKEN'] = 'testkey'
os.environ['EZOTV_DISCORD_GUILD_ID'] = '123'
os.environ['EZOTV_DISCORD_ADMIN_ROLE'] = 'admin'
os.environ['EZOTV_DISCORD_ADMIN_CHAT'] = '123'
os.environ['EZOTV_REDIS_URL'] = 'redis://localhost:6379/0'
os.environ['EZOTV_CACHE_TIMEOUT'] = '2'