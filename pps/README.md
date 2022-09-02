# PPS pro synchronizaci času. 

Pro přesnou synchronyzaci času se v autech použivá více zdrojů. Jedním z nich jsou NMEA/UBX zprávy a PPS signál z ublox GNSS přijimače. Jako lokální server času pak slouží [chrony]().

GPS se zapojuje do GPIO portu routeru OMNIA. Celé řešení NTP/CHRONY serveru je nainstalované v openwrt linuxu omnie. 

![PPS z GPS](/doc/omnia_gps_connection/omnia_gps_connection.svg)


## Instalace (S přimou úpravou DeviceTree)
Instalace je trochu obtížnější, protože je potřeba upravit device-tree, což je velmi citlivé místo. A může toho docela dost rozbít. 

> [20220901] Nepodařilo se mi rozfungovat device-tree overlay, takže je nutné tyto úpravy realizovat přimo v devicetree omnie. 

> Toto řešení má problém, že při aktualizaci omnie může dojít k obnovení (nahrazení za nové) DeviceTree a tím příjdeme o naše úpravy. V případě, že se to stane, tak stačí provést pouze úpravu DeviceTree. 

nejdříve je potřeba nainstalovat určité balíčky. To lze přimo z repozitářů OpenWRT

```
 opkg update
 opkg install pps-tools kmod-pps kmod-pps-gpio dtc
```


> Tohle pravděpodobně není nutné dělat. Ale nechávám to tu pro případ, že by něco nefungovalo správně
> ```
>  echo 18 > /sys/class/gpio/export
>  echo in > /sys/class/gpio/gpio18/direction
> ```


#### DeviceTree
Nejdříve je vhdoné si starý devicetree zazálohovat. Následně původní device tree rozbalit a provést v něm úpravy. 
```
cd /boot 
cp armada-385-turris-omnia-phy.dtb armada-385-turris-omnia-phy_backu.dtb
dtc -I dtb -O dts -f armada-385-turris-omnia-phy.dtb -o armada-385-turris-omnia-phy.dts
vi armada-385-turris-omnia-phy.dts
```

Ve `vi` editoru pak najděte blok, který je označený `gpio@18100` a na jeho konec (do závorek) připište:
```
                                 linux,phandle = <0x1e>;
                                 phandle = <0x1e>;
```

Na konec souboru (před poslední závorku, na stejnou úroveň jako je například `sfp` blok) připište:
```
        pps@18 {
                gpios = <0x1e 0x12 0x0>;
                compatible = "pps-gpio";
                status = "okay";
        };
```

Po uložení souboru musíme devicetree zase zabalit příkazem
```
dtc -I dts -O dtb -f armada-385-turris-omnia-phy.dts -o armada-385-turris-omnia-phy.dtb
```

Nyní je potřeba Omnii zrestartovat. 

## Ověření funkce
Jestli je správně devicetree nastaveno lze ověřit tím, že v /dev se nám vytvořil soubor `/dev/pps0`. 

V `dmesg` pak vydíme takovéto výpisy:
```
root@turris:~# dmesg | grep pps
[    6.562033] pps_core: LinuxPPS API ver. 1 registered
[    6.567011] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
[    6.576738] pps pps0: new PPS source pps@18.-1
[    6.581220] pps pps0: Registered IRQ 76 as PPS source
```

Pokud chceme ověřit, že počítač detekuje PPS signály, tak to lze udělat příkazem `ppstest /dev/pps0`, kde každý řádek značí jeden PPS signál. 




## Instalace pomocí DeviceTree Overlay (Nefunkční postup)
Tento způsob by měl pomoct, aby se nemusel devicetree upravovat po aktualizaci omnie. 
* soubor `[pps_overlay.dtso](CRREAT_cars/pps/pps_overlay.dtso)` zkopírovat do `/boot`
* Zabalit ho příkazem `dtc -@ -I dts -O dtb -o /boot/overlays/pps_overlay.dtbo /boot/pps_overlay.dtso`
* Vytvořit soubor `/boot/config.txt` s řádekm `dtoverlay=pps_overlay`

To by mělo být vše. Ale tento postup mi nefunguje a nevím, kde je chyba. Možná v samotném overlay soboru, možná v kompilaci nebo v config.txt souboru, který na omnii z neznámého důvodu neexistuje. 
