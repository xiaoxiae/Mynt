# Brainstorming

## HW
- RPI-zero (w), micro USB napájení
- RGB (individuálně ovladatelné) LEDky
	- https://www.tme.eu/cz/details/hcbaa30w/zdroje-svetla-pasy-led/worldsemi/hc-f5v-30l-30led-w-ws2813-ip20/
- design z 3D scanu (ručního) nějaké modelíny -- ať je to hezky přírodní tvar
- žádné zvuky
- heartrate sensor
	- aktivace přes chycení
	- https://www.ebay.com/itm/254337746890
	- na druhé straně to bude tak vibrovat a svítit
		- https://www.ebay.com/itm/133285018930
	- asi palec-ukazováček
- pohodlné držení

## SW
- povídání si s centralním serverem přes Wifinu
	- IP bude hard-kódnutá v configu
	- na nějakém portu bude otevřená služba, která si se zařízeními bude povídat
- každý pár bude mít nějaké unikátní číslo, přes které si bude povídat s tím druhým přípojeným k serveru
	- nějaké vygenerované hashem z hardwaru, aby nemohl random troll vytvářet stejný
		- stejně na to bude muset server myslet
- TODO: co znamená číslo u USBčka?


### Kabel-based konfigurace
- připojení vystaví složku s konfigurákem, který si uživatel upraví
- použití MTP, aby se to chovalo, jako když se připojuje mobil
	- TODO: jde přes to soubor in-place editovat?
- `yaml` soubor, na který RPIčko kouká a něco dělá, když se změní
	- dát tomu .txt příponu, ať to můžou noobové také otevřít
- rovněž nějak rozumně uložit RGB nastavení

### Animace, TODO: pobavit se o tom s Kačkou
| nahrání configu         | bílé pulznutí (že ho to vzalo)                              |
| odstranění configu      | červené pulznutí (že zmizel)                                |
| připojování k Wifi      | tikání jako hodiny (bíle)                                   |
| připojování k serveru   | tikání jako hodiny (zeleně); dělat to pořád, ikdyž to nejde |
| čekání na druhého       | plynulé posouvání ledek, do tlukotu srdce pak měnit barvu   |
| stalo se něco strašnýho | červené pulzování                                           |

## Misc.
- zkusit jiné fonty u loga, srdce ale vypadá docela hezky
- `inotify` (u configu) v separátním Python threadu?
- `public` klíč -- veřejné připojování
	- vždy má každý timeout, ať to nemůže spamovat
- umožnění více připojení
- neromantické/nepárové edice -- jiné barvy, žádný tlukot srdce
	- user-defined
