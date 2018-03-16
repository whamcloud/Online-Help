NAME            := iml-online-help
PACKAGE_VERSION := 2.4.1
PACKAGE_RELEASE := 1

BASEURL ?= $(PWD)/targetdir

MD_FILES    := $(shell find docs -name \*.md)
OTHER_FILES := $(shell find docs -name \*.png -name \*.css)
HTML_FILES  := $(addprefix targetdir/,$(patsubst %.md,%.html,$(MD_FILES))) \
	       targetdir/index.html
SOURCES     := $(MD_FILES) $(OTHER_FILES)
DISTCLEAN   += vendor

# see https://stackoverflow.com/questions/2973445/ for why we subst
# the ".html" for "%html" to effectively turn this into a multiple
# matching target pattern rule
$(subst .html,%html,$(HTML_FILES)): vendor/cache $(SOURCES)
	bundle exec jekyll build --destination targetdir --baseurl \
	    $(BASEURL) --incremental
	find targetdir -name \*.md -print0 | xargs -0 rm -f

view: targetdir
	google-chrome-stable --new-window file://$$PWD/targetdir/index.html

vendor/cache: Gemfile Gemfile.lock
	bundle install --path vendor/cache
	touch $@

install_build_deps:
	yum -y install https://rpm.nodesource.com/pub_8.x/el/7/x86_64/nodesource-release-el7-1.noarch.rpm
	yum -y install nodejs rubygem-bundler ruby-devel gcc autoconf \
		       automake libtool yum-plugin-copr zlib-devel
	yum -y copr enable managerforlustre/CentOS_Ruby22
	yum -y install ruby

NPM_PREREQS := $(HTML_FILES) README.md
include ./include/npm.mk
