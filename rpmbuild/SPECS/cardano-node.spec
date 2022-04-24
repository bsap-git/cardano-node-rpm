Name: cardano-node
Version: 1.34.1
Release: 1%{?dist}
Summary: Cardano's node and IOHK's custom libsodium.

License: ASL 2.0, ISC
URL: https://github.com/input-output-hk/%{name}
Source0: https://github.com/input-output-hk/%{name}/archive/refs/tags/%{version}.tar.gz

BuildRequires: systemd systemd-rpm-macros git gcc gcc-c++ tmux gmp-devel make tar xz wget zlib-devel libtool autoconf libffi-devel systemd-devel ncurses-devel ncurses-compat-libs

%description
The core component that is used to participate in a Cardano decentralised blockchain, cardano-node is the top level for the node and aggregates the other components from other packages: consensus, ledger and networking, with configuration, CLI (cardano-cli), logging and monitoring.

Compiled to use host libffi and including IOHK's custom libsodium 66f017f1.

%define debug_package %{nil}
%define sodium %{_builddir}/libsodium
%define _etc %{buildroot}/etc/opt/%{name}
%define __etc /etc/opt/%{name}
%define _sysd %{buildroot}/etc/systemd/system
%define __sysd /etc/systemd/system
%define _bin %{buildroot}/opt/%{name}
%define __bin /opt/%{name}
%define _db %{buildroot}/srv/cardano-node
%define __db /srv/cardano-node
%define _sprefix %{buildroot}/usr/local
%define _sexec_prefix %{buildroot}/usr/local
%define _slibdir %{buildroot}/usr/local/lib
%define _sincludedir %{buildroot}/usr/local/include
%define __rpm_state %{_localstatedir}/lib/rpm-state/%{name}

%prep
%setup -q -c
rm -rf %{sodium}
git clone https://github.com/input-output-hk/libsodium %{sodium}
cd %{sodium}
git checkout 66f017f1

%build
cd %{sodium}
./autogen.sh
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p -m 0755 %{_bin} %{_etc} %{_sysd} %{_sincludedir}/sodium %{_slibdir}/pkgconfig
mkdir -p -m 0775 %{_db}
install -m 0744 %{name} %{_bin}/
install -m 0754 cardano-cli %{_bin}/
install -m 0644 mainnet-* %{_etc}/
install -m 0644 %{name}.service %{name}.socket %{_sysd}/
install -p -D -m 0644 %{name}.sysusers %{buildroot}%{_sysusersdir}/%{name}.conf
cd %{sodium}
make prefix=%{_sprefix} exec_prefix=%{_sexec_prefix} libdir=%{_slibdir} includedir=%{_sincludedir} install

%clean
rm -rf %{buildroot}
rm -rf %{sodium}

%pre
%sysusers_create_compat %{name}.sysusers

%files
%license LICENSE
%license libsodium_LICENSE
%config(noreplace) %{__etc}/mainnet-topology.json
%config(noreplace) %{__etc}/mainnet-p2p-toplogy.json
%config(noreplace) %{__etc}/mainnet-config.yaml
%config(noreplace) %{__etc}/mainnet-config.json
%config(noreplace) %{__etc}/mainnet-config-new-tracing.yaml
%config(noreplace) %{__etc}/mainnet-alonzo-genesis.json
%config(noreplace) %{__etc}/mainnet-byron-genesis.json
%config(noreplace) %{__etc}/mainnet-shelley-genesis.json
%config(noreplace) %{__sysd}/%{name}.socket
%config(noreplace) %{__sysd}/%{name}.service

%doc doc/*
/opt/%{name}/%{name}
/opt/%{name}/cardano-cli
/usr/local/include/
/usr/local/lib/
%dir %{__db}
%{_sysusersdir}/%{name}.conf

%post
%systemd_post %{name}.service %{name}.socket
if [ $1 -eq 1 ] ; then
    # install
    mkdir -p -m 0755 %{__rpm_state}
    touch %{__rpm_state}/setup
fi

%posttrans
ls %{__rpm_state}/setup
if [ $? -eq 0 ] ; then
    # setup, start
    systemd-sysusers %{_sysusersdir}/%{name}.conf
    chown cardano-node:cardano-node %{__db}
    chown cardano-node:cardano-node %{__bin}/%{name}
    chown cardano-node:cardano %{__bin}/cardano-cli
    systemctl enable %{name}.socket
    systemctl start %{name}.socket
    rm -f %{__rpm_state}/setup || :
fi

%preun
%systemd_preun %{name}.service %{name}.socket
if [ $1 -eq 0 ] ; then
    # removal
    find / -ignore_readdir_race -user cardano-node ! -group cardano -delete
    rm -rf %{__rpm_state}
    userdel cardano-node || :
fi

%postun
%systemd_postun_with_restart %{name}.service %{name}.socket

%changelog
* Thu Apr 21 2022 Matthew Walker <comrade@matt.ag> - %{version}-%{release}
- First cardano-node package