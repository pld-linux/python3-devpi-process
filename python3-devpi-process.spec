# Conditional build:
%bcond_without	tests	# unit tests

%define		module	devpi-process
Summary:	Programmatic API to create and use a devpi server process
Name:		python3-%{module}
Version:	1.0.2
Release:	1
License:	MIT
Group:		Libraries/Python
# if pypi:
#Source0Download: https://pypi.org/simple/devpi-process/
Source0:	https://files.pythonhosted.org/packages/source/d/devpi-process/devpi_process-%{version}.tar.gz
# Source0-md5:	7f00f42d265d1aa0f026507cd62011e8
URL:		https://pypi.org/project/devpi-process/
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-build
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-httpx
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows you to create devpi server process with indexes, and upload
artifacts to that programmatically.

%prep
%setup -q -n devpi_process-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md LICENSE.txt
%dir %{py3_sitescriptdir}/devpi_process
%{py3_sitescriptdir}/devpi_process/*.py
%{py3_sitescriptdir}/devpi_process/py.typed
%{py3_sitescriptdir}/devpi_process/__pycache__
%{py3_sitescriptdir}/devpi_process-%{version}.dist-info
