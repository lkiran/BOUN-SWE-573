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


class EmojiKeyword(models.Model):
	Id = models.AutoField(primary_key = True)
	Emoji =  models.CharField(max_length = 250)
	Keyword = models.CharField(max_length = 250)
	Vote = models.IntegerField(default = 0)
	SuggestedByUser = models.BooleanField(default = False)

	def __str__(self):
		return u'{0} {1}'.format(self.Emoji, self.Keyword)

	def __unicode__(self):
		return u'{0} {1}'.format(self.Emoji, self.Keyword)
