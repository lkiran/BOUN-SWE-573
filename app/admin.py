from django.contrib import admin

from app.models import Emoji, Vote, EmojiKeyword, Conversion

admin.site.register(Vote)
admin.site.register(Emoji)
admin.site.register(EmojiKeyword)
admin.site.register(Conversion)