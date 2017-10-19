BASEURL ?= $$PWD/dist

all: vendor/cache
	bundle exec jekyll build --destination dist --baseurl $(BASEURL) --incremental

view: all
	google-chrome-stable --new-window file://$$PWD/dist/index.html

vendor/cache: Gemfile Gemfile.lock
	bundle install --path vendor/cache
