from django.contrib import admin

from app.models import Emoji, EmojiKeyword

admin.site.register(Emoji)
admin.site.register(EmojiKeyword)

