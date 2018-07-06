MD_DOCS   := $(wildcard *.md)
HTML_DOCS  = $(MD_DOCS:.md=.html)
GH_CSS     = github-pandoc.css

%.html : %.md Makefile $(GH_CSS)
	sed -e 's/\.md)/.html)/g' < $< | pandoc --to html5 --css $(GH_CSS) -o $@

all: $(HTML_DOCS)
