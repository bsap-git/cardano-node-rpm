Name: cardano-node
Version: 1.34.1
Release: 2%{?dist}
Summary: Cardano's node.

License: ASL 2.0
URL: https://github.com/input-output-hk/%{name}
Source0: https://github.com/bsap-git/%{name}-rpm/releases/download/%{version}-2/%{name}-%{version}-2-conf.tar.gz
Source1: https://github.com/bsap-git/%{name}-rpm/releases/download/%{version}-2/%{name}-%{version}-2-ghc-patches.tar.gz

BuildRequires: alex autoconf automake firewalld-filesystem gcc gcc-c++ ghcup-hs git glibc-devel gmp-devel happy iohk-libsodium jq libffi-devel libtool make ncurses-devel perl python systemd-devel systemd-rpm-macros tar xz zlib-devel
Requires: firewalld-filesystem systemd

%description
The core component that is used to participate in a Cardano decentralised blockchain, cardano-node is the top level for the node and aggregates the other components from other packages: consensus, ledger and networking, with configuration, CLI (cardano-cli), logging and monitoring.

Compiled to use system libffi.

# TODO: error: Empty %%files file /builddir/build/BUILD/cardano-node-1.34.1/debugsourcefiles.list
%define debug_package %{nil}
%define cardano_node %{_builddir}/cardano-node

%define _etc %{buildroot}/etc/opt/%{name}
%define __etc /etc/opt/%{name}

%define _sysd %{buildroot}/etc/systemd/system
%define __sysd /etc/systemd/system

%define _bin %{buildroot}/opt/cardano/%{name}
%define __bin /opt/cardano/%{name}

%define _db %{buildroot}/srv/cardano-node
%define __db /srv/cardano-node

%define __slibdir /opt/cardano/lib
%define __rpm_state %{_localstatedir}/lib/rpm-state/%{name}

%define _firewallds %{buildroot}/%{_libdir}/firewalld/services
%define __firewallds %{_libdir}/firewalld/services

%prep
%setup -q -a 1
ghcup-hs install ghc 8.10.7
ghcup-hs install cabal 3.6.2.0
ghcup-hs set ghc 8.10.7
ghcup-hs set cabal 3.6.2.0
export PATH="$HOME/.ghcup/bin:$PATH"
# TODO: If you have autoconf >= 2.70 you'll need to apply this patch https://gitlab.haskell.org/ghc/ghc/-/snippets/2040 (see the --patchdir option)
ghcup-hs -v compile ghc %{?_smp_mflags} -v 8.10.7 -b 8.10.7 -p $(pwd)/patches -c $(pwd)/patches/build.mk -o 8.10.7-fPIC -- --with-system-libffi
ghcup-hs set ghc 8.10.7-fPIC
rm -rf %{cardano_node}
git clone https://github.com/input-output-hk/%{name} %{cardano_node}
cd %{cardano_node}
git checkout tags/%{version}


%build
cd %{cardano_node}
export PATH="$HOME/.ghcup/bin:$PATH"
export LD_LIBRARY_PATH="%{__slibdir}"
export PKG_CONFIG_PATH="%{__slibdir}/pkgconfig"
cabal update
cabal configure --with-compiler=ghc-8.10.7-fPIC
cabal build all


%install
rm -rf %{buildroot}
mkdir -p -m 0755 %{_bin} %{_etc} %{_sysd}
mkdir -p %{_db}
install mainnet-* %{_etc}/
install %{name}.service %{name}.socket %{_sysd}/
install -p -D %{name}.sysusers %{buildroot}/%{_sysusersdir}/%{name}.conf
install -p -D %{name}.xml %{_firewallds}/%{name}.xml
cd %{cardano_node}
install $(./scripts/bin-path.sh cardano-node) %{_bin}/
install $(./scripts/bin-path.sh cardano-cli) %{_bin}/
mv doc/ LICENSE %{_builddir}/%{name}-%{version}/


%check
export LD_LIBRARY_PATH="%{__slibdir}"
%{_bin}/cardano-cli --version


%clean
rm -rf %{buildroot}
rm -rf %{cardano_node}


%pre
#%%sysusers_create_compat
# generated from cardano-node.sysusers
getent group 'cardano-node' >/dev/null || groupadd -r 'cardano-node'
getent passwd 'cardano-node' >/dev/null || \
    useradd -r -g 'cardano-node' -d '/' -s '/sbin/nologin' -c 'Runs cardano-node' 'cardano-node'
getent group 'cardano' >/dev/null || groupadd -r 'cardano'

%files
%defattr(0444,cardano-node,cardano-node)
%doc doc/*
%license LICENSE
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
%config(noreplace) %{_sysusersdir}/%{name}.conf
%config(noreplace) %{__firewallds}/%{name}.xml

%attr(0544,cardano-node,cardano) %{__bin}/%{name}
%attr(0554,cardano-node,cardano) %{__bin}/cardano-cli
%attr(0755,cardano-node,cardano) %dir %{__db}


%post
%systemd_post %{name}.socket
if [ $1 -eq 1 ] ; then
    # install
    mkdir -p -m 0700 %{__rpm_state}
    touch %{__rpm_state}/setup
fi

%posttrans
ls %{__rpm_state}/setup
if [ $? -eq 0 ] ; then
    # setup, start
    systemd-sysusers %{_sysusersdir}/%{name}.conf
    systemctl enable %{name}.socket
    # firewall-cmd --permanent --new-service-from-file=%%{__firewallds}/%%{name}.xml
    # firewall-cmd --reload
    # ip route get $(getent ahosts relays-new.cardano-mainnet.iohk.io | awk '{print $1; exit}') | grep -Po '(?<=(dev ))(\S+)' | tr -d '\n'
    # firewall-cmd --get-default-zone | tr -d '\n’ && firewall-cmd --get-zone-of-interface
    # firewall-cmd --zone=public --add-service=cardano-node
    systemctl start %{name}.socket
    rm -f %{__rpm_state}/setup || :
fi

%preun
%systemd_preun %{name}.socket
if [ $1 -eq 0 ] ; then
    # removal
    #find / -ignore_readdir_race -user cardano-node ! -group cardano -delete
    rm -rf %{__rpm_state} || :
    # firewall-cmd --zone=public --remove-service=cardano-node || :
    #userdel cardano-node || :
fi

%postun
%systemd_postun_with_restart %{name}.socket

%changelog
* Thu Apr 21 2022 Matthew Walker <mattwalkerstarted@gmail.com>
- First cardano-node package
- Started systemd tcp sockets, firewalld service, moved libsodium into it's own package and stopped using prebuilt binary in srpm. 1.34.1-2