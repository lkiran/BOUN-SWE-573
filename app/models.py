from django.db import models


class Emoji(models.Model):
	Id = models.AutoField(primary_key = True)
	Text = models.CharField(max_length = 5)
	Order = models.IntegerField()

class EmojiKeyword(models.Model):
	Id = models.AutoField(primary_key = True)
	Emoji = models.ForeignKey(Emoji, on_delete = models.CASCADE, verbose_name = "Emoji")
	Keyword = models.CharField(max_length = 250)
	SuggestedByUser = models.BooleanField(default = False)

class Conversion(models.Model):
	Id = models.AutoField(primary_key = True)
	Raw = models.CharField(max_length = 500)
	EmojiList = models.ManyToManyField(EmojiKeyword, verbose_name = "Emoji List")

class Vote(models.Model):
	Id = models.AutoField(primary_key = True)
	Value = models.BooleanField(default = True)  # True=Like, False=Hate
	Conversion = models.ForeignKey(Conversion, on_delete = models.CASCADE, verbose_name = "Processed Tweet")
