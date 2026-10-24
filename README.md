# WifiMonit-r
With this program, you can identify the makes and models of devices connected to your Wi-Fi network, as well as the websites they visit; furthermore, you can slow down the internet access of any specific device without disconnecting it from the network.


# WiFiMonitor

Windows üzerinde çalışan, ağdaki cihazları keşfeden, hangi sitelere gittiklerini izleyen ve seçili cihazın internet bağlantısını ARP spoofing ile kesen bir masaüstü aracı.

> **Uyarı:** Bu araç yalnızca **kendi ağınızda** ve **yetkili olduğunuz cihazlarda** kullanılmak üzere tasarlanmıştır. Başkasının ağında veya izinsiz cihazlarda kullanmak yasalara aykırıdır. Tüm sorumluluk kullanıcıya aittir.

---

## Özellikler

- **Cihaz Keşfi:** ARP taraması ile ağdaki tüm canlı cihazları listeler (IP + MAC).
- **Marka/Model Tespiti:** MAC OUI, mDNS, UPnP ve SSDP üzerinden cihaz üreticisi ve modelini tespit eder.
- **Trafik İzleme:** DNS sorguları, HTTP Host başlıkları ve TLS SNI üzerinden hangi cihazın hangi siteye gittiğini gösterir.
- **İnternet Kesme:** ARP spoofing ile seçili cihazın veya tüm cihazların internet bağlantısını keser.
- **Modern Arayüz:** PyQt6 ile koyu temalı, tablo tabanlı kullanıcı dostu arayüz.
- **Otomatik ARP Restore:** Atma işlemi durdurulduğunda ARP tabloları otomatik olarak geri yüklenir.

---

## Gereksinimler

| Bileşen | Sürüm | Not |
|---|---|---|
| Windows | 10 / 11 | Yönetici yetkisi gerekli |
| Python | 3.10+ | [python.org](https://python.org) |
| Npcap | 1.70+ | [npcap.com](https://npcap.com) — kurulumda "WinPcap API-compatible Mode" işaretli olmalı |
| PyQt6 | 6.x | `pip install PyQt6` |
| scapy | 2.5+ | `pip install scapy` |
| hostlens | son sürüm | `pip install hostlens` |
| etherlyzer | son sürüm | `pip install etherlyzer` |

---

## Kurulum

### 1. Npcap kurulumu

1. [npcap.com](https://npcap.com) adresinden en son sürümü indir.
2. Kurulum ekranında **"Install Npcap in WinPcap API-compatible Mode"** kutusunu işaretle.
3. Kurulumu bitir, bilgisayarı yeniden başlat.

Npcap olmadan Python ağ paketlerini okuyamaz.

### 2. Python kütüphaneleri

CMD aç ve şunu çalıştır:

```bat
py -m pip install PyQt6 scapy hostlens etherlyzer pyinstaller
