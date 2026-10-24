================================================================
  WiFiMonitor — KURULUM VE KULLANIM KILAVUZU
  Windows 10 / 11 icin, EXE haline getirme dahil
================================================================


================================================================
  BOLUM 1 — GEREKSINIMLER
================================================================

Kuruluma baslamadan once iki sey kurulu olmali:

  [1] Python 3.10 veya uzeri
  [2] Npcap (ag paketi okumak icin surucu)

Kontrol etmek icin:

  1. Windows tusu -> "cmd" yaz -> Enter
  2. Su komutu calistir:

       py --version

  3. Cikti "Python 3.12.x" gibi bir seyse Python kurulu.
     "'py' is not recognized" hatasi alirsan -> BOLUM 2'ye gec.
     Surum goruyorsan -> BOLUM 3'e gec (Npcap).


================================================================
  BOLUM 2 — PYTHON KURULUMU (sadece Python yoksa)
================================================================

  1. Tarayicida su adrese git:
       https://www.python.org/downloads/

  2. Sari renkli "Download Python 3.12.x" butonuna bas.

  3. Indirilen dosyayi calistir.

  4. ONEMLI: Kurulum ekraninin ALTINDA
     "Add Python to PATH" kutusunu isaretle.
     Bu kutu isaretli olmazsa program calismaz.

  5. "Install Now" butonuna bas, bekle.

  6. Kurulum bitince bilgisayari yeniden baslat.

  7. CMD'de tekrar kontrol et:
       py --version

     Surum gorunduyse tamam. Gormediysen Python'u
     kaldir, 1. adimdan tekrar kur. "Add to PATH"
     kutusunu bu sefer kacirma.


================================================================
  BOLUM 3 — NPCAP KURULUMU
================================================================

Npcap, Python'un ag paketlerini okuyabilmesi icin
gereken surucudur. BU ADIM ATLANAMAZ.

  1. Tarayicida:
       https://npcap.com/#download

  2. "Download Npcap 1.79 installer" (veya en son surum)
     butonuna bas.

  3. Indirilen dosyayi calistir.

  4. Kurulum ekraninda:
       [x] "Install Npcap in WinPcap API-compatible Mode"
     Kutusunu MUTLAKA isaretle.
     Diger ayarlara dokunma.

  5. "Install" -> "Finish".

  6. Bilgisayari yeniden baslat.

Not: Npcap olmadan program acilsa bile tarama
     calismaz, "Npcap bulunamadi" hatasi verir.


================================================================
  BOLUM 4 — KAYNAK KODU INDIR
================================================================

  1. GitHub repo sayfasina git (sana verilen link).

  2. Sag ustteki yesil "<> Code" butonuna bas.

  3. "Download ZIP" sec.

  4. Indirilen "WiFiMonitor-main.zip" dosyasina
     sag tik -> "Tumunu ayikla".

  5. Cikan klasoru ac. Icinde "wifimon_gui.py" var.

  6. Bu klasoru C:\Users\Tuna\Downloads altina tasi
     (ya da nerede duruyorsa orada birak, yol onemli degil).


================================================================
  BOLUM 5 — KUTUPHANELERI KUR (tek seferlik)
================================================================

  1. CMD ac.

  2. Klasorunun icine gir. Ornek:

       cd C:\Users\%USERNAME%\Downloads\WiFiMonitor-main

     (%USERNAME% yerine kendi kullanici adin yazili olmali,
      CMD otomatik doldurur, aynen yapistir.)

  3. Su komutu tek satir olarak calistir:

       py -m pip install PyQt6 scapy hostlens etherlyzer pyinstaller

  4. 1-2 dakika bekle. "Successfully installed ..."
     gorursen tamam.

  Hata alirsan once pip'i guncelle:

       py -m pip install --upgrade pip

  Sonra 3. adimi tekrar calistir.


================================================================
  BOLUM 6 — PYTHON ILE TEST ET (EXE'DEN ONCE)
================================================================

  1. Ayni CMD penceresinde:

       py wifimon_gui.py

  2. UAC onay penceresi acilir -> "Evet" de.

  3. Program penceresi acildi mi?
       ACILDI  -> BOLUM 7'ye gec (exe yap).
       ACILMADI -> BOLUM 10'a bak (sorun giderme).


================================================================
  BOLUM 7 — EXE HALINE GETIR
================================================================

  1. Ayni CMD'de, ayni klasorde:

       py -m PyInstaller --onefile --windowed --uac-admin --hidden-import=scapy --hidden-import=scapy.all --hidden-import=scapy.arch.windows --hidden-import=scapy.layers.all --hidden-import=scapy.layers.inet --hidden-import=scapy.layers.l2 --hidden-import=scapy.layers.dns --hidden-import=hostlens --hidden-import=etherlyzer --name WiFiMonitor wifimon_gui.py

  2. 1-2 dakika bekle. Bircok INFO satiri akar, normal.

  3. Bittiginde klasorde "dist" adinda bir klasor olusur.

  4. Icine gir: "WiFiMonitor.exe" dosyasi orada.

  5. WiFiMonitor.exe dosyasina sag tik -> Kopyala.

  6. Masaustune sag tik -> Yapistir.

  7. Masaustundeki WiFiMonitor.exe'ye sag tik ->
     "Yonetici olarak calistir" -> "Evet".


================================================================
  BOLUM 8 — HER SEFERINDE YONETICI IZNI ISTEYMESIN
================================================================

  (Opsiyonel, tek seferlik ayar)

  1. Masaustundeki WiFiMonitor.exe'ye sag tik -> Ozellikler.

  2. "Uyumluluk" sekmesine gec.

  3. En alttaki "Bu programi yonetici olarak calistir"
     kutusunu isaretle.

  4. "Uygula" -> "Tamam".

  Bundan sonra cift tiklamak yeterli, UAC sormaz.


================================================================
  BOLUM 9 — PROGRAMI KULLANMA
================================================================

Program acildiginda 3 adim:

  ADIM 1 — Adaptor sec
  --------------------
  En ustteki "Adaptor" acilir listesinden internete
  bagli Wi-Fi adaptorunu sec.
  Genelde "Wi-Fi" veya "WLAN" yazar.
  Emin degilsen: CMD'de "ipconfig" calistir, aktif
  adaptorun adini gor.

  ADIM 2 — Agi tara
  -----------------
  "Gateway" kutusu otomatik dolar. Dokunma.
  (Yanlissa: ipconfig -> "Default Gateway" satirindaki
   IP'yi kopyala, kutuya yapistir.)

  "Agi Tara" butonuna bas.
  3-5 saniye bekle.

  Tabloda cihazlar belirir:
     IP       MAC              Uretici      Model
     192.168.1.42  a4:50:46:...  Samsung    Galaxy S23
     192.168.1.55  3c:5a:b4:...  Apple      iPhone
     192.168.1.88  b0:be:76:...  TP-Link    Router

  ADIM 3A — Trafigi izle
  ----------------------
  "Izlemeyi Baslat" butonuna bas.
  Alt taraftaki siyah kutuda cihazlarin hangi siteye
  gittigi akmaya baslar:

     [DNS] 192.168.1.42 -> google.com
     [TLS] 192.168.1.42 -> youtube.com
     [TLS] 192.168.1.55 -> instagram.com
     [HTTP] 192.168.1.88 GET /index.html

  Durmak icin "Izlemeyi Durdur".

  ADIM 3B — Bir cihazin internetini kes
  -------------------------------------
  1. Tablodan cihazi sec (satira tikla).
  2. "Secili Cihazi At" butonuna bas.
  3. Cihazin interneti kesilir.

  Geri acmak icin: "Atmayi Durdur" butonuna bas.
  Cihaz 5-10 saniye icinde yeniden baglanir.

  Tum cihazlari birden atmak icin: "Tumunu At".


================================================================
  BOLUM 10 — SORUN GIDERME
================================================================

  SORUN: "'py' is not recognized"
  COZUM: Python PATH'te degil.
         Python'u kaldir, tekrar kur,
         "Add Python to PATH" kutusunu isaretle,
         bilgisayari yeniden baslat.

  SORUN: "Npcap bulunamadi"
  COZUM: Npcap kurulu degil veya yanlis modda.
         npcap.com'dan tekrar kur,
         "WinPcap API-compatible Mode" isaretli olsun,
         bilgisayari yeniden baslat.

  SORUN: "scapy bulunamadi"
  COZUM: py -m pip install scapy

  SORUN: "PyQt6 bulunamadi"
  COZUM: py -m pip install PyQt6

  SORUN: EXE'ye cift tikliyorum, bir sey olmuyor
  COZUM: CMD'den calistir, hatayi oku:
         cd C:\Users\%USERNAME%\Downloads\dist
         WiFiMonitor.exe

  SORUN: "Agi Tara"ya basinca program donuyor
  COZUM: Kaynak kod eski surum. GitHub'dan tekrar indir,
         yeni surumde tarama arka planda calisir.

  SORUN: Cihazlar taranmiyor, tablo bos
  COZUM: 1. Dogru adaptoru sectiginden emin ol.
         2. Modemde "AP isolation" / "client isolation"
            ayari aciksa kapat.
         3. Gateway IP'yi ipconfig ile kontrol et.

  SORUN: "Gateway MAC bulunamadi"
  COZUM: Gateway IP yanlis. ipconfig calistir,
         "Default Gateway" satirindaki IP'yi kutuya gir.

  SORUN: Cihaz atilmiyor, internet kesilmiyor
  COZUM: 1. Programi yonetici olarak calistir.
         2. Modemde statik ARP binding kapali olmali.
         3. Hedef cihaz Wi-Fi'da mi, kontrol et.

  SORUN: Windows Defender exe'yi siliyor
  COZUM: Windows Guvenlik -> Virus ve tehdit korumasi
         -> Ayarlari yonet -> Dislamalar -> Dislama ekle
         -> Klasor -> "dist" klasorunu sec.

  SORUN: "An administrator is required" hatasi
  COZUM: Sag tik -> "Yonetici olarak calistir".


================================================================
  BOLUM 11 — ONEMLI NOTLAR
================================================================

  - HTTPS icerigi gorunmez. Sadece site adi (domain)
    gorunur. Sayfa icerigi, mesajlar, form verileri
    sifreli oldugu icin okunamaz.

  - Bazi Android (10+) ve iOS (14+) cihazlar rastgele
    MAC kullanir. Bu durumda uretici "?" gorunebilir.

  - Bazi modemlerde "client isolation" aciksa cihazlar
    birbirini goremez. Modem arayuzunden kapat.

  - Program sadece kendi cihazini hedef listesinden
    cikarmaz; kendi internetini kesmez.

  - Atma islemi sirasinda cihaz internete cikamaz.
    "Atmayi Durdur" deyince ARP tablosu duzelir,
    cihaz yeniden baglanir.

  - Bu program sadece kendi aginda ve yetkili
    oldugun cihazlarda kullanilmak icindir.
    Baskasinin aginda kullanmak TCK 243/244
    kapsaminda suctur.


================================================================
  BOLUM 12 — HIZLI OZET (ezber)
================================================================

  Kurulum sirasi:
    1. Python kur (Add to PATH isaretle)
    2. Npcap kur (WinPcap modu isaretle)
    3. Bilgisayari yeniden baslat
    4. Kodu indir, klasore cikar
    5. py -m pip install PyQt6 scapy hostlens etherlyzer pyinstaller
    6. py wifimon_gui.py         (test)
    7. PyInstaller komutu        (exe)
    8. dist\WiFiMonitor.exe'yi masaustune tasi
    9. Sag tik -> Yonetici olarak calistir

  Kullanim:
    1. Adaptor sec
    2. Agi Tara
    3. Izlemeyi Baslat  (izlemek icin)
       Secili Cihazi At  (kesmek icin)
       Atmayi Durdur     (geri acmak icin)


================================================================
  SON
================================================================

Takildigin yer olursa BOLUM 10'a bak.
Hala cozulmediyse hata mesajini kopyala, bana yolla.
