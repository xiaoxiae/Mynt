# Brainstorming

## Jména
- thinking of you
	- TOY
- thinking about you
	- THAY
	- TAYO
	- TABY

## HW
- RPI-zero (w)
	- micro USB napájení
	- baterie? možná ty samsungácké, které mám ve skříni?
		- bylo by složitější na implementaci
		- někde by musel být indikátor baterie
- nějaké RGB diody
- button by měl být fluffy
	- ne příliš pevné
	- aby to bylo příjemné na dotek
	- mělo by stačit jemně položit ruku, aby se to stisklo
	- nějaké jemné pružinky?

## Ostatní?
- lokální mód -- zařízení by se na síti našla a začala spolu komunikovat
- žádné zvuky -- pouze obraz
- co vibrace (variabilní)?

## Setup

### Wifi-based
- RPI hostne wifinu, na kterou se uživatel připojí
- bude tam interface, do kterého se zadá jméno a heslo Wifi sítě, na kterou se má připojit
- pokud to vyjde, tak se to připojí a zůstane to na té wifině, člověk s tím bude moci komunikovat přes stejný interface, ale přes internet
	- tohle je TODO, bude výrazně těžší a bude chtít server
- configure button -- zmáčknutí odpojí od wifiny a promptne ten config

### Bluetooth-based
- podobné jako wifi, ale přes bluetooth
- možná větší oser -- aplikace na různá zařízení
