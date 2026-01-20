# Digitalizace
#### Podproblémy:
- Vzorkování (sampling) - měříme jen na diskrétních místech - mřížka
- Kvantování - a měříme jen s určitou přesností - hloubka pixelu

## Vzorkování (sampling)
- **vzorkovací teorém**
	- za určitých podmínek je možné zrekonstruovat z diskrétních hodnot kontinuum
	- za jakých?
- matematický model
	- obrazová oblast
		- naši funkci pronásobíme polem delta funkcí (značíme $s$) - Diracův hřeben 
	- frekvenční oblast
		- v mřížce opakujeme celé spektrum - spektrum musí být středově souměrné <img src="attachments/Pasted image 20260119164002.png" width="300px">
		- získat zpátky obrázek znamená vyříznout jedno to spektrum a udělat fourierku - tohle v praxi nejde ale je to jen myšlenkový koncept
			- nyquistova podmínka (nyquistovi nerovnosti)
				- do kdy můžeme vzorkovat, bez toho abychom ztratily informace
					- aby se nám nezačali spektra překrývat (jejich bounding boxy)$$\Delta x \leq \frac{1}{2W_u},\quad\Delta y \leq \frac{1}{2W_v}$$
					- pokud se toto stane tak nastane aliasing (např kvůli nedostatečnou frekvencí vzorkování)
						- to pak tvoří **Moiré efekt!
							- falešné nízké frekvence<img src="attachments/Pasted image 20260119163508.png">
								- může způsobit že třeba kola se točí ve filmu opačným směrem, nebo že cirkulárka pod žárovkou vypadá že stojí
								- využití - námořní navigace
							- řešení - anti-aliasing
								- zvýšení rozlišení
								- jediný způsob jak to skutečně řešit je malinko rozmazat obrázek
				- v praxi se vzorkuje nyquistovsky, protože čočka slouží jako low pass filter (pustí jen vysoké freq) -> sama od sebe to frekvenčně omezí
			- vyříznutí odpovídá
				- matematicky - pronásobení box funkcí, která je všude jinde 0, značíme H(x,y)
				- obrazově - interpolace d(x, y) konvolucí s funkcí h(x, y)
					- to by v případě nearest neighbor byla zase box funkce s supportem 1, v případě lineární to bude troúhelník s supportem 2, kvadratická je kopeček se supportem 4
						- v praxi se hodně používá bilineární (kompromis rychlost a vyhlazení) 
							- ve 2D jsou to 3 lineární interpolace
							- interpolační plocha je hyperbolický paraboloid - přímková plocha
					- stejný koncept jako u B-spline, kde $B_n = B_{n-1} * B_0$
## Kvantování
- vždy ztrátové - převádíme reálné číslo na 0...L (kde L je nejčastěji 255)
	- nevratné!
- parametry:
	- L - počet kvantovacích hladin
	- rozmístění kvantovacích prahů
		- v praxi jsou většinou rovnoměrně
		- existuje i logaritmické kvantování
- kvantizační šum (falešné kvantovací hrany) <img src="attachments/Pasted image 20260119163638.png" width="400px">
	- tyto hrany jsou nerozeznatelné od reálných
- pokud optimalizujeme poměr vzorkovací frekvence k počtu kvantovacích hladin aby vypadal co nejlépe
	- pokud obrázek je detailní (má převážně vysoké frekvence) -> důležitější je vzorkovací frekvence
	- pokud obrázek má jemné přechody (má převážně nízké frekvence) -> důležitější je počet kvantovacích prahů