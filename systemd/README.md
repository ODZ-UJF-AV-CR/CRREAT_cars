

## Konfigurace softwaru

Auta vždy byla v trochu rozdílném stavu, a dosáhnout toho že budou úplně stejné je dost složité. Kvůli tomu vznikl globální konfigurační soubor pro celé auto. V principu to nastavuje sysenv, které jsou v každém kontejneru nastaveny globálně a skripty pro obsluhu jednotlivých zařízní by s tím měli pracovat. 

Konfigurace je uložena v [tomto]() repozitáři a do systému se zavádí pomocí symlinku. Pro případ aktualizace je forma symlinku vhodná, protože tato konfigurace bude vždy uložena na githubu.

```
ln -s /home/kaklik/repos/CRREAT_cars/systemd/CAR2_env.conf /etc/environment.d/00-crreat.conf
```

## Proměnné

Seznam proměnných, které by měly obsahovat věchny konfigurace:

* **STATION** - název detekční stanice, např CAR0
