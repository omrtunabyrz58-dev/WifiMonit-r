╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              W I F I M O N I T O R                           ║
║                                                              ║
║              Kurulum ve Kullanım Kılavuzu                    ║
║                                                              ║
║              Windows 10 / 11 için                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📌 BU KILAVUZ NE ANLATIYOR?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Bu dosya, WiFiMonitor programını sıfırdan kurmayı,
  çalıştırmayı ve kullanmayı adım adım anlatır.

  Hiç bilmeyen biri bile takip edebilir. Sırayla git,
  hiçbir adımı atlama.

  ⏱  Toplam süre: 10-15 dakika
  📦  Kurulacak: Python + Npcap + 5 kütüphane
  💻  Sonuç: Masaüstünde çift tıklanabilir bir .exe


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔍 ADIM 0 — PYTHON KURULU MU KONTROL ET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ① Windows tuşuna bas, "cmd" yaz, Enter'a bas.
     Siyah bir pencere açılır. Buna "komut istemi" denir.

  ② Şu komutu yaz, Enter'a bas:

       py --version

  ③ Sonuç ne oldu?

     ✅ "Python 3.12.x" gibi bir şey yazdıysa
        → Python zaten kurulu. ADIM 2'ye atla.

     ❌ "'py' is not recognized" gibi bir hata yazdıysa
        → Python yok. ADIM 1'e geç.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🐍 ADIM 1 — PYTHON KUR (Python yoksa)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ① Tarayıcıyı aç, şu adrese git:

       https://www.python.org/downloads/

  ② Büyük SARI butona bas: "Download Python 3.12.x"

  ③ İndirilen dosyayı çift tıkla, kurulumu başlat.

  ④ ⚠️ ÇOK ÖNEMLİ:
     Kurulumun İLK ekranında, en altta şu kutu var:
     
         ☐ Add Python to PATH
     
     Bu kutuyu MUTLAKA işaretle (✓ yap).
     
     İşaretlemezsen program çalışmaz. Bu, en sık
     yapılan hatadır.

  ⑤ "Install Now" butonuna bas, bekle.

  ⑥ Kurulum bitince bilgisayarı yeniden başlat.

  ⑦ CMD'yi tekrar aç, kontrol et:

       py --version

     ✅ Sürüm göründüyse → ADIM 2'ye geç.
     ❌ Hâlâ hata veriyorsa → Python'u kaldır,
        ④. adımdaki "Add to PATH" kutusunu işaretleyerek
        tekrar kur.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌐 ADIM 2 — NPCAP KUR (zorunlu!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Npcap, programın ağdaki cihazları görmesini sağlayan
  bir sürücüdür. BU ADIM ATLANAMAZ.

  ① Tarayıcıda:

       https://npcap.com/#download

  ② "Download Npcap 1.79 installer" butonuna bas.

  ③ İndirilen dosyayı çalıştır.

  ④ ⚠️ Kurulum ekranında şu kutuyu MUTLAKA işaretle:

         ☑ Install Npcap in WinPcap API-compatible Mode

     Diğer ayarlara dokunma.

  ⑤ "Install" → "Finish".

  ⑥ Bilgisayarı yeniden başlat.

  💡 Npcap olmadan program açılır ama "cihazları
     tarayamaz". "Npcap bulunamadı" hatası verir.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📥 ADIM 3 — PROGRAMI İNDİR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ① GitHub'da repo sayfasına git (sana verilen link).

  ② Sağ üstteki YEŞİL "<> Code" butonuna bas.

  ③ "Download ZIP" seç.

  ④ İndirilen "WiFiMonitor-main.zip" dosyasına
     SAĞ TIK → "Tümünü ayıkla".

  ⑤ Çıkan klasörün içinde "wifimon_gui.py" dosyası var.
     Bu klasörü açık tut, birazdan kullanacağız.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📚 ADIM 4 — KÜTÜPHANELERİ KUR (tek seferlik)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ① CMD aç.

  ② Programın olduğu klasöre gir. Örnek:

       cd C:\Users\%USERNAME%\Downloads\WiFiMonitor-main

     (%USERNAME% CMD tarafından otomatik doldurulur,
      aynen yapıştır.)

  ③ Şu komutu TEK SATIR olarak yapıştır, Enter:

       py -m pip install PyQt6 scapy hostlens etherlyzer pyinstaller

  ④ 1-2 dakika bekle. Bir sürü metin akar, normal.

  ⑤ En sonda şunu görürsen TAMAM:

       Successfully installed ...

  ❌ Hata alırsan, önce şunu çalıştır:

       py -m pip install --upgrade pip

     Sonra ③. adımı tekrar dene.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ▶️  ADIM 5 — PROGRAMI TEST ET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ① Aynı CMD penceresinde:

       py wifimon_gui.py

  ② Ekranda mavi bir "İzin ver" penceresi çıkar
     (UAC onayı). "Evet" butonuna bas.

  ③ Program penceresi açıldı mı?

     ✅ AÇILDI → ADIM 6'ya geç (exe yap).
     ❌ AÇILMADI → KILAVUZUN EN ALTINDAKİ
                    "SORUN GİDERME" bölümüne bak.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📦 ADIM 6 — EXE HALİNE GETİR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Bu adım, programı tek dosya haline getirir.
  Bir daha CMD açmana gerek kalmaz, çift tıklarsın.

  ① CMD'de, aynı klasörde, şu komutu TEK SATIR
     olarak yapıştır, Enter:

       py -m PyInstaller --onefile --windowed --uac-admin --hidden-import=scapy --hidden-import=scapy.all --hidden-import=scapy.arch.windows --hidden-import=scapy.layers.all --hidden-import=scapy.layers.inet --hidden-import=scapy.layers.l2 --hidden-import=scapy.layers.dns --hidden-import=hostlens --hidden-import=etherlyzer --name WiFiMonitor wifimon_gui.py

  ② 1-2 dakika bekle. Bir sürü "INFO" satırı akar,
     normal. Panik yapma.

  ③ Bitince klasörde "dist" adında yeni bir klasör
     oluşur.

  ④ "dist" klasörüne gir. İçinde:

       WiFiMonitor.exe

     İşte bu senin programın.

  ⑤ WiFiMonitor.exe'ye SAĞ TIK → Kopyala.

  ⑥ Masaüstüne SAĞ TIK → Yapıştır.

  ⑦ Masaüstündeki WiFiMonitor.exe'ye SAĞ TIK →
     "Yönetici olarak çalıştır" → "Evet".

  🎉 TEBRİKLER! Programın hazır. Masaüstünde duruyor.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚙️  ADIM 7 — HER SEFERİNDE İZİN İSTEMESİN (opsiyonel)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Bunu yaparsan, bir daha "Yönetici olarak çalıştır"
  demene gerek kalmaz. Çift tıklamak yeter.

  ① Masaüstündeki WiFiMonitor.exe'ye SAĞ TIK →
     "Özellikler".

  ② "Uyumluluk" sekmesine geç.

  ③ En alttaki şu kutuyu işaretle:

       ☑ Bu programı yönetici olarak çalıştır

  ④ "Uygula" → "Tamam".


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎮 ADIM 8 — PROGRAMI KULLANMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Program açıldığında üstte iki kutu, ortada bir tablo,
  altta siyah bir log alanı görürsün.

  ┌──────────────────────────────────────────────────────────┐
  │  ADIM A: Adaptör seç                                     │
  └──────────────────────────────────────────────────────────┘

     En üstteki "Adaptör" açılır listesinden internete
     bağlı Wi-Fi adaptörünü seç.

     Genelde "Wi-Fi" veya "WLAN" yazar.

     Emin değilsen: CMD'de "ipconfig" çalıştır,
     aktif olan adaptörün adını orada görürsün.

  ┌──────────────────────────────────────────────────────────┐
  │  ADIM B: Ağı tara                                        │
  └──────────────────────────────────────────────────────────┘

     "Gateway" kutusu otomatik dolar. DOKUNMA.

     "Ağı Tara" butonuna bas. 3-5 saniye bekle.

     Tabloda cihazlar belirir:

       ┌──────────────┬──────────────────┬─────────┬───────────┐
       │ IP           │ MAC              │ Üretici │ Model     │
       ├──────────────┼──────────────────┼─────────┼───────────┤
       │ 192.168.1.42 │ a4:50:46:...     │ Samsung │ Galaxy S23│
       │ 192.168.1.55 │ 3c:5a:b4:...     │ Apple   │ iPhone    │
       │ 192.168.1.88 │ b0:be:76:...     │ TP-Link │ Router    │
       └──────────────┴──────────────────┴─────────┴───────────┘

  ┌──────────────────────────────────────────────────────────┐
  │  ADIM C: Ne yapmak istiyorsun?                           │
  └──────────────────────────────────────────────────────────┘

     🔍 İZLEMEK İSTİYORSAN:

        "İzlemeyi Başlat" butonuna bas.

        Alt taraftaki siyah kutuda cihazların hangi
        siteye gittiği akmaya başlar:

           [DNS] 192.168.1.42 -> google.com
           [TLS] 192.168.1.42 -> youtube.com
           [TLS] 192.168.1.55 -> instagram.com

        Durdurmak için: "İzlemeyi Durdur".

     ✂️ İNTERNETİNİ KESMEK İSTİYORSAN:

        ① Tablodan cihaza tıkla (satır seçilir).
        ② "Seçili Cihazı At" butonuna bas.
        ③ Cihazın interneti kesilir.

        Geri açmak için: "Atmayı Durdur".
        Cihaz 5-10 saniye içinde yeniden bağlanır.

     💥 TÜM CİHAZLARI ATMAK İSTİYORSAN:

        "Tümünü At" butonuna bas.
        Onay penceresinde "Evet" de.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠️  ÖNEMLİ BİLGİLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🔒 HTTPS İÇERİĞİ GÖRÜNMEZ
     Sadece site adı (google.com gibi) görünür.
     Sayfa içeriği, mesajlar, form verileri şifreli
     olduğu için okunamaz. Bu, modern şifrelemenin
     doğal sınırıdır.

  📱 MAC ADRESİ DEĞİŞEBİLİR
     Bazı Android (10+) ve iOS (14+) cihazlar Wi-Fi'da
     rastgele MAC kullanır. Bu durumda "Üretici"
     sütununda "?" görünebilir. Normal.

  🌐 CLIENT ISOLATION
     Bazı modemlerde "AP isolation" veya "client
     isolation" açıksa cihazlar birbirini göremez.
     Modem arayüzünden kapat.

  🎯 KENDİ İNTERNETİN KESİLMEZ
     Program sadece seçili hedef cihazı keser.
     Kendi bilgisayarını hedef listesinden çıkarır.

  ⚖️  SADECE KENDİ AĞINDA KULLAN
     Bu program kendi ağında ve yetkili olduğun
     cihazlarda kullanılmak içindir. Başkasının
     ağında kullanmak TCK 243/244 kapsamında suçtur.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔧 SORUN GİDERME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ❌ "'py' is not recognized"
  ✅ Python PATH'te değil.
     → Python'u kaldır, tekrar kur.
     → "Add Python to PATH" kutusunu işaretle.
     → Bilgisayarı yeniden başlat.

  ❌ "Npcap bulunamadı"
  ✅ Npcap kurulu değil veya yanlış modda.
     → npcap.com'dan indir.
     → "WinPcap API-compatible Mode" işaretle.
     → Bilgisayarı yeniden başlat.

  ❌ "scapy bulunamadı"
  ✅ Kütüphane eksik.
     → py -m pip install scapy

  ❌ "PyQt6 bulunamadı"
  ✅ Kütüphane eksik.
     → py -m pip install PyQt6

  ❌ EXE'ye çift tıklıyorum, hiçbir şey olmuyor
  ✅ Hata gizlenmiş olabilir. CMD'den çalıştır:
     → cd C:\Users\%USERNAME%\Downloads\dist
     → WiFiMonitor.exe
     → Çıkan hata mesajını oku.

  ❌ "Ağı Tara"ya basınca program donuyor
  ✅ Eski sürüm kullanıyorsun.
     → GitHub'dan en son sürümü indir.
     → Yeni sürümde tarama arka planda çalışır,
        program donmaz.

  ❌ Cihazlar taranmıyor, tablo boş
  ✅ 1. Doğru adaptörü seçtiğinden emin ol.
     2. Modemde client isolation açıksa kapat.
     3. Gateway IP'yi ipconfig ile kontrol et.

  ❌ "Gateway MAC bulunamadı"
  ✅ Gateway IP yanlış.
     → CMD'de ipconfig çalıştır.
     → "Default Gateway" satırındaki IP'yi kopyala.
     → Kutuya yapıştır.

  ❌ Cihaz atılmıyor, internet kesilmiyor
  ✅ 1. Programı YÖNETİCİ olarak çalıştır.
     2. Modemde statik ARP binding kapalı olmalı.
     3. Hedef cihaz Wi-Fi'da mı, kontrol et.

  ❌ Windows Defender exe'yi siliyor
  ✅ İmzasız exe'lerde sık görülür.
     → Windows Güvenlik → Virüs ve tehdit koruması
     → Ayarları yönet → Dışlamalar → Dışlama ekle
     → Klasör → "dist" klasörünü seç.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 HIZLI ÖZET (ezber kartı)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  KURULUM (sırayla):

    1. Python kur  →  "Add to PATH" işaretle ✓
    2. Npcap kur   →  "WinPcap modu" işaretle ✓
    3. Bilgisayarı yeniden başlat
    4. Kodu indir, klasöre çıkar
    5. py -m pip install PyQt6 scapy hostlens etherlyzer pyinstaller
    6. py wifimon_gui.py              ← test
    7. PyInstaller komutu             ← exe üret
    8. dist\WiFiMonitor.exe'yi masaüstüne kopyala
    9. Sağ tık → Yönetici olarak çalıştır

  KULLANIM (3 adım):

    1. Adaptör seç
    2. Ağı Tara
    3. İzle / At / Durdur


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🆘 TAKILDIN MI?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Önce yukarıdaki "SORUN GİDERME" bölümüne bak.

  Hâlâ çözülmediyse:
    → Hata mesajını kopyala
    → Hangi adımda takıldığını yaz
    → Bana gönder

  Her sorunun bir çözümü var. Pes etme.

╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    KOLAY GELSİN! 🚀                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝





NOT:Bu wifi monitör programı ai ile yapılmıştır
