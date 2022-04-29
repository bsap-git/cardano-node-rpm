# cardano-node-rpm

A package to make compiling, installing and managing node upgrades easy for rpm-based distributions. The node is ran as a systemd service, residing in /opt/cardano with the chain in /srv/ and you can find the unix socket in /run.

## Installation

Yum should work too.

```bash
sudo dnf install <cardano-node>.rpm <iohk-libsodium>.rpm
```

## Compiling

```bash
# clone repo
git clone https://github.com/bsap-git/cardano-node-rpm ~/rpmbuild && cd ~/rpmbuild

# check autoconf, if >= 2.70 look at comment in SPECS/cardano-node.spec
autoconf --version

# build source rpms for your distro
rm -f SRPMS/* && rpmbuild -bs SPECS/*

# compile in chroot with mock (this includes compiling ghc so be warned!)
mock --chain --enable-network --localrepo=./cardano-node/"{{dist}}"/"{{target_arch}}"/ SRPMS/ghcup-* SRPMS/iohk-* SRPMS/cardano-*
```
If it fails there should be a build.log in /var/lib/mock/ you can peak at. It takes about 75-90 minutes with 12 cores. If you want to build for something other than your machine you can pass an `-r` flag to mock with a `--buildsrpm` command to generate the correct srpms.
 
## Contributing
Tips, advice, concerns and pull requests are all welcome. I have an [open question](https://cardano.stackexchange.com/questions/8044/how-to-get-cardano-node-to-work-with-public-systemd-sockets) I'm particularly interested in getting solved.

### TODO
- Prevent the regular libsodium from coming up as ok.
- The above open question.
- Whatever else might pop up!
