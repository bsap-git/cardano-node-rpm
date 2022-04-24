# cardano-node-rpm

I am working on a desktop wallet and needed an easy way to manage getting a node setup so this is the start. I am hoping this might help someone else and hearing about any problems or concerns would help me! This repository holds the rpmbuild directory, mock results directory, and ghc patches used. IOHK's libsodium is downloaded and compiled on the host.

# installing

`sudo dnf install cardano-node-1.34.1-1.fc34.x86_64.rpm`

# building for something else

You'll need to make sure mock has the `--enable-network` flag if you use it and the included cardano-node is compiled for x86_64.

# cautions

I explicitly run `find / -ignore_readdir_race -user cardano-node ! -group cardano -delete` on package removal, so if you already have files owned by user cardano-node they will get deleted. You can change this in the `cardano-node.spec` and run `rpmbuild -bs cardano-node.spec` to make a new source, or prevent it by making those files owned by group cardano.

The node will start on it's own and vim might freak out if you don't install the regular libsodium.

# other

Eventually this will end up as three packges, ghc, libsodium, node... for now it's all bundled together. You can find the unix socket in /run/cardano-node.sk and the chain in /srv/cardano-node.

# resources

https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html-single/RPM_Guide/index.html

http://0pointer.de/public/systemd-man/index.html

https://docs.fedoraproject.org/en-US/packaging-guidelines/

https://www.hobson.space/posts/haskell-foreign-library/
