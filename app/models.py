from django.db import models

class Emoji(models.Model):
	Id = models.AutoField(primary_key = True)
	Icon = models.CharField(max_length = 10)
	Name = models.CharField(max_length = 50)
	Description = models.CharField(max_length = 1000)
	Order = models.IntegerField()

	def __str__(self):
		return u'{0} {1}'.format(self.Icon, self.Name)

	def __unicode__(self):
		return u'{0} {1}'.format(self.Icon, self.Name)

class IgnoredPhrases(models.Model):
	Id = models.AutoField(primary_key = True)
	Phrase = models.CharField(max_length = 250)

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
