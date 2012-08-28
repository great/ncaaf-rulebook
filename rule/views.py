from rule.models import Meta, Toc, Chapter, Article
from django.http import HttpResponse
from django.template import Context, loader


def index(request, language='EN'):
	toc = Toc.create(Meta.objects.filter(section_id=0).filter(article_id=0), language)
	t = loader.get_template('rule/index.html')
	c = Context({
		'toc' : toc,
	})
	return HttpResponse(t.render(c))


def chapter(request, language):
	metas = Meta.objects.all()
	chapters = []
	for meta in metas:
		chapters.append(Chapter(meta, language))
	t = loader.get_template('rule/toc.html')
	c = Context({
		'chapters' : chapters,
	})
	return HttpResponse(t.render(c))


def articles(request, language, rule_id, section_id):
	keys = Meta.objects.filter(rule_id=rule_id, section_id=section_id, article_id__gt=0)
	articles = Article.objects.filter(meta__in=keys, lang=language)
	t = loader.get_template('rule/articles.html')
	c = Context({
		'articles' : articles,
	})
	return HttpResponse(t.render(c))


def article(request, language, meta_id):
	article = Article.objects.filter(lang=language).get(meta_id=meta_id)
	t = loader.get_template('rule/article.html')
	c = Context({
		'article' : article,
	})
	return HttpResponse(t.render(c))

