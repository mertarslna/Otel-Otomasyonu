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
        self.setGeometry(200, 200, 600, 400)

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
        self.setGeometry(200, 200, 600, 400)

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

        # Butonları oluştur
        button_layout = QtWidgets.QHBoxLayout()  # Yatay düzen oluşturuyoruz

        save_button = QtWidgets.QPushButton("Oda Ekle")
        save_button.clicked.connect(self.save_room)
        save_button.setFixedSize(150, 40)

        list_button = QtWidgets.QPushButton("Odaları Listele")
        list_button.clicked.connect(self.list_rooms)
        list_button.setFixedSize(150, 40)

        status_button = QtWidgets.QPushButton("Durumları Listele")
        status_button.clicked.connect(self.list_room_status)
        status_button.setFixedSize(170, 40)

        # Butonları yatay düzene ekle
        button_layout.addWidget(save_button)
        button_layout.addWidget(list_button)
        button_layout.addWidget(status_button)

        # Buton düzenini form düzeninin altına ekle
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)  # Buton düzenini ana düzene ekle

        # Ana düzeni pencereye ekle
        self.setLayout(layout)

    def save_room(self):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Rooms (RoomNumber, RoomType, Price, IsOccupied) 
                    VALUES (?, ?, ?, ?)
                """, (self.room_number_entry.text(),
                      self.room_type_entry.text(),
                      self.price_entry.text(),
                      0))  # Yeni eklenen odalar varsayılan olarak boş
                conn.commit()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Oda başarıyla eklendi.")
            except Exception as e:
                print(f"Oda eklenirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Oda eklenirken hata oluştu.")
            finally:
                conn.close()

    def list_rooms(self):
        # List rooms logic remains unchanged
        pass

    def update_room_status(self, room_number, is_occupied):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Rooms SET IsOccupied = ? WHERE RoomNumber = ?
                """, (is_occupied, room_number))
                conn.commit()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Oda durumu güncellendi.")
            except Exception as e:
                print(f"Durum güncellenirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Durum güncellenirken hata oluştu.")
            finally:
                conn.close()

    def list_room_status(self):
        try:
            conn = connect_to_db()
            if not conn:
                raise Exception("Veritabanı bağlantısı sağlanamadı.")

            cursor = conn.cursor()
            cursor.execute("SELECT RoomNumber, RoomType, Price, IsOccupied FROM Rooms")
            rooms = cursor.fetchall()

            if not rooms:
                QtWidgets.QMessageBox.information(self, "Bilgi", "Henüz eklenmiş oda yok.")
                return

            # Odaların durumlarını yeni bir pencere ile göster
            status_window = QtWidgets.QDialog(self)
            status_window.setWindowTitle("Oda Durumları")
            status_window.setGeometry(600, 200, 400, 300)

            status_layout = QtWidgets.QVBoxLayout()
            status_label = QtWidgets.QLabel("Oda Durumları:")
            status_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2E4053;")
            status_layout.addWidget(status_label)

            # Listeyi gösteren widget
            room_status_list = QtWidgets.QListWidget()
            for room in rooms:
                room_number, room_type, price, is_occupied = room
                status_icon = "❌" if is_occupied else "✔"
                room_item = f"Oda No: {room_number} - Tip: {room_type} - Fiyat: {price} TL - Durum: {status_icon}"
                room_status_list.addItem(room_item)

            status_layout.addWidget(room_status_list)

            # Durum güncelleme butonu
            def update_status():
                # Seçilen oda numarasını al
                selected_item = room_status_list.selectedItems()
                if selected_item:
                    selected_room = selected_item[0].text()
                    room_number = selected_room.split(" - ")[0].split(": ")[1]  # Oda numarasını al

                    # Odanın mevcut durumunu al
                    cursor.execute("SELECT IsOccupied FROM Rooms WHERE RoomNumber = ?", (room_number,))
                    is_occupied = cursor.fetchone()[0]

                    # Durumu tersine çevir
                    new_status = 0 if is_occupied == 1 else 1
                    self.update_room_status(room_number, new_status)  # Durumu güncelle

                    # Durum simgesini güncelle
                    room_status_list.clear()
                    for room in rooms:
                        room_number, room_type, price, is_occupied = room
                        status_icon = "✔️" if is_occupied else "❌"
                        room_item = f"Oda No: {room_number} - Tip: {room_type} - Fiyat: {price} TL - Durum: {status_icon}"
                        room_status_list.addItem(room_item)

            update_button = QtWidgets.QPushButton("Durumu Güncelle")
            update_button.clicked.connect(update_status)
            status_layout.addWidget(update_button)

            status_window.setLayout(status_layout)

            # Pencereyi göster ve modal olarak açık tut
            status_window.exec_()

        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            QtWidgets.QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

        finally:
            if conn:
                conn.close()


# Müşteri Yönetim Penceresi
class CustomerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri Yönetimi")
        self.setGeometry(200, 200, 600, 400)

        # Ana düzen
        main_layout = QtWidgets.QVBoxLayout()
        self.setup_customer_table()
        self.setup_buttons()

        # Düzenleri ana düzene ekle
        main_layout.addWidget(self.customer_table)
        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)

        # Müşterileri yükle
        self.load_customers()

    def setup_customer_table(self):
        # Müşteri tablosu oluştur
        self.customer_table = QtWidgets.QTableWidget()
        self.customer_table.setColumnCount(6)
        self.customer_table.setHorizontalHeaderLabels(
            ["Müşteri ID", "Müşteri Adı", "Cinsiyet", "Yaş", "Telefon", "E-posta"])
        self.customer_table.horizontalHeader().setStretchLastSection(True)
        self.customer_table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

    def setup_buttons(self):
        # Ekle, Düzenle, Sil butonları
        self.button_layout = QtWidgets.QHBoxLayout()

        self.add_button = QtWidgets.QPushButton("Müşteri Ekle")
        self.add_button.clicked.connect(self.add_customer)

        self.edit_button = QtWidgets.QPushButton("Müşteri Düzenle")
        self.edit_button.clicked.connect(self.edit_customer)

        self.delete_button = QtWidgets.QPushButton("Müşteri Sil")
        self.delete_button.clicked.connect(self.delete_customer)

        # Butonları yerleştir
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)

    def add_customer(self):
        # Müşteri eklemek için yeni pencere
        self.show_customer_form()

    def edit_customer(self):
        # Seçili müşteriyi düzenlemek için
        selected_row = self.customer_table.currentRow()
        if selected_row >= 0:
            customer_id = self.customer_table.item(selected_row, 0).text()
            name = self.customer_table.item(selected_row, 1).text()
            gender = self.customer_table.item(selected_row, 2).text()
            age = self.customer_table.item(selected_row, 3).text()
            phone = self.customer_table.item(selected_row, 4).text()
            email = self.customer_table.item(selected_row, 5).text()

            # Müşteri bilgilerini formda göster
            self.show_customer_form(customer_id, name, gender, age, phone, email)
        else:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir müşteri seçin.")

    def delete_customer(self):
        # Seçili müşteriyi silmek için
        selected_row = self.customer_table.currentRow()
        if selected_row >= 0:
            customer_id = self.customer_table.item(selected_row, 0).text()
            reply = QtWidgets.QMessageBox.question(self, "Onay", "Bu müşteriyi silmek istediğinize emin misiniz?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                conn = connect_to_db()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM Customers WHERE Customer_id = ?", (customer_id,))
                        conn.commit()
                        self.load_customers()  # Listeyi güncelle
                        QtWidgets.QMessageBox.information(self, "Başarılı", "Müşteri başarıyla silindi.")
                    except Exception as e:
                        print(f"Müşteri silinirken hata oluştu: {e}")
                        QtWidgets.QMessageBox.critical(self, "Hata", "Müşteri silinirken hata oluştu.")
                    finally:
                        conn.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir müşteri seçin.")

    def load_customers(self):
        # Müşteri tablosunu doldurma
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Customer_id, Name, Gender, Age, Phone, Email FROM Customers")
                rows = cursor.fetchall()

                self.customer_table.setRowCount(0)  # Eski veriyi temizle
                for row_data in rows:
                    row = self.customer_table.rowCount()
                    self.customer_table.insertRow(row)
                    for column, data in enumerate(row_data):
                        self.customer_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
            except Exception as e:
                print(f"Müşteri listesi yüklenirken hata oluştu: {e}")
            finally:
                conn.close()

    def show_customer_form(self, customer_id=None, name="", gender="", age="", phone="", email=""):
        # Müşteri ekleme/düzenleme formu
        form_dialog = QtWidgets.QDialog(self)
        form_dialog.setWindowTitle("Müşteri Formu")
        form_dialog.setFixedSize(300, 400)

        layout = QtWidgets.QFormLayout(form_dialog)
        id_entry = QtWidgets.QLineEdit(customer_id)
        name_entry = QtWidgets.QLineEdit(name)
        gender_entry = QtWidgets.QLineEdit(gender)
        age_entry = QtWidgets.QLineEdit(age)
        phone_entry = QtWidgets.QLineEdit(phone)
        email_entry = QtWidgets.QLineEdit(email)

        layout.addRow("Müşteri ID:", id_entry)
        layout.addRow("Müşteri Adı:", name_entry)
        layout.addRow("Cinsiyet:", gender_entry)
        layout.addRow("Yaş:", age_entry)
        layout.addRow("Telefon:", phone_entry)
        layout.addRow("E-posta:", email_entry)

        # Kaydetme butonu
        save_button = QtWidgets.QPushButton("Kaydet", form_dialog)
        save_button.clicked.connect(lambda: self.save_customer(
            id_entry.text(), name_entry.text(), gender_entry.text(),
            age_entry.text(), phone_entry.text(), form_dialog, email_entry.text()
        ))

        layout.addWidget(save_button)
        form_dialog.exec_()

    def save_customer(self, customer_id, name, gender, age, phone, dialog, email):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                if customer_id:  # Güncelleme işlemi
                    cursor.execute("""UPDATE Customers SET Name=?, Gender=?, Age=?, Phone=?, Email=?
                                      WHERE Customer_id=?""",
                                   (name, gender, age, phone, email, customer_id))
                else:  # Yeni müşteri ekleme
                    cursor.execute("""INSERT INTO Customers (Name, Gender, Age, Phone, Email)
                                      VALUES (?, ?, ?, ?, ?)""",
                                   (name, gender, age, phone, email))
                conn.commit()
                self.load_customers()
                dialog.accept()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Müşteri bilgileri başarıyla kaydedildi.")
            except Exception as e:
                print(f"Müşteri bilgisi kaydedilirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Müşteri bilgisi kaydedilirken hata oluştu.")
            finally:
                conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())