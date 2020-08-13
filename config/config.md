# config.md
Poznámky k tomu, jak setupnout RPI.
Eventuálně bude nahrazeno skriptem, který na čersvé RPI nastaví Mynt.

## Úvod
- `scp` věcí, které budou potřeba
	- věci v `config/` složce na správná místa
		- nezapomenout všechny `+x` chmodnout
	- adresář `mynt/` do homu
	- instalace `config_watch.sh` skriptu (a jeho `+x` chmodnutí)
		- nezapomenout dát spouštění do `rc.local`
- update systému (`sudo apt-get update`, `sudo apt-get upgrade`)
- instalace programů (`sudo apt install git`)

## MTP
Přes [uMTP](https://github.com/viveris/uMTP-Responder).
```
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
git clone https://github.com/viveris/uMTP-Responder umtp
make -C umtp
sudo mv umtp/umtprd /usr/bin/
```

## Poznámky
- `rc.conf` musí být executable
- musí taky mít nějaký rozumný shebang, jinak se to nenastartuje
