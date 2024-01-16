# make file for Stock Bots

tests:
	python -m unittest

clean_src:
	rm -rf sb/__pycache__

clean_test:
	rm -rf test/__pycache__

clean: clean_src clean_test
	find . -name sb.zip -delete
	rm -rf __pycache__

zip: clean
	zip -r sb.zip sb test Makefile
