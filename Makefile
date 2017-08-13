POOL = pool

GENOME_SIZE = 16384
MEMORY_SIZE = 4096
POOL_SIZE = 128

GENOMES = $(wildcard $(POOL)/*)

# disable builtin rules
.SUFFIXES:
.PHONY: evaluate trainset pool breed
.SECONDARY: $(patsubst %,%/compiled,$(GENOMES))

breed:
	python genome/crossover_generation.py \
		--pool $(POOL) \
		--count 8
	python genome/mutation_generation.py \
		--pool $(POOL) \
		--count 8 \
		--span-min 1 \
		--span-max 128 \
		--max-arg-value $(MEMORY_SIZE)

kill: evaluate
	mkdir -p graveyard
	python genome/kill.py --count $(POOL_SIZE) --pool $(POOL)

wikislownik:
	mkdir -p '$@'
	python scrape/get_wikimedia_category_files.py Polish_pronunciation | \
		xargs -n 100 -P 5 wget -q -P '$@' -nc

trainset: wikislownik
	rm -rf '$@'
	rm -rf pool/*/score  # invalidate scores
	mkdir -p '$@'
	python make_ws_trainset.py \
		-s 128 \
		-i '$<' \
		-o '$@'

$(POOL):
	mkdir -p '$@'
	python genome/generate_random_generation.py \
		-o '$@' \
		--genome-size $(GENOME_SIZE) \
		--max-arg-value $(MEMORY_SIZE) \
		--count $(POOL_SIZE)

$(POOL)/%/compiled: $(POOL)/%/genome
	cat '$<' | python genome/transpile_to_c.py \
		--memory-size $(MEMORY_SIZE) \
		--input-chunk 128 \
		--output-chunk 4 \
		| gcc -o '$@' -xc -

$(POOL)/%/score: $(POOL)/%/compiled
	python evaluate.py '$<' > '$@'

evaluate: $(patsubst %,%/score,$(GENOMES))
