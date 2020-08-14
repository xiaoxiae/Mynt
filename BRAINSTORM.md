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
	- na druhé straně to bude tak vibrovat
	- asi palec-ukazováček
- pohodlné držení
- možné vibrace
	- https://www.ebay.com/itm/133285018930

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
- `yaml` soubor, na který RPIčko kouká a něco dělá, když se změní
	- dát tomu .txt příponu, ať to můžou noobové také otevřít
- rovněž nějak rozumně uložit RGB nastavení

### Chování ledek, TODO: pobavit se o tom s Kačkou
| něco se posralo       | červené pulzování, TODO: nějak rozlišit co?               |
| změna configu         | bílé pulznutí (že ho to vzalo)                            |
| připojování k Wifi    | tikání jako hodiny (bíle)                                 |
| připojování k serveru | tikání jako hodiny (zeleně)                               |
| čekání na druhého     | plynulé posouvání ledek, do tlukotu srdce pak měnit barvu |

## Misc.
- zkusit jiné fonty u loga, srdce ale vypadá docela hezky
