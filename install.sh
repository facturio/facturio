if [ -n "$1" ]; then
	cd "$1"
fi

TAG="v0.9"

rm -fr .facturio "${XDG_DATA_HOME:-~/.local/share}/applications"/facturio.desktop ~/.local/bin/facturio

mkdir -p .facturio
mkdir -p "${XDG_DATA_HOME:-~/.local/share}/applications"

echo "$PATH" | grep -q "$HOME/.local/bin" && echo 'PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc

wget https://azaleth.xyz/facturio/${TAG}/facturio-${TAG}.tar.gz

tar xvf facturio-${TAG}.tar.gz -C .facturio
ln -s "$PWD/.facturio/run.sh" ~/.local/bin/facturio
cp .facturio/facturio.desktop "${XDG_DATA_HOME:-~/.local/share}/applications"
rm facturio-${TAG}.tar.gz
