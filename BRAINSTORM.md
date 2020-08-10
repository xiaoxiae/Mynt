# Brainstorming

## Jména
- thinking of you
	- TOY
- thinking about you
	- THAY
	- TAYO
	- TABY
- myslím na tebe
	- MYNT

## HW
- RPI-zero (w)
	- micro USB napájení
	- baterie? možná ty samsungácké, které mám ve skříni?
		- bylo by složitější na implementaci
		- někde by musel být indikátor baterie ()
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

## Setup

### Wifi-based
- RPI hostne wifinu, na kterou se uživatel připojí
- bude tam interface, do kterého se zadá jméno a heslo Wifi sítě, na kterou se má připojit
- pokud to vyjde, tak se to připojí a zůstane to na té wifině, člověk s tím bude moci komunikovat přes stejný interface, ale přes internet
	- tohle je TODO, bude výrazně těžší a bude chtít server
- configure button -- zmáčknutí odpojí od wifiny a promptne ten config

### Bluetooth-based
- podobné jako wifi, ale přes bluetooth
	- RPI hostuje aplikaci a mobil na ni vidí přes Bluetooth -- jde tohle vůbec?
- asi větší oser -- aplikace na různá zařízení

### Kabel-based
- připojení vystaví na světlo nějakou složku s konfigurákem, který si uživatel upraví
- mohlo by fungovat paralelně s dalšími metodami
