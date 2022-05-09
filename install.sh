mkdir .facturio
wget https://azaleth.xyz/facturio/facturio-1.0.tar.gz
tar facturio-1.0.tar.gz -C .facturio
ln -s "$PWD/.facturio/run.sh" ~/.local/bin/facturio
mv .facturio/facturio.desktop "${XDG_DATA_HOME:-~/.local/share}/applications"
