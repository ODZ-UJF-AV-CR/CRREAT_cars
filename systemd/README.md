# Jak se používají systemd skripty? 
Použití je relativně jednoduché. Je k tomu pár příkazů, kterými lze zjistit stav, zapnout nebo vypnout jednotlivé služby. 

## Zjištění aktuálního stavu 
sudo service <název sluzby> status

## Ruční zapnutí služby
sudo service <nazev sluby> start

## Ruční vypnutí služby
sudo service <nazev sluby> stop


## Používání skriptů v autech. 
Služby lze používat dvojím způsobem. Buď jsou do systemd nalinkované a jejich umístění může být kdekoliv v počítači nebo je možné ho přesunout do správné systemd složky. Vhodnejši je používat varinatu linkování, protože je tak vetší přehled nad tím, jaké skripty se kde používají. A také je snazší jejich aktualizace, protože mohou být nalinkované přímo z nějakého repozitáře, který lze zálohovat. 

## Linkování nového skriptu

```
systemctl link <cela cesta k souboru s připonou .service> 
```
Tím by systemd měl náši novou službu znát a měl by být možné ji spustit. 


## Změna služby 
Pokud provedeme nějakou úpravu v .service souboru, pak 
