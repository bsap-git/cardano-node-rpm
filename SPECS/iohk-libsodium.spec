Name:           iohk-libsodium
Version:        1.0.18.66f017f1
Release:        1%{?dist}
Summary:        A modern, portable, easy to use crypto library-- iohk-style.

License:        ISC
URL:            https://github.com/input-output-hk/libsodium

BuildRequires:  autoconf gcc gcc-c++ git libtool make

%description
Sodium is a new, easy-to-use software library for encryption, decryption, signatures, password hashing and more.

It is a portable, cross-compilable, installable, packageable fork of NaCl, with a compatible API, and an extended API to improve usability even further.

Its goal is to provide all of the core operations needed to build higher-level cryptographic tools.

Sodium supports a variety of compilers and operating systems, including Windows (with MingW or Visual Studio, x86 and x64), iOS, Android, as well as Javascript and Webassembly.

This is IOHK's version used by cardano-node and other tools, installed in /opt/cardano.


%define sodium %{_builddir}/libsodium

%define _sprefix %{buildroot}/opt/cardano
%define __sprefix /opt/cardano

%define _sexec_prefix %{buildroot}/opt/cardano
%define __sexec_prefix /opt/cardano

%define _slibdir %{buildroot}/opt/cardano/lib
%define __slibdir /opt/cardano/lib

%define _sincludedir %{buildroot}/opt/cardano/include
%define __sincludedir /opt/cardano/include

%prep
rm -rf %{sodium}
git clone https://github.com/input-output-hk/libsodium %{sodium}
cp -p %{sodium}/LICENSE %{_builddir}
cd %{sodium}
git checkout 66f017f1

%build
cd %{sodium}
./autogen.sh
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{_sincludedir}/sodium %{_slibdir}/pkgconfig
cd %{sodium}
make prefix=%{_sprefix} exec_prefix=%{_sexec_prefix} libdir=%{_slibdir} includedir=%{_sincludedir} install
sed -i -e 's|^pre.*|prefix=%{__sprefix}|' -e 's|^exe.*|exec_prefix=%{__sexec_prefix}|' -e 's|^lib.*|libdir=%{__slibdir}|' -e 's|^inc.*|includedir=%{__sincludedir}|' %{_slibdir}/pkgconfig/libsodium.pc


%check
ls %{_slibdir}/pkgconfig/libsodium.pc


%clean
rm -rf %{buildroot}
rm -rf %{sodium}


%files
%defattr(0555,root,root)
%license LICENSE
%{__slibdir}
%{__sincludedir}


%changelog
* Mon Apr 25 2022 Matthew Walker <mattwalkerstarted@gmail.com>
- Initial package.
