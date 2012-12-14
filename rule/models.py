from django.db.models import *


LANG_CHOICES= {
	('EN', 'English'),
	('KR', 'Korean'),
}


# consider more suitable name
class Meta(Model):
	rule_id = IntegerField()
	section_id = IntegerField()
	article_id = IntegerField()

	class Meta:
		unique_together = (('rule_id', 'section_id', 'article_id'),)

	def __unicode__(self):
		idx = 'Rule ' + str(self.rule_id)
		if self.section_id > 0: idx += ' - Section ' + str(self.section_id)
		if self.article_id > 0: idx += ' - Article ' + str(self.article_id)
		return idx


class Title(Model):
	text = CharField(max_length=200)
	lang = CharField(max_length=2, choices=LANG_CHOICES)
	meta = ForeignKey(Meta)

	class Meta:
		unique_together = (('lang', 'meta'),)

	def __unicode__(self):
		return self.index() + '. ' + self.text

	def index(self):
		'''
		rule = 'R' + str(self.meta.rule_id)
		section = '-S' + str(self.meta.section_id) if self.meta.section_id > 0 else ''
		article = '-A' + str(self.meta.article_id) if self.meta.article_id > 0 else ''
		return rule + section + article
		'''
		idx = 'R' + str(self.meta.rule_id)
		if self.meta.section_id > 0: idx += '-S' + str(self.meta.section_id)
		if self.meta.article_id > 0: idx += '-A' + str(self.meta.article_id)
		return idx


class Article(Model):
	content = TextField(max_length=5000)
	lang = CharField(max_length=2, choices=LANG_CHOICES)
	meta = ForeignKey(Meta)

	class Meta:
		unique_together = (('lang', 'meta'),)

	def __unicode__(self):
		return self.content

	def title(self):
		return Title.objects.filter(lang=self.lang).get(meta=self.meta).text

	def index(self):
		return Title.objects.filter(lang=self.lang).get(meta=self.meta).index()


'''
class Penalty(Model):
	pass

class Picture(Model):	# or, generally, objects?
	pass
'''


class Toc:
	def __init__(self, meta, lang):
		self.meta = meta
		self.title = Title.objects.filter(meta=meta.id).filter(lang=lang)
		self.lang = lang

	#http://mkseo.pe.kr/blog/?p=1714
	@classmethod
	def create(cls, meta, lang):
		l = []
		for each in meta:
			l.append(Toc(each, lang))
		return l

	def seq(self):
		if self.meta.section_id == 0:
			return self.meta.rule_id
		if self.meta.article_id > 0:
			return self.meta.article_id
		else:
			return self.meta.section_id

	def subject(self):
		if self.title:
			return self.title[0].text
		else:
			return ''

	def children(self):
		des = Meta.objects.filter(rule_id=self.meta.rule_id)
		if self.meta.section_id == 0:
			# python variable should asign explicitly?
			des = des.filter(section_id__gt=0).filter(article_id=0)
		else:
			des = des.filter(section_id=self.meta.section_id).filter(article_id__gt=0)
		# or, else if then raise error?
		return Toc.create(des, self.lang)

	def level(self):
		if self.meta.section_id == 0:
			return 'rule'
		if self.meta.article_id > 0:
			return 'article'
		else:
			return 'section'

	def id(self):
		if self.title:
			return self.title[0].id
		else:
			return -1


#deprecated?
class Chapter:
	def __init__(self, meta, language):
		self.meta = meta
		self.title = Title.objects.filter(meta=meta.id).filter(lang=language)

	def key(self):
		return self.meta.id

	def index(self):
		return self.meta.__unicode__()

	def subject(self):
		if self.title:
			return self.title[0].text
		else:
			return ''

	def level(self):
		if self.meta.section_id == 0:
			return 'rule'
		if self.meta.article_id > 0:
			return 'article'
		else:
			return 'section'

	def seq(self):
		if self.meta.section_id == 0:
			return self.meta.rule_id
		if self.meta.article_id > 0:
			return self.meta.article_id
		else:
			return self.meta.section_id
		
	def meta(self):
		return self.meta


class Rule:
	pass
