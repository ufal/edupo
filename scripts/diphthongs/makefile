all: diphthongs.patterns

all_training.txt: diphthongs_from_corpus.txt lexcorp.txt data_rucni.txt
	cat $^ > $@

all_training.txt.out: all_training.txt
	./run_patgen.sh $<

diphthongs.patterns: all_training.txt.out
	mv $< $@
