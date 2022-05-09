if [ -n "$1" ]; then
	cd "$1"
fi

rm -fr .facturio "${XDG_DATA_HOME:-~/.local/share}/applications"/facturio.desktop ~/.local/bin/facturio

mkdir -p .facturio
mkdir -p "${XDG_DATA_HOME:-~/.local/share}/applications"

echo "$PATH" | grep -q "$HOME/.local/bin" && echo 'PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc

wget https://azaleth.xyz/facturio-1.0.tar.gz

tar xf facturio-1.0.tar.gz -C .facturio
ln -s "$PWD/.facturio/run.sh" ~/.local/bin/facturio
cp .facturio/facturio.desktop "${XDG_DATA_HOME:-~/.local/share}/applications"
rm facturio-1.0.tar.gz
