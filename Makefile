# disable builtin rules
.SUFFIXES:

.PHONY: trainset scrape_nadblog_wszystkich_blogow

trainset: scrape_nadblog_wszystkich_blogow
	mkdir -p trainset

scrape_nadblog_wszystkich_blogow:
	mkdir -p trainset
	python scrape/list_blog_onet_pl_archives.py http://nadblog-wszystkich-blogow.blog.onet.pl/ | \
		head -n 48 | \
		xargs -n 1 -P 3 python scrape/get_blog_onet_pl_archive.py \
			-c 'trainset/nadblog-wszystkich-blogow-{}.in' \
			-t 'trainset/nadblog-wszystkich-blogow-{}.out'
