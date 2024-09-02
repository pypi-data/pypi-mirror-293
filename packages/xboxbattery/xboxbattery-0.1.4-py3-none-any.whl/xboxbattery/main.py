import subprocess, glob

from PySide6 import QtDBus
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtCore import SLOT, QTimer, Slot

class Config:
    SERVICE = "org.freedesktop.UPower"
    PATH = "/org/freedesktop/UPower"
    INTERFACE = "org.freedesktop.UPower"
    DEVICE_INTERFACE = "org.freedesktop.UPower.Device"

    @classmethod
    def default(cls):
        return cls.SERVICE, cls.PATH, cls.INTERFACE

    @classmethod
    def device(cls, path):
        return cls.SERVICE, path, cls.DEVICE_INTERFACE

class App(QApplication):
    def __init__(self):
        super().__init__()
        self.connection = QtDBus.QDBusConnection.systemBus()
        self.interface = QtDBus.QDBusInterface(*Config.default(), self.connection)
        self.tray = QSystemTrayIcon()

        self.icon = QIcon.fromTheme(QIcon.ThemeIcon.InputGaming)
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.no_devices = QAction("No devices found")
        self.quit_action = QAction("Quit")

        self.devices = []

        self.menu = QMenu()
        self.tray.setContextMenu(self.menu)

        self.connection.connect(*Config.default(), "DeviceAdded", self, SLOT("build_menu()"))
        self.connection.connect(*Config.default(), "DeviceRemoved", self, SLOT("build_menu()"))

        self.timer = QTimer()
        self.timer.timeout.connect(self.build_menu)
        self.timer.start(15000)

        self.build_menu()

    def enumerate_devices(self):
        reply = QtDBus.QDBusReply(self.interface.call("EnumerateDevices"))

        device_paths = []
        if reply.isValid():
            devices = reply.value()
            devices.beginArray()
            while not devices.atEnd():
                device = QtDBus.QDBusObjectPath()
                devices >> device
                device_paths.append(device.path())
            devices.endArray()

        return device_paths

    @Slot()
    def build_menu(self):
        self.menu.clear()

        paths = self.enumerate_devices()
        for path in paths:
            device = Device(path)
            device.connect(self.connection)
            self.devices.append(device)
            self.menu.addAction(device.action)

        if not paths:
            self.no_devices.setEnabled(False)
            self.menu.addAction(self.no_devices)

        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)
        self.quit_action.triggered.connect(self.quit)

class Device:
    def __init__(self, path):
        self.path = path
        self.gip = self.path.split("/")[-1].split("_")[-1].replace("x", ".")
        self.interface = None
        self.action = None

    def property(self, prop):
        if not self.interface:
            return None
        return self.interface.property(prop)

    def blink_led(self):
        self.set_led(3)
        QTimer.singleShot(3000, lambda: self.set_led(1))

    def set_led(self, signal):
        targets = glob.glob(f"/sys/class/leds/{self.gip}:*:status/mode")
        for target in targets:
            subprocess.Popen(f"echo {signal} > {target}", shell=True)

    def connect(self, connection):
        self.interface = QtDBus.QDBusInterface(*Config.device(self.path), connection)
        self.build_action()

    def build_action(self):
        self.action = QAction(f"{self.property("Model")} ({self.property("Percentage")}%)")
        self.action.triggered.connect(self.blink_led)

def main():
    app = App()
    app.exec()
