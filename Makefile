out.csv: aircraft/mxs2/mxs2.xml mxs2_jsb.py
	./mxs2_jsb.py out.csv

test: aircraft/mxs2/mxs2.xml
	./mxs2_jsb.py
.PHONY: test

aircraft/mxs2/mxs2.xml: mxs2.xml.xacro
	mkdir -p $(shell dirname $@)
	xacro --xacro-ns -o $@ $<

xacro: aircraft/mxs2/mxs2.xml
.PHONY: xacro

install: requirements.txt
	python -m pip install -r requirements.txt
.PHONY: install
