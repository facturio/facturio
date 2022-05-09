if [ -n "$1" ]; then
	cd $DIR
fi
mkdir .facturio
grep -q "$HOME/.local/bin" <<< "$PATH" && echo 'PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
wget https://azaleth.xyz/facturio-1.0.tar.gz
tar xf facturio-1.0.tar.gz -C .facturio
ln -s "$PWD/.facturio/run.sh" ~/.local/bin/facturio
mv .facturio/facturio.desktop "${XDG_DATA_HOME:-~/.local/share}/applications"
