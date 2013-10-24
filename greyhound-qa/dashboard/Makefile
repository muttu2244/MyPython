FILES=Makefile \
      gh_test/ \
      gh-test.spec 

RELEASE=$(shell grep "Release: " gh-test.spec | sed -e "s/Release://g" -e "s/\s*//g")
VERSION=$(shell grep "Version: " gh-test.spec | sed -e "s/Version://g" -e "s/\s*//g")
BUILDVERSION=$(VERSION)-$(RELEASE)
BASEDIR=/opt/zynga/greyhound/
PACKAGEDIR=$(BASEDIR)/$(BUILDVERSION)/

DIRS=$(PACKAGEDIR)/gh_test \

BUILDROOT=.
#svn info | grep "Revision" | sed "s/Revision: /r/"

all: 
	@@true # do nothing


tarball:
	tar -czv --exclude=.svn --dereference -f $(BUILDROOT)/gh-test-$(BUILDVERSION).tgz $(FILES)

rpm: tarball
	rpmbuild -tb $(BUILDROOT)/gh-test-$(BUILDVERSION).tgz

install: $(INSTALL_ROOT) copyfiles

makedirs: $(INSTALL_ROOT) 
	test -d $(INSTALL_ROOT) || echo "Invalid build root specified - $(INSTALL_ROOT)"
	test -d $(INSTALL_ROOT) # fail make
	for dir in $(DIRS); do mkdir -p $(INSTALL_ROOT)/$$dir; done
	mkdir -p $(INSTALL_ROOT)/$(PACKAGEDIR)/internal/services

copyfiles: makedirs
	cp -rv gh_test/ $(INSTALL_ROOT)/$(PACKAGEDIR)/
	cp gh_test/scripts/test/internal/user.payments.meta.append.php $(INSTALL_ROOT)/$(PACKAGEDIR)/internal/services/
	#cp gh_test/scripts/test/internal/user.blob.revert.php $(INSTALL_ROOT)/$(PACKAGEDIR)/internal/services/
	cd $(INSTALL_ROOT)/$(PACKAGEDIR)/gh_test/scripts/test/public/;ln -vsf --target-directory=./ ../../lib ;
	cd $(INSTALL_ROOT)/$(PACKAGEDIR)/gh_test/scripts/test/internal/;ln -vsf --target-directory=./ ../../lib ;		
	cd $(INSTALL_ROOT)/$(PACKAGEDIR)/gh_test/scripts/test/admin/;ln -vsf --target-directory=./ ../../lib ;
	cd $(INSTALL_ROOT)/$(PACKAGEDIR)/gh_test/scripts/test/mqs/;ln -vsf --target-directory=./ ../../lib ;
