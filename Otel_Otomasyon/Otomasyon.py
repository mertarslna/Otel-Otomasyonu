import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pyodbc

# MSSQL bağlantı ayarları
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-SQOF8L4\\SQLEXPRESS;"
    "DATABASE=Otel;"
    "Trusted_Connection=yes;"
)

# Veritabanı bağlantısını kurma fonksiyonu
def connect_to_db():
    try:
        connection = pyodbc.connect(conn_str)
        print("MSSQL bağlantısı başarılı.")
        return connection
    except Exception as e:
        print("MSSQL bağlantısı başarısız:", e)
        return None


# Yönetici ekleme fonksiyonu
def add_admin(username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO Users (Username, Password) VALUES (?, ?)""", (username, password))
            conn.commit()
            QtWidgets.QMessageBox.information(None, "Başarılı", "Yönetici başarıyla eklendi.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Hata", f"Yönetici eklenirken hata oluştu: {e}")
        finally:
            conn.close()

# Kullanıcı girişi doğrulama fonksiyonu
def validate_admin(username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM Users WHERE Username = ? AND Password = ?""", (username, password))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Giriş doğrulama sırasında hata oluştu: {e}")
        finally:
            conn.close()
    return False


# S plash ekranı
class SplashScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Y&M KONAKLAMA")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2E4053;")  # Arka plan rengi

        # Metin etiketini oluştur
        label = QtWidgets.QLabel("Y&M KONAKLAMA", self)
        label.setAlignment(QtCore.Qt.AlignCenter)

        # Yazı tipi ve stil ayarları
        font = QtGui.QFont("Arial", 48, QtGui.QFont.Bold)
        label.setFont(font)
        label.setStyleSheet("color: #FFFFFF;")  # Yazı rengi

        # Ekranda ortala
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Tam ekran açılmasını sağla
        self.showFullScreen()

        # Zamanlayıcıyı ayarla (2 saniye sonra giriş ekranını açacak)
        QtCore.QTimer.singleShot(2000, self.show_login)

    # Giriş ekranını tam ekran aç
    def show_login(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.showFullScreen()

# Kullanıcı Giriş Penceresi
class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setGeometry(300, 300, 400, 300)

        # Ana düzen (her şeyi ortalamak için QVBoxLayout kullanacağız)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)  # Ana düzeni ortala

        # Başlık etiketini oluştur
        title_label = QtWidgets.QLabel("Kullanıcı Girişi")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E4053;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)  # Başlığı ortala
        main_layout.addWidget(title_label)

        # Form düzeni (Kullanıcı adı ve şifre giriş alanları için)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)  # Etiketleri sağa hizala
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)  # Formu ortala

        # Kullanıcı adı ve şifre giriş kutuları
        self.username_entry = QtWidgets.QLineEdit()
        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)

        # Giriş kutuları için stil ayarları
        self.username_entry.setFixedSize(250, 30)
        self.password_entry.setFixedSize(250, 30)
        self.username_entry.setStyleSheet("padding: 5px; border-radius: 8px; border: 1px solid #B2BABB;")
        self.password_entry.setStyleSheet("padding: 5px; border-radius: 8px; border: 1px solid #B2BABB;")
        self.username_entry.setPlaceholderText("Kullanıcı Adı") # Placeholder text (soluk yazı)
        self.password_entry.setPlaceholderText("Şifre")

        # Etiket ve giriş kutularını form düzenine ekle
        form_layout.addRow(self.username_entry)
        form_layout.addRow(self.password_entry)

        # Form düzenini ana düzene ekle
        main_layout.addLayout(form_layout)

        # Butonları yatayda hizalamak için bir QHBoxLayout oluştur
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)  # Butonları yatayda ortala

        # Giriş butonunu oluştur ve stil ekle
        login_button = QtWidgets.QPushButton("Giriş Yap")
        login_button.clicked.connect(self.login)
        login_button.setFixedSize(122, 40)
        button_layout.addWidget(login_button)

        # Çıkış butonunu oluştur ve stil ekle
        exit_button = QtWidgets.QPushButton("Çıkış")
        exit_button.clicked.connect(self.close)
        exit_button.setFixedSize(122, 40)
        button_layout.addWidget(exit_button)

        # Buton düzenini ana düzene ekle
        main_layout.addLayout(button_layout)

        # Ana düzeni pencereye ekle
        self.setLayout(main_layout)

    def login(self):
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        # Kullanıcı adı ve şifre kontrolü
        if not username and not password:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Kullanıcı adı ve şifre giriniz.")
        elif not username:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Kullanıcı adı giriniz.")
        elif not password:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Şifre giriniz.")
        elif validate_admin(username, password):
            self.close()
            self.main_menu = MainMenu()
            self.main_menu.showFullScreen()
        else:
            QtWidgets.QMessageBox.critical(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

# Ana menü penceresi
class MainMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Otel Otomasyon Sistemi")
        self.setGeometry(100, 100, 800, 600)

        # Ana düzen (her şeyi ortalamak için QVBoxLayout kullanacağız)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)  # Ana düzeni ortala

        # Butonlar düzeni (Yönlendirme butonları)
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignTop)

        self.add_buttons(button_layout)

        # Çıkış butonu
        exit_button = QtWidgets.QPushButton("Çıkış")
        exit_button.clicked.connect(self.logout)  # Çıkış butonunu tıklayınca login sayfasına yönlendir
        exit_button.setFixedSize(150, 40)  # Buton boyutunu ayarla
        button_layout.addWidget(exit_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)

        # Görselleri ekle
        self.add_images(main_layout)

        # Butonlar ve görselleri düzeni ana düzenle birleştir
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def add_buttons(self, button_layout):
        reservation_button = QtWidgets.QPushButton("Rezervasyon Yönetimi")
        reservation_button.clicked.connect(self.open_reservation_management)
        button_layout.addWidget(reservation_button)

        room_management_button = QtWidgets.QPushButton("Oda Yönetimi")
        room_management_button.clicked.connect(self.open_room_management)
        button_layout.addWidget(room_management_button)

        customer_management_button = QtWidgets.QPushButton("Müşteri Yönetimi")
        customer_management_button.clicked.connect(self.open_customer_management)
        button_layout.addWidget(customer_management_button)

    def add_images(self, layout):
        # Resimleri ekle
        image1 = QtGui.QPixmap("image1.jpg").scaled(1500, 300, QtCore.Qt.KeepAspectRatio)
        image2 = QtGui.QPixmap("image2.jpg").scaled(1500, 300, QtCore.Qt.KeepAspectRatio)
        image3 = QtGui.QPixmap("image3.jpg").scaled(1500, 300, QtCore.Qt.KeepAspectRatio)

        # Üst satır için layout
        top_layout = QtWidgets.QHBoxLayout()
        label1 = QtWidgets.QLabel()
        label1.setPixmap(image1)
        label2 = QtWidgets.QLabel()
        label2.setPixmap(image2)
        top_layout.addWidget(label1)
        top_layout.addWidget(label2)

        # Alt satır için layout
        bottom_layout = QtWidgets.QVBoxLayout()
        bottom_layout.addLayout(top_layout)

        label3 = QtWidgets.QLabel()
        label3.setPixmap(image3)
        bottom_layout.addWidget(label3)

        layout.addLayout(bottom_layout)

    def open_reservation_management(self):
        self.reservation_window = ReservationWindow()
        self.reservation_window.show()

    def open_room_management(self):
        self.room_window = RoomWindow()
        self.room_window.show()

    def open_customer_management(self):
        self.customer_window = CustomerWindow()
        self.customer_window.show()

    def logout(self):
        self.close()  # Ana menüyü kapat
        self.login_window = LoginWindow()  # Giriş penceresini yeniden oluştur
        self.login_window.showFullScreen()  # Giriş penceresini tam ekran olarak göster


# Rezervasyon Yönetim Penceresi
class ReservationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rezervasyon Yönetimi")
        self.setGeometry(200, 200, 400, 350)  # Genişlik ve yükseklik değerleri

        # Ana düzen
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Düzeni ortala

        # Başlık etiketini oluştur
        title_label = QtWidgets.QLabel("Rezervasyon Yönetimi")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E4053;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)  # Başlığı ortala
        layout.addWidget(title_label)

        # Form düzeni (Kullanıcı ID, Oda ID, Tarih bilgileri için)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)  # Etiketleri sağa hizala
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)  # Formu ortala

        # Giriş kutuları (Kullanıcı ID, Oda ID, Başlangıç ve Bitiş Tarihleri)
        self.customer_id_entry = QtWidgets.QLineEdit()
        self.room_id_entry = QtWidgets.QLineEdit()
        self.start_date_entry = QtWidgets.QLineEdit()
        self.end_date_entry = QtWidgets.QLineEdit()

        # Giriş kutuları için stil
        self.customer_id_entry.setFixedSize(250, 30)
        self.room_id_entry.setFixedSize(250, 30)
        self.start_date_entry.setFixedSize(250, 30)
        self.end_date_entry.setFixedSize(250, 30)

        # Placeholder text (soluk yazılar)
        self.customer_id_entry.setPlaceholderText("Müşteri ID")
        self.room_id_entry.setPlaceholderText("Oda ID")
        self.start_date_entry.setPlaceholderText("Başlangıç Tarihi (YYYY-MM-DD)")
        self.end_date_entry.setPlaceholderText("Bitiş Tarihi (YYYY-MM-DD)")

        # Etiketler ve giriş kutularını form düzenine ekle
        form_layout.addRow("Müşteri ID:", self.customer_id_entry)
        form_layout.addRow("Oda ID:", self.room_id_entry)
        form_layout.addRow("Başlangıç Tarihi:", self.start_date_entry)
        form_layout.addRow("Bitiş Tarihi:", self.end_date_entry)

        # Giriş butonunu oluştur ve stil ekle
        save_button = QtWidgets.QPushButton("Rezervasyon Ekle")
        save_button.clicked.connect(self.save_reservation)
        save_button.setFixedSize(150, 40)  # Buton boyutunu ayarla

        # Butonu form düzenine ekle
        form_layout.addWidget(save_button)

        # Form düzenini ana düzene ekle
        layout.addLayout(form_layout)

        # Ana düzeni pencereye ekle
        self.setLayout(layout)

    def save_reservation(self):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO Reservations (CustomerID, RoomID, StartDate, EndDate) VALUES (?, ?, ?, ?)""",
                    (self.customer_id_entry.text(),
                     self.room_id_entry.text(),
                     self.start_date_entry.text(),
                     self.end_date_entry.text()))
                conn.commit()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Rezervasyon başarıyla eklendi.")
            except Exception as e:
                print(f"Rezervasyon eklenirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Rezervasyon eklenirken hata oluştu.")
            finally:
                conn.close()


# Oda Yönetim Penceresi
class RoomWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oda Yönetimi")
        self.setGeometry(200, 200, 400, 350)  # Genişlik ve yükseklik değerleri

        # Ana düzen
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Düzeni ortala

        # Başlık etiketini oluştur
        title_label = QtWidgets.QLabel("Oda Yönetimi")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E4053;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)  # Başlığı ortala
        layout.addWidget(title_label)

        # Form düzeni (Oda Numarası, Oda Tipi ve Fiyat bilgileri için)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)  # Etiketleri sağa hizala
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)  # Formu ortala

        # Giriş kutuları (Oda Numarası, Oda Tipi, Fiyat)
        self.room_number_entry = QtWidgets.QLineEdit()
        self.room_type_entry = QtWidgets.QLineEdit()
        self.price_entry = QtWidgets.QLineEdit()

        # Giriş kutuları için stil
        self.room_number_entry.setFixedSize(250, 30)
        self.room_type_entry.setFixedSize(250, 30)
        self.price_entry.setFixedSize(250, 30)

        # Placeholder text (soluk yazılar)
        self.room_number_entry.setPlaceholderText("Oda Numarası")
        self.room_type_entry.setPlaceholderText("Oda Tipi")
        self.price_entry.setPlaceholderText("Fiyat")

        # Etiketler ve giriş kutularını form düzenine ekle
        form_layout.addRow("Oda Numarası:", self.room_number_entry)
        form_layout.addRow("Oda Tipi:", self.room_type_entry)
        form_layout.addRow("Fiyat:", self.price_entry)

        # Giriş butonunu oluştur ve stil ekle
        save_button = QtWidgets.QPushButton("Oda Ekle")
        save_button.clicked.connect(self.save_room)
        save_button.setFixedSize(150, 40)  # Buton boyutunu ayarla

        # Butonu form düzenine ekle
        form_layout.addWidget(save_button)

        # Form düzenini ana düzene ekle
        layout.addLayout(form_layout)

        # Ana düzeni pencereye ekle
        self.setLayout(layout)

    def save_room(self):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO Rooms (RoomNumber, RoomType, Price) VALUES (?, ?, ?)""",
                               (self.room_number_entry.text(),
                                self.room_type_entry.text(),
                                self.price_entry.text()))
                conn.commit()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Oda başarıyla eklendi.")
            except Exception as e:
                print(f"Oda eklenirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Oda eklenirken hata oluştu.")
            finally:
                conn.close()


# Müşteri Yönetim Penceresi
class CustomerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri Yönetimi")
        self.setGeometry(200, 200, 400, 350)  # Genişlik ve yükseklik değerleri

        # Ana düzen
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Düzeni ortala

        # Başlık etiketini oluştur
        title_label = QtWidgets.QLabel("Müşteri Yönetimi")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E4053;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)  # Başlığı ortala
        layout.addWidget(title_label)

        # Form düzeni (Müşteri Adı, E-posta ve Telefon bilgileri için)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)  # Etiketleri sağa hizala
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)  # Formu ortala

        # Giriş kutuları (Müşteri Adı, E-posta, Telefon)
        self.customer_name_entry = QtWidgets.QLineEdit()
        self.customer_email_entry = QtWidgets.QLineEdit()
        self.customer_phone_entry = QtWidgets.QLineEdit()

        # Giriş kutuları için stil
        self.customer_name_entry.setFixedSize(250, 30)
        self.customer_email_entry.setFixedSize(250, 30)
        self.customer_phone_entry.setFixedSize(250, 30)

        # Placeholder text (soluk yazılar)
        self.customer_name_entry.setPlaceholderText("Müşteri Adı")
        self.customer_email_entry.setPlaceholderText("E-posta")
        self.customer_phone_entry.setPlaceholderText("Telefon")

        # Etiketler ve giriş kutularını form düzenine ekle
        form_layout.addRow("Müşteri Adı:", self.customer_name_entry)
        form_layout.addRow("E-posta:", self.customer_email_entry)
        form_layout.addRow("Telefon:", self.customer_phone_entry)

        # Giriş butonunu oluştur ve stil ekle
        save_button = QtWidgets.QPushButton("Müşteri Ekle")
        save_button.clicked.connect(self.save_customer)
        save_button.setFixedSize(150, 40)  # Buton boyutunu ayarla

        # Butonu form düzenine ekle
        form_layout.addWidget(save_button)

        # Form düzenini ana düzene ekle
        layout.addLayout(form_layout)

        # Ana düzeni pencereye ekle
        self.setLayout(layout)

    def save_customer(self):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO Customers (Name, Email, Phone) VALUES (?, ?, ?)""",
                               (self.customer_name_entry.text(),
                                self.customer_email_entry.text(),
                                self.customer_phone_entry.text()))
                conn.commit()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Müşteri başarıyla eklendi.")
            except Exception as e:
                print(f"Müşteri eklenirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Müşteri eklenirken hata oluştu.")
            finally:
                conn.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())