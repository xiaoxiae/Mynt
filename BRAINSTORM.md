# Brainstorming

## HW
- RPI-zero (w), micro USB napájení
- RGB (individuálně ovladatelné) LEDky
	- https://www.tme.eu/cz/details/hcbaa30w/zdroje-svetla-pasy-led/worldsemi/hc-f5v-30l-30led-w-ws2813-ip20/
- z buttonu by měl být dobrý pocit
	- příjemné na dotek
	- ne příliš tuhé (ať člověk ne musí tlačit)
	- mělo by stačit jemně položit ruku, aby se to stisklo
		- https://www.ebay.com/itm/133046589546
		- https://www.ebay.com/itm/363054390399
- design z 3D scanu (ručního) nějaké modelíny -- ať je to hezky přírodní tvar
- žádné zvuky (pro uživatele otravné, těžké na implemetaci... fuj)
- vibrace?
	- https://www.ebay.com/itm/133285018930
	- variabilní se silou stisku?
	- co vibrovat do tlukotu srdce?
		- vestavěný, definovaný rytmus
		- co to měřit?
			- https://www.ebay.com/itm/254337746890

## Ostatní?
- lokální -- zařízení by se na síti našla a začala spolu komunikovat
- server -- povídání si se serverem přes Wifinu

## Kabel-based konfigurace
- připojení vystaví složku s konfigurákem, který si uživatel upraví
- použití MTP, aby se to chovalo, jako když se připojuje mobil
- `yaml` soubor, na který RPIčko kouká a něco dělá, když se změní
- rovněž nějak rozumně uložit RGB nastavení
- dát tomu .txt příponu, ať to můžou noobové také otevřít
