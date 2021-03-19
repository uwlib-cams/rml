import csv
import rdflib
from rdflib import *
import os
from sys import argv
import time

script, csv_dir = argv

"""Lists"""

nosplit_bnode_list = [
"Provisionactivity_Publication_",
"Provisionactivity_Production_",
"Provisionactivity_Distribution_",
"Provisionactivity_Manufacture_",
"Lang_Contribution_10001_",
"Not_Lang_Contribution_10001_",
"IRI_Contribution_10001_",
"Lang_Contribution_10005_",
"Not_Lang_Contribution_10005_",
"IRI_Contribution_10005_",
"Lang_Contribution_10007_",
"Not_Lang_Contribution_10007_",
"IRI_Contribution_10007_",
"Lang_Contribution_10008_",
"Not_Lang_Contribution_10008_",
"Lang_Contribution_10008_",
"Not_Lang_Contribution_10008_",
"IRI_Contribution_10008_",
"Lang_Contribution_10009_",
"Not_Lang_Contribution_10009_",
"IRI_Contribution_10009_",
"Lang_Contribution_10010_",
"Not_Lang_Contribution_10010_",
"IRI_Contribution_10010_",
"Lang_Contribution_10013_",
"Not_Lang_Contribution_10013_",
"Lang_Contribution_10013_",
"Not_Lang_Contribution_10013_",
"IRI_Contribution_10013_",
"Lang_Contribution_10014_",
"Not_Lang_Contribution_10014_",
"IRI_Contribution_10014_",
"Lang_Contribution_10015_",
"Not_Lang_Contribution_10015_",
"Lang_Contribution_10015_",
"Not_Lang_Contribution_10015_",
"IRI_Contribution_10015_",
"Lang_Contribution_10017_",
"Not_Lang_Contribution_10017_",
"IRI_Contribution_10017_",
"Lang_Contribution_10018_",
"Not_Lang_Contribution_10018_",
"IRI_Contribution_10018_",
"Lang_Contribution_10035_",
"Not_Lang_Contribution_10035_",
"IRI_Contribution_10035_",
"Lang_Contribution_10036_",
"Not_Lang_Contribution_10036_",
"IRI_Contribution_10036_",
"Lang_Contribution_10041_",
"Not_Lang_Contribution_10041_",
"IRI_Contribution_10041_",
"Lang_Contribution_10042_",
"Not_Lang_Contribution_10042_",
"IRI_Contribution_10042_",
"Lang_Contribution_10043_",
"Not_Lang_Contribution_10043_",
"IRI_Contribution_10043_",
"Lang_Contribution_10044_",
"Not_Lang_Contribution_10044_",
"IRI_Contribution_10044_",
"Lang_Contribution_10045_",
"Not_Lang_Contribution_10045_",
"IRI_Contribution_10045_",
"Lang_Contribution_10046_",
"Not_Lang_Contribution_10046_",
"IRI_Contribution_10046_",
"Lang_Contribution_10048_",
"Not_Lang_Contribution_10048_",
"IRI_Contribution_10048_",
"Lang_Contribution_10049_",
"Not_Lang_Contribution_10049_",
"IRI_Contribution_10049_",
"Lang_Contribution_10050_",
"Not_Lang_Contribution_10050_",
"IRI_Contribution_10050_",
"Lang_Contribution_10051_",
"Not_Lang_Contribution_10051_",
"IRI_Contribution_10051_",
"Lang_Contribution_10052_",
"Not_Lang_Contribution_10052_",
"Lang_Contribution_10052_",
"Not_Lang_Contribution_10052_",
"IRI_Contribution_10052_",
"Lang_Contribution_10053_",
"Not_Lang_Contribution_10053_",
"IRI_Contribution_10053_",
"Lang_Contribution_10054_",
"Not_Lang_Contribution_10054_",
"IRI_Contribution_10054_",
"Lang_Contribution_10055_",
"Not_Lang_Contribution_10055_",
"Lang_Contribution_10055_",
"Not_Lang_Contribution_10055_",
"IRI_Contribution_10055_",
"Lang_Contribution_10056_",
"Not_Lang_Contribution_10056_",
"IRI_Contribution_10056_",
"Lang_Contribution_10057_",
"Not_Lang_Contribution_10057_",
"IRI_Contribution_10057_",
"Lang_Contribution_10058_",
"Not_Lang_Contribution_10058_",
"Lang_Contribution_10058_",
"Not_Lang_Contribution_10058_",
"IRI_Contribution_10058_",
"Lang_Contribution_10059_",
"Not_Lang_Contribution_10059_",
"IRI_Contribution_10059_",
"Lang_Contribution_10060_",
"Not_Lang_Contribution_10060_",
"IRI_Contribution_10060_",
"Lang_Contribution_10061_",
"Not_Lang_Contribution_10061_",
"Lang_Contribution_10061_",
"Not_Lang_Contribution_10061_",
"IRI_Contribution_10061_",
"Lang_Contribution_10062_",
"Not_Lang_Contribution_10062_",
"IRI_Contribution_10062_",
"Lang_Contribution_10063_",
"Not_Lang_Contribution_10063_",
"IRI_Contribution_10063_",
"Lang_Contribution_10064_",
"Not_Lang_Contribution_10064_",
"IRI_Contribution_10064_",
"Lang_Contribution_10065_",
"Not_Lang_Contribution_10065_",
"IRI_Contribution_10065_",
"Lang_Contribution_10066_",
"Not_Lang_Contribution_10066_",
"IRI_Contribution_10066_",
"Lang_Contribution_10067_",
"Not_Lang_Contribution_10067_",
"IRI_Contribution_10067_",
"Lang_Contribution_10068_",
"Not_Lang_Contribution_10068_",
"Lang_Contribution_10068_",
"Not_Lang_Contribution_10068_",
"IRI_Contribution_10068_",
"Lang_Contribution_10069_",
"Not_Lang_Contribution_10069_",
"IRI_Contribution_10069_",
"Lang_Contribution_10070_",
"Not_Lang_Contribution_10070_",
"IRI_Contribution_10070_",
"Lang_Contribution_10071_",
"Not_Lang_Contribution_10071_",
"IRI_Contribution_10071_",
"Lang_Contribution_10073_",
"Not_Lang_Contribution_10073_",
"Lang_Contribution_10073_",
"Not_Lang_Contribution_10073_",
"IRI_Contribution_10073_",
"Lang_Contribution_10074_",
"Not_Lang_Contribution_10074_",
"IRI_Contribution_10074_",
"Lang_Contribution_10075_",
"Not_Lang_Contribution_10075_",
"Lang_Contribution_10075_",
"Not_Lang_Contribution_10075_",
"IRI_Contribution_10075_",
"Lang_Contribution_10200_",
"Not_Lang_Contribution_10200_",
"IRI_Contribution_10200_",
"Lang_Contribution_10202_",
"Not_Lang_Contribution_10202_",
"IRI_Contribution_10202_",
"Lang_Contribution_10203_",
"Not_Lang_Contribution_10203_",
"Lang_Contribution_10203_",
"Not_Lang_Contribution_10203_",
"IRI_Contribution_10203_",
"Lang_Contribution_10204_",
"Not_Lang_Contribution_10204_",
"IRI_Contribution_10204_",
"Lang_Contribution_10205_",
"Not_Lang_Contribution_10205_",
"IRI_Contribution_10205_",
"Lang_Contribution_10253_",
"Not_Lang_Contribution_10253_",
"IRI_Contribution_10253_",
"Lang_Contribution_10254_",
"Not_Lang_Contribution_10254_",
"IRI_Contribution_10254_",
"Lang_Contribution_10255_",
"Not_Lang_Contribution_10255_",
"IRI_Contribution_10255_",
"Lang_Contribution_10284_",
"Not_Lang_Contribution_10284_",
"IRI_Contribution_10284_",
"Lang_Contribution_10285_",
"Not_Lang_Contribution_10285_",
"IRI_Contribution_10285_",
"Lang_Contribution_10286_",
"Not_Lang_Contribution_10286_",
"IRI_Contribution_10286_",
"Lang_Contribution_10287_",
"Not_Lang_Contribution_10287_",
"Lang_Contribution_10287_",
"Not_Lang_Contribution_10287_",
"IRI_Contribution_10287_",
"Lang_Contribution_10292_",
"Not_Lang_Contribution_10292_",
"Lang_Contribution_10292_",
"Not_Lang_Contribution_10292_",
"IRI_Contribution_10292_",
"Lang_Contribution_10293_",
"Not_Lang_Contribution_10293_",
"IRI_Contribution_10293_",
"Lang_Contribution_10297_",
"Not_Lang_Contribution_10297_",
"IRI_Contribution_10297_",
"Lang_Contribution_10298_",
"Not_Lang_Contribution_10298_",
"IRI_Contribution_10298_",
"Lang_Contribution_10299_",
"Not_Lang_Contribution_10299_",
"Lang_Contribution_10299_",
"Not_Lang_Contribution_10299_",
"IRI_Contribution_10299_",
"Lang_Contribution_10304_",
"Not_Lang_Contribution_10304_",
"Lang_Contribution_10304_",
"Not_Lang_Contribution_10304_",
"IRI_Contribution_10304_",
"Lang_Contribution_10305_",
"Not_Lang_Contribution_10305_",
"Lang_Contribution_10305_",
"Not_Lang_Contribution_10305_",
"IRI_Contribution_10305_",
"Lang_Contribution_10306_",
"Not_Lang_Contribution_10306_",
"Lang_Contribution_10306_",
"Not_Lang_Contribution_10306_",
"IRI_Contribution_10306_",
"Lang_Contribution_10311_",
"Not_Lang_Contribution_10311_",
"IRI_Contribution_10311_",
"Lang_Contribution_10312_",
"Not_Lang_Contribution_10312_",
"IRI_Contribution_10312_",
"Lang_Contribution_10313_",
"Not_Lang_Contribution_10313_",
"IRI_Contribution_10313_",
"Lang_Contribution_10314_",
"Not_Lang_Contribution_10314_",
"IRI_Contribution_10314_",
"Lang_Contribution_10315_",
"Not_Lang_Contribution_10315_",
"IRI_Contribution_10315_",
"Lang_Contribution_10394_",
"Not_Lang_Contribution_10394_",
"IRI_Contribution_10394_",
"Lang_Contribution_10395_",
"Not_Lang_Contribution_10395_",
"IRI_Contribution_10395_",
"Lang_Contribution_10396_",
"Not_Lang_Contribution_10396_",
"IRI_Contribution_10396_",
"Lang_Contribution_10397_",
"Not_Lang_Contribution_10397_",
"IRI_Contribution_10397_",
"Lang_Contribution_10412_",
"Not_Lang_Contribution_10412_",
"IRI_Contribution_10412_",
"Lang_Contribution_10413_",
"Not_Lang_Contribution_10413_",
"IRI_Contribution_10413_",
"Lang_Contribution_10414_",
"Not_Lang_Contribution_10414_",
"IRI_Contribution_10414_",
"Lang_Contribution_10415_",
"Not_Lang_Contribution_10415_",
"Lang_Contribution_10415_",
"Not_Lang_Contribution_10415_",
"IRI_Contribution_10415_",
"Lang_Contribution_10416_",
"Not_Lang_Contribution_10416_",
"IRI_Contribution_10416_",
"Lang_Contribution_10417_",
"Not_Lang_Contribution_10417_",
"IRI_Contribution_10417_",
"Lang_Contribution_10418_",
"Not_Lang_Contribution_10418_",
"Lang_Contribution_10418_",
"Not_Lang_Contribution_10418_",
"IRI_Contribution_10418_",
"Lang_Contribution_10419_",
"Not_Lang_Contribution_10419_",
"IRI_Contribution_10419_",
"Lang_Contribution_10420_",
"Not_Lang_Contribution_10420_",
"Lang_Contribution_10420_",
"Not_Lang_Contribution_10420_",
"IRI_Contribution_10420_",
"Lang_Contribution_10421_",
"Not_Lang_Contribution_10421_",
"Lang_Contribution_10421_",
"Not_Lang_Contribution_10421_",
"IRI_Contribution_10421_",
"Lang_Contribution_10422_",
"Not_Lang_Contribution_10422_",
"Lang_Contribution_10422_",
"Not_Lang_Contribution_10422_",
"IRI_Contribution_10422_",
"Lang_Contribution_10423_",
"Not_Lang_Contribution_10423_",
"IRI_Contribution_10423_",
"Lang_Contribution_10424_",
"Not_Lang_Contribution_10424_",
"Lang_Contribution_10424_",
"Not_Lang_Contribution_10424_",
"IRI_Contribution_10424_",
"Lang_Contribution_10425_",
"Not_Lang_Contribution_10425_",
"IRI_Contribution_10425_",
"Lang_Contribution_10426_",
"Not_Lang_Contribution_10426_",
"IRI_Contribution_10426_",
"Lang_Contribution_10427_",
"Not_Lang_Contribution_10427_",
"IRI_Contribution_10427_",
"Lang_Contribution_10428_",
"Not_Lang_Contribution_10428_",
"IRI_Contribution_10428_",
"Lang_Contribution_10429_",
"Not_Lang_Contribution_10429_",
"Lang_Contribution_10429_",
"Not_Lang_Contribution_10429_",
"IRI_Contribution_10429_",
"Lang_Contribution_10430_",
"Not_Lang_Contribution_10430_",
"IRI_Contribution_10430_",
"Lang_Contribution_10431_",
"Not_Lang_Contribution_10431_",
"IRI_Contribution_10431_",
"Lang_Contribution_10432_",
"Not_Lang_Contribution_10432_",
"IRI_Contribution_10432_",
"Lang_Contribution_10433_",
"Not_Lang_Contribution_10433_",
"IRI_Contribution_10433_",
"Lang_Contribution_10434_",
"Not_Lang_Contribution_10434_",
"IRI_Contribution_10434_",
"Lang_Contribution_10435_",
"Not_Lang_Contribution_10435_",
"Lang_Contribution_10435_",
"Not_Lang_Contribution_10435_",
"IRI_Contribution_10435_",
"Lang_Contribution_10436_",
"Not_Lang_Contribution_10436_",
"Lang_Contribution_10436_",
"Not_Lang_Contribution_10436_",
"IRI_Contribution_10436_",
"Lang_Contribution_10437_",
"Not_Lang_Contribution_10437_",
"IRI_Contribution_10437_",
"Lang_Contribution_10438_",
"Not_Lang_Contribution_10438_",
"IRI_Contribution_10438_",
"Lang_Contribution_10439_",
"Not_Lang_Contribution_10439_",
"Lang_Contribution_10439_",
"Not_Lang_Contribution_10439_",
"IRI_Contribution_10439_",
"Lang_Contribution_10440_",
"Not_Lang_Contribution_10440_",
"IRI_Contribution_10440_",
"Lang_Contribution_10441_",
"Not_Lang_Contribution_10441_",
"IRI_Contribution_10441_",
"Lang_Contribution_10442_",
"Not_Lang_Contribution_10442_",
"IRI_Contribution_10442_",
"Lang_Contribution_10443_",
"Not_Lang_Contribution_10443_",
"IRI_Contribution_10443_",
"Lang_Contribution_10444_",
"Not_Lang_Contribution_10444_",
"Lang_Contribution_10444_",
"Not_Lang_Contribution_10444_",
"IRI_Contribution_10444_",
"Lang_Contribution_10445_",
"Not_Lang_Contribution_10445_",
"IRI_Contribution_10445_",
"Lang_Contribution_10446_",
"Not_Lang_Contribution_10446_",
"IRI_Contribution_10446_",
"Lang_Contribution_10447_",
"Not_Lang_Contribution_10447_",
"IRI_Contribution_10447_",
"Lang_Contribution_10449_",
"Not_Lang_Contribution_10449_",
"Lang_Contribution_10449_",
"Not_Lang_Contribution_10449_",
"IRI_Contribution_10449_",
"Lang_Contribution_10450_",
"Not_Lang_Contribution_10450_",
"IRI_Contribution_10450_",
"Lang_Contribution_10451_",
"Not_Lang_Contribution_10451_",
"Lang_Contribution_10451_",
"Not_Lang_Contribution_10451_",
"IRI_Contribution_10451_",
"Lang_Contribution_10452_",
"Not_Lang_Contribution_10452_",
"Lang_Contribution_10452_",
"Not_Lang_Contribution_10452_",
"IRI_Contribution_10452_",
"Lang_Contribution_10453_",
"Not_Lang_Contribution_10453_",
"Lang_Contribution_10453_",
"Not_Lang_Contribution_10453_",
"IRI_Contribution_10453_",
"Lang_Contribution_10454_",
"Not_Lang_Contribution_10454_",
"IRI_Contribution_10454_",
"Lang_Contribution_10455_",
"Not_Lang_Contribution_10455_",
"IRI_Contribution_10455_",
"Lang_Contribution_10456_",
"Not_Lang_Contribution_10456_",
"IRI_Contribution_10456_",
"Lang_Contribution_10457_",
"Not_Lang_Contribution_10457_",
"IRI_Contribution_10457_",
"Lang_Contribution_10458_",
"Not_Lang_Contribution_10458_",
"IRI_Contribution_10458_",
"Lang_Contribution_10459_",
"Not_Lang_Contribution_10459_",
"IRI_Contribution_10459_",
"Lang_Contribution_10460_",
"Not_Lang_Contribution_10460_",
"IRI_Contribution_10460_",
"Lang_Contribution_10461_",
"Not_Lang_Contribution_10461_",
"IRI_Contribution_10461_",
"Lang_Contribution_10462_",
"Not_Lang_Contribution_10462_",
"Lang_Contribution_10462_",
"Not_Lang_Contribution_10462_",
"IRI_Contribution_10462_",
"Lang_Contribution_10463_",
"Not_Lang_Contribution_10463_",
"IRI_Contribution_10463_",
"Lang_Contribution_10464_",
"Not_Lang_Contribution_10464_",
"IRI_Contribution_10464_",
"Lang_Contribution_10465_",
"Not_Lang_Contribution_10465_",
"Lang_Contribution_10465_",
"Not_Lang_Contribution_10465_",
"IRI_Contribution_10465_",
"Lang_Contribution_10466_",
"Not_Lang_Contribution_10466_",
"IRI_Contribution_10466_",
"Lang_Contribution_10467_",
"Not_Lang_Contribution_10467_",
"Lang_Contribution_10467_",
"Not_Lang_Contribution_10467_",
"IRI_Contribution_10467_",
"Lang_Contribution_10468_",
"Not_Lang_Contribution_10468_",
"Lang_Contribution_10468_",
"Not_Lang_Contribution_10468_",
"IRI_Contribution_10468_",
"Lang_Contribution_10469_",
"Not_Lang_Contribution_10469_",
"Lang_Contribution_10469_",
"Not_Lang_Contribution_10469_",
"IRI_Contribution_10469_",
"Lang_Contribution_10470_",
"Not_Lang_Contribution_10470_",
"IRI_Contribution_10470_",
"Lang_Contribution_10471_",
"Not_Lang_Contribution_10471_",
"Lang_Contribution_10471_",
"Not_Lang_Contribution_10471_",
"IRI_Contribution_10471_",
"Lang_Contribution_10472_",
"Not_Lang_Contribution_10472_",
"IRI_Contribution_10472_",
"Lang_Contribution_10473_",
"Not_Lang_Contribution_10473_",
"IRI_Contribution_10473_",
"Lang_Contribution_10474_",
"Not_Lang_Contribution_10474_",
"IRI_Contribution_10474_",
"Lang_Contribution_10475_",
"Not_Lang_Contribution_10475_",
"IRI_Contribution_10475_",
"Lang_Contribution_10476_",
"Not_Lang_Contribution_10476_",
"Lang_Contribution_10476_",
"Not_Lang_Contribution_10476_",
"IRI_Contribution_10476_",
"Lang_Contribution_10477_",
"Not_Lang_Contribution_10477_",
"IRI_Contribution_10477_",
"Lang_Contribution_10478_",
"Not_Lang_Contribution_10478_",
"IRI_Contribution_10478_",
"Lang_Contribution_10479_",
"Not_Lang_Contribution_10479_",
"IRI_Contribution_10479_",
"Lang_Contribution_10480_",
"Not_Lang_Contribution_10480_",
"IRI_Contribution_10480_",
"Lang_Contribution_10481_",
"Not_Lang_Contribution_10481_",
"IRI_Contribution_10481_",
"Lang_Contribution_10482_",
"Not_Lang_Contribution_10482_",
"Lang_Contribution_10482_",
"Not_Lang_Contribution_10482_",
"IRI_Contribution_10482_",
"Lang_Contribution_10483_",
"Not_Lang_Contribution_10483_",
"Lang_Contribution_10483_",
"Not_Lang_Contribution_10483_",
"IRI_Contribution_10483_",
"Lang_Contribution_10484_",
"Not_Lang_Contribution_10484_",
"IRI_Contribution_10484_",
"Lang_Contribution_10485_",
"Not_Lang_Contribution_10485_",
"IRI_Contribution_10485_",
"Lang_Contribution_10486_",
"Not_Lang_Contribution_10486_",
"Lang_Contribution_10486_",
"Not_Lang_Contribution_10486_",
"IRI_Contribution_10486_",
"Lang_Contribution_10487_",
"Not_Lang_Contribution_10487_",
"IRI_Contribution_10487_",
"Lang_Contribution_10488_",
"Not_Lang_Contribution_10488_",
"IRI_Contribution_10488_",
"Lang_Contribution_10489_",
"Not_Lang_Contribution_10489_",
"IRI_Contribution_10489_",
"Lang_Contribution_10490_",
"Not_Lang_Contribution_10490_",
"IRI_Contribution_10490_",
"Lang_Contribution_10491_",
"Not_Lang_Contribution_10491_",
"Lang_Contribution_10491_",
"Not_Lang_Contribution_10491_",
"IRI_Contribution_10491_",
"Lang_Contribution_10492_",
"Not_Lang_Contribution_10492_",
"IRI_Contribution_10492_",
"Lang_Contribution_10493_",
"Not_Lang_Contribution_10493_",
"IRI_Contribution_10493_",
"Lang_Contribution_10494_",
"Not_Lang_Contribution_10494_",
"IRI_Contribution_10494_",
"Lang_Contribution_10496_",
"Not_Lang_Contribution_10496_",
"Lang_Contribution_10496_",
"Not_Lang_Contribution_10496_",
"IRI_Contribution_10496_",
"Lang_Contribution_10497_",
"Not_Lang_Contribution_10497_",
"IRI_Contribution_10497_",
"Lang_Contribution_10498_",
"Not_Lang_Contribution_10498_",
"Lang_Contribution_10498_",
"Not_Lang_Contribution_10498_",
"IRI_Contribution_10498_",
"Lang_Contribution_10499_",
"Not_Lang_Contribution_10499_",
"Lang_Contribution_10499_",
"Not_Lang_Contribution_10499_",
"IRI_Contribution_10499_",
"Lang_Contribution_10500_",
"Not_Lang_Contribution_10500_",
"Lang_Contribution_10500_",
"Not_Lang_Contribution_10500_",
"IRI_Contribution_10500_",
"Lang_Contribution_10501_",
"Not_Lang_Contribution_10501_",
"IRI_Contribution_10501_",
"Lang_Contribution_10502_",
"Not_Lang_Contribution_10502_",
"IRI_Contribution_10502_",
"Lang_Contribution_10503_",
"Not_Lang_Contribution_10503_",
"IRI_Contribution_10503_",
"Lang_Contribution_10504_",
"Not_Lang_Contribution_10504_",
"IRI_Contribution_10504_",
"Lang_Contribution_10505_",
"Not_Lang_Contribution_10505_",
"IRI_Contribution_10505_",
"Lang_Contribution_10506_",
"Not_Lang_Contribution_10506_",
"IRI_Contribution_10506_",
"Lang_Contribution_10507_",
"Not_Lang_Contribution_10507_",
"IRI_Contribution_10507_",
"Lang_Contribution_10508_",
"Not_Lang_Contribution_10508_",
"IRI_Contribution_10508_",
"Lang_Contribution_10509_",
"Not_Lang_Contribution_10509_",
"Lang_Contribution_10509_",
"Not_Lang_Contribution_10509_",
"IRI_Contribution_10509_",
"Lang_Contribution_10510_",
"Not_Lang_Contribution_10510_",
"IRI_Contribution_10510_",
"Lang_Contribution_10511_",
"Not_Lang_Contribution_10511_",
"IRI_Contribution_10511_",
"Lang_Contribution_10512_",
"Not_Lang_Contribution_10512_",
"Lang_Contribution_10512_",
"Not_Lang_Contribution_10512_",
"IRI_Contribution_10512_",
"Lang_Contribution_10513_",
"Not_Lang_Contribution_10513_",
"IRI_Contribution_10513_",
"Lang_Contribution_10514_",
"Not_Lang_Contribution_10514_",
"Lang_Contribution_10514_",
"Not_Lang_Contribution_10514_",
"IRI_Contribution_10514_",
"Lang_Contribution_10515_",
"Not_Lang_Contribution_10515_",
"Lang_Contribution_10515_",
"Not_Lang_Contribution_10515_",
"IRI_Contribution_10515_",
"Lang_Contribution_10516_",
"Not_Lang_Contribution_10516_",
"Lang_Contribution_10516_",
"Not_Lang_Contribution_10516_",
"IRI_Contribution_10516_",
"Lang_Contribution_10517_",
"Not_Lang_Contribution_10517_",
"IRI_Contribution_10517_",
"Lang_Contribution_10518_",
"Not_Lang_Contribution_10518_",
"Lang_Contribution_10518_",
"Not_Lang_Contribution_10518_",
"IRI_Contribution_10518_",
"Lang_Contribution_10519_",
"Not_Lang_Contribution_10519_",
"IRI_Contribution_10519_",
"Lang_Contribution_10520_",
"Not_Lang_Contribution_10520_",
"IRI_Contribution_10520_",
"Lang_Contribution_10521_",
"Not_Lang_Contribution_10521_",
"IRI_Contribution_10521_",
"Lang_Contribution_10522_",
"Not_Lang_Contribution_10522_",
"IRI_Contribution_10522_",
"Lang_Contribution_10523_",
"Not_Lang_Contribution_10523_",
"Lang_Contribution_10523_",
"Not_Lang_Contribution_10523_",
"IRI_Contribution_10523_",
"Lang_Contribution_10524_",
"Not_Lang_Contribution_10524_",
"IRI_Contribution_10524_",
"Lang_Contribution_10525_",
"Not_Lang_Contribution_10525_",
"IRI_Contribution_10525_",
"Lang_Contribution_10526_",
"Not_Lang_Contribution_10526_",
"IRI_Contribution_10526_",
"Lang_Contribution_10527_",
"Not_Lang_Contribution_10527_",
"IRI_Contribution_10527_",
"Lang_Contribution_10528_",
"Not_Lang_Contribution_10528_",
"IRI_Contribution_10528_",
"Lang_Contribution_10529_",
"Not_Lang_Contribution_10529_",
"Lang_Contribution_10529_",
"Not_Lang_Contribution_10529_",
"IRI_Contribution_10529_",
"Lang_Contribution_10530_",
"Not_Lang_Contribution_10530_",
"Lang_Contribution_10530_",
"Not_Lang_Contribution_10530_",
"IRI_Contribution_10530_",
"Lang_Contribution_10531_",
"Not_Lang_Contribution_10531_",
"IRI_Contribution_10531_",
"Lang_Contribution_10532_",
"Not_Lang_Contribution_10532_",
"IRI_Contribution_10532_",
"Lang_Contribution_10533_",
"Not_Lang_Contribution_10533_",
"Lang_Contribution_10533_",
"Not_Lang_Contribution_10533_",
"IRI_Contribution_10533_",
"Lang_Contribution_10534_",
"Not_Lang_Contribution_10534_",
"IRI_Contribution_10534_",
"Lang_Contribution_10535_",
"Not_Lang_Contribution_10535_",
"IRI_Contribution_10535_",
"Lang_Contribution_10536_",
"Not_Lang_Contribution_10536_",
"IRI_Contribution_10536_",
"Lang_Contribution_10537_",
"Not_Lang_Contribution_10537_",
"IRI_Contribution_10537_",
"Lang_Contribution_10538_",
"Not_Lang_Contribution_10538_",
"Lang_Contribution_10538_",
"Not_Lang_Contribution_10538_",
"IRI_Contribution_10538_",
"Lang_Contribution_10539_",
"Not_Lang_Contribution_10539_",
"IRI_Contribution_10539_",
"Lang_Contribution_10540_",
"Not_Lang_Contribution_10540_",
"IRI_Contribution_10540_",
"Lang_Contribution_10541_",
"Not_Lang_Contribution_10541_",
"IRI_Contribution_10541_",
"Lang_Contribution_10543_",
"Not_Lang_Contribution_10543_",
"Lang_Contribution_10543_",
"Not_Lang_Contribution_10543_",
"IRI_Contribution_10543_",
"Lang_Contribution_10544_",
"Not_Lang_Contribution_10544_",
"IRI_Contribution_10544_",
"Lang_Contribution_10545_",
"Not_Lang_Contribution_10545_",
"Lang_Contribution_10545_",
"Not_Lang_Contribution_10545_",
"IRI_Contribution_10545_",
"Lang_Contribution_10546_",
"Not_Lang_Contribution_10546_",
"Lang_Contribution_10546_",
"Not_Lang_Contribution_10546_",
"IRI_Contribution_10546_",
"Lang_Contribution_10547_",
"Not_Lang_Contribution_10547_",
"Lang_Contribution_10547_",
"Not_Lang_Contribution_10547_",
"IRI_Contribution_10547_",
"Lang_Contribution_10548_",
"Not_Lang_Contribution_10548_",
"IRI_Contribution_10548_",
"Lang_Contribution_10549_",
"Not_Lang_Contribution_10549_",
"IRI_Contribution_10549_",
"Lang_Contribution_10550_",
"Not_Lang_Contribution_10550_",
"IRI_Contribution_10550_",
"Lang_Contribution_10551_",
"Not_Lang_Contribution_10551_",
"IRI_Contribution_10551_",
"Lang_Contribution_10552_",
"Not_Lang_Contribution_10552_",
"IRI_Contribution_10552_",
"Lang_Contribution_10553_",
"Not_Lang_Contribution_10553_",
"IRI_Contribution_10553_",
"Lang_Contribution_10554_",
"Not_Lang_Contribution_10554_",
"IRI_Contribution_10554_",
"Lang_Contribution_10555_",
"Not_Lang_Contribution_10555_",
"IRI_Contribution_10555_",
"Lang_Contribution_10556_",
"Not_Lang_Contribution_10556_",
"Lang_Contribution_10556_",
"Not_Lang_Contribution_10556_",
"IRI_Contribution_10556_",
"Lang_Contribution_10557_",
"Not_Lang_Contribution_10557_",
"IRI_Contribution_10557_",
"Lang_Contribution_10558_",
"Not_Lang_Contribution_10558_",
"IRI_Contribution_10558_",
"Lang_Contribution_10559_",
"Not_Lang_Contribution_10559_",
"Lang_Contribution_10559_",
"Not_Lang_Contribution_10559_",
"IRI_Contribution_10559_",
"Lang_Contribution_10560_",
"Not_Lang_Contribution_10560_",
"IRI_Contribution_10560_",
"Lang_Contribution_10561_",
"Not_Lang_Contribution_10561_",
"Lang_Contribution_10561_",
"Not_Lang_Contribution_10561_",
"IRI_Contribution_10561_",
"Lang_Contribution_10562_",
"Not_Lang_Contribution_10562_",
"Lang_Contribution_10562_",
"Not_Lang_Contribution_10562_",
"IRI_Contribution_10562_",
"Lang_Contribution_10563_",
"Not_Lang_Contribution_10563_",
"Lang_Contribution_10563_",
"Not_Lang_Contribution_10563_",
"IRI_Contribution_10563_",
"Lang_Contribution_10564_",
"Not_Lang_Contribution_10564_",
"IRI_Contribution_10564_",
"Lang_Contribution_10565_",
"Not_Lang_Contribution_10565_",
"Lang_Contribution_10565_",
"Not_Lang_Contribution_10565_",
"IRI_Contribution_10565_",
"Lang_Contribution_10566_",
"Not_Lang_Contribution_10566_",
"IRI_Contribution_10566_",
"Lang_Contribution_10567_",
"Not_Lang_Contribution_10567_",
"IRI_Contribution_10567_",
"Lang_Contribution_10568_",
"Not_Lang_Contribution_10568_",
"IRI_Contribution_10568_",
"Lang_Contribution_10569_",
"Not_Lang_Contribution_10569_",
"IRI_Contribution_10569_",
"Lang_Contribution_10570_",
"Not_Lang_Contribution_10570_",
"Lang_Contribution_10570_",
"Not_Lang_Contribution_10570_",
"IRI_Contribution_10570_",
"Lang_Contribution_10571_",
"Not_Lang_Contribution_10571_",
"IRI_Contribution_10571_",
"Lang_Contribution_10572_",
"Not_Lang_Contribution_10572_",
"IRI_Contribution_10572_",
"Lang_Contribution_10573_",
"Not_Lang_Contribution_10573_",
"IRI_Contribution_10573_",
"Lang_Contribution_10574_",
"Not_Lang_Contribution_10574_",
"IRI_Contribution_10574_",
"Lang_Contribution_10575_",
"Not_Lang_Contribution_10575_",
"IRI_Contribution_10575_",
"Lang_Contribution_10576_",
"Not_Lang_Contribution_10576_",
"Lang_Contribution_10576_",
"Not_Lang_Contribution_10576_",
"IRI_Contribution_10576_",
"Lang_Contribution_10577_",
"Not_Lang_Contribution_10577_",
"Lang_Contribution_10577_",
"Not_Lang_Contribution_10577_",
"IRI_Contribution_10577_",
"Lang_Contribution_10578_",
"Not_Lang_Contribution_10578_",
"IRI_Contribution_10578_",
"Lang_Contribution_10579_",
"Not_Lang_Contribution_10579_",
"IRI_Contribution_10579_",
"Lang_Contribution_10580_",
"Not_Lang_Contribution_10580_",
"Lang_Contribution_10580_",
"Not_Lang_Contribution_10580_",
"IRI_Contribution_10580_",
"Lang_Contribution_10581_",
"Not_Lang_Contribution_10581_",
"IRI_Contribution_10581_",
"Lang_Contribution_10582_",
"Not_Lang_Contribution_10582_",
"IRI_Contribution_10582_",
"Lang_Contribution_10583_",
"Not_Lang_Contribution_10583_",
"IRI_Contribution_10583_",
"Lang_Contribution_10584_",
"Not_Lang_Contribution_10584_",
"IRI_Contribution_10584_",
"Lang_Contribution_10585_",
"Not_Lang_Contribution_10585_",
"Lang_Contribution_10585_",
"Not_Lang_Contribution_10585_",
"IRI_Contribution_10585_",
"Lang_Contribution_10586_",
"Not_Lang_Contribution_10586_",
"IRI_Contribution_10586_",
"Lang_Contribution_10587_",
"Not_Lang_Contribution_10587_",
"IRI_Contribution_10587_",
"Lang_Contribution_10588_",
"Not_Lang_Contribution_10588_",
"IRI_Contribution_10588_",
"Lang_Contribution_10590_",
"Not_Lang_Contribution_10590_",
"Lang_Contribution_10590_",
"Not_Lang_Contribution_10590_",
"IRI_Contribution_10590_",
"Lang_Contribution_10591_",
"Not_Lang_Contribution_10591_",
"IRI_Contribution_10591_",
"Lang_Contribution_10592_",
"Not_Lang_Contribution_10592_",
"Lang_Contribution_10592_",
"Not_Lang_Contribution_10592_",
"IRI_Contribution_10592_",
"Lang_Contribution_10593_",
"Not_Lang_Contribution_10593_",
"Lang_Contribution_10593_",
"Not_Lang_Contribution_10593_",
"IRI_Contribution_10593_",
"Lang_Contribution_10594_",
"Not_Lang_Contribution_10594_",
"Lang_Contribution_10594_",
"Not_Lang_Contribution_10594_",
"IRI_Contribution_10594_",
"Lang_Contribution_10595_",
"Not_Lang_Contribution_10595_",
"IRI_Contribution_10595_",
"Lang_Contribution_10596_",
"Not_Lang_Contribution_10596_",
"IRI_Contribution_10596_",
"Lang_Contribution_10597_",
"Not_Lang_Contribution_10597_",
"IRI_Contribution_10597_",
"Lang_Contribution_10598_",
"Not_Lang_Contribution_10598_",
"IRI_Contribution_10598_",
"Lang_Contribution_10599_",
"Not_Lang_Contribution_10599_",
"IRI_Contribution_10599_",
"Lang_Contribution_10604_",
"Not_Lang_Contribution_10604_",
"IRI_Contribution_10604_",
"Lang_Contribution_10605_",
"Not_Lang_Contribution_10605_",
"IRI_Contribution_10605_",
"Lang_Contribution_10606_",
"Not_Lang_Contribution_10606_",
"IRI_Contribution_10606_",
"Lang_Contribution_10607_",
"Not_Lang_Contribution_10607_",
"IRI_Contribution_10607_",
"IRI_Contribution_hasContributorAgent_",
"Lang_Contribution_hasContributorAgent_",
"Not_Lang_Contribution_hasContributorAgent_",
"Lang_Contribution_20011_",
"Not_Lang_Contribution_20011_",
"Lang_Contribution_20011_",
"Not_Lang_Contribution_20011_",
"IRI_Contribution_20011_",
"Lang_Contribution_20012_",
"Not_Lang_Contribution_20012_",
"Lang_Contribution_20012_",
"Not_Lang_Contribution_20012_",
"IRI_Contribution_20012_",
"Lang_Contribution_20013_",
"Not_Lang_Contribution_20013_",
"Lang_Contribution_20013_",
"Not_Lang_Contribution_20013_",
"IRI_Contribution_20013_",
"Lang_Contribution_20014_",
"Not_Lang_Contribution_20014_",
"Lang_Contribution_20014_",
"Not_Lang_Contribution_20014_",
"IRI_Contribution_20014_",
"Lang_Contribution_20015_",
"Not_Lang_Contribution_20015_",
"Lang_Contribution_20015_",
"Not_Lang_Contribution_20015_",
"IRI_Contribution_20015_",
"Lang_Contribution_20016_",
"Not_Lang_Contribution_20016_",
"Lang_Contribution_20016_",
"Not_Lang_Contribution_20016_",
"IRI_Contribution_20016_",
"Lang_Contribution_20017_",
"Not_Lang_Contribution_20017_",
"Lang_Contribution_20017_",
"Not_Lang_Contribution_20017_",
"IRI_Contribution_20017_",
"Lang_Contribution_20018_",
"Not_Lang_Contribution_20018_",
"Lang_Contribution_20018_",
"Not_Lang_Contribution_20018_",
"IRI_Contribution_20018_",
"Lang_Contribution_20019_",
"Not_Lang_Contribution_20019_",
"Lang_Contribution_20019_",
"Not_Lang_Contribution_20019_",
"IRI_Contribution_20019_",
"Lang_Contribution_20020_",
"Not_Lang_Contribution_20020_",
"Lang_Contribution_20020_",
"Not_Lang_Contribution_20020_",
"IRI_Contribution_20020_",
"Lang_Contribution_20021_",
"Not_Lang_Contribution_20021_",
"Lang_Contribution_20021_",
"Not_Lang_Contribution_20021_",
"IRI_Contribution_20021_",
"Lang_Contribution_20022_",
"Not_Lang_Contribution_20022_",
"Lang_Contribution_20022_",
"Not_Lang_Contribution_20022_",
"IRI_Contribution_20022_",
"Lang_Contribution_20023_",
"Not_Lang_Contribution_20023_",
"Lang_Contribution_20023_",
"Not_Lang_Contribution_20023_",
"IRI_Contribution_20023_",
"Lang_Contribution_20024_",
"Not_Lang_Contribution_20024_",
"Lang_Contribution_20024_",
"Not_Lang_Contribution_20024_",
"IRI_Contribution_20024_",
"Lang_Contribution_20025_",
"Not_Lang_Contribution_20025_",
"Lang_Contribution_20025_",
"Not_Lang_Contribution_20025_",
"IRI_Contribution_20025_",
"Lang_Contribution_20026_",
"Not_Lang_Contribution_20026_",
"Lang_Contribution_20026_",
"Not_Lang_Contribution_20026_",
"IRI_Contribution_20026_",
"Lang_Contribution_20028_",
"Not_Lang_Contribution_20028_",
"Lang_Contribution_20028_",
"Not_Lang_Contribution_20028_",
"IRI_Contribution_20028_",
"Lang_Contribution_20029_",
"Not_Lang_Contribution_20029_",
"Lang_Contribution_20029_",
"Not_Lang_Contribution_20029_",
"IRI_Contribution_20029_",
"Lang_Contribution_20030_",
"Not_Lang_Contribution_20030_",
"Lang_Contribution_20030_",
"Not_Lang_Contribution_20030_",
"IRI_Contribution_20030_",
"Lang_Contribution_20031_",
"Not_Lang_Contribution_20031_",
"Lang_Contribution_20031_",
"Not_Lang_Contribution_20031_",
"IRI_Contribution_20031_",
"Lang_Contribution_20032_",
"Not_Lang_Contribution_20032_",
"Lang_Contribution_20032_",
"Not_Lang_Contribution_20032_",
"IRI_Contribution_20032_",
"Lang_Contribution_20033_",
"Not_Lang_Contribution_20033_",
"Lang_Contribution_20033_",
"Not_Lang_Contribution_20033_",
"IRI_Contribution_20033_",
"Lang_Contribution_20034_",
"Not_Lang_Contribution_20034_",
"Lang_Contribution_20034_",
"Not_Lang_Contribution_20034_",
"IRI_Contribution_20034_",
"Lang_Contribution_20035_",
"Not_Lang_Contribution_20035_",
"Lang_Contribution_20035_",
"Not_Lang_Contribution_20035_",
"IRI_Contribution_20035_",
"Lang_Contribution_20036_",
"Not_Lang_Contribution_20036_",
"Lang_Contribution_20036_",
"Not_Lang_Contribution_20036_",
"IRI_Contribution_20036_",
"Lang_Contribution_20037_",
"Not_Lang_Contribution_20037_",
"Lang_Contribution_20037_",
"Not_Lang_Contribution_20037_",
"IRI_Contribution_20037_",
"Lang_Contribution_20038_",
"Not_Lang_Contribution_20038_",
"Lang_Contribution_20038_",
"Not_Lang_Contribution_20038_",
"IRI_Contribution_20038_",
"Lang_Contribution_20039_",
"Not_Lang_Contribution_20039_",
"Lang_Contribution_20039_",
"Not_Lang_Contribution_20039_",
"IRI_Contribution_20039_",
"Lang_Contribution_20040_",
"Not_Lang_Contribution_20040_",
"Lang_Contribution_20040_",
"Not_Lang_Contribution_20040_",
"IRI_Contribution_20040_",
"Lang_Contribution_20041_",
"Not_Lang_Contribution_20041_",
"Lang_Contribution_20041_",
"Not_Lang_Contribution_20041_",
"IRI_Contribution_20041_",
"Lang_Contribution_20044_",
"Not_Lang_Contribution_20044_",
"Lang_Contribution_20044_",
"Not_Lang_Contribution_20044_",
"IRI_Contribution_20044_",
"Lang_Contribution_20045_",
"Not_Lang_Contribution_20045_",
"Lang_Contribution_20045_",
"Not_Lang_Contribution_20045_",
"IRI_Contribution_20045_",
"Lang_Contribution_20046_",
"Not_Lang_Contribution_20046_",
"Lang_Contribution_20046_",
"Not_Lang_Contribution_20046_",
"IRI_Contribution_20046_",
"Lang_Contribution_20047_",
"Not_Lang_Contribution_20047_",
"Lang_Contribution_20047_",
"Not_Lang_Contribution_20047_",
"IRI_Contribution_20047_",
"Lang_Contribution_20049_",
"Not_Lang_Contribution_20049_",
"Lang_Contribution_20049_",
"Not_Lang_Contribution_20049_",
"IRI_Contribution_20049_",
"Lang_Contribution_20050_",
"Not_Lang_Contribution_20050_",
"Lang_Contribution_20050_",
"Not_Lang_Contribution_20050_",
"IRI_Contribution_20050_",
"Lang_Contribution_20051_",
"Not_Lang_Contribution_20051_",
"Lang_Contribution_20051_",
"Not_Lang_Contribution_20051_",
"IRI_Contribution_20051_",
"Lang_Contribution_20052_",
"Not_Lang_Contribution_20052_",
"Lang_Contribution_20052_",
"Not_Lang_Contribution_20052_",
"IRI_Contribution_20052_",
"Lang_Contribution_20053_",
"Not_Lang_Contribution_20053_",
"Lang_Contribution_20053_",
"Not_Lang_Contribution_20053_",
"IRI_Contribution_20053_",
"Lang_Contribution_20054_",
"Not_Lang_Contribution_20054_",
"Lang_Contribution_20054_",
"Not_Lang_Contribution_20054_",
"IRI_Contribution_20054_",
"Lang_Contribution_20055_",
"Not_Lang_Contribution_20055_",
"Lang_Contribution_20055_",
"Not_Lang_Contribution_20055_",
"IRI_Contribution_20055_",
"Lang_Contribution_20056_",
"Not_Lang_Contribution_20056_",
"Lang_Contribution_20056_",
"Not_Lang_Contribution_20056_",
"IRI_Contribution_20056_",
"Lang_Contribution_20058_",
"Not_Lang_Contribution_20058_",
"Lang_Contribution_20058_",
"Not_Lang_Contribution_20058_",
"IRI_Contribution_20058_",
"Lang_Contribution_20068_",
"Not_Lang_Contribution_20068_",
"Lang_Contribution_20068_",
"Not_Lang_Contribution_20068_",
"IRI_Contribution_20068_",
"Lang_Contribution_20070_",
"Not_Lang_Contribution_20070_",
"Lang_Contribution_20070_",
"Not_Lang_Contribution_20070_",
"IRI_Contribution_20070_",
"Lang_Contribution_20237_",
"Not_Lang_Contribution_20237_",
"Lang_Contribution_20237_",
"Not_Lang_Contribution_20237_",
"IRI_Contribution_20237_",
"Lang_Contribution_20238_",
"Not_Lang_Contribution_20238_",
"Lang_Contribution_20238_",
"Not_Lang_Contribution_20238_",
"IRI_Contribution_20238_",
"Lang_Contribution_20257_",
"Not_Lang_Contribution_20257_",
"Lang_Contribution_20257_",
"Not_Lang_Contribution_20257_",
"IRI_Contribution_20257_",
"Lang_Contribution_20258_",
"Not_Lang_Contribution_20258_",
"Lang_Contribution_20258_",
"Not_Lang_Contribution_20258_",
"IRI_Contribution_20258_",
"Lang_Contribution_20259_",
"Not_Lang_Contribution_20259_",
"Lang_Contribution_20259_",
"Not_Lang_Contribution_20259_",
"IRI_Contribution_20259_",
"Lang_Contribution_20275_",
"Not_Lang_Contribution_20275_",
"Lang_Contribution_20275_",
"Not_Lang_Contribution_20275_",
"IRI_Contribution_20275_",
"Lang_Contribution_20276_",
"Not_Lang_Contribution_20276_",
"Lang_Contribution_20276_",
"Not_Lang_Contribution_20276_",
"IRI_Contribution_20276_",
"Lang_Contribution_20277_",
"Not_Lang_Contribution_20277_",
"Lang_Contribution_20277_",
"Not_Lang_Contribution_20277_",
"IRI_Contribution_20277_",
"Lang_Contribution_20279_",
"Not_Lang_Contribution_20279_",
"Lang_Contribution_20279_",
"Not_Lang_Contribution_20279_",
"IRI_Contribution_20279_",
"Lang_Contribution_20280_",
"Not_Lang_Contribution_20280_",
"Lang_Contribution_20280_",
"Not_Lang_Contribution_20280_",
"IRI_Contribution_20280_",
"Lang_Contribution_20283_",
"Not_Lang_Contribution_20283_",
"Lang_Contribution_20283_",
"Not_Lang_Contribution_20283_",
"IRI_Contribution_20283_",
"Lang_Contribution_20284_",
"Not_Lang_Contribution_20284_",
"Lang_Contribution_20284_",
"Not_Lang_Contribution_20284_",
"IRI_Contribution_20284_",
"Lang_Contribution_20285_",
"Not_Lang_Contribution_20285_",
"Lang_Contribution_20285_",
"Not_Lang_Contribution_20285_",
"IRI_Contribution_20285_",
"Lang_Contribution_20286_",
"Not_Lang_Contribution_20286_",
"Lang_Contribution_20286_",
"Not_Lang_Contribution_20286_",
"IRI_Contribution_20286_",
"Lang_Contribution_20287_",
"Not_Lang_Contribution_20287_",
"Lang_Contribution_20287_",
"Not_Lang_Contribution_20287_",
"IRI_Contribution_20287_",
"Lang_Contribution_20289_",
"Not_Lang_Contribution_20289_",
"Lang_Contribution_20289_",
"Not_Lang_Contribution_20289_",
"IRI_Contribution_20289_",
"Lang_Contribution_20292_",
"Not_Lang_Contribution_20292_",
"Lang_Contribution_20292_",
"Not_Lang_Contribution_20292_",
"IRI_Contribution_20292_",
"Lang_Contribution_20293_",
"Not_Lang_Contribution_20293_",
"Lang_Contribution_20293_",
"Not_Lang_Contribution_20293_",
"IRI_Contribution_20293_",
"Lang_Contribution_20294_",
"Not_Lang_Contribution_20294_",
"Lang_Contribution_20294_",
"Not_Lang_Contribution_20294_",
"IRI_Contribution_20294_",
"Lang_Contribution_20295_",
"Not_Lang_Contribution_20295_",
"Lang_Contribution_20295_",
"Not_Lang_Contribution_20295_",
"IRI_Contribution_20295_",
"Lang_Contribution_20296_",
"Not_Lang_Contribution_20296_",
"Lang_Contribution_20296_",
"Not_Lang_Contribution_20296_",
"IRI_Contribution_20296_",
"Lang_Contribution_20301_",
"Not_Lang_Contribution_20301_",
"IRI_Contribution_20301_",
"Lang_Contribution_20302_",
"Not_Lang_Contribution_20302_",
"IRI_Contribution_20302_",
"Lang_Contribution_20303_",
"Not_Lang_Contribution_20303_",
"IRI_Contribution_20303_",
"Lang_Contribution_20304_",
"Not_Lang_Contribution_20304_",
"IRI_Contribution_20304_",
"Lang_Contribution_20305_",
"Not_Lang_Contribution_20305_",
"IRI_Contribution_20305_",
"Lang_Contribution_20327_",
"Not_Lang_Contribution_20327_",
"Lang_Contribution_20327_",
"Not_Lang_Contribution_20327_",
"IRI_Contribution_20327_",
"Lang_Contribution_20328_",
"Not_Lang_Contribution_20328_",
"Lang_Contribution_20328_",
"Not_Lang_Contribution_20328_",
"IRI_Contribution_20328_",
"Lang_Contribution_20329_",
"Not_Lang_Contribution_20329_",
"Lang_Contribution_20329_",
"Not_Lang_Contribution_20329_",
"IRI_Contribution_20329_",
"Lang_Contribution_20330_",
"Not_Lang_Contribution_20330_",
"Lang_Contribution_20330_",
"Not_Lang_Contribution_20330_",
"IRI_Contribution_20330_",
"Lang_Contribution_20336_",
"Not_Lang_Contribution_20336_",
"IRI_Contribution_20336_",
"Lang_Contribution_20337_",
"Not_Lang_Contribution_20337_",
"Lang_Contribution_20337_",
"Not_Lang_Contribution_20337_",
"IRI_Contribution_20337_",
"Lang_Contribution_20338_",
"Not_Lang_Contribution_20338_",
"Lang_Contribution_20338_",
"Not_Lang_Contribution_20338_",
"IRI_Contribution_20338_",
"Lang_Contribution_20339_",
"Not_Lang_Contribution_20339_",
"Lang_Contribution_20339_",
"Not_Lang_Contribution_20339_",
"IRI_Contribution_20339_",
"Lang_Contribution_20340_",
"Not_Lang_Contribution_20340_",
"Lang_Contribution_20340_",
"Not_Lang_Contribution_20340_",
"IRI_Contribution_20340_",
"Lang_Contribution_20341_",
"Not_Lang_Contribution_20341_",
"Lang_Contribution_20341_",
"Not_Lang_Contribution_20341_",
"IRI_Contribution_20341_",
"Lang_Contribution_20342_",
"Not_Lang_Contribution_20342_",
"Lang_Contribution_20342_",
"Not_Lang_Contribution_20342_",
"IRI_Contribution_20342_",
"Lang_Contribution_20343_",
"Not_Lang_Contribution_20343_",
"Lang_Contribution_20343_",
"Not_Lang_Contribution_20343_",
"IRI_Contribution_20343_",
"Lang_Contribution_20344_",
"Not_Lang_Contribution_20344_",
"Lang_Contribution_20344_",
"Not_Lang_Contribution_20344_",
"IRI_Contribution_20344_",
"Lang_Contribution_20345_",
"Not_Lang_Contribution_20345_",
"Lang_Contribution_20345_",
"Not_Lang_Contribution_20345_",
"IRI_Contribution_20345_",
"Lang_Contribution_20346_",
"Not_Lang_Contribution_20346_",
"Lang_Contribution_20346_",
"Not_Lang_Contribution_20346_",
"IRI_Contribution_20346_",
"Lang_Contribution_20347_",
"Not_Lang_Contribution_20347_",
"Lang_Contribution_20347_",
"Not_Lang_Contribution_20347_",
"IRI_Contribution_20347_",
"Lang_Contribution_20348_",
"Not_Lang_Contribution_20348_",
"Lang_Contribution_20348_",
"Not_Lang_Contribution_20348_",
"IRI_Contribution_20348_",
"Lang_Contribution_20349_",
"Not_Lang_Contribution_20349_",
"Lang_Contribution_20349_",
"Not_Lang_Contribution_20349_",
"IRI_Contribution_20349_",
"Lang_Contribution_20350_",
"Not_Lang_Contribution_20350_",
"Lang_Contribution_20350_",
"Not_Lang_Contribution_20350_",
"IRI_Contribution_20350_",
"Lang_Contribution_20351_",
"Not_Lang_Contribution_20351_",
"Lang_Contribution_20351_",
"Not_Lang_Contribution_20351_",
"IRI_Contribution_20351_",
"Lang_Contribution_20352_",
"Not_Lang_Contribution_20352_",
"Lang_Contribution_20352_",
"Not_Lang_Contribution_20352_",
"IRI_Contribution_20352_",
"Lang_Contribution_20353_",
"Not_Lang_Contribution_20353_",
"Lang_Contribution_20353_",
"Not_Lang_Contribution_20353_",
"IRI_Contribution_20353_",
"Lang_Contribution_20354_",
"Not_Lang_Contribution_20354_",
"Lang_Contribution_20354_",
"Not_Lang_Contribution_20354_",
"IRI_Contribution_20354_",
"Lang_Contribution_20355_",
"Not_Lang_Contribution_20355_",
"Lang_Contribution_20355_",
"Not_Lang_Contribution_20355_",
"IRI_Contribution_20355_",
"Lang_Contribution_20356_",
"Not_Lang_Contribution_20356_",
"Lang_Contribution_20356_",
"Not_Lang_Contribution_20356_",
"IRI_Contribution_20356_",
"Lang_Contribution_20357_",
"Not_Lang_Contribution_20357_",
"Lang_Contribution_20357_",
"Not_Lang_Contribution_20357_",
"IRI_Contribution_20357_",
"Lang_Contribution_20358_",
"Not_Lang_Contribution_20358_",
"Lang_Contribution_20358_",
"Not_Lang_Contribution_20358_",
"IRI_Contribution_20358_",
"Lang_Contribution_20359_",
"Not_Lang_Contribution_20359_",
"Lang_Contribution_20359_",
"Not_Lang_Contribution_20359_",
"IRI_Contribution_20359_",
"Lang_Contribution_20360_",
"Not_Lang_Contribution_20360_",
"Lang_Contribution_20360_",
"Not_Lang_Contribution_20360_",
"IRI_Contribution_20360_",
"Lang_Contribution_20361_",
"Not_Lang_Contribution_20361_",
"Lang_Contribution_20361_",
"Not_Lang_Contribution_20361_",
"IRI_Contribution_20361_",
"Lang_Contribution_20362_",
"Not_Lang_Contribution_20362_",
"Lang_Contribution_20362_",
"Not_Lang_Contribution_20362_",
"IRI_Contribution_20362_",
"Lang_Contribution_20363_",
"Not_Lang_Contribution_20363_",
"Lang_Contribution_20363_",
"Not_Lang_Contribution_20363_",
"IRI_Contribution_20363_",
"Lang_Contribution_20364_",
"Not_Lang_Contribution_20364_",
"Lang_Contribution_20364_",
"Not_Lang_Contribution_20364_",
"IRI_Contribution_20364_",
"Lang_Contribution_20365_",
"Not_Lang_Contribution_20365_",
"Lang_Contribution_20365_",
"Not_Lang_Contribution_20365_",
"IRI_Contribution_20365_",
"Lang_Contribution_20366_",
"Not_Lang_Contribution_20366_",
"Lang_Contribution_20366_",
"Not_Lang_Contribution_20366_",
"IRI_Contribution_20366_",
"Lang_Contribution_20367_",
"Not_Lang_Contribution_20367_",
"Lang_Contribution_20367_",
"Not_Lang_Contribution_20367_",
"IRI_Contribution_20367_",
"Lang_Contribution_20368_",
"Not_Lang_Contribution_20368_",
"Lang_Contribution_20368_",
"Not_Lang_Contribution_20368_",
"IRI_Contribution_20368_",
"Lang_Contribution_20369_",
"Not_Lang_Contribution_20369_",
"Lang_Contribution_20369_",
"Not_Lang_Contribution_20369_",
"IRI_Contribution_20369_",
"Lang_Contribution_20370_",
"Not_Lang_Contribution_20370_",
"Lang_Contribution_20370_",
"Not_Lang_Contribution_20370_",
"IRI_Contribution_20370_",
"Lang_Contribution_20371_",
"Not_Lang_Contribution_20371_",
"Lang_Contribution_20371_",
"Not_Lang_Contribution_20371_",
"IRI_Contribution_20371_",
"Lang_Contribution_20372_",
"Not_Lang_Contribution_20372_",
"Lang_Contribution_20372_",
"Not_Lang_Contribution_20372_",
"IRI_Contribution_20372_",
"Lang_Contribution_20373_",
"Not_Lang_Contribution_20373_",
"Lang_Contribution_20373_",
"Not_Lang_Contribution_20373_",
"IRI_Contribution_20373_",
"Lang_Contribution_20374_",
"Not_Lang_Contribution_20374_",
"Lang_Contribution_20374_",
"Not_Lang_Contribution_20374_",
"IRI_Contribution_20374_",
"Lang_Contribution_20375_",
"Not_Lang_Contribution_20375_",
"Lang_Contribution_20375_",
"Not_Lang_Contribution_20375_",
"IRI_Contribution_20375_",
"Lang_Contribution_20376_",
"Not_Lang_Contribution_20376_",
"Lang_Contribution_20376_",
"Not_Lang_Contribution_20376_",
"IRI_Contribution_20376_",
"Lang_Contribution_20377_",
"Not_Lang_Contribution_20377_",
"Lang_Contribution_20377_",
"Not_Lang_Contribution_20377_",
"IRI_Contribution_20377_",
"Lang_Contribution_20378_",
"Not_Lang_Contribution_20378_",
"Lang_Contribution_20378_",
"Not_Lang_Contribution_20378_",
"IRI_Contribution_20378_",
"Lang_Contribution_20379_",
"Not_Lang_Contribution_20379_",
"Lang_Contribution_20379_",
"Not_Lang_Contribution_20379_",
"IRI_Contribution_20379_",
"Lang_Contribution_20380_",
"Not_Lang_Contribution_20380_",
"Lang_Contribution_20380_",
"Not_Lang_Contribution_20380_",
"IRI_Contribution_20380_",
"Lang_Contribution_20381_",
"Not_Lang_Contribution_20381_",
"Lang_Contribution_20381_",
"Not_Lang_Contribution_20381_",
"IRI_Contribution_20381_",
"Lang_Contribution_20382_",
"Not_Lang_Contribution_20382_",
"Lang_Contribution_20382_",
"Not_Lang_Contribution_20382_",
"IRI_Contribution_20382_",
"Lang_Contribution_20383_",
"Not_Lang_Contribution_20383_",
"Lang_Contribution_20383_",
"Not_Lang_Contribution_20383_",
"IRI_Contribution_20383_",
"Lang_Contribution_20384_",
"Not_Lang_Contribution_20384_",
"Lang_Contribution_20384_",
"Not_Lang_Contribution_20384_",
"IRI_Contribution_20384_",
"Lang_Contribution_20385_",
"Not_Lang_Contribution_20385_",
"Lang_Contribution_20385_",
"Not_Lang_Contribution_20385_",
"IRI_Contribution_20385_",
"Lang_Contribution_20386_",
"Not_Lang_Contribution_20386_",
"Lang_Contribution_20386_",
"Not_Lang_Contribution_20386_",
"IRI_Contribution_20386_",
"Lang_Contribution_20387_",
"Not_Lang_Contribution_20387_",
"Lang_Contribution_20387_",
"Not_Lang_Contribution_20387_",
"IRI_Contribution_20387_",
"Lang_Contribution_20388_",
"Not_Lang_Contribution_20388_",
"Lang_Contribution_20388_",
"Not_Lang_Contribution_20388_",
"IRI_Contribution_20388_",
"Lang_Contribution_20389_",
"Not_Lang_Contribution_20389_",
"Lang_Contribution_20389_",
"Not_Lang_Contribution_20389_",
"IRI_Contribution_20389_",
"Lang_Contribution_20390_",
"Not_Lang_Contribution_20390_",
"Lang_Contribution_20390_",
"Not_Lang_Contribution_20390_",
"IRI_Contribution_20390_",
"Lang_Contribution_20391_",
"Not_Lang_Contribution_20391_",
"Lang_Contribution_20391_",
"Not_Lang_Contribution_20391_",
"IRI_Contribution_20391_",
"Lang_Contribution_20392_",
"Not_Lang_Contribution_20392_",
"Lang_Contribution_20392_",
"Not_Lang_Contribution_20392_",
"IRI_Contribution_20392_",
"Lang_Contribution_20393_",
"Not_Lang_Contribution_20393_",
"Lang_Contribution_20393_",
"Not_Lang_Contribution_20393_",
"IRI_Contribution_20393_",
"Lang_Contribution_20394_",
"Not_Lang_Contribution_20394_",
"Lang_Contribution_20394_",
"Not_Lang_Contribution_20394_",
"IRI_Contribution_20394_",
"Lang_Contribution_20395_",
"Not_Lang_Contribution_20395_",
"Lang_Contribution_20395_",
"Not_Lang_Contribution_20395_",
"IRI_Contribution_20395_",
"Lang_Contribution_20396_",
"Not_Lang_Contribution_20396_",
"Lang_Contribution_20396_",
"Not_Lang_Contribution_20396_",
"IRI_Contribution_20396_",
"Lang_Contribution_20397_",
"Not_Lang_Contribution_20397_",
"Lang_Contribution_20397_",
"Not_Lang_Contribution_20397_",
"IRI_Contribution_20397_",
"Lang_Contribution_20398_",
"Not_Lang_Contribution_20398_",
"Lang_Contribution_20398_",
"Not_Lang_Contribution_20398_",
"IRI_Contribution_20398_",
"Lang_Contribution_20399_",
"Not_Lang_Contribution_20399_",
"Lang_Contribution_20399_",
"Not_Lang_Contribution_20399_",
"IRI_Contribution_20399_",
"Lang_Contribution_20400_",
"Not_Lang_Contribution_20400_",
"Lang_Contribution_20400_",
"Not_Lang_Contribution_20400_",
"IRI_Contribution_20400_",
"Lang_Contribution_20401_",
"Not_Lang_Contribution_20401_",
"Lang_Contribution_20401_",
"Not_Lang_Contribution_20401_",
"IRI_Contribution_20401_",
"Lang_Contribution_20402_",
"Not_Lang_Contribution_20402_",
"Lang_Contribution_20402_",
"Not_Lang_Contribution_20402_",
"IRI_Contribution_20402_",
"Lang_Contribution_20403_",
"Not_Lang_Contribution_20403_",
"Lang_Contribution_20403_",
"Not_Lang_Contribution_20403_",
"IRI_Contribution_20403_",
"Lang_Contribution_20404_",
"Not_Lang_Contribution_20404_",
"Lang_Contribution_20404_",
"Not_Lang_Contribution_20404_",
"IRI_Contribution_20404_",
"Lang_Contribution_20405_",
"Not_Lang_Contribution_20405_",
"Lang_Contribution_20405_",
"Not_Lang_Contribution_20405_",
"IRI_Contribution_20405_",
"Lang_Contribution_20406_",
"Not_Lang_Contribution_20406_",
"Lang_Contribution_20406_",
"Not_Lang_Contribution_20406_",
"IRI_Contribution_20406_",
"Lang_Contribution_20407_",
"Not_Lang_Contribution_20407_",
"Lang_Contribution_20407_",
"Not_Lang_Contribution_20407_",
"IRI_Contribution_20407_",
"Lang_Contribution_20408_",
"Not_Lang_Contribution_20408_",
"Lang_Contribution_20408_",
"Not_Lang_Contribution_20408_",
"IRI_Contribution_20408_",
"Lang_Contribution_20409_",
"Not_Lang_Contribution_20409_",
"Lang_Contribution_20409_",
"Not_Lang_Contribution_20409_",
"IRI_Contribution_20409_",
"Lang_Contribution_20410_",
"Not_Lang_Contribution_20410_",
"Lang_Contribution_20410_",
"Not_Lang_Contribution_20410_",
"IRI_Contribution_20410_",
"Lang_Contribution_20411_",
"Not_Lang_Contribution_20411_",
"Lang_Contribution_20411_",
"Not_Lang_Contribution_20411_",
"IRI_Contribution_20411_",
"Lang_Contribution_20412_",
"Not_Lang_Contribution_20412_",
"Lang_Contribution_20412_",
"Not_Lang_Contribution_20412_",
"IRI_Contribution_20412_",
"Lang_Contribution_20413_",
"Not_Lang_Contribution_20413_",
"Lang_Contribution_20413_",
"Not_Lang_Contribution_20413_",
"IRI_Contribution_20413_",
"Lang_Contribution_20414_",
"Not_Lang_Contribution_20414_",
"Lang_Contribution_20414_",
"Not_Lang_Contribution_20414_",
"IRI_Contribution_20414_",
"Lang_Contribution_20415_",
"Not_Lang_Contribution_20415_",
"Lang_Contribution_20415_",
"Not_Lang_Contribution_20415_",
"IRI_Contribution_20415_",
"Lang_Contribution_20416_",
"Not_Lang_Contribution_20416_",
"Lang_Contribution_20416_",
"Not_Lang_Contribution_20416_",
"IRI_Contribution_20416_",
"Lang_Contribution_20417_",
"Not_Lang_Contribution_20417_",
"Lang_Contribution_20417_",
"Not_Lang_Contribution_20417_",
"IRI_Contribution_20417_",
"Lang_Contribution_20418_",
"Not_Lang_Contribution_20418_",
"Lang_Contribution_20418_",
"Not_Lang_Contribution_20418_",
"IRI_Contribution_20418_",
"Lang_Contribution_20419_",
"Not_Lang_Contribution_20419_",
"Lang_Contribution_20419_",
"Not_Lang_Contribution_20419_",
"IRI_Contribution_20419_",
"Lang_Contribution_20420_",
"Not_Lang_Contribution_20420_",
"Lang_Contribution_20420_",
"Not_Lang_Contribution_20420_",
"IRI_Contribution_20420_",
"Lang_Contribution_20421_",
"Not_Lang_Contribution_20421_",
"Lang_Contribution_20421_",
"Not_Lang_Contribution_20421_",
"IRI_Contribution_20421_",
"Lang_Contribution_20422_",
"Not_Lang_Contribution_20422_",
"Lang_Contribution_20422_",
"Not_Lang_Contribution_20422_",
"IRI_Contribution_20422_",
"Lang_Contribution_20423_",
"Not_Lang_Contribution_20423_",
"Lang_Contribution_20423_",
"Not_Lang_Contribution_20423_",
"IRI_Contribution_20423_",
"Lang_Contribution_20424_",
"Not_Lang_Contribution_20424_",
"Lang_Contribution_20424_",
"Not_Lang_Contribution_20424_",
"IRI_Contribution_20424_",
"Lang_Contribution_20425_",
"Not_Lang_Contribution_20425_",
"Lang_Contribution_20425_",
"Not_Lang_Contribution_20425_",
"IRI_Contribution_20425_",
"Lang_Contribution_20426_",
"Not_Lang_Contribution_20426_",
"Lang_Contribution_20426_",
"Not_Lang_Contribution_20426_",
"IRI_Contribution_20426_",
"Lang_Contribution_20427_",
"Not_Lang_Contribution_20427_",
"Lang_Contribution_20427_",
"Not_Lang_Contribution_20427_",
"IRI_Contribution_20427_",
"Lang_Contribution_20428_",
"Not_Lang_Contribution_20428_",
"Lang_Contribution_20428_",
"Not_Lang_Contribution_20428_",
"IRI_Contribution_20428_",
"Lang_Contribution_20429_",
"Not_Lang_Contribution_20429_",
"Lang_Contribution_20429_",
"Not_Lang_Contribution_20429_",
"IRI_Contribution_20429_",
"Lang_Contribution_20430_",
"Not_Lang_Contribution_20430_",
"Lang_Contribution_20430_",
"Not_Lang_Contribution_20430_",
"IRI_Contribution_20430_",
"Lang_Contribution_20431_",
"Not_Lang_Contribution_20431_",
"Lang_Contribution_20431_",
"Not_Lang_Contribution_20431_",
"IRI_Contribution_20431_",
"Lang_Contribution_20432_",
"Not_Lang_Contribution_20432_",
"Lang_Contribution_20432_",
"Not_Lang_Contribution_20432_",
"IRI_Contribution_20432_",
"Lang_Contribution_20433_",
"Not_Lang_Contribution_20433_",
"Lang_Contribution_20433_",
"Not_Lang_Contribution_20433_",
"IRI_Contribution_20433_",
"Lang_Contribution_20434_",
"Not_Lang_Contribution_20434_",
"Lang_Contribution_20434_",
"Not_Lang_Contribution_20434_",
"IRI_Contribution_20434_",
"Lang_Contribution_20435_",
"Not_Lang_Contribution_20435_",
"Lang_Contribution_20435_",
"Not_Lang_Contribution_20435_",
"IRI_Contribution_20435_",
"Lang_Contribution_20436_",
"Not_Lang_Contribution_20436_",
"Lang_Contribution_20436_",
"Not_Lang_Contribution_20436_",
"IRI_Contribution_20436_",
"Lang_Contribution_20437_",
"Not_Lang_Contribution_20437_",
"Lang_Contribution_20437_",
"Not_Lang_Contribution_20437_",
"IRI_Contribution_20437_",
"Lang_Contribution_20438_",
"Not_Lang_Contribution_20438_",
"Lang_Contribution_20438_",
"Not_Lang_Contribution_20438_",
"IRI_Contribution_20438_",
"Lang_Contribution_20439_",
"Not_Lang_Contribution_20439_",
"Lang_Contribution_20439_",
"Not_Lang_Contribution_20439_",
"IRI_Contribution_20439_",
"Lang_Contribution_20440_",
"Not_Lang_Contribution_20440_",
"Lang_Contribution_20440_",
"Not_Lang_Contribution_20440_",
"IRI_Contribution_20440_",
"Lang_Contribution_20441_",
"Not_Lang_Contribution_20441_",
"Lang_Contribution_20441_",
"Not_Lang_Contribution_20441_",
"IRI_Contribution_20441_",
"Lang_Contribution_20442_",
"Not_Lang_Contribution_20442_",
"Lang_Contribution_20442_",
"Not_Lang_Contribution_20442_",
"IRI_Contribution_20442_",
"Lang_Contribution_20443_",
"Not_Lang_Contribution_20443_",
"Lang_Contribution_20443_",
"Not_Lang_Contribution_20443_",
"IRI_Contribution_20443_",
"Lang_Contribution_20444_",
"Not_Lang_Contribution_20444_",
"Lang_Contribution_20444_",
"Not_Lang_Contribution_20444_",
"IRI_Contribution_20444_",
"Lang_Contribution_20445_",
"Not_Lang_Contribution_20445_",
"Lang_Contribution_20445_",
"Not_Lang_Contribution_20445_",
"IRI_Contribution_20445_",
"Lang_Contribution_20446_",
"Not_Lang_Contribution_20446_",
"Lang_Contribution_20446_",
"Not_Lang_Contribution_20446_",
"IRI_Contribution_20446_",
"Lang_Contribution_20447_",
"Not_Lang_Contribution_20447_",
"Lang_Contribution_20447_",
"Not_Lang_Contribution_20447_",
"IRI_Contribution_20447_",
"Lang_Contribution_20448_",
"Not_Lang_Contribution_20448_",
"Lang_Contribution_20448_",
"Not_Lang_Contribution_20448_",
"IRI_Contribution_20448_",
"Lang_Contribution_20449_",
"Not_Lang_Contribution_20449_",
"IRI_Contribution_20449_",
"Lang_Contribution_20450_",
"Not_Lang_Contribution_20450_",
"Lang_Contribution_20450_",
"Not_Lang_Contribution_20450_",
"IRI_Contribution_20450_",
"Lang_Contribution_20451_",
"Not_Lang_Contribution_20451_",
"Lang_Contribution_20451_",
"Not_Lang_Contribution_20451_",
"IRI_Contribution_20451_",
"Lang_Contribution_20452_",
"Not_Lang_Contribution_20452_",
"Lang_Contribution_20452_",
"Not_Lang_Contribution_20452_",
"IRI_Contribution_20452_",
"Lang_Contribution_20453_",
"Not_Lang_Contribution_20453_",
"Lang_Contribution_20453_",
"Not_Lang_Contribution_20453_",
"IRI_Contribution_20453_",
"Lang_Contribution_20454_",
"Not_Lang_Contribution_20454_",
"Lang_Contribution_20454_",
"Not_Lang_Contribution_20454_",
"IRI_Contribution_20454_",
"Lang_Contribution_20455_",
"Not_Lang_Contribution_20455_",
"Lang_Contribution_20455_",
"Not_Lang_Contribution_20455_",
"IRI_Contribution_20455_",
"Lang_Contribution_20456_",
"Not_Lang_Contribution_20456_",
"Lang_Contribution_20456_",
"Not_Lang_Contribution_20456_",
"IRI_Contribution_20456_",
"Lang_Contribution_20457_",
"Not_Lang_Contribution_20457_",
"Lang_Contribution_20457_",
"Not_Lang_Contribution_20457_",
"IRI_Contribution_20457_",
"Lang_Contribution_20458_",
"Not_Lang_Contribution_20458_",
"Lang_Contribution_20458_",
"Not_Lang_Contribution_20458_",
"IRI_Contribution_20458_",
"Lang_Contribution_20459_",
"Not_Lang_Contribution_20459_",
"Lang_Contribution_20459_",
"Not_Lang_Contribution_20459_",
"IRI_Contribution_20459_",
"Lang_Contribution_20460_",
"Not_Lang_Contribution_20460_",
"Lang_Contribution_20460_",
"Not_Lang_Contribution_20460_",
"IRI_Contribution_20460_",
"Lang_Contribution_20461_",
"Not_Lang_Contribution_20461_",
"Lang_Contribution_20461_",
"Not_Lang_Contribution_20461_",
"IRI_Contribution_20461_",
"Lang_Contribution_20462_",
"Not_Lang_Contribution_20462_",
"Lang_Contribution_20462_",
"Not_Lang_Contribution_20462_",
"IRI_Contribution_20462_",
"Lang_Contribution_20463_",
"Not_Lang_Contribution_20463_",
"Lang_Contribution_20463_",
"Not_Lang_Contribution_20463_",
"IRI_Contribution_20463_",
"Lang_Contribution_20464_",
"Not_Lang_Contribution_20464_",
"Lang_Contribution_20464_",
"Not_Lang_Contribution_20464_",
"IRI_Contribution_20464_",
"Lang_Contribution_20465_",
"Not_Lang_Contribution_20465_",
"Lang_Contribution_20465_",
"Not_Lang_Contribution_20465_",
"IRI_Contribution_20465_",
"Lang_Contribution_20466_",
"Not_Lang_Contribution_20466_",
"Lang_Contribution_20466_",
"Not_Lang_Contribution_20466_",
"IRI_Contribution_20466_",
"Lang_Contribution_20467_",
"Not_Lang_Contribution_20467_",
"Lang_Contribution_20467_",
"Not_Lang_Contribution_20467_",
"IRI_Contribution_20467_",
"Lang_Contribution_20468_",
"Not_Lang_Contribution_20468_",
"Lang_Contribution_20468_",
"Not_Lang_Contribution_20468_",
"IRI_Contribution_20468_",
"Lang_Contribution_20469_",
"Not_Lang_Contribution_20469_",
"Lang_Contribution_20469_",
"Not_Lang_Contribution_20469_",
"IRI_Contribution_20469_",
"Lang_Contribution_20470_",
"Not_Lang_Contribution_20470_",
"Lang_Contribution_20470_",
"Not_Lang_Contribution_20470_",
"IRI_Contribution_20470_",
"Lang_Contribution_20471_",
"Not_Lang_Contribution_20471_",
"Lang_Contribution_20471_",
"Not_Lang_Contribution_20471_",
"IRI_Contribution_20471_",
"Lang_Contribution_20472_",
"Not_Lang_Contribution_20472_",
"Lang_Contribution_20472_",
"Not_Lang_Contribution_20472_",
"IRI_Contribution_20472_",
"Lang_Contribution_20473_",
"Not_Lang_Contribution_20473_",
"Lang_Contribution_20473_",
"Not_Lang_Contribution_20473_",
"IRI_Contribution_20473_",
"Lang_Contribution_20474_",
"Not_Lang_Contribution_20474_",
"Lang_Contribution_20474_",
"Not_Lang_Contribution_20474_",
"IRI_Contribution_20474_",
"Lang_Contribution_20475_",
"Not_Lang_Contribution_20475_",
"Lang_Contribution_20475_",
"Not_Lang_Contribution_20475_",
"IRI_Contribution_20475_",
"Lang_Contribution_20476_",
"Not_Lang_Contribution_20476_",
"Lang_Contribution_20476_",
"Not_Lang_Contribution_20476_",
"IRI_Contribution_20476_",
"Lang_Contribution_20477_",
"Not_Lang_Contribution_20477_",
"Lang_Contribution_20477_",
"Not_Lang_Contribution_20477_",
"IRI_Contribution_20477_",
"Lang_Contribution_20478_",
"Not_Lang_Contribution_20478_",
"Lang_Contribution_20478_",
"Not_Lang_Contribution_20478_",
"IRI_Contribution_20478_",
"Lang_Contribution_20479_",
"Not_Lang_Contribution_20479_",
"Lang_Contribution_20479_",
"Not_Lang_Contribution_20479_",
"IRI_Contribution_20479_",
"Lang_Contribution_20480_",
"Not_Lang_Contribution_20480_",
"Lang_Contribution_20480_",
"Not_Lang_Contribution_20480_",
"IRI_Contribution_20480_",
"Lang_Contribution_20481_",
"Not_Lang_Contribution_20481_",
"Lang_Contribution_20481_",
"Not_Lang_Contribution_20481_",
"IRI_Contribution_20481_",
"Lang_Contribution_20482_",
"Not_Lang_Contribution_20482_",
"Lang_Contribution_20482_",
"Not_Lang_Contribution_20482_",
"IRI_Contribution_20482_",
"Lang_Contribution_20483_",
"Not_Lang_Contribution_20483_",
"Lang_Contribution_20483_",
"Not_Lang_Contribution_20483_",
"IRI_Contribution_20483_",
"Lang_Contribution_20484_",
"Not_Lang_Contribution_20484_",
"Lang_Contribution_20484_",
"Not_Lang_Contribution_20484_",
"IRI_Contribution_20484_",
"Lang_Contribution_20485_",
"Not_Lang_Contribution_20485_",
"Lang_Contribution_20485_",
"Not_Lang_Contribution_20485_",
"IRI_Contribution_20485_",
"Lang_Contribution_20486_",
"Not_Lang_Contribution_20486_",
"Lang_Contribution_20486_",
"Not_Lang_Contribution_20486_",
"IRI_Contribution_20486_",
"Lang_Contribution_20487_",
"Not_Lang_Contribution_20487_",
"Lang_Contribution_20487_",
"Not_Lang_Contribution_20487_",
"IRI_Contribution_20487_",
"Lang_Contribution_20488_",
"Not_Lang_Contribution_20488_",
"Lang_Contribution_20488_",
"Not_Lang_Contribution_20488_",
"IRI_Contribution_20488_",
"Lang_Contribution_20489_",
"Not_Lang_Contribution_20489_",
"Lang_Contribution_20489_",
"Not_Lang_Contribution_20489_",
"IRI_Contribution_20489_",
"Lang_Contribution_20490_",
"Not_Lang_Contribution_20490_",
"Lang_Contribution_20490_",
"Not_Lang_Contribution_20490_",
"IRI_Contribution_20490_",
"Lang_Contribution_20491_",
"Not_Lang_Contribution_20491_",
"Lang_Contribution_20491_",
"Not_Lang_Contribution_20491_",
"IRI_Contribution_20491_",
"Lang_Contribution_20492_",
"Not_Lang_Contribution_20492_",
"Lang_Contribution_20492_",
"Not_Lang_Contribution_20492_",
"IRI_Contribution_20492_",
"Lang_Contribution_20493_",
"Not_Lang_Contribution_20493_",
"Lang_Contribution_20493_",
"Not_Lang_Contribution_20493_",
"IRI_Contribution_20493_",
"Lang_Contribution_20494_",
"Not_Lang_Contribution_20494_",
"Lang_Contribution_20494_",
"Not_Lang_Contribution_20494_",
"IRI_Contribution_20494_",
"Lang_Contribution_20495_",
"Not_Lang_Contribution_20495_",
"Lang_Contribution_20495_",
"Not_Lang_Contribution_20495_",
"IRI_Contribution_20495_",
"Lang_Contribution_20496_",
"Not_Lang_Contribution_20496_",
"Lang_Contribution_20496_",
"Not_Lang_Contribution_20496_",
"IRI_Contribution_20496_",
"Lang_Contribution_20497_",
"Not_Lang_Contribution_20497_",
"Lang_Contribution_20497_",
"Not_Lang_Contribution_20497_",
"IRI_Contribution_20497_",
"Lang_Contribution_20498_",
"Not_Lang_Contribution_20498_",
"Lang_Contribution_20498_",
"Not_Lang_Contribution_20498_",
"IRI_Contribution_20498_",
"Lang_Contribution_20499_",
"Not_Lang_Contribution_20499_",
"Lang_Contribution_20499_",
"Not_Lang_Contribution_20499_",
"IRI_Contribution_20499_",
"Lang_Contribution_20500_",
"Not_Lang_Contribution_20500_",
"Lang_Contribution_20500_",
"Not_Lang_Contribution_20500_",
"IRI_Contribution_20500_",
"Lang_Contribution_20501_",
"Not_Lang_Contribution_20501_",
"Lang_Contribution_20501_",
"Not_Lang_Contribution_20501_",
"IRI_Contribution_20501_",
"Lang_Contribution_20502_",
"Not_Lang_Contribution_20502_",
"Lang_Contribution_20502_",
"Not_Lang_Contribution_20502_",
"IRI_Contribution_20502_",
"Lang_Contribution_20503_",
"Not_Lang_Contribution_20503_",
"Lang_Contribution_20503_",
"Not_Lang_Contribution_20503_",
"IRI_Contribution_20503_",
"Lang_Contribution_20504_",
"Not_Lang_Contribution_20504_",
"Lang_Contribution_20504_",
"Not_Lang_Contribution_20504_",
"IRI_Contribution_20504_",
"Lang_Contribution_20505_",
"Not_Lang_Contribution_20505_",
"Lang_Contribution_20505_",
"Not_Lang_Contribution_20505_",
"IRI_Contribution_20505_",
"Lang_Contribution_20506_",
"Not_Lang_Contribution_20506_",
"Lang_Contribution_20506_",
"Not_Lang_Contribution_20506_",
"IRI_Contribution_20506_",
"Lang_Contribution_20507_",
"Not_Lang_Contribution_20507_",
"Lang_Contribution_20507_",
"Not_Lang_Contribution_20507_",
"IRI_Contribution_20507_",
"Lang_Contribution_20508_",
"Not_Lang_Contribution_20508_",
"Lang_Contribution_20508_",
"Not_Lang_Contribution_20508_",
"IRI_Contribution_20508_",
"Lang_Contribution_20509_",
"Not_Lang_Contribution_20509_",
"Lang_Contribution_20509_",
"Not_Lang_Contribution_20509_",
"IRI_Contribution_20509_",
"Lang_Contribution_20510_",
"Not_Lang_Contribution_20510_",
"Lang_Contribution_20510_",
"Not_Lang_Contribution_20510_",
"IRI_Contribution_20510_",
"Lang_Contribution_20511_",
"Not_Lang_Contribution_20511_",
"Lang_Contribution_20511_",
"Not_Lang_Contribution_20511_",
"IRI_Contribution_20511_",
"Lang_Contribution_20512_",
"Not_Lang_Contribution_20512_",
"Lang_Contribution_20512_",
"Not_Lang_Contribution_20512_",
"IRI_Contribution_20512_",
"Lang_Contribution_20513_",
"Not_Lang_Contribution_20513_",
"Lang_Contribution_20513_",
"Not_Lang_Contribution_20513_",
"IRI_Contribution_20513_",
"Lang_Contribution_20514_",
"Not_Lang_Contribution_20514_",
"Lang_Contribution_20514_",
"Not_Lang_Contribution_20514_",
"IRI_Contribution_20514_",
"Lang_Contribution_20515_",
"Not_Lang_Contribution_20515_",
"Lang_Contribution_20515_",
"Not_Lang_Contribution_20515_",
"IRI_Contribution_20515_",
"Lang_Contribution_20516_",
"Not_Lang_Contribution_20516_",
"Lang_Contribution_20516_",
"Not_Lang_Contribution_20516_",
"IRI_Contribution_20516_",
"Lang_Contribution_20517_",
"Not_Lang_Contribution_20517_",
"Lang_Contribution_20517_",
"Not_Lang_Contribution_20517_",
"IRI_Contribution_20517_",
"Lang_Contribution_20518_",
"Not_Lang_Contribution_20518_",
"Lang_Contribution_20518_",
"Not_Lang_Contribution_20518_",
"IRI_Contribution_20518_",
"Lang_Contribution_20519_",
"Not_Lang_Contribution_20519_",
"Lang_Contribution_20519_",
"Not_Lang_Contribution_20519_",
"IRI_Contribution_20519_",
"Lang_Contribution_20520_",
"Not_Lang_Contribution_20520_",
"Lang_Contribution_20520_",
"Not_Lang_Contribution_20520_",
"IRI_Contribution_20520_",
"Lang_Contribution_20521_",
"Not_Lang_Contribution_20521_",
"Lang_Contribution_20521_",
"Not_Lang_Contribution_20521_",
"IRI_Contribution_20521_",
"Lang_Contribution_20522_",
"Not_Lang_Contribution_20522_",
"Lang_Contribution_20522_",
"Not_Lang_Contribution_20522_",
"IRI_Contribution_20522_",
"Lang_Contribution_20523_",
"Not_Lang_Contribution_20523_",
"Lang_Contribution_20523_",
"Not_Lang_Contribution_20523_",
"IRI_Contribution_20523_",
"Lang_Contribution_20524_",
"Not_Lang_Contribution_20524_",
"Lang_Contribution_20524_",
"Not_Lang_Contribution_20524_",
"IRI_Contribution_20524_",
"Lang_Contribution_20525_",
"Not_Lang_Contribution_20525_",
"Lang_Contribution_20525_",
"Not_Lang_Contribution_20525_",
"IRI_Contribution_20525_",
"Lang_Contribution_20526_",
"Not_Lang_Contribution_20526_",
"Lang_Contribution_20526_",
"Not_Lang_Contribution_20526_",
"IRI_Contribution_20526_",
"Lang_Contribution_20527_",
"Not_Lang_Contribution_20527_",
"Lang_Contribution_20527_",
"Not_Lang_Contribution_20527_",
"IRI_Contribution_20527_",
"Lang_Contribution_20528_",
"Not_Lang_Contribution_20528_",
"Lang_Contribution_20528_",
"Not_Lang_Contribution_20528_",
"IRI_Contribution_20528_",
"Lang_Contribution_20529_",
"Not_Lang_Contribution_20529_",
"Lang_Contribution_20529_",
"Not_Lang_Contribution_20529_",
"IRI_Contribution_20529_",
"Lang_Contribution_20530_",
"Not_Lang_Contribution_20530_",
"Lang_Contribution_20530_",
"Not_Lang_Contribution_20530_",
"IRI_Contribution_20530_",
"Lang_Contribution_20531_",
"Not_Lang_Contribution_20531_",
"Lang_Contribution_20531_",
"Not_Lang_Contribution_20531_",
"IRI_Contribution_20531_",
"Lang_Contribution_20532_",
"Not_Lang_Contribution_20532_",
"Lang_Contribution_20532_",
"Not_Lang_Contribution_20532_",
"IRI_Contribution_20532_",
"Lang_Contribution_20533_",
"Not_Lang_Contribution_20533_",
"Lang_Contribution_20533_",
"Not_Lang_Contribution_20533_",
"IRI_Contribution_20533_",
"Lang_Contribution_20534_",
"Not_Lang_Contribution_20534_",
"Lang_Contribution_20534_",
"Not_Lang_Contribution_20534_",
"IRI_Contribution_20534_",
"Lang_Contribution_20535_",
"Not_Lang_Contribution_20535_",
"Lang_Contribution_20535_",
"Not_Lang_Contribution_20535_",
"IRI_Contribution_20535_",
"Lang_Contribution_20536_",
"Not_Lang_Contribution_20536_",
"Lang_Contribution_20536_",
"Not_Lang_Contribution_20536_",
"IRI_Contribution_20536_",
"Lang_Contribution_20537_",
"Not_Lang_Contribution_20537_",
"Lang_Contribution_20537_",
"Not_Lang_Contribution_20537_",
"IRI_Contribution_20537_",
"Lang_Contribution_20538_",
"Not_Lang_Contribution_20538_",
"Lang_Contribution_20538_",
"Not_Lang_Contribution_20538_",
"IRI_Contribution_20538_",
"Lang_Contribution_20539_",
"Not_Lang_Contribution_20539_",
"Lang_Contribution_20539_",
"Not_Lang_Contribution_20539_",
"IRI_Contribution_20539_",
"Lang_Contribution_20540_",
"Not_Lang_Contribution_20540_",
"Lang_Contribution_20540_",
"Not_Lang_Contribution_20540_",
"IRI_Contribution_20540_",
"Lang_Contribution_20541_",
"Not_Lang_Contribution_20541_",
"Lang_Contribution_20541_",
"Not_Lang_Contribution_20541_",
"IRI_Contribution_20541_",
"Lang_Contribution_20542_",
"Not_Lang_Contribution_20542_",
"Lang_Contribution_20542_",
"Not_Lang_Contribution_20542_",
"IRI_Contribution_20542_",
"Lang_Contribution_20543_",
"Not_Lang_Contribution_20543_",
"Lang_Contribution_20543_",
"Not_Lang_Contribution_20543_",
"IRI_Contribution_20543_",
"Lang_Contribution_20544_",
"Not_Lang_Contribution_20544_",
"Lang_Contribution_20544_",
"Not_Lang_Contribution_20544_",
"IRI_Contribution_20544_",
"Lang_Contribution_20545_",
"Not_Lang_Contribution_20545_",
"Lang_Contribution_20545_",
"Not_Lang_Contribution_20545_",
"IRI_Contribution_20545_",
"Lang_Contribution_20546_",
"Not_Lang_Contribution_20546_",
"Lang_Contribution_20546_",
"Not_Lang_Contribution_20546_",
"IRI_Contribution_20546_",
"Lang_Contribution_20547_",
"Not_Lang_Contribution_20547_",
"Lang_Contribution_20547_",
"Not_Lang_Contribution_20547_",
"IRI_Contribution_20547_",
"Lang_Contribution_20548_",
"Not_Lang_Contribution_20548_",
"Lang_Contribution_20548_",
"Not_Lang_Contribution_20548_",
"IRI_Contribution_20548_",
"Lang_Contribution_20549_",
"Not_Lang_Contribution_20549_",
"Lang_Contribution_20549_",
"Not_Lang_Contribution_20549_",
"IRI_Contribution_20549_",
"Lang_Contribution_20550_",
"Not_Lang_Contribution_20550_",
"Lang_Contribution_20550_",
"Not_Lang_Contribution_20550_",
"IRI_Contribution_20550_",
"Lang_Contribution_20551_",
"Not_Lang_Contribution_20551_",
"Lang_Contribution_20551_",
"Not_Lang_Contribution_20551_",
"IRI_Contribution_20551_",
"Lang_Contribution_20552_",
"Not_Lang_Contribution_20552_",
"Lang_Contribution_20552_",
"Not_Lang_Contribution_20552_",
"IRI_Contribution_20552_",
"Lang_Contribution_20553_",
"Not_Lang_Contribution_20553_",
"Lang_Contribution_20553_",
"Not_Lang_Contribution_20553_",
"IRI_Contribution_20553_",
"Lang_Contribution_20554_",
"Not_Lang_Contribution_20554_",
"Lang_Contribution_20554_",
"Not_Lang_Contribution_20554_",
"IRI_Contribution_20554_",
"Lang_Contribution_20555_",
"Not_Lang_Contribution_20555_",
"Lang_Contribution_20555_",
"Not_Lang_Contribution_20555_",
"IRI_Contribution_20555_",
"Lang_Contribution_20556_",
"Not_Lang_Contribution_20556_",
"Lang_Contribution_20556_",
"Not_Lang_Contribution_20556_",
"IRI_Contribution_20556_",
"Lang_Contribution_20557_",
"Not_Lang_Contribution_20557_",
"Lang_Contribution_20557_",
"Not_Lang_Contribution_20557_",
"IRI_Contribution_20557_",
"Lang_Contribution_20558_",
"Not_Lang_Contribution_20558_",
"Lang_Contribution_20558_",
"Not_Lang_Contribution_20558_",
"IRI_Contribution_20558_",
"Lang_Contribution_20559_",
"Not_Lang_Contribution_20559_",
"Lang_Contribution_20559_",
"Not_Lang_Contribution_20559_",
"IRI_Contribution_20559_",
"Lang_Contribution_20560_",
"Not_Lang_Contribution_20560_",
"Lang_Contribution_20560_",
"Not_Lang_Contribution_20560_",
"IRI_Contribution_20560_",
"Lang_Contribution_20561_",
"Not_Lang_Contribution_20561_",
"Lang_Contribution_20561_",
"Not_Lang_Contribution_20561_",
"IRI_Contribution_20561_",
"Lang_Contribution_20562_",
"Not_Lang_Contribution_20562_",
"Lang_Contribution_20562_",
"Not_Lang_Contribution_20562_",
"IRI_Contribution_20562_",
"Lang_Contribution_20563_",
"Not_Lang_Contribution_20563_",
"Lang_Contribution_20563_",
"Not_Lang_Contribution_20563_",
"IRI_Contribution_20563_",
"Lang_Contribution_20564_",
"Not_Lang_Contribution_20564_",
"Lang_Contribution_20564_",
"Not_Lang_Contribution_20564_",
"IRI_Contribution_20564_",
"Lang_Contribution_20565_",
"Not_Lang_Contribution_20565_",
"Lang_Contribution_20565_",
"Not_Lang_Contribution_20565_",
"IRI_Contribution_20565_",
"Lang_Contribution_20566_",
"Not_Lang_Contribution_20566_",
"Lang_Contribution_20566_",
"Not_Lang_Contribution_20566_",
"IRI_Contribution_20566_",
"Lang_Contribution_20567_",
"Not_Lang_Contribution_20567_",
"Lang_Contribution_20567_",
"Not_Lang_Contribution_20567_",
"IRI_Contribution_20567_",
"Lang_Contribution_20568_",
"Not_Lang_Contribution_20568_",
"Lang_Contribution_20568_",
"Not_Lang_Contribution_20568_",
"IRI_Contribution_20568_",
"Lang_Contribution_20569_",
"Not_Lang_Contribution_20569_",
"Lang_Contribution_20569_",
"Not_Lang_Contribution_20569_",
"IRI_Contribution_20569_",
"Lang_Contribution_20570_",
"Not_Lang_Contribution_20570_",
"Lang_Contribution_20570_",
"Not_Lang_Contribution_20570_",
"IRI_Contribution_20570_",
"Lang_Contribution_20571_",
"Not_Lang_Contribution_20571_",
"Lang_Contribution_20571_",
"Not_Lang_Contribution_20571_",
"IRI_Contribution_20571_",
"IRI_Contribution_hasContributorAgent_",
"Lang_Contribution_hasContributorAgent_",
"Not_Lang_Contribution_hasContributorAgent_",
"Lang_Contribution_30067_",
"Not_Lang_Contribution_30067_",
"Lang_Contribution_30067_",
"Not_Lang_Contribution_30067_",
"IRI_Contribution_30067_",
"Lang_Contribution_30068_",
"Not_Lang_Contribution_30068_",
"Lang_Contribution_30068_",
"Not_Lang_Contribution_30068_",
"IRI_Contribution_30068_",
"Lang_Contribution_30069_",
"Not_Lang_Contribution_30069_",
"Lang_Contribution_30069_",
"Not_Lang_Contribution_30069_",
"IRI_Contribution_30069_",
"Lang_Contribution_30070_",
"Not_Lang_Contribution_30070_",
"Lang_Contribution_30070_",
"Not_Lang_Contribution_30070_",
"IRI_Contribution_30070_",
"Lang_Contribution_30071_",
"Not_Lang_Contribution_30071_",
"Lang_Contribution_30071_",
"Not_Lang_Contribution_30071_",
"IRI_Contribution_30071_",
"Lang_Contribution_30072_",
"Not_Lang_Contribution_30072_",
"Lang_Contribution_30072_",
"Not_Lang_Contribution_30072_",
"IRI_Contribution_30072_",
"Lang_Contribution_30073_",
"Not_Lang_Contribution_30073_",
"Lang_Contribution_30073_",
"Not_Lang_Contribution_30073_",
"IRI_Contribution_30073_",
"Lang_Contribution_30074_",
"Not_Lang_Contribution_30074_",
"Lang_Contribution_30074_",
"Not_Lang_Contribution_30074_",
"IRI_Contribution_30074_",
"Lang_Contribution_30075_",
"Not_Lang_Contribution_30075_",
"Lang_Contribution_30075_",
"Not_Lang_Contribution_30075_",
"IRI_Contribution_30075_",
"Lang_Contribution_30076_",
"Not_Lang_Contribution_30076_",
"Lang_Contribution_30076_",
"Not_Lang_Contribution_30076_",
"IRI_Contribution_30076_",
"Lang_Contribution_30077_",
"Not_Lang_Contribution_30077_",
"Lang_Contribution_30077_",
"Not_Lang_Contribution_30077_",
"IRI_Contribution_30077_",
"Lang_Contribution_30078_",
"Not_Lang_Contribution_30078_",
"Lang_Contribution_30078_",
"Not_Lang_Contribution_30078_",
"IRI_Contribution_30078_",
"Lang_Contribution_30081_",
"Not_Lang_Contribution_30081_",
"Lang_Contribution_30081_",
"Not_Lang_Contribution_30081_",
"IRI_Contribution_30081_",
"Lang_Contribution_30215_",
"Not_Lang_Contribution_30215_",
"Lang_Contribution_30215_",
"Not_Lang_Contribution_30215_",
"IRI_Contribution_30215_",
"Lang_Contribution_30267_",
"Not_Lang_Contribution_30267_",
"IRI_Contribution_30267_",
"Lang_Contribution_30268_",
"Not_Lang_Contribution_30268_",
"IRI_Contribution_30268_",
"Lang_Contribution_30269_",
"Not_Lang_Contribution_30269_",
"IRI_Contribution_30269_",
"Lang_Contribution_30270_",
"Not_Lang_Contribution_30270_",
"IRI_Contribution_30270_",
"Lang_Contribution_30271_",
"Not_Lang_Contribution_30271_",
"IRI_Contribution_30271_",
"Lang_Contribution_30311_",
"Not_Lang_Contribution_30311_",
"IRI_Contribution_30311_",
"Lang_Contribution_30312_",
"Not_Lang_Contribution_30312_",
"Lang_Contribution_30312_",
"Not_Lang_Contribution_30312_",
"IRI_Contribution_30312_",
"Lang_Contribution_30315_",
"Not_Lang_Contribution_30315_",
"IRI_Contribution_30315_",
"Lang_Contribution_30316_",
"Not_Lang_Contribution_30316_",
"IRI_Contribution_30316_",
"Lang_Contribution_30321_",
"Not_Lang_Contribution_30321_",
"IRI_Contribution_30321_",
"Lang_Contribution_30326_",
"Not_Lang_Contribution_30326_",
"IRI_Contribution_30326_",
"Lang_Contribution_30328_",
"Not_Lang_Contribution_30328_",
"IRI_Contribution_30328_",
"Lang_Contribution_30329_",
"Not_Lang_Contribution_30329_",
"Lang_Contribution_30329_",
"Not_Lang_Contribution_30329_",
"IRI_Contribution_30329_",
"Lang_Contribution_30331_",
"Not_Lang_Contribution_30331_",
"IRI_Contribution_30331_",
"Lang_Contribution_30332_",
"Not_Lang_Contribution_30332_",
"IRI_Contribution_30332_",
"Lang_Contribution_30333_",
"Not_Lang_Contribution_30333_",
"IRI_Contribution_30333_",
"Lang_Contribution_30337_",
"Not_Lang_Contribution_30337_",
"Lang_Contribution_30337_",
"Not_Lang_Contribution_30337_",
"IRI_Contribution_30337_",
"Lang_Contribution_30338_",
"Not_Lang_Contribution_30338_",
"IRI_Contribution_30338_",
"Lang_Contribution_30339_",
"Not_Lang_Contribution_30339_",
"IRI_Contribution_30339_",
"Lang_Contribution_30340_",
"Not_Lang_Contribution_30340_",
"IRI_Contribution_30340_",
"Lang_Contribution_30341_",
"Not_Lang_Contribution_30341_",
"IRI_Contribution_30341_",
"Lang_Contribution_30342_",
"Not_Lang_Contribution_30342_",
"IRI_Contribution_30342_",
"Lang_Contribution_30343_",
"Not_Lang_Contribution_30343_",
"IRI_Contribution_30343_",
"Lang_Contribution_30344_",
"Not_Lang_Contribution_30344_",
"IRI_Contribution_30344_",
"Lang_Contribution_30345_",
"Not_Lang_Contribution_30345_",
"IRI_Contribution_30345_",
"Lang_Contribution_30346_",
"Not_Lang_Contribution_30346_",
"IRI_Contribution_30346_",
"Lang_Contribution_30347_",
"Not_Lang_Contribution_30347_",
"Lang_Contribution_30347_",
"Not_Lang_Contribution_30347_",
"IRI_Contribution_30347_",
"Lang_Contribution_30348_",
"Not_Lang_Contribution_30348_",
"Lang_Contribution_30348_",
"Not_Lang_Contribution_30348_",
"IRI_Contribution_30348_",
"Lang_Contribution_30349_",
"Not_Lang_Contribution_30349_",
"Lang_Contribution_30349_",
"Not_Lang_Contribution_30349_",
"IRI_Contribution_30349_",
"Lang_Contribution_30350_",
"Not_Lang_Contribution_30350_",
"Lang_Contribution_30350_",
"Not_Lang_Contribution_30350_",
"IRI_Contribution_30350_",
"Lang_Contribution_30351_",
"Not_Lang_Contribution_30351_",
"Lang_Contribution_30351_",
"Not_Lang_Contribution_30351_",
"IRI_Contribution_30351_",
"Lang_Contribution_30352_",
"Not_Lang_Contribution_30352_",
"Lang_Contribution_30352_",
"Not_Lang_Contribution_30352_",
"IRI_Contribution_30352_",
"Lang_Contribution_30353_",
"Not_Lang_Contribution_30353_",
"Lang_Contribution_30353_",
"Not_Lang_Contribution_30353_",
"IRI_Contribution_30353_",
"Lang_Contribution_30354_",
"Not_Lang_Contribution_30354_",
"Lang_Contribution_30354_",
"Not_Lang_Contribution_30354_",
"IRI_Contribution_30354_",
"Lang_Contribution_30355_",
"Not_Lang_Contribution_30355_",
"Lang_Contribution_30355_",
"Not_Lang_Contribution_30355_",
"IRI_Contribution_30355_",
"Lang_Contribution_30356_",
"Not_Lang_Contribution_30356_",
"Lang_Contribution_30356_",
"Not_Lang_Contribution_30356_",
"IRI_Contribution_30356_",
"Lang_Contribution_30357_",
"Not_Lang_Contribution_30357_",
"Lang_Contribution_30357_",
"Not_Lang_Contribution_30357_",
"IRI_Contribution_30357_",
"Lang_Contribution_30358_",
"Not_Lang_Contribution_30358_",
"Lang_Contribution_30358_",
"Not_Lang_Contribution_30358_",
"IRI_Contribution_30358_",
"Lang_Contribution_30360_",
"Not_Lang_Contribution_30360_",
"Lang_Contribution_30360_",
"Not_Lang_Contribution_30360_",
"IRI_Contribution_30360_",
"Lang_Contribution_30363_",
"Not_Lang_Contribution_30363_",
"Lang_Contribution_30363_",
"Not_Lang_Contribution_30363_",
"IRI_Contribution_30363_",
"Lang_Contribution_30364_",
"Not_Lang_Contribution_30364_",
"Lang_Contribution_30364_",
"Not_Lang_Contribution_30364_",
"IRI_Contribution_30364_",
"Lang_Contribution_30366_",
"Not_Lang_Contribution_30366_",
"Lang_Contribution_30366_",
"Not_Lang_Contribution_30366_",
"IRI_Contribution_30366_",
"Lang_Contribution_30367_",
"Not_Lang_Contribution_30367_",
"IRI_Contribution_30367_",
"Lang_Contribution_30368_",
"Not_Lang_Contribution_30368_",
"IRI_Contribution_30368_",
"Lang_Contribution_30369_",
"Not_Lang_Contribution_30369_",
"IRI_Contribution_30369_",
"Lang_Contribution_30370_",
"Not_Lang_Contribution_30370_",
"IRI_Contribution_30370_",
"Lang_Contribution_30371_",
"Not_Lang_Contribution_30371_",
"IRI_Contribution_30371_",
"Lang_Contribution_30372_",
"Not_Lang_Contribution_30372_",
"IRI_Contribution_30372_",
"Lang_Contribution_30373_",
"Not_Lang_Contribution_30373_",
"IRI_Contribution_30373_",
"Lang_Contribution_30374_",
"Not_Lang_Contribution_30374_",
"IRI_Contribution_30374_",
"Lang_Contribution_30375_",
"Not_Lang_Contribution_30375_",
"IRI_Contribution_30375_",
"Lang_Contribution_30376_",
"Not_Lang_Contribution_30376_",
"Lang_Contribution_30376_",
"Not_Lang_Contribution_30376_",
"IRI_Contribution_30376_",
"Lang_Contribution_30377_",
"Not_Lang_Contribution_30377_",
"Lang_Contribution_30377_",
"Not_Lang_Contribution_30377_",
"IRI_Contribution_30377_",
"Lang_Contribution_30378_",
"Not_Lang_Contribution_30378_",
"Lang_Contribution_30378_",
"Not_Lang_Contribution_30378_",
"IRI_Contribution_30378_",
"Lang_Contribution_30379_",
"Not_Lang_Contribution_30379_",
"Lang_Contribution_30379_",
"Not_Lang_Contribution_30379_",
"IRI_Contribution_30379_",
"Lang_Contribution_30380_",
"Not_Lang_Contribution_30380_",
"Lang_Contribution_30380_",
"Not_Lang_Contribution_30380_",
"IRI_Contribution_30380_",
"Lang_Contribution_30381_",
"Not_Lang_Contribution_30381_",
"Lang_Contribution_30381_",
"Not_Lang_Contribution_30381_",
"IRI_Contribution_30381_",
"Lang_Contribution_30382_",
"Not_Lang_Contribution_30382_",
"Lang_Contribution_30382_",
"Not_Lang_Contribution_30382_",
"IRI_Contribution_30382_",
"Lang_Contribution_30383_",
"Not_Lang_Contribution_30383_",
"Lang_Contribution_30383_",
"Not_Lang_Contribution_30383_",
"IRI_Contribution_30383_",
"Lang_Contribution_30384_",
"Not_Lang_Contribution_30384_",
"Lang_Contribution_30384_",
"Not_Lang_Contribution_30384_",
"IRI_Contribution_30384_",
"Lang_Contribution_30385_",
"Not_Lang_Contribution_30385_",
"Lang_Contribution_30385_",
"Not_Lang_Contribution_30385_",
"IRI_Contribution_30385_",
"Lang_Contribution_30386_",
"Not_Lang_Contribution_30386_",
"Lang_Contribution_30386_",
"Not_Lang_Contribution_30386_",
"IRI_Contribution_30386_",
"Lang_Contribution_30387_",
"Not_Lang_Contribution_30387_",
"Lang_Contribution_30387_",
"Not_Lang_Contribution_30387_",
"IRI_Contribution_30387_",
"Lang_Contribution_30389_",
"Not_Lang_Contribution_30389_",
"Lang_Contribution_30389_",
"Not_Lang_Contribution_30389_",
"IRI_Contribution_30389_",
"Lang_Contribution_30392_",
"Not_Lang_Contribution_30392_",
"Lang_Contribution_30392_",
"Not_Lang_Contribution_30392_",
"IRI_Contribution_30392_",
"Lang_Contribution_30393_",
"Not_Lang_Contribution_30393_",
"Lang_Contribution_30393_",
"Not_Lang_Contribution_30393_",
"IRI_Contribution_30393_",
"Lang_Contribution_30395_",
"Not_Lang_Contribution_30395_",
"Lang_Contribution_30395_",
"Not_Lang_Contribution_30395_",
"IRI_Contribution_30395_",
"Lang_Contribution_30396_",
"Not_Lang_Contribution_30396_",
"IRI_Contribution_30396_",
"Lang_Contribution_30397_",
"Not_Lang_Contribution_30397_",
"IRI_Contribution_30397_",
"Lang_Contribution_30398_",
"Not_Lang_Contribution_30398_",
"IRI_Contribution_30398_",
"Lang_Contribution_30399_",
"Not_Lang_Contribution_30399_",
"IRI_Contribution_30399_",
"Lang_Contribution_30400_",
"Not_Lang_Contribution_30400_",
"IRI_Contribution_30400_",
"Lang_Contribution_30401_",
"Not_Lang_Contribution_30401_",
"IRI_Contribution_30401_",
"Lang_Contribution_30402_",
"Not_Lang_Contribution_30402_",
"IRI_Contribution_30402_",
"Lang_Contribution_30403_",
"Not_Lang_Contribution_30403_",
"IRI_Contribution_30403_",
"Lang_Contribution_30404_",
"Not_Lang_Contribution_30404_",
"IRI_Contribution_30404_",
"Lang_Contribution_30405_",
"Not_Lang_Contribution_30405_",
"Lang_Contribution_30405_",
"Not_Lang_Contribution_30405_",
"IRI_Contribution_30405_",
"Lang_Contribution_30406_",
"Not_Lang_Contribution_30406_",
"Lang_Contribution_30406_",
"Not_Lang_Contribution_30406_",
"IRI_Contribution_30406_",
"Lang_Contribution_30407_",
"Not_Lang_Contribution_30407_",
"Lang_Contribution_30407_",
"Not_Lang_Contribution_30407_",
"IRI_Contribution_30407_",
"Lang_Contribution_30408_",
"Not_Lang_Contribution_30408_",
"Lang_Contribution_30408_",
"Not_Lang_Contribution_30408_",
"IRI_Contribution_30408_",
"Lang_Contribution_30409_",
"Not_Lang_Contribution_30409_",
"Lang_Contribution_30409_",
"Not_Lang_Contribution_30409_",
"IRI_Contribution_30409_",
"Lang_Contribution_30410_",
"Not_Lang_Contribution_30410_",
"Lang_Contribution_30410_",
"Not_Lang_Contribution_30410_",
"IRI_Contribution_30410_",
"Lang_Contribution_30411_",
"Not_Lang_Contribution_30411_",
"Lang_Contribution_30411_",
"Not_Lang_Contribution_30411_",
"IRI_Contribution_30411_",
"Lang_Contribution_30412_",
"Not_Lang_Contribution_30412_",
"Lang_Contribution_30412_",
"Not_Lang_Contribution_30412_",
"IRI_Contribution_30412_",
"Lang_Contribution_30413_",
"Not_Lang_Contribution_30413_",
"Lang_Contribution_30413_",
"Not_Lang_Contribution_30413_",
"IRI_Contribution_30413_",
"Lang_Contribution_30414_",
"Not_Lang_Contribution_30414_",
"Lang_Contribution_30414_",
"Not_Lang_Contribution_30414_",
"IRI_Contribution_30414_",
"Lang_Contribution_30415_",
"Not_Lang_Contribution_30415_",
"Lang_Contribution_30415_",
"Not_Lang_Contribution_30415_",
"IRI_Contribution_30415_",
"Lang_Contribution_30416_",
"Not_Lang_Contribution_30416_",
"Lang_Contribution_30416_",
"Not_Lang_Contribution_30416_",
"IRI_Contribution_30416_",
"Lang_Contribution_30418_",
"Not_Lang_Contribution_30418_",
"Lang_Contribution_30418_",
"Not_Lang_Contribution_30418_",
"IRI_Contribution_30418_",
"Lang_Contribution_30421_",
"Not_Lang_Contribution_30421_",
"Lang_Contribution_30421_",
"Not_Lang_Contribution_30421_",
"IRI_Contribution_30421_",
"Lang_Contribution_30422_",
"Not_Lang_Contribution_30422_",
"Lang_Contribution_30422_",
"Not_Lang_Contribution_30422_",
"IRI_Contribution_30422_",
"Lang_Contribution_30424_",
"Not_Lang_Contribution_30424_",
"Lang_Contribution_30424_",
"Not_Lang_Contribution_30424_",
"IRI_Contribution_30424_",
"Lang_Contribution_30425_",
"Not_Lang_Contribution_30425_",
"IRI_Contribution_30425_",
"Lang_Contribution_30426_",
"Not_Lang_Contribution_30426_",
"IRI_Contribution_30426_",
"Lang_Contribution_30427_",
"Not_Lang_Contribution_30427_",
"IRI_Contribution_30427_",
"Lang_Contribution_30428_",
"Not_Lang_Contribution_30428_",
"IRI_Contribution_30428_",
"Lang_Contribution_30429_",
"Not_Lang_Contribution_30429_",
"IRI_Contribution_30429_",
"Lang_Contribution_30430_",
"Not_Lang_Contribution_30430_",
"IRI_Contribution_30430_",
"Lang_Contribution_30431_",
"Not_Lang_Contribution_30431_",
"IRI_Contribution_30431_",
"Lang_Contribution_30432_",
"Not_Lang_Contribution_30432_",
"IRI_Contribution_30432_",
"Lang_Contribution_30433_",
"Not_Lang_Contribution_30433_",
"IRI_Contribution_30433_",
"Lang_Contribution_30434_",
"Not_Lang_Contribution_30434_",
"Lang_Contribution_30434_",
"Not_Lang_Contribution_30434_",
"IRI_Contribution_30434_",
"Lang_Contribution_30435_",
"Not_Lang_Contribution_30435_",
"Lang_Contribution_30435_",
"Not_Lang_Contribution_30435_",
"IRI_Contribution_30435_",
"Lang_Contribution_30436_",
"Not_Lang_Contribution_30436_",
"Lang_Contribution_30436_",
"Not_Lang_Contribution_30436_",
"IRI_Contribution_30436_",
"Lang_Contribution_30437_",
"Not_Lang_Contribution_30437_",
"Lang_Contribution_30437_",
"Not_Lang_Contribution_30437_",
"IRI_Contribution_30437_",
"Lang_Contribution_30438_",
"Not_Lang_Contribution_30438_",
"Lang_Contribution_30438_",
"Not_Lang_Contribution_30438_",
"IRI_Contribution_30438_",
"Lang_Contribution_30439_",
"Not_Lang_Contribution_30439_",
"Lang_Contribution_30439_",
"Not_Lang_Contribution_30439_",
"IRI_Contribution_30439_",
"Lang_Contribution_30440_",
"Not_Lang_Contribution_30440_",
"Lang_Contribution_30440_",
"Not_Lang_Contribution_30440_",
"IRI_Contribution_30440_",
"Lang_Contribution_30441_",
"Not_Lang_Contribution_30441_",
"Lang_Contribution_30441_",
"Not_Lang_Contribution_30441_",
"IRI_Contribution_30441_",
"Lang_Contribution_30442_",
"Not_Lang_Contribution_30442_",
"Lang_Contribution_30442_",
"Not_Lang_Contribution_30442_",
"IRI_Contribution_30442_",
"Lang_Contribution_30443_",
"Not_Lang_Contribution_30443_",
"Lang_Contribution_30443_",
"Not_Lang_Contribution_30443_",
"IRI_Contribution_30443_",
"Lang_Contribution_30444_",
"Not_Lang_Contribution_30444_",
"Lang_Contribution_30444_",
"Not_Lang_Contribution_30444_",
"IRI_Contribution_30444_",
"Lang_Contribution_30445_",
"Not_Lang_Contribution_30445_",
"Lang_Contribution_30445_",
"Not_Lang_Contribution_30445_",
"IRI_Contribution_30445_",
"Lang_Contribution_30447_",
"Not_Lang_Contribution_30447_",
"Lang_Contribution_30447_",
"Not_Lang_Contribution_30447_",
"IRI_Contribution_30447_",
"Lang_Contribution_30450_",
"Not_Lang_Contribution_30450_",
"Lang_Contribution_30450_",
"Not_Lang_Contribution_30450_",
"IRI_Contribution_30450_",
"Lang_Contribution_30451_",
"Not_Lang_Contribution_30451_",
"Lang_Contribution_30451_",
"Not_Lang_Contribution_30451_",
"IRI_Contribution_30451_",
"IRI_Contribution_hasContributorAgent_",
"Lang_Contribution_hasContributorAgent_",
"Not_Lang_Contribution_hasContributorAgent_",
"Lang_Contribution_40004_",
"Not_Lang_Contribution_40004_",
"Lang_Contribution_40004_",
"Not_Lang_Contribution_40004_",
"IRI_Contribution_40004_",
"Lang_Contribution_40005_",
"Not_Lang_Contribution_40005_",
"Lang_Contribution_40005_",
"Not_Lang_Contribution_40005_",
"IRI_Contribution_40005_",
"Lang_Contribution_40006_",
"Not_Lang_Contribution_40006_",
"IRI_Contribution_40006_",
"Lang_Contribution_40007_",
"Not_Lang_Contribution_40007_",
"IRI_Contribution_40007_",
"Lang_Contribution_40008_",
"Not_Lang_Contribution_40008_",
"IRI_Contribution_40008_",
"Lang_Contribution_40012_",
"Not_Lang_Contribution_40012_",
"IRI_Contribution_40012_",
"Lang_Contribution_40013_",
"Not_Lang_Contribution_40013_",
"IRI_Contribution_40013_",
"Lang_Contribution_40014_",
"Not_Lang_Contribution_40014_",
"IRI_Contribution_40014_",
"Lang_Contribution_40015_",
"Not_Lang_Contribution_40015_",
"IRI_Contribution_40015_",
"Lang_Contribution_40016_",
"Not_Lang_Contribution_40016_",
"IRI_Contribution_40016_",
"Lang_Contribution_40017_",
"Not_Lang_Contribution_40017_",
"Lang_Contribution_40017_",
"Not_Lang_Contribution_40017_",
"IRI_Contribution_40017_",
"Lang_Contribution_40018_",
"Not_Lang_Contribution_40018_",
"Lang_Contribution_40018_",
"Not_Lang_Contribution_40018_",
"IRI_Contribution_40018_",
"Lang_Contribution_40019_",
"Not_Lang_Contribution_40019_",
"IRI_Contribution_40019_",
"Lang_Contribution_40020_",
"Not_Lang_Contribution_40020_",
"Lang_Contribution_40020_",
"Not_Lang_Contribution_40020_",
"IRI_Contribution_40020_",
"Lang_Contribution_40021_",
"Not_Lang_Contribution_40021_",
"Lang_Contribution_40021_",
"Not_Lang_Contribution_40021_",
"IRI_Contribution_40021_",
"Lang_Contribution_40022_",
"Not_Lang_Contribution_40022_",
"Lang_Contribution_40022_",
"Not_Lang_Contribution_40022_",
"IRI_Contribution_40022_",
"Lang_Contribution_40024_",
"Not_Lang_Contribution_40024_",
"IRI_Contribution_40024_",
"Lang_Contribution_40025_",
"Not_Lang_Contribution_40025_",
"Lang_Contribution_40025_",
"Not_Lang_Contribution_40025_",
"IRI_Contribution_40025_",
"Lang_Contribution_40072_",
"Not_Lang_Contribution_40072_",
"IRI_Contribution_40072_",
"Lang_Contribution_40073_",
"Not_Lang_Contribution_40073_",
"IRI_Contribution_40073_",
"Lang_Contribution_40074_",
"Not_Lang_Contribution_40074_",
"IRI_Contribution_40074_",
"Lang_Contribution_40075_",
"Not_Lang_Contribution_40075_",
"IRI_Contribution_40075_",
"Lang_Contribution_40076_",
"Not_Lang_Contribution_40076_",
"IRI_Contribution_40076_",
"Lang_Contribution_40093_",
"Not_Lang_Contribution_40093_",
"Lang_Contribution_40093_",
"Not_Lang_Contribution_40093_",
"IRI_Contribution_40093_",
"Lang_Contribution_40097_",
"Not_Lang_Contribution_40097_",
"Lang_Contribution_40097_",
"Not_Lang_Contribution_40097_",
"IRI_Contribution_40097_",
"Lang_Contribution_40098_",
"Not_Lang_Contribution_40098_",
"IRI_Contribution_40098_",
"Lang_Contribution_40099_",
"Not_Lang_Contribution_40099_",
"Lang_Contribution_40099_",
"Not_Lang_Contribution_40099_",
"IRI_Contribution_40099_",
"Lang_Contribution_40100_",
"Not_Lang_Contribution_40100_",
"IRI_Contribution_40100_",
"Lang_Contribution_40101_",
"Not_Lang_Contribution_40101_",
"Lang_Contribution_40101_",
"Not_Lang_Contribution_40101_",
"IRI_Contribution_40101_",
"Lang_Contribution_40102_",
"Not_Lang_Contribution_40102_",
"IRI_Contribution_40102_",
"Lang_Contribution_40103_",
"Not_Lang_Contribution_40103_",
"Lang_Contribution_40103_",
"Not_Lang_Contribution_40103_",
"IRI_Contribution_40103_",
"Lang_Contribution_40104_",
"Not_Lang_Contribution_40104_",
"Lang_Contribution_40104_",
"Not_Lang_Contribution_40104_",
"IRI_Contribution_40104_",
"Lang_Contribution_40105_",
"Not_Lang_Contribution_40105_",
"Lang_Contribution_40105_",
"Not_Lang_Contribution_40105_",
"IRI_Contribution_40105_",
"Lang_Contribution_40106_",
"Not_Lang_Contribution_40106_",
"Lang_Contribution_40106_",
"Not_Lang_Contribution_40106_",
"IRI_Contribution_40106_",
"Lang_Contribution_40107_",
"Not_Lang_Contribution_40107_",
"IRI_Contribution_40107_",
"Lang_Contribution_40108_",
"Not_Lang_Contribution_40108_",
"IRI_Contribution_40108_",
"Lang_Contribution_40109_",
"Not_Lang_Contribution_40109_",
"IRI_Contribution_40109_",
"Lang_Contribution_40110_",
"Not_Lang_Contribution_40110_",
"Lang_Contribution_40110_",
"Not_Lang_Contribution_40110_",
"IRI_Contribution_40110_",
"Lang_Contribution_40111_",
"Not_Lang_Contribution_40111_",
"IRI_Contribution_40111_",
"Lang_Contribution_40112_",
"Not_Lang_Contribution_40112_",
"Lang_Contribution_40112_",
"Not_Lang_Contribution_40112_",
"IRI_Contribution_40112_",
"Lang_Contribution_40113_",
"Not_Lang_Contribution_40113_",
"Lang_Contribution_40113_",
"Not_Lang_Contribution_40113_",
"IRI_Contribution_40113_",
"Lang_Contribution_40114_",
"Not_Lang_Contribution_40114_",
"IRI_Contribution_40114_",
"Lang_Contribution_40115_",
"Not_Lang_Contribution_40115_",
"Lang_Contribution_40115_",
"Not_Lang_Contribution_40115_",
"IRI_Contribution_40115_",
"Lang_Contribution_40116_",
"Not_Lang_Contribution_40116_",
"IRI_Contribution_40116_",
"Lang_Contribution_40117_",
"Not_Lang_Contribution_40117_",
"Lang_Contribution_40117_",
"Not_Lang_Contribution_40117_",
"IRI_Contribution_40117_",
"Lang_Contribution_40118_",
"Not_Lang_Contribution_40118_",
"IRI_Contribution_40118_",
"Lang_Contribution_40119_",
"Not_Lang_Contribution_40119_",
"Lang_Contribution_40119_",
"Not_Lang_Contribution_40119_",
"IRI_Contribution_40119_",
"Lang_Contribution_40120_",
"Not_Lang_Contribution_40120_",
"Lang_Contribution_40120_",
"Not_Lang_Contribution_40120_",
"IRI_Contribution_40120_",
"Lang_Contribution_40121_",
"Not_Lang_Contribution_40121_",
"Lang_Contribution_40121_",
"Not_Lang_Contribution_40121_",
"IRI_Contribution_40121_",
"Lang_Contribution_40122_",
"Not_Lang_Contribution_40122_",
"Lang_Contribution_40122_",
"Not_Lang_Contribution_40122_",
"IRI_Contribution_40122_",
"Lang_Contribution_40123_",
"Not_Lang_Contribution_40123_",
"IRI_Contribution_40123_",
"Lang_Contribution_40124_",
"Not_Lang_Contribution_40124_",
"IRI_Contribution_40124_",
"Lang_Contribution_40125_",
"Not_Lang_Contribution_40125_",
"IRI_Contribution_40125_",
"Lang_Contribution_40126_",
"Not_Lang_Contribution_40126_",
"Lang_Contribution_40126_",
"Not_Lang_Contribution_40126_",
"IRI_Contribution_40126_",
"Lang_Contribution_40127_",
"Not_Lang_Contribution_40127_",
"IRI_Contribution_40127_",
"Lang_Contribution_40128_",
"Not_Lang_Contribution_40128_",
"Lang_Contribution_40128_",
"Not_Lang_Contribution_40128_",
"IRI_Contribution_40128_",
"Lang_Contribution_40129_",
"Not_Lang_Contribution_40129_",
"Lang_Contribution_40129_",
"Not_Lang_Contribution_40129_",
"IRI_Contribution_40129_",
"Lang_Contribution_40130_",
"Not_Lang_Contribution_40130_",
"IRI_Contribution_40130_",
"Lang_Contribution_40131_",
"Not_Lang_Contribution_40131_",
"Lang_Contribution_40131_",
"Not_Lang_Contribution_40131_",
"IRI_Contribution_40131_",
"Lang_Contribution_40132_",
"Not_Lang_Contribution_40132_",
"IRI_Contribution_40132_",
"Lang_Contribution_40133_",
"Not_Lang_Contribution_40133_",
"Lang_Contribution_40133_",
"Not_Lang_Contribution_40133_",
"IRI_Contribution_40133_",
"Lang_Contribution_40134_",
"Not_Lang_Contribution_40134_",
"IRI_Contribution_40134_",
"Lang_Contribution_40135_",
"Not_Lang_Contribution_40135_",
"Lang_Contribution_40135_",
"Not_Lang_Contribution_40135_",
"IRI_Contribution_40135_",
"Lang_Contribution_40136_",
"Not_Lang_Contribution_40136_",
"Lang_Contribution_40136_",
"Not_Lang_Contribution_40136_",
"IRI_Contribution_40136_",
"Lang_Contribution_40137_",
"Not_Lang_Contribution_40137_",
"Lang_Contribution_40137_",
"Not_Lang_Contribution_40137_",
"IRI_Contribution_40137_",
"Lang_Contribution_40138_",
"Not_Lang_Contribution_40138_",
"Lang_Contribution_40138_",
"Not_Lang_Contribution_40138_",
"IRI_Contribution_40138_",
"Lang_Contribution_40139_",
"Not_Lang_Contribution_40139_",
"IRI_Contribution_40139_",
"Lang_Contribution_40140_",
"Not_Lang_Contribution_40140_",
"IRI_Contribution_40140_",
"Lang_Contribution_40141_",
"Not_Lang_Contribution_40141_",
"IRI_Contribution_40141_",
"Lang_Contribution_40142_",
"Not_Lang_Contribution_40142_",
"Lang_Contribution_40142_",
"Not_Lang_Contribution_40142_",
"IRI_Contribution_40142_",
"Lang_Contribution_40143_",
"Not_Lang_Contribution_40143_",
"IRI_Contribution_40143_",
"Lang_Contribution_40144_",
"Not_Lang_Contribution_40144_",
"Lang_Contribution_40144_",
"Not_Lang_Contribution_40144_",
"IRI_Contribution_40144_",
"Lang_Contribution_40145_",
"Not_Lang_Contribution_40145_",
"Lang_Contribution_40145_",
"Not_Lang_Contribution_40145_",
"IRI_Contribution_40145_",
"Lang_Contribution_40146_",
"Not_Lang_Contribution_40146_",
"IRI_Contribution_40146_",
"Lang_Contribution_40147_",
"Not_Lang_Contribution_40147_",
"Lang_Contribution_40147_",
"Not_Lang_Contribution_40147_",
"IRI_Contribution_40147_",
"Lang_Contribution_40148_",
"Not_Lang_Contribution_40148_",
"IRI_Contribution_40148_",
"Lang_Contribution_40149_",
"Not_Lang_Contribution_40149_",
"Lang_Contribution_40149_",
"Not_Lang_Contribution_40149_",
"IRI_Contribution_40149_",
"Lang_Contribution_40150_",
"Not_Lang_Contribution_40150_",
"IRI_Contribution_40150_",
"Lang_Contribution_40151_",
"Not_Lang_Contribution_40151_",
"Lang_Contribution_40151_",
"Not_Lang_Contribution_40151_",
"IRI_Contribution_40151_",
"Lang_Contribution_40152_",
"Not_Lang_Contribution_40152_",
"Lang_Contribution_40152_",
"Not_Lang_Contribution_40152_",
"IRI_Contribution_40152_",
"Lang_Contribution_40153_",
"Not_Lang_Contribution_40153_",
"Lang_Contribution_40153_",
"Not_Lang_Contribution_40153_",
"IRI_Contribution_40153_",
"Lang_Contribution_40154_",
"Not_Lang_Contribution_40154_",
"Lang_Contribution_40154_",
"Not_Lang_Contribution_40154_",
"IRI_Contribution_40154_",
"Lang_Contribution_40155_",
"Not_Lang_Contribution_40155_",
"IRI_Contribution_40155_",
"Lang_Contribution_40156_",
"Not_Lang_Contribution_40156_",
"IRI_Contribution_40156_",
"Lang_Contribution_40157_",
"Not_Lang_Contribution_40157_",
"IRI_Contribution_40157_",
"Lang_Contribution_40158_",
"Not_Lang_Contribution_40158_",
"Lang_Contribution_40158_",
"Not_Lang_Contribution_40158_",
"IRI_Contribution_40158_",
"Lang_Contribution_40159_",
"Not_Lang_Contribution_40159_",
"IRI_Contribution_40159_",
"Lang_Contribution_40160_",
"Not_Lang_Contribution_40160_",
"Lang_Contribution_40160_",
"Not_Lang_Contribution_40160_",
"IRI_Contribution_40160_",
"IRI_Contribution_hasContributorAgent_",
"Lang_Contribution_hasContributorAgent_",
"Not_Lang_Contribution_hasContributorAgent_"
]

no_language_tag_list = ["P10219", "P20214", "P30007", "P30011", "P30009"]

provisionActivityDistributionList = [
	"P30008",
	"P30017",
	"P30068",
	"P30080",
	"P30085",
	"P30089",
	"P30173",
	"P30348",
	"P30359",
	"P30377",
	"P30388",
	"P30406",
	"P30417",
	"P30435",
	"P30446"
]

provisionActivityManufactureList = [
	"P30010",
	"P30049",
	"P30069",
	"P30070",
	"P30071",
	"P30072",
	"P30073",
	"P30074",
	"P30075",
	"P30076",
	"P30077",
	"P30078",
	"P30082",
	"P30087",
	"P30090",
	"P30175",
	"P30215",
	"P30349",
	"P30350",
	"P30351",
	"P30352",
	"P30353",
	"P30354",
	"P30355",
	"P30356",
	"P30357",
	"P30358",
	"P30361",
	"P30364",
	"P30378",
	"P30379",
	"P30380",
	"P30381",
	"P30382",
	"P30383",
	"P30384",
	"P30385",
	"P30386",
	"P30387",
	"P30390",
	"P30393",
	"P30407",
	"P30408",
	"P30409",
	"P30410",
	"P30411",
	"P30412",
	"P30413",
	"P30414",
	"P30415",
	"P30416",
	"P30419",
	"P30422",
	"P30436",
	"P30437",
	"P30438",
	"P30439",
	"P30440",
	"P30441",
	"P30442",
	"P30443",
	"P30444",
	"P30445",
	"P30448",
	"P30451"
]

provisionActivityProductionList = [
	"P30009",
	"P30081",
	"P30086",
	"P30091",
	"P30094",
	"P30174",
	"P30360",
	"P30389",
	"P30418",
	"P30447"
]

provisionActivityPublicationList = [
	"P30011",
	"P30067",
	"P30083",
	"P30088",
	"P30092",
	"P30095",
	"P30176",
	"P30347",
	"P30362",
	"P30376",
	"P30391",
	"P30405",
	"P30420",
	"P30434",
	"P30449"
]

provisionActivityList = provisionActivityDistributionList + provisionActivityManufactureList + provisionActivityProductionList + provisionActivityPublicationList

work_title_props = [
	"P10012",
	"P10088",
	"P10223"
]

expression_title_props = [
	"P20312",
	"P20315"
]

manifestation_title_props = [
	"P30134",
	"P30142",
	"P30156"
]

item_title_props = [
	"P40082",
	"P40085"
]

classificationLcc_props = ["hasLcClassificationPartA", "hasLcClassificationPartB"]

classificationNlm_props = ["hasNlmClassificationPartA", "hasNlmClassificationPartB"]

prefix_list = [
"@prefix bf: <http://id.loc.gov/ontologies/bibframe/>.",
"@prefix bflc: <http://id.loc.gov/ontologies/bflc/>.",
"@prefix dbo: <http://dbpedia.org/ontology/>.",
"@prefix ex: <http://example.org/rules/>.",
"@prefix madsrdf: <http://www.loc.gov/mads/rdf/v1#>.",
"@prefix rdac: <http://rdaregistry.info/Elements/c/>.",
"@prefix rdae: <http://rdaregistry.info/Elements/e/>.",
"@prefix rdai: <http://rdaregistry.info/Elements/i/>.",
"@prefix rdam: <http://rdaregistry.info/Elements/m/>.",
"@prefix rdamdt: <http://rdaregistry.info/Elements/m/datatype/>.",
"@prefix rdau: <http://rdaregistry.info/Elements/u/>.",
"@prefix rdaw: <http://rdaregistry.info/Elements/w/>.",
"@prefix rdax: <https://doi.org/10.6069/uwlib.55.d.4#>.",
"@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.",
"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.",
"@prefix rml: <http://semweb.mmlab.be/ns/rml#>.",
"@prefix rr: <http://www.w3.org/ns/r2rml#>.",
"@prefix ql: <http://semweb.mmlab.be/ns/ql#>.",
"@prefix schema: <http://schema.org/>.",
"@prefix sin: <http://sinopia.io/vocabulary/>.",
"@prefix skos: <http://www.w3.org/2004/02/skos/core#>.\n"
]

def generate_admin_metadata_list(entity):
	admin_metadata_list = [
f"ex:{entity.capitalize()}Map rr:predicateObjectMap [",
"  rr:predicate bf:adminMetadata;",
"  rr:objectMap [",
"    rr:parentTriplesMap ex:AdminMetadataMap",
"  ]",
"].\n",
"ex:AdminMetadataMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"    rml:source \"../../!!{entity}_filepath!!.xml\";",
"    rml:referenceFormulation ql:XPath;",
"    rml:iterator \"/RDF/Description[catalogerID]\"",
"  ].\n",
"ex:AdminMetadataMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:AdminMetadata",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bflc:catalogerID;",
"  rr:objectMap [",
"    rml:reference \"catalogerID[@lang]\";",
"    rr:termType rr:Literal;",
"    rml:languageMap [",
"      rml:reference \"catalogerID/@lang\"",
"    ]",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bflc:catalogerID;",
"  rr:objectMap [",
"    rml:reference \"catalogerID[not(@lang)]\";",
"    rr:termType rr:Literal",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:status;",
"  rr:objectMap [",
"    rr:parentTriplesMap ex:StatusMap",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bflc:encodingLevel;",
"  rr:objectMap [",
"    rml:reference \"encodingLevel/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:descriptionConventions;",
"  rr:objectMap [",
"    rml:reference \"descriptionConventions/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:source;",
"  rr:objectMap [",
"    rml:reference \"source/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:descriptionLanguage;",
"  rr:objectMap [",
"    rml:reference \"descriptionLanguage/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:creationDate;",
"  rr:objectMap [",
"    rml:reference \"creationDate\";",
"    rr:termType rr:Literal",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:changeDate;",
"  rr:objectMap [",
"    rml:reference \"changeDate\";",
"    rr:termType rr:Literal",
"  ]",
"].\n",
"ex:StatusMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"    rml:source \"../../{default_path}.xml\";",
"    rml:referenceFormulation ql:XPath;",
"    rml:iterator \"/RDF/Description[code]\"",
"  ].\n",
"ex:StatusMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:Status",
"].\n",
"ex:StatusMap rr:predicateObjectMap [",
"  rr:predicate bf:code;",
"  rr:objectMap [",
"    rml:reference \"code\"",
"  ]",
"].\n"
]
	return admin_metadata_list

# has identifier for work
P10002_list = [
"ex:WorkMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rr:parentTriplesMap ex:IdentifierMap",
"  ]",
"].\n",
f"ex:WorkMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rml:reference \"P10002/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:IdentifierMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"    rml:source \"../../!!work_filepath!!.xml\";",
"    rml:referenceFormulation ql:XPath;",
"    rml:iterator \"/RDF/Description/P10002[not(@resource)]\"",
"  ].\n",
"ex:IdentifierMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:Identifier",
"].\n",
"ex:IdentifierMap rr:predicateObjectMap [",
"  rr:predicate rdf:value;",
"  rr:objectMap [",
"    rml:reference \".\";",
"    rr:termType rr:Literal",
"  ]",
"].\n"
]

# has identifier for expression
P20002_list = [
"ex:ExpressionMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rr:parentTriplesMap ex:IdentifierMap",
"  ]",
"].\n",
f"ex:ExpressionMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rml:reference \"P20002/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:IdentifierMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"    rml:source \"../../!!expression_filepath!!.xml\";",
"    rml:referenceFormulation ql:XPath;",
"    rml:iterator \"/RDF/Description/P20002[not(@resource)]\"",
"  ].\n",
"ex:IdentifierMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:Identifier",
"].\n",
"ex:IdentifierMap rr:predicateObjectMap [",
"  rr:predicate rdf:value;",
"  rr:objectMap [",
"    rml:reference \".\";",
"    rr:termType rr:Literal",
"  ]",
"].\n"
]

# has identifier for manifestation
P30004_list = [
"ex:ManifestationMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rr:parentTriplesMap ex:IdentifierMap",
"  ]",
"].\n",
f"ex:ManifestationMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rml:reference \"P30004/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:IdentifierMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"    rml:source \"../../!!manifestation_filepath!!.xml\";",
"    rml:referenceFormulation ql:XPath;",
"    rml:iterator \"/RDF/Description/P30004[not(@resource)]\"",
"  ].\n",
"ex:IdentifierMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:Identifier",
"].\n",
"ex:IdentifierMap rr:predicateObjectMap [",
"  rr:predicate rdf:value;",
"  rr:objectMap [",
"    rml:reference \".\";",
"    rr:termType rr:Literal",
"  ]",
"].\n"
]

# has identifier for item
P40001_list = [
"ex:ItemMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rr:parentTriplesMap ex:IdentifierMap",
"  ]",
"].\n",
f"ex:ItemMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"    rml:reference \"P40001/@resource\";",
"    rr:termType rr:IRI",
"  ]",
"].\n",
"ex:IdentifierMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"    rml:source \"../../!!item_filepath!!.xml\";",
"    rml:referenceFormulation ql:XPath;",
"    rml:iterator \"/RDF/Description/P40001[not(@resource)]\"",
"  ].\n",
"ex:IdentifierMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:Identifier",
"].\n",
"ex:IdentifierMap rr:predicateObjectMap [",
"  rr:predicate rdf:value;",
"  rr:objectMap [",
"    rml:reference \".\";",
"    rr:termType rr:Literal",
"  ]",
"].\n"
]

skip_work_props = ["P10002"]
skip_expression_props = ["P20002"]
skip_manifestation_props = ["P30004"]
skip_item_props = ["P40001"]

"""Functions to parse CSV"""

def get_work_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	work_files = []
	for file in csv_file_list:
		if "work" in file:
			work_files.append(file)

	work_property_list = []
	for csv_file in work_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/w/') in skip_work_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/w/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					work_property_list.append(prop_num)
				line_count += 1

	return work_property_list

def get_work_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	work_files = []
	for file in csv_file_list:
		if "work" in file:
			work_files.append(file)

	work_kiegel_list = []
	for csv_file in work_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/w/') in skip_work_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					work_kiegel_list.append(kiegel)
				line_count += 1

	return work_kiegel_list

def get_expression_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	expression_files = []
	for file in csv_file_list:
		if "expression" in file:
			expression_files.append(file)

	expression_property_list = []
	for csv_file in expression_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/e/') in skip_expression_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/e/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					expression_property_list.append(prop_num)
				line_count += 1

	return expression_property_list

def get_expression_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	expression_files = []
	for file in csv_file_list:
		if "expression" in file:
			expression_files.append(file)

	expression_kiegel_list = []
	for csv_file in expression_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/e/') in skip_expression_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					expression_kiegel_list.append(kiegel)
				line_count += 1

	return expression_kiegel_list

def get_manifestation_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	manifestation_files = []
	for file in csv_file_list:
		if "manifestation" in file:
			manifestation_files.append(file)

	manifestation_property_list = []
	for csv_file in manifestation_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/m/') in skip_manifestation_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/m/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					manifestation_property_list.append(prop_num)
				line_count += 1

	return manifestation_property_list

def get_manifestation_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	manifestation_files = []
	for file in csv_file_list:
		if "manifestation" in file:
			manifestation_files.append(file)

	manifestation_kiegel_list = []
	for csv_file in manifestation_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/m/') in skip_manifestation_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					manifestation_kiegel_list.append(kiegel)
				line_count += 1

	return manifestation_kiegel_list

def get_item_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	item_files = []
	for file in csv_file_list:
		if "item" in file:
			item_files.append(file)

	item_property_list = []
	for csv_file in item_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/i/') in skip_item_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/i/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					item_property_list.append(prop_num)
				line_count += 1

	return item_property_list

def get_item_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	item_files = []
	for file in csv_file_list:
		if "item" in file:
			item_files.append(file)

	item_kiegel_list = []
	for csv_file in item_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/i/') in skip_item_props:
					pass
				elif "rdf-syntax" in line[1]:
					pass
				else:
					kiegel = line[3]

					if ".subclass" in kiegel:
						kiegel_split = kiegel.split("\nor\n")
						for line in kiegel_split:
							if ".subclass" in line:
								kiegel_split.remove(line)
						kiegel = "\nor\n".join(kiegel_split)

					item_kiegel_list.append(kiegel)
				line_count += 1

	return item_kiegel_list

"""Functions to write RML code"""

def start_RML_map(entity):
	default_map = f"{entity.capitalize()}"
	default_class = f"{entity.capitalize()}"
	default_path = f"!!{entity}_filepath!!"

	RML_list = []
	for prefix in prefix_list:
		RML_list.append(prefix + "\n")

	main_logical_source = generate_main_logical_source(entity)
	RML_list.append(main_logical_source + "\n")

	main_subject_map = generate_main_subject_map(entity)
	RML_list.append(main_subject_map + "\n")

	admin_metadata_list = generate_admin_metadata_list(entity)

	for line in admin_metadata_list:
		RML_list.append(line + "\n")

	if entity == "work":
		for line in P10002_list:
			RML_list.append(line + "\n")
	elif entity == "expression":
		for line in P20002_list:
			RML_list.append(line + "\n")
	elif entity == "manifestation":
		for line in P30004_list:
			RML_list.append(line + "\n")
	elif entity == "item":
		for line in P40001_list:
			RML_list.append(line + "\n")

	return RML_list

def create_bnode_name(predicate_name, class_name, property_number, kiegel_map):
	map_number = property_number.strip('P')
	bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
	if "Provisionactivity" in bnode_map_name:
		bnode_map_name = "Provisionactivity_" + class_name + "_"
	elif "Title" in bnode_map_name:
		if "Variant" in class_name:
			bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
		elif "Abbreviated" in class_name:
			bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
		else:
			bnode_map_name = "Title_"
	elif property_number in classificationLcc_props:
		bnode_map_name = "Classification_Lcc_"
	elif property_number in classificationNlm_props:
		bnode_map_name = "Classification_Nlm_"
	elif "*" not in kiegel_map:
		if property_number not in no_language_tag_list:
			bnode_map_name = f"Lang_{bnode_map_name}"
	elif "*" in kiegel_map:
		bnode_map_name = f"IRI_{bnode_map_name}"

	return bnode_map_name

# logical sources
def generate_main_logical_source(entity):
	if "w" in entity:
		class_number = "C10001"
	elif "exp" in entity:
		class_number = "C10006"
	elif "mani" in entity:
		class_number = "C10007"
	elif "item" in entity:
		class_number = "C10003"
	lang_logical_source = f"""ex:{entity.capitalize()}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../!!{entity}_filepath!!.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[type/@resource='http://rdaregistry.info/Elements/c/{class_number}']\"
  ].\n"""

	return lang_logical_source

def generate_IRI_logical_source(map_name, file_path, property_number):
	IRI_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description/{property_number}/@resource\"
  ].\n"""

	return IRI_logical_source

def generate_neutral_literal_logical_source(map_name, file_path, property_number):
	literal_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description/{property_number}[not(@resource)]\"
  ].\n"""

	return literal_logical_source

def generate_lang_logical_source(map_name, file_path, property_number):
	lang_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description/{property_number}[not(@resource)][@lang]\"
  ].\n"""

	return lang_logical_source

def generate_constant_logical_source(map_name, file_path, property_number):
	constant_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}]\"
  ].\n"""

	return constant_logical_source

def generate_not_lang_logical_source(map_name, file_path, property_number):
	not_lang_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description/{property_number}[not(@resource) and not(@lang)]\"
  ].\n"""

	return not_lang_logical_source

def generate_provact_logical_source(class_name, map_name, file_path):
	if class_name == "Distribution":
		property_numbers = " or ".join(provisionActivityDistributionList)
	elif class_name == "Manufacture":
		property_numbers = " or ".join(provisionActivityManufactureList)
	elif class_name == "Production":
		property_numbers = " or ".join(provisionActivityProductionList)
	elif class_name == "Publication":
		property_numbers = " or ".join(provisionActivityPublicationList)

	provact_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_numbers}]\"
  ].\n"""

	return provact_logical_source

def generate_title_logical_source(map_name, file_path):
	if "work" in file_path.lower():
		property_numbers = " or ".join(work_title_props)
	elif "exp" in file_path.lower():
		property_numbers = " or ".join(expression_title_props)
	elif "mani" in file_path.lower():
		property_numbers = " or ".join(manifestation_title_props)
	elif "item" in file_path.lower():
		property_numbers = " or ".join(item_title_props)

	title_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_numbers}]\"
  ].\n"""

	return title_logical_source

def generate_classification_logical_source(map_name, file_path):
	if "Lcc" in map_name:
		property_numbers = " or ".join(classificationLcc_props)
	elif "Nlm" in map_name:
		property_numbers = " or ".join(classificationNlm_props)

	title_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_numbers}]\"
  ].\n"""

	return title_logical_source

def generate_lang_nosplit_logical_source(map_name, file_path, property_number):
	lang_nosplit_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}[not(@resource)][@lang]]\"
  ].\n"""

	return lang_nosplit_logical_source

def generate_not_lang_nosplit_logical_source(map_name, file_path, property_number):
	not_lang_nosplit_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"../../{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}[not(@resource) and not(@lang)]]\"
  ].\n"""

	return not_lang_nosplit_logical_source

# subject maps

def generate_main_subject_map(entity):
	if entity.lower() == "work":
		class_name = "bf:Work"
	elif entity.lower() == "expression":
		class_name = "bf:Work"
	elif entity.lower() == "manifestation":
		class_name = "bf:Instance"
	elif entity.lower() == "item":
		class_name = "bf:Item"

	main_subject_map = f"""ex:{entity.capitalize()}Map rr:subjectMap [
  rml:reference "@about";
  rr:class {class_name}
].\n"""

	return main_subject_map

def generate_bnode_subject_map(map_name, class_name):
	if ":" not in class_name:
		class_name = f"bf:{class_name}"

	bnode_subject_map = f"""ex:{map_name}Map rr:subjectMap [
  rr:termType rr:BlankNode;
  rr:class {class_name}
].\n"""

	return bnode_subject_map

# predicate object maps

def generate_bnode_po_map(predicate, bnode_map_name, map_name):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	bnode_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:parentTriplesMap ex:{bnode_map_name}Map
  ]
].\n"""

	return bnode_po_map

def generate_langnotlang_literal_po_main_map(predicate, map_name, property_number):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	langnotlang_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"{property_number}[not(@resource)][@lang]\";
    rr:termType rr:Literal;
    rml:languageMap [
      rml:reference \"{property_number}/@lang\"
    ]
  ]
].

ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rml:reference \"{property_number}[not(@resource) and not(@lang)]\";
    rr:termType rr:Literal
  ]
].\n"""

	return langnotlang_literal_po_map

def generate_neutral_literal_po_main_map(predicate, map_name, property_number):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	neutral_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"{property_number}[not(@resource)]\";
    rr:termType rr:Literal
  ]
].\n"""

	return neutral_literal_po_map

def generate_IRI_po_main_map(predicate, map_name, property_number):
	if "*" in predicate:
		predicate = predicate.strip("*")
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	IRI_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"{property_number}/@resource\";
    rr:termType rr:IRI
  ]
].\n"""

	return IRI_po_map

def generate_lang_literal_split_po_map(predicate, map_name):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	lang_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \".\";
    rr:termType rr:Literal;
    rml:languageMap [
      rml:reference \"@lang\"
    ]
  ]
].\n"""

	return lang_literal_po_map

def generate_not_lang_literal_split_po_map(predicate, map_name):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	not_lang_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \".\";
    rr:termType rr:Literal
  ]
].\n"""

	return not_lang_literal_po_map

def generate_neutral_literal_split_po_map(predicate, map_name):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	neutral_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \".\";
    rr:termType rr:Literal
  ]
].\n"""

	return neutral_literal_po_map

def generate_IRI_split_po_map(predicate, map_name):
	if "*" in predicate:
		predicate = predicate.strip("*")
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	IRI_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"self::node()\";
    rr:termType rr:IRI
  ]
].\n"""

	return IRI_po_map

def generate_lang_literal_nosplit_po_map(predicate, map_name, property_number):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	lang_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"{property_number}[@lang]\";
    rr:termType rr:Literal;
    rml:languageMap [
      rml:reference \"{property_number}/@lang\"
    ]
  ]
].\n"""

	return lang_literal_po_map

def generate_not_lang_literal_nosplit_po_map(predicate, map_name, property_number):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	not_lang_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"{property_number}[not(@lang)]\";
    rr:termType rr:Literal
  ]
].\n"""

	return not_lang_literal_po_map

def generate_neutral_literal_nosplit_po_map(predicate, map_name, property_number):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	neutral_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"{property_number}\";
    rr:termType rr:Literal
  ]
].\n"""

	return neutral_literal_po_map

def generate_IRI_nosplit_po_map(predicate, map_name, property_number):
	if "*" in predicate:
		predicate = predicate.strip("*")
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	IRI_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
    rr:objectMap [
    rml:reference \"{property_number}/@resource\";
    rr:termType rr:IRI
  ]
].\n"""

	return IRI_po_map

# constants

def generate_constant(node, map_name):
	predicate_constant = node.split("=")
	predicate_name = predicate_constant[0]
	constant_value = predicate_constant[1]

	if ">" in constant_value: # the constant is an IRI
		constant_value = constant_value.strip("<")
		constant_value = constant_value.strip(">")

		po_map = generate_constant_IRI(constant_value, predicate_name, map_name)

	else: # the constant is a literal
		po_map = generate_constant_literal(constant_value, predicate_name, map_name)

	return po_map

def generate_constant_IRI(IRI_value, predicate, map_name):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"
	constant_IRI_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:constant \"{IRI_value}\";
    rr:termType rr:IRI
  ]
].\n"""
	return constant_IRI_po_map

def generate_constant_literal(literal_value, predicate, map_name, language="en"):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"
	constant_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:constant {literal_value};
    rr:termType rr:Literal;
    rr:language \"{language}\"
  ]
].\n"""
	return constant_literal_po_map

# template

def generate_template_po_map(predicate, part_a, part_b, map_name, format=""):
	open_curly_brace = "{"
	close_curly_brace = "}"

	po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:template \"{open_curly_brace}{part_a}{close_curly_brace}{format}{open_curly_brace}{part_b}{close_curly_brace}\";
    rr:termType rr:Literal
  ]
]."""
	return po_map

"""Functions to parse kiegel"""

def replace_semicolons(kiegel_map):
	"""Replace shorthand semicolons in kiegel map with "long-hand" map that is more easily parsed"""
	if ";" in kiegel_map:
		kiegel_map = kiegel_map.replace("; >", ";>")
		kiegel_map = kiegel_map.split(" ; ")

		new_map_list = []

		for map in kiegel_map:
			map = map.replace(";>", "; >")
			map_list = map.split(" ; ")

			num_of_nodes = len(map_list)

			node_range = range(0, num_of_nodes)

			for num in node_range:
				map = map_list[num]
				if map[0] == ">": # if the first character is >, i.e. it was "; >"
					predicate_class_map = map_list[0]
					predicate_name = predicate_class_map.split(" ")[0]
					class_name = predicate_class_map.split(" ")[2]
					new_map = f"{predicate_name} >> {class_name} {map}"
					new_map_list.append(new_map)
				else:
					new_map_list.append(map)

		new_kiegel = "\nand\n".join(new_map_list)
		return new_kiegel
	else:
		return kiegel_map

def split_by_space(map):
	"""Takes in a kiegel map as a string, and returns the elements in the map separated as a list"""
	map = map.strip()
	map_list = map.split(" ")

	# some constant literal values will have spaces in them that shouldn't be split; the following code will look for these instances and fix them
	if '="' in map:
		continue_search = False
		new_map_list = []
		for item in map_list:
			if len(item) < 1:
				pass
			else:
				item = item.strip()
				if item.split('=')[-1][0] == '"' and item[-1] != '"': # first character after = is " and the last character of string is NOT "...
					broken_constant_list = []
					broken_constant_list.append(item)
					continue_search = True
				else:
					if continue_search == True:
						broken_constant_list.append(item)
						if item[-1] == '"': # if the last character is ", the broken constant list has all the parts of the literal
							continue_search = False
							fixed_constant = fix_broken_constants(broken_constant_list)
							new_map_list.append(fixed_constant)
					else:
						new_map_list.append(item)

		map_list = new_map_list

	return map_list

def fix_broken_constants(constant_list):
	"""Takes in a list of values that ought to be one literal, and outputs them as a single literal"""
	space = " "
	new_literal = space.join(constant_list)
	return new_literal

def generate_bnode_po_map_test(default_map, map_name, bnode_map_name, bnode_map_list):
	if map_name == default_map:
		if bnode_map_name not in bnode_map_list:
			generate_map = True

def constant_only_test(node_list, start_point):
	num_of_nodes = len(node_list)
	start_num = 0
	bnode = ""
	for num in range(0, num_of_nodes):
		node = node_list[num].strip()
		if node == start_point:
			start_num = 1
		if start_num > 0:
			bnode = bnode + node + " "
		else:
			pass
	bnode_contents = bnode.split(" >> ")[1:]
	bnode_contents = (" >> ").join(bnode_contents)
	bnode_contents_list = split_by_space(bnode_contents)
	if "" in bnode_contents_list:
		bnode_contents_list.remove("")
	only_constants = True
	for node in bnode_contents_list:
		if node[0].isupper() == True: # class
			pass
		elif node == ">":
			pass
		elif node == ">>":
			only_constants = False
		else:
			if "*" in node: # IRI
				only_constants = False
			elif "=" not in node: # literal
				only_constants = False
	return only_constants

###

"""Work"""

default_map = "Work"
default_class = "Work"
default_path = "!!work_filepath!!"

work_RML_list = start_RML_map("work")
work_property_list = get_work_property_list(csv_dir)
work_kiegel_list = get_work_kiegel_list(csv_dir)

work_property_range = range(0, len(work_property_list))

work_bnode_po_dict = {}
work_logsource_subject_list = []

for number in work_property_range:
	property_number = work_property_list[number]

	kiegel = work_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			map_name = default_map

			node_list = split_by_space(map_2)

			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					if map_name == default_map:
						po_map = generate_IRI_po_main_map(node, map_name, property_number)
					elif map_name in nosplit_bnode_list:
						po_map = generate_IRI_nosplit_po_map(node, map_name, property_number)
					else:
						po_map = generate_IRI_split_po_map(node, map_name)
					work_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_IRI_split_po_map(node, not_lang_map)
						work_RML_list.append(second_po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					work_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_constant(node, not_lang_map)
						work_RML_list.append(second_po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)
					if constant_only_test(node_list, predicate_name) == True:
						if predicate_name != "contribution":
							bnode_map_name = f"Constant_{predicate_name.capitalize()}_{property_number}_"

					generate_new_bnode_po_map = False
					generate_new_logical_source = False
					generate_new_subject_map = False

					if map_name in work_bnode_po_dict.keys():
						if bnode_map_name not in work_bnode_po_dict[map_name]:
							generate_new_bnode_po_map = True
					else:
						generate_new_bnode_po_map = True

					if bnode_map_name not in work_logsource_subject_list:
						generate_new_logical_source = True
						generate_new_subject_map = True

					if generate_new_bnode_po_map == True:
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						work_RML_list.append(bnode_po_map + "\n")

						if "Lang" in map_name:
							not_lang_map_name = f"Not_{map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, not_lang_map_name)
							work_RML_list.append(second_bnode_po_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map_name = f"Not_{bnode_map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, map_name)
							work_RML_list.append(second_bnode_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, not_lang_map_name)
								work_RML_list.append(second_bnode_po_map + "\n")

					if map_name not in work_bnode_po_dict.keys():
						work_bnode_po_dict[map_name] = []
					work_bnode_po_dict[map_name].append(bnode_map_name)

					if generate_new_logical_source == True: ###
						if "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							work_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							work_RML_list.append(logical_source + "\n")
						elif bnode_map_name in nosplit_bnode_list:
							logical_source = generate_lang_nosplit_logical_source(bnode_map_name, default_path, property_number)
							work_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_nosplit_logical_source(not_lang_bnode_map_name, default_path, property_number)
								work_RML_list.append(second_logical_source + "\n")
						elif "Constant_" in bnode_map_name:
							logical_source = generate_constant_logical_source(bnode_map_name, default_path, property_number)
							work_RML_list.append(logical_source + "\n")
						elif "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							work_RML_list.append(logical_source + "\n")
						elif property_number in no_language_tag_list: # the blank node takes a literal, lang tag doesn't matter
							logical_source = generate_neutral_literal_logical_source(bnode_map_name, default_path, property_number)
							work_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal, lang tag does matter
							logical_source = generate_lang_logical_source(bnode_map_name, default_path, property_number)
							work_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_logical_source(not_lang_bnode_map_name, default_path, property_number)
								work_RML_list.append(second_logical_source + "\n")

						work_logsource_subject_list.append(bnode_map_name)

					if generate_new_subject_map == True:
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						work_RML_list.append(subject_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map = f"Not_{bnode_map_name}"
							second_subject_map = generate_bnode_subject_map(not_lang_bnode_map_name, class_name)
							work_RML_list.append(second_subject_map + "\n")

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = work_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					work_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						work_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if map_name == default_map:
							if property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
								work_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								work_RML_list.append(literal_po_map + "\n")
						elif map_name == "Title_":
							literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
							work_RML_list.append(literal_po_map + "\n")
						elif map_name in nosplit_bnode_list:
							literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
							work_RML_list.append(literal_po_map + "\n")
						elif property_number in no_language_tag_list:
							literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
							work_RML_list.append(literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
								work_RML_list.append(second_literal_po_map + "\n")
						else:
							lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
							work_RML_list.append(lang_literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
								work_RML_list.append(not_lang_literal_po_map + "\n")

					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if map_name == default_map:
								if property_number in no_language_tag_list:
									literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
									work_RML_list.append(literal_po_map + "\n")
								else:
									literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
									work_RML_list.append(literal_po_map + "\n")
							elif map_name == "Title_":
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								work_RML_list.append(literal_po_map + "\n")
							elif map_name in nosplit_bnode_list:
								literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
								work_RML_list.append(literal_po_map + "\n")
							elif property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
								work_RML_list.append(literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
									work_RML_list.append(second_literal_po_map + "\n")
							else:
								lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
								work_RML_list.append(lang_literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
									work_RML_list.append(not_lang_literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/workRML.ttl", "w") as output_file:
	for code in work_RML_list:
		output_file.write(code)

###

"""Expression"""

default_map = "Expression"
default_class = "Expression"
default_path = "!!expression_filepath!!"

expression_RML_list = start_RML_map("expression")
expression_property_list = get_expression_property_list(csv_dir)
expression_kiegel_list = get_expression_kiegel_list(csv_dir)

expression_property_range = range(0, len(expression_property_list))

expression_bnode_po_dict = {}
expression_logsource_subject_list = []

for number in expression_property_range:
	property_number = expression_property_list[number]

	kiegel = expression_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			map_name = default_map

			node_list = split_by_space(map_2)
			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					if map_name == default_map:
						po_map = generate_IRI_po_main_map(node, map_name, property_number)
					elif map_name in nosplit_bnode_list:
						po_map = generate_IRI_nosplit_po_map(node, map_name, property_number)
					else:
						po_map = generate_IRI_split_po_map(node, map_name)
					expression_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_IRI_split_po_map(node, not_lang_map)
						expression_RML_list.append(second_po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					expression_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_constant(node, not_lang_map)
						expression_RML_list.append(second_po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)
					if constant_only_test(node_list, predicate_name) == True:
						if predicate_name != "contribution":
							bnode_map_name = f"Constant_{predicate_name.capitalize()}_{property_number}_"

					generate_new_bnode_po_map = False
					generate_new_logical_source = False
					generate_new_subject_map = False

					if map_name in expression_bnode_po_dict.keys():
						if bnode_map_name not in expression_bnode_po_dict[map_name]:
							generate_new_bnode_po_map = True
					else:
						generate_new_bnode_po_map = True

					if bnode_map_name not in expression_logsource_subject_list:
						generate_new_logical_source = True
						generate_new_subject_map = True

					if generate_new_bnode_po_map == True:
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						expression_RML_list.append(bnode_po_map + "\n")

						if "Lang" in map_name:
							not_lang_map_name = f"Not_{map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, not_lang_map_name)
							expression_RML_list.append(second_bnode_po_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map_name = f"Not_{bnode_map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, map_name)
							expression_RML_list.append(second_bnode_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, not_lang_map_name)
								expression_RML_list.append(second_bnode_po_map + "\n")

					if map_name not in expression_bnode_po_dict.keys():
						expression_bnode_po_dict[map_name] = []
					expression_bnode_po_dict[map_name].append(bnode_map_name)

					if generate_new_logical_source == True:
						if "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							expression_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							expression_RML_list.append(logical_source + "\n")
						elif bnode_map_name in nosplit_bnode_list:
							logical_source = generate_lang_nosplit_logical_source(bnode_map_name, default_path, property_number)
							expression_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_nosplit_logical_source(not_lang_bnode_map_name, default_path, property_number)
								expression_RML_list.append(second_logical_source + "\n")
						elif "Constant_" in bnode_map_name:
							logical_source = generate_constant_logical_source(bnode_map_name, default_path, property_number)
							expression_RML_list.append(logical_source + "\n")
						elif "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							expression_RML_list.append(logical_source + "\n")
						elif property_number in no_language_tag_list: # the blank node takes a literal, lang tag doesn't matter
							logical_source = generate_neutral_literal_logical_source(bnode_map_name, default_path, property_number)
							expression_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal, lang tag does matter
							logical_source = generate_lang_logical_source(bnode_map_name, default_path, property_number)
							expression_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_logical_source(not_lang_bnode_map_name, default_path, property_number)
								expression_RML_list.append(second_logical_source + "\n")

						expression_logsource_subject_list.append(bnode_map_name)

					if generate_new_subject_map == True:
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						expression_RML_list.append(subject_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map = f"Not_{bnode_map_name}"
							second_subject_map = generate_bnode_subject_map(not_lang_bnode_map_name, class_name)
							expression_RML_list.append(second_subject_map + "\n")

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = expression_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					expression_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						expression_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if map_name == default_map:
							if property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
								expression_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								expression_RML_list.append(literal_po_map + "\n")
						elif map_name == "Title_":
							literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
							expression_RML_list.append(literal_po_map + "\n")
						elif map_name in nosplit_bnode_list:
							literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
							expression_RML_list.append(literal_po_map + "\n")
						elif property_number in no_language_tag_list:
							literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
							expression_RML_list.append(literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
								expression_RML_list.append(second_literal_po_map + "\n")
						else:
							lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
							expression_RML_list.append(lang_literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
								expression_RML_list.append(not_lang_literal_po_map + "\n")

					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if map_name == default_map:
								if property_number in no_language_tag_list:
									literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
									expression_RML_list.append(literal_po_map + "\n")
								else:
									literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
									expression_RML_list.append(literal_po_map + "\n")
							elif map_name == "Title_":
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								expression_RML_list.append(literal_po_map + "\n")
							elif map_name in nosplit_bnode_list:
								literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
								expression_RML_list.append(literal_po_map + "\n")
							elif property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
								expression_RML_list.append(literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
									expression_RML_list.append(second_literal_po_map + "\n")
							else:
								lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
								expression_RML_list.append(lang_literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
									expression_RML_list.append(not_lang_literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/expressionRML.ttl", "w") as output_file:
	for code in expression_RML_list:
		output_file.write(code)

###

"""Manifestation"""

default_map = "Manifestation"
default_class = "Manifestation"
default_path = "!!manifestation_filepath!!"

manifestation_RML_list = start_RML_map("manifestation")
manifestation_property_list = get_manifestation_property_list(csv_dir)
manifestation_kiegel_list = get_manifestation_kiegel_list(csv_dir)

manifestation_property_range = range(0, len(manifestation_property_list))

manifestation_bnode_po_dict = {}
manifestation_logsource_subject_list = []

for number in manifestation_property_range:
	property_number = manifestation_property_list[number]

	kiegel = manifestation_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			map_name = default_map

			node_list = split_by_space(map_2)

			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					if map_name == default_map:
						po_map = generate_IRI_po_main_map(node, map_name, property_number)
					elif map_name in nosplit_bnode_list:
						po_map = generate_IRI_nosplit_po_map(node, map_name, property_number)
					else:
						po_map = generate_IRI_split_po_map(node, map_name)
					manifestation_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_IRI_split_po_map(node, not_lang_map)
						manifestation_RML_list.append(second_po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					manifestation_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_constant(node, not_lang_map)
						manifestation_RML_list.append(second_po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)
					if constant_only_test(node_list, predicate_name) == True:
						skip_list = ["contribution", "expressionOf", "instanceOf"]
						if predicate_name not in skip_list:
							bnode_map_name = f"Constant_{predicate_name.capitalize()}_{property_number}_"

					generate_new_bnode_po_map = False
					generate_new_logical_source = False
					generate_new_subject_map = False

					if map_name in manifestation_bnode_po_dict.keys():
						if bnode_map_name not in manifestation_bnode_po_dict[map_name]:
							generate_new_bnode_po_map = True
					else:
						generate_new_bnode_po_map = True

					if bnode_map_name not in manifestation_logsource_subject_list:
						generate_new_logical_source = True
						generate_new_subject_map = True

					if generate_new_bnode_po_map == True:
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						manifestation_RML_list.append(bnode_po_map + "\n")

						if "Lang" in map_name:
							not_lang_map_name = f"Not_{map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, not_lang_map_name)
							manifestation_RML_list.append(second_bnode_po_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map_name = f"Not_{bnode_map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, map_name)
							manifestation_RML_list.append(second_bnode_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, not_lang_map_name)
								manifestation_RML_list.append(second_bnode_po_map + "\n")

					if map_name not in manifestation_bnode_po_dict.keys():
						manifestation_bnode_po_dict[map_name] = []
					manifestation_bnode_po_dict[map_name].append(bnode_map_name)

					if generate_new_logical_source == True:
						if "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							manifestation_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							manifestation_RML_list.append(logical_source + "\n")
						elif bnode_map_name in nosplit_bnode_list:
							logical_source = generate_lang_nosplit_logical_source(bnode_map_name, default_path, property_number)
							manifestation_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_nosplit_logical_source(not_lang_bnode_map_name, default_path, property_number)
								manifestation_RML_list.append(second_logical_source + "\n")
						elif "Constant_" in bnode_map_name:
							logical_source = generate_constant_logical_source(bnode_map_name, default_path, property_number)
							manifestation_RML_list.append(logical_source + "\n")
						elif "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							manifestation_RML_list.append(logical_source + "\n")
						elif property_number in no_language_tag_list: # the blank node takes a literal, lang tag doesn't matter
							logical_source = generate_neutral_literal_logical_source(bnode_map_name, default_path, property_number)
							manifestation_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal, lang tag does matter
							logical_source = generate_lang_logical_source(bnode_map_name, default_path, property_number)
							manifestation_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_logical_source(not_lang_bnode_map_name, default_path, property_number)
								manifestation_RML_list.append(second_logical_source + "\n")

						manifestation_logsource_subject_list.append(bnode_map_name)

					if generate_new_subject_map == True:
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						manifestation_RML_list.append(subject_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map = f"Not_{bnode_map_name}"
							second_subject_map = generate_bnode_subject_map(not_lang_bnode_map_name, class_name)
							manifestation_RML_list.append(second_subject_map + "\n")

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = manifestation_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					manifestation_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						manifestation_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if map_name == default_map:
							if property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")
						elif map_name == "Title_":
							literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
							manifestation_RML_list.append(literal_po_map + "\n")
						elif "Provisionactivity_" in map_name:
							if property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")
						elif map_name in nosplit_bnode_list:
							literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
							manifestation_RML_list.append(literal_po_map + "\n")
						elif property_number in no_language_tag_list:
							literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
							manifestation_RML_list.append(literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
								manifestation_RML_list.append(second_literal_po_map + "\n")
						else:
							lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
							manifestation_RML_list.append(lang_literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
								manifestation_RML_list.append(not_lang_literal_po_map + "\n")

					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if map_name == default_map:
								if property_number in no_language_tag_list:
									literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
									manifestation_RML_list.append(literal_po_map + "\n")
								else:
									literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
									manifestation_RML_list.append(literal_po_map + "\n")
							elif map_name == "Title_":
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")
							elif map_name in nosplit_bnode_list:
								literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")
							elif property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
								manifestation_RML_list.append(literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
									manifestation_RML_list.append(second_literal_po_map + "\n")
							else:
								lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
								manifestation_RML_list.append(lang_literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
									manifestation_RML_list.append(not_lang_literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/manifestationRML.ttl", "w") as output_file:
	for code in manifestation_RML_list:
		output_file.write(code)

###

"""Item"""

default_map = "Item"
default_class = "Item"
default_path = "!!item_filepath!!"

item_RML_list = start_RML_map("item")
item_property_list = get_item_property_list(csv_dir)
item_kiegel_list = get_item_kiegel_list(csv_dir)

item_property_range = range(0, len(item_property_list))

item_bnode_po_dict = {}
item_logsource_subject_list = []

for number in item_property_range:
	property_number = item_property_list[number]

	kiegel = item_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			map_name = default_map

			node_list = split_by_space(map_2)

			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					if map_name == default_map:
						po_map = generate_IRI_po_main_map(node, map_name, property_number)
					elif map_name in nosplit_bnode_list:
						po_map = generate_IRI_nosplit_po_map(node, map_name, property_number)
					else:
						po_map = generate_IRI_split_po_map(node, map_name)
					item_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_IRI_split_po_map(node, not_lang_map)
						item_RML_list.append(second_po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					item_RML_list.append(po_map + "\n")

					if "Lang" in map_name:
						not_lang_map = f"Not_{map_name}"
						second_po_map = generate_constant(node, not_lang_map)
						item_RML_list.append(second_po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)
					if constant_only_test(node_list, predicate_name) == True:
						if predicate_name != "contribution":
							bnode_map_name = f"Constant_{predicate_name.capitalize()}_{property_number}_"

					generate_new_bnode_po_map = False
					generate_new_logical_source = False
					generate_new_subject_map = False

					if map_name in item_bnode_po_dict.keys():
						if bnode_map_name not in item_bnode_po_dict[map_name]:
							generate_new_bnode_po_map = True
					else:
						generate_new_bnode_po_map = True

					if bnode_map_name not in item_logsource_subject_list:
						generate_new_logical_source = True
						generate_new_subject_map = True

					if generate_new_bnode_po_map == True:
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						item_RML_list.append(bnode_po_map + "\n")

						if "Lang" in map_name:
							not_lang_map_name = f"Not_{map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, not_lang_map_name)
							item_RML_list.append(second_bnode_po_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map_name = f"Not_{bnode_map_name}"
							second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, map_name)
							item_RML_list.append(second_bnode_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_bnode_po_map = generate_bnode_po_map(predicate_name, not_lang_bnode_map_name, not_lang_map_name)
								item_RML_list.append(second_bnode_po_map + "\n")

					if map_name not in item_bnode_po_dict.keys():
						item_bnode_po_dict[map_name] = []
					item_bnode_po_dict[map_name].append(bnode_map_name)

					if generate_new_logical_source == True:
						if "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							item_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Classification_Lcc_":
							logical_source = generate_classification_logical_source(bnode_map_name, default_path)
							item_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Classification_Nlm_":
							logical_source = generate_classification_logical_source(bnode_map_name, default_path)
							item_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							item_RML_list.append(logical_source + "\n")
						elif bnode_map_name in nosplit_bnode_list:
							logical_source = generate_lang_nosplit_logical_source(bnode_map_name, default_path, property_number)
							item_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_nosplit_logical_source(not_lang_bnode_map_name, default_path, property_number)
								item_RML_list.append(second_logical_source + "\n")
						elif "Constant_" in bnode_map_name:
							logical_source = generate_constant_logical_source(bnode_map_name, default_path, property_number)
							item_RML_list.append(logical_source + "\n")
						elif "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							item_RML_list.append(logical_source + "\n")
						elif property_number in no_language_tag_list: # the blank node takes a literal, lang tag doesn't matter
							logical_source = generate_neutral_literal_logical_source(bnode_map_name, default_path, property_number)
							item_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal, lang tag does matter
							logical_source = generate_lang_logical_source(bnode_map_name, default_path, property_number)
							item_RML_list.append(logical_source + "\n")

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								second_logical_source = generate_not_lang_logical_source(not_lang_bnode_map_name, default_path, property_number)
								item_RML_list.append(second_logical_source + "\n")

						item_logsource_subject_list.append(bnode_map_name)

					if generate_new_subject_map == True:
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						item_RML_list.append(subject_map + "\n")

						if "Lang" in bnode_map_name:
							not_lang_bnode_map = f"Not_{bnode_map_name}"
							second_subject_map = generate_bnode_subject_map(not_lang_bnode_map_name, class_name)
							item_RML_list.append(second_subject_map + "\n")

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = item_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					item_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						item_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if map_name == default_map:
							if property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")
						elif map_name == "Title_":
							literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
							item_RML_list.append(literal_po_map + "\n")
						elif map_name == "Classification_Lcc_":
							literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
							item_RML_list.append(literal_po_map + "\n")
						elif map_name == "Classification_Nlm_":
							literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
							item_RML_list.append(literal_po_map + "\n")
						elif map_name in nosplit_bnode_list:
							literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
							item_RML_list.append(literal_po_map + "\n")
						elif property_number in no_language_tag_list:
							literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
							item_RML_list.append(literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
								item_RML_list.append(second_literal_po_map + "\n")
						else:
							lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
							item_RML_list.append(lang_literal_po_map + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
								item_RML_list.append(not_lang_literal_po_map + "\n")

					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if map_name == default_map:
								if property_number in no_language_tag_list:
									literal_po_map = generate_neutral_literal_po_main_map(node, map_name, property_number)
									item_RML_list.append(literal_po_map + "\n")
								else:
									literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
									item_RML_list.append(literal_po_map + "\n")
							elif map_name == "Title_":
								literal_po_map = generate_langnotlang_literal_po_main_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")
							elif map_name == "Classification_Lcc_":
								literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")
							elif map_name == "Classification_Nlm_":
								literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")
							elif map_name in nosplit_bnode_list:
								literal_po_map = generate_neutral_literal_nosplit_po_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")
							elif property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
								item_RML_list.append(literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
									item_RML_list.append(second_literal_po_map + "\n")
							else:
								lang_literal_po_map = generate_lang_literal_split_po_map(node, map_name)
								item_RML_list.append(lang_literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									not_lang_literal_po_map = generate_not_lang_literal_split_po_map(node, not_lang_map_name)
									item_RML_list.append(not_lang_literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/itemRML.ttl", "w") as output_file:
	for code in item_RML_list:
		output_file.write(code)
