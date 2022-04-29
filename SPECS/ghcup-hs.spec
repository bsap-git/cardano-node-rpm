Name:           ghcup-hs
Version:        0.1.17.5    
Release:        1%{?dist}
Summary:        GHCup is an installer for the general purpose language Haskell.

License:        LGPLv3
URL:            https://github.com/haskell/ghcup-hs

BuildRequires: curl coreutils

%description
GHCup is an installer for the general purpose language Haskell.


%define _name %{_arch}-linux-ghcup-0.1.17.5

%prep
curl -Lf https://github.com/haskell/ghcup-hs/releases/download/v0.1.17.5/%{_name} > %{_builddir}/%{_name}
curl -Lf https://raw.githubusercontent.com/haskell/ghcup-hs/v0.1.17.5/LICENSE > %{_builddir}/LICENSE
curl -Lf https://github.com/haskell/ghcup-hs/releases/download/v0.1.17.5/SHA256SUMS > %{_builddir}/SHA256SUMS


%build
sha256sum --ignore-missing --check --quiet SHA256SUMS


%install
rm -rf %{buildroot}
install -p -D %{_name} %{buildroot}/%{_bindir}/%{name}


%check
%{buildroot}/%{_bindir}/%{name} --version


%clean
rm -rf %{buildroot}


%files
%license LICENSE
%attr(0755,root,root) %{_bindir}/%{name}


%changelog
* Mon Apr 25 2022 Matthew Walker <mattwalkerstarted@gmail.com>
- Initial package.
