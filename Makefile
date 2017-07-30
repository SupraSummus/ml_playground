# disable builtin rules
.SUFFIXES:

trainset: trainset/blog_onet_pl
	mkdir -p $@

trainset/blog_onet_pl: \
	trainset/blog_onet_pl/nadblog-wszystkich-blogow \
	trainset/blog_onet_pl/ryszardczarnecki \
	trainset/blog_onet_pl/senyszyn \
	trainset/blog_onet_pl/kuzmiuk \
	trainset/blog_onet_pl/tglogowski \
	trainset/blog_onet_pl/sieniawski-marek \
	trainset/blog_onet_pl/adamszejnfeld \
	trainset/blog_onet_pl/aleksandrajakubowska \
	trainset/blog_onet_pl/zbigniewsosnowski \
	trainset/blog_onet_pl/iwinski \
	trainset/blog_onet_pl/cichocki \
	trainset/blog_onet_pl/jflibicki \

	mkdir -p $@

trainset/blog_onet_pl/%: raw/blog_onet_pl/%
	mkdir -p $@
	cat '$</ids' | python scrape/map_tags.py \
		-c '$</{}.content' \
		-t '$</{}.tags' \
		-i '$@/{}.in' \
		-o '$@/{}.out' \
		--missing-mappings '$@/{}.missing_mappings' \
		-m 'data/blog_onet_pl/tag_map/$*.json' \
		> '$@/ids'

raw/blog_onet_pl/%:
	mkdir -p $@
	python scrape/list_blog_onet_pl_archives.py 'http://$*.blog.onet.pl/' | \
		head -n 48 | \
		xargs python scrape/get_blog_onet_pl_archive.py \
			-c '$@/{}.content' \
			-t '$@/{}.tags' \
		> '$@/ids'
