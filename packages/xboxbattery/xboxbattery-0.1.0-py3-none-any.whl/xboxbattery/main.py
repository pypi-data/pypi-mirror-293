import time
import subprocess
import glob

from PySide6 import QtDBus
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtCore import QTimer, SLOT, Slot, QThreadPool

SERVICE = "org.freedesktop.UPower"
PATH = "/org/freedesktop/UPower"
INTERFACE = "org.freedesktop.UPower"
DEVICE_INTERFACE = "org.freedesktop.UPower.Device"

class App(QApplication):
    def __init__(self):
        super().__init__()
        self.connection = QtDBus.QDBusConnection.systemBus()
        self.interface = QtDBus.QDBusInterface(SERVICE, PATH, INTERFACE, self.connection)
        self.tray = QSystemTrayIcon()

        self.icon = QIcon.fromTheme(QIcon.ThemeIcon.InputGaming)
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = Menu(self)
        self.menu.quit_action.triggered.connect(self.quit)

        self.connection.connect(SERVICE, PATH, INTERFACE, "DeviceAdded", self.menu, SLOT("build_menu()"))
        self.connection.connect(SERVICE, PATH, INTERFACE, "DeviceRemoved", self.menu, SLOT("build_menu()"))

        self.timer = QTimer()
        self.timer.timeout.connect(self.menu.build_menu)
        self.timer.start(15000)

        self.tray.setContextMenu(self.menu)

    def enumerate_devices(self):
        res = self.interface.call("EnumerateDevices")
        reply = QtDBus.QDBusReply(res)

        if not reply.isValid():
            return None

        device_paths = []
        devices = reply.value()

        devices.beginArray()
        while not devices.atEnd():
            device = devices.asVariant()
            device_paths.append(device.path())
            devices >> device
        devices.endArray()

        return device_paths

class Menu(QMenu):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.devices = []
        self.no_devices = QAction("No devices found")
        self.quit_action = QAction("Quit")
        self.aboutToShow.connect(self.build_menu)

    @Slot()
    def build_menu(self):
        self.clear()
        self.devices = []

        paths = self.app.enumerate_devices()
        for path in paths:
            device = Device(path)
            device.connect(self.app.connection)

            self.devices.append(device)
            self.addAction(device.action)

        if not paths:
            self.no_devices.setEnabled(False)
            self.addAction(self.no_devices)

        self.addSeparator()
        self.addAction(self.quit_action)

class Device:
    thread_pool = QThreadPool()
    def __init__(self, path):
        self.path = path
        self.interface = None
        self.action = None

    @property
    def gip(self):
        return self.path.split("/")[-1].split("_")[-1].replace("x", ".")

    @property
    def model(self):
        if not self.interface:
            return None
        return self.interface.property("Model")

    @property
    def percentage(self):
        if not self.interface:
            return None
        return self.interface.property("Percentage")

    def _unsafe_identify(self):
        self.set_led(3)
        time.sleep(3)
        self.set_led(1)

    def identify(self):
        self.thread_pool.start(self._unsafe_identify)

    def set_led(self, signal):
        targets = glob.glob(f"/sys/class/leds/{self.gip}:*:status/mode")
        for target in targets:
            subprocess.Popen(f"echo {signal} > {target}", shell=True)

    def connect(self, connection):
        self.interface = QtDBus.QDBusInterface(SERVICE, self.path, DEVICE_INTERFACE, connection)
        self.build_action()

    def build_action(self):
        self.action = QAction(f"{self.model} ({self.percentage}%)")
        self.action.triggered.connect(self.identify)

def main():
    app = App()
    app.exec()
