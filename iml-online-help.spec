%define base_name online-help
%define managerdir /iml-manager/
%define backcompatdir /usr/lib%{managerdir}

Name:       iml-%{base_name}
Version:    2.4.1
Release:    1%{?dist}
Summary:    IML Online Help
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/intel-hpdd/%{base_name}
Source0:    https://registry.npmjs.org/@iml/%{base_name}/-/%{base_name}-%{version}.tgz

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
