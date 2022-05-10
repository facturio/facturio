if [ -n "$1" ]; then
	cd "$1"
fi

TAG="v0.9"

rm -fr .facturio "${XDG_DATA_HOME:-$HOME/.local/share}/applications"/facturio.desktop $HOME/.local/bin/facturio

mkdir -p .facturio
mkdir -p "${XDG_DATA_HOME:-$HOME/.local/share}/applications"

echo "$PATH" | grep -q "$HOME/.local/bin" && echo 'PATH=$PATH:$HOME/.local/bin' >> $HOME/.bashrc

wget https://github.com/facturio/facturio/releases/download/${TAG}/facturio-${TAG}.tar.gz

tar xvf facturio-${TAG}.tar.gz -C .facturio
ln -s "$PWD/.facturio/run.sh" $HOME/.local/bin/facturio
cp .facturio/facturio.desktop "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
rm facturio-${TAG}.tar.gz
