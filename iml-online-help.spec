%define base_name online-help
%define managerdir /iml-manager/
%define backcompatdir /usr/lib%{managerdir}

Name:       iml-%{base_name}
Version:    3.0.0
# Release Start
Release:    1%{?dist}
# Release End
Summary:    IML Online Help
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/whamcloud/%{base_name}
Source0:    %{name}-%{version}.tgz

BuildRequires: nodejs-packaging
BuildArch:  noarch

%description
This module is a static html website based on the online-help markdown docs. The html is generated using jekyll.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}%{managerdir}%{name}
cp -al targetdir/. %{buildroot}%{_datadir}%{managerdir}%{name}
mkdir -p %{buildroot}%{backcompatdir}
ln -s %{_datadir}%{managerdir}%{name} %{buildroot}%{backcompatdir}%{name}

%clean
rm -rf %{buildroot}

%files
%{_datadir}
%{backcompatdir}

%changelog
* Mon May 13 2019 Joe Grund <jgrund@whamcloud.com> - 2.5.5-1
- IML 5 documentation updates

* Tue Apr 09 2019 Will Johnson <wjohnson@whamcloud.com> - 2.5.4-1
- Integrate deploy copr

* Mon Apr 08 2019 Will Johnson <wjohnson@whamcloud.com> - 2.5.3-1
- Bump IML refs to 4.0.10

* Mon Jan 28 2019 Joe Grund <jgrund@whamcloud.com> - 2.5.2-1
- Bump IML refs to 4.0.9

* Fri Aug 31 2018 Joe Grund <jgrund@whamcloud.com> - 2.5.1-1
- Bump IML refs to 4.0.8.

* Tue Aug 14 2018 Joe Grund <jgrund@ddn.com> - 2.5.0-1
- Bump IML refs to 4.0.7.

* Fri Mar 16 2018 Joe Grund <joe.grund@intel.com> - 2.4.1-1
- Remove *.md files
- Move deployment dir to datadir.

* Wed Mar 14 2018 Joe Grund <joe.grund@intel.com> - 2.4.0-1
- Add upgrade docs.
- Add debugging rust section.
- Add module-tools.

* Mon Oct 23 2017 Joe Grund <joe.grund@intel.com> - 2.3.2-1
- Add doc on building IML.
- Fix ZFS on Vagrant docs to reflect persistent disk serials.

* Thu Oct 05 2017 Will Johnson <william.c.johnson@intel.com> - 2.3.0-1
- Add page for managed zfs filesystem creation
- Add page for creating offline repos
- Small fix-up for installing repos on client nodes

* Tue Oct 03 2017 Will Johnson <william.c.johnson@intel.com> - 2.2.0-1
- Add contributor docs
- Clean-ups

* Wed Sep 27 2017 Will Johnson <william.c.johnson@intel.com> - 2.1.1-1
- Thorough review of Online Help Docs
- Thorough review of Install Guide
- Thorough review of API docs
- Update root readme file to link to Online Help Docs, Install Guide, and API Docs

* Mon Aug 07 2017 Will Johnson <william.c.johnson@intel.com> - 2.0.3-1
- Initial package
