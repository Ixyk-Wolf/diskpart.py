import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QComboBox, QStyle
import os
import io


class Diskpart:

    def __init__(self):
        if os.name != "nt":
            raise OSError("Only Windows is Supported")
        with open("script.txt", "w+") as f:
            f.write("rescan")
            f.close()

        print("Checking for new disks. . .")
        os.popen("diskpart /s script.txt")
        print("Checking complete.")

    def assign(self, vol_number):
        with open("script.txt", "w+") as f:
            f.write(f"sel vol {vol_number}\nassign")
            f.close()

        return os.popen("diskpart /s script.txt").read()

    def remove(self, vol_number):
        with open("script.txt", "w+") as f:
            f.write(f"sel vol {vol_number}\nremove")
            f.close()

        return os.popen("diskpart /s script.txt").read()

    def fsinfo(self, vol_number):
        with open("script.txt", "w+") as f:
            f.write(f"sel vol {vol_number}\nfilesystems")
            f.close()

        return os.popen("diskpart /s script.txt").read()

    def check_volumes(self):
        with open("script.txt", "w+") as f:
            f.write(f"lis vol")
            f.close()

        return os.popen("diskpart /s script.txt").read()

    def check_drives(self):
        with open("script.txt", "w+") as f:
            f.write(f"lis dis")
            f.close()

        return os.popen("diskpart /s script.txt").read()


part = Diskpart()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QLabel()

    font = QFont("Cascadia Code", 10)

    win.resize(700, 365)
    win.setWindowTitle("Diskpart")


    def refresh_volumes():
        volume_cog = QComboBox(win)
        volume_cog.setFont(font)
        help_vol_label = QLabel(win)
        help_vol_label.setFont(font)
        volumes = part.check_volumes()
        string_volumes = io.StringIO(volumes)
        for line in string_volumes:
            if "Volume" in line and "###" not in line:
                volume_cog.addItem(line)
            elif "###" in line:
                help_vol_label.setText(line)

        return volume_cog, help_vol_label


    def refresh_drives():
        drive_cog = QComboBox(win)
        drive_cog.setFont(font)
        drives = part.check_drives()
        string_drives = io.StringIO(drives)
        help_label = QLabel(win)
        help_label.setFont(font)
        for line in string_drives:
            if "Disk" in line and "###" not in line and "Microsoft" not in line:
                drive_cog.addItem(line)
            elif "###" in line:
                help_label.setText(line)

        return drive_cog, help_label


    assign_button = QPushButton(win)
    assign_button.setText("Assign volume?")
    assign_button.move(25, 60)
    assign_button.resize(150, 25)
    assign_button.show()

    assign_button.setStyleSheet("QPushButton::hover"
                         "{"
                         "background-color : lightblue;"
                         "}")

    remove_button = QPushButton(win)
    remove_button.setText("Remove volume's letter?")
    remove_button.move(200, 60)
    remove_button.resize(225, 25)
    remove_button.show()

    remove_button.setStyleSheet("QPushButton::hover"
                         "{"
                         "background-color : lightblue;"
                         "}")

    fsinfo_button = QPushButton(win)
    fsinfo_button.setText("View filesystem info?")
    fsinfo_button.move(450, 60)
    fsinfo_button.resize(225, 25)

    fsinfo_button.setStyleSheet("QPushButton::hover"
                         "{"
                         "background-color : lightblue;"
                         "}")

    def confirmation(prompt):
        box = QMessageBox(win)
        test = box.question(win, "Diskpart", prompt, box.Yes | box.No)
        if test == box.Yes:
            return True
        else:
            return False


    def assign():
        vol = volume_cog.currentText().replace(" ", "")
        do = confirmation("Are you sure you want to assign a letter to this volume?")
        char = vol[:9]
        if do:
            part.assign("".join(x for x in char if x.isdigit()))


    def remove():
        vol = volume_cog.currentText().replace(" ", "")
        char = vol[:9]
        do = confirmation("Are you sure you want to remove the drive letter from this volume?")
        if do:
            part.remove("".join(x for x in char if x.isdigit()))

    def fsinfo():
        info = volume_cog.currentText().replace(" ", "")
        num = info[:9]
        data = part.fsinfo("".join(x for x in num if x.isdigit()))
        sdata = io.StringIO(data)
        final = ""
        for line in sdata:
            if "Microsoft DiskPart" not in line:
                if "Copyright" not in line:
                    if "On computer" not in line:
                        if "selected volume" not in line:
                            if line.replace(" ", "") != "":
                                final = f"{final}\n{line.strip()}"

        box = QMessageBox(win)
        box.about(win, "Filesystem Information", final)

    remove_button.setFont(font)
    assign_button.setFont(font)
    fsinfo_button.setFont(font)
    remove_button.clicked.connect(remove)
    assign_button.clicked.connect(assign)
    fsinfo_button.clicked.connect(fsinfo)

    volume_cog, help_vol_label = refresh_volumes()
    drive_cog, help_label = refresh_drives()
    help_vol_label.move(23, 0)
    help_vol_label.show()
    drive_cog.move(20, 115)
    drive_cog.show()
    help_label.move(23, 90)
    help_label.show()
    volume_cog.move(20, 25)
    volume_cog.show()
    win.show()
    sys.exit(app.exec_())
