Name: pg_upgrade2o
Version: 1.0
Release: 1%{?dist}
Summary: A optimized PostgreSQL upgrade tool for clone, copy, and link methods
License: MIT
Source0: %{name}

# Dependencies (modify if additional dependencies are required)
Requires: postgresql, bash

# Where to install the script
%define _bindir /usr/local/bin

%description
The pg_upgrade2o script is a flexible utility for managing PostgreSQL upgrades,
supporting clone, copy, and link methods. It automates upgrade tasks, handles extension 
management, and provides detailed timing logs.

%prep
# No prep is needed, but the section is required

%build
# No build steps are required for a script

%install
# Create the target directory and install the script
install -D -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/pg_upgrade2o

%files
%attr(0755, root, root) %{_bindir}/pg_upgrade2o

%doc
# Add optional documentation files here (README, license, etc.)

%changelog
* Fri Nov 10 2024 Sheikh Wasiu Al Hasib <wasiualhasib@gmail.com> - 1.0-1
- Initial package creation for pg_upgrade2o

