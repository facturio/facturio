if [ -n "$1" ]; then
	cd "$1"
fi

TAG="v1.0"

rm -fr .facturio "${XDG_DATA_HOME:-$HOME/.local/share}/applications"/facturio.desktop $HOME/.local/bin/facturio

mkdir -p .facturio
mkdir -p "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$HOME"/.local/bin

echo "$PATH" | grep -q "$HOME/.local/bin" || echo 'PATH=$PATH:$HOME/.local/bin' >> $HOME/.bashrc

tar xvf facturio-${TAG}.tar.gz -C .facturio
ln -s "$PWD/.facturio/run.sh" $HOME/.local/bin/facturio
chmod +x $HOME/.local/bin/facturio
cp .facturio/facturio.desktop "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
rm facturio-${TAG}.tar.gz
