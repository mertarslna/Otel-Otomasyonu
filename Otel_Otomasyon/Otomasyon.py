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

# Yönetici ekleme fonksiyonu
def add_admin(admin_name, username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Admin (Admin_name, Username, Password) 
                VALUES (?, ?, ?)
            """, (admin_name, username, password))
            conn.commit()
            QtWidgets.QMessageBox.information(None, "Başarılı", "Yönetici başarıyla eklendi.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Hata", f"Yönetici eklenirken hata oluştu: {e}")
        finally:
            conn.close()

# Veritabanı bağlantısını kurma fonksiyonu
def connect_to_db():
    try:
        connection = pyodbc.connect(conn_str)
        print("MSSQL bağlantısı başarılı.")
        return connection
    except Exception as e:
        print("MSSQL bağlantısı başarısız:", e)
        return None

# Yönetici girişi doğrulama fonksiyonu
def validate_admin(username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM Admin WHERE Username = ? AND Password = ?""", (username, password))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Giriş doğrulama sırasında hata oluştu: {e}")
        finally:
            conn.close()
    return False

# Açılış Ekranı
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

# Yönetici Giriş Penceresi
class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setGeometry(300, 300, 400, 300)

        # Ana düzen (her şeyi ortalamak için QVBoxLayout kullanacağız)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)  # Ana düzeni ortala

        # Başlık etiketini oluştur
        title_label = QtWidgets.QLabel("Yönetici Girişi")
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
        elif validate_admin(username, password):  # validate_admin fonksiyonunun tanımlı olduğunu varsayıyoruz
            self.close()
            self.main_menu = MainMenu()  # MainMenu sınıfının tanımlı olduğundan emin olun
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

        # Form düzeni (Oda ID, Tarih bilgileri için)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)  # Etiketleri sağa hizala
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)  # Formu ortala

        # Giriş kutuları (Oda ID, Başlangıç ve Bitiş Tarihleri)
        self.room_id_entry = QtWidgets.QLineEdit()
        self.start_date_entry = QtWidgets.QLineEdit()
        self.end_date_entry = QtWidgets.QLineEdit()

        # Giriş kutuları için stil
        self.room_id_entry.setFixedSize(250, 30)
        self.start_date_entry.setFixedSize(250, 30)
        self.end_date_entry.setFixedSize(250, 30)

        # Placeholder text (soluk yazılar)
        self.room_id_entry.setPlaceholderText("Oda ID")
        self.start_date_entry.setPlaceholderText("Başlangıç Tarihi (YYYY-MM-DD)")
        self.end_date_entry.setPlaceholderText("Bitiş Tarihi (YYYY-MM-DD)")

        # Etiketler ve giriş kutularını form düzenine ekle
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
                    """INSERT INTO Reservation (Room_Number, Start_Date, End_Date) 
                    VALUES (?, ?, ?, ?)""",
                    (self.room_id_entry.text(),
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
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Başlık etiketini oluştur
        title_label = QtWidgets.QLabel("Oda Yönetimi")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E4053;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        # Form düzeni (Oda Numarası, Oda Tipi ve Fiyat bilgileri için)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)

        # Giriş kutuları
        self.room_number_entry = QtWidgets.QLineEdit()
        self.room_type_entry = QtWidgets.QLineEdit()
        self.price_entry = QtWidgets.QLineEdit()

        # Giriş kutuları için stil
        self.room_number_entry.setFixedSize(250, 30)
        self.room_type_entry.setFixedSize(250, 30)
        self.price_entry.setFixedSize(250, 30)

        # Placeholder text
        self.room_number_entry.setPlaceholderText("Oda Numarası")
        self.room_type_entry.setPlaceholderText("Oda Tipi")
        self.price_entry.setPlaceholderText("Fiyat")

        # Etiketler ve giriş kutularını form düzenine ekle
        form_layout.addRow("Oda Numarası:", self.room_number_entry)
        form_layout.addRow("Oda Tipi:", self.room_type_entry)
        form_layout.addRow("Fiyat:", self.price_entry)

        # Butonları oluştur
        button_layout = QtWidgets.QHBoxLayout()

        save_button = QtWidgets.QPushButton("Oda Ekle")
        save_button.clicked.connect(self.save_room)
        save_button.setFixedSize(150, 40)

        list_button = QtWidgets.QPushButton("Odaları Listele")
        list_button.clicked.connect(self.list_rooms)
        list_button.setFixedSize(150, 40)

        # Butonları yatay düzene ekle
        button_layout.addWidget(save_button)
        button_layout.addWidget(list_button)

        # Buton düzenini form düzeninin altına ekle
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        # Ana düzeni pencereye ekle
        self.setLayout(layout)

    def save_room(self):
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Oda bilgileri alındı
                room_number_text = self.room_number_entry.text().strip()
                room_type = self.room_type_entry.text().strip()
                price_text = self.price_entry.text().strip()

                # Giriş doğrulama
                if not room_number_text or not room_type or not price_text:
                    QtWidgets.QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalıdır.")
                    return

                try:
                    room_number = int(room_number_text)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Hata", "Oda numarası geçerli bir sayı olmalıdır.")
                    return

                try:
                    price = float(price_text)
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Hata", "Fiyat geçerli bir sayı olmalıdır.")
                    return

                # Hotel_id manuel olarak belirlenir veya UI'den alınır
                hotel_id = 1

                # Oda numarasının benzersiz olmasını sağla
                cursor.execute("SELECT COUNT(*) FROM Room WHERE Room_id = ?", (room_number,))
                if cursor.fetchone()[0] > 0:
                    QtWidgets.QMessageBox.warning(self, "Hata", "Bu oda numarası zaten var.")
                    return

                # Odayı ekle
                cursor.execute(""" 
                    INSERT INTO Room (Room_id, Hotel_id, Room_Type, Price, Available)
                    VALUES (?, ?, ?, ?, ?)
                """, (room_number, hotel_id, room_type, price, 1))

                conn.commit()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Oda başarıyla eklendi.")

            except Exception as e:
                print(f"Oda eklenirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Oda eklenirken hata oluştu.")
            finally:
                conn.close()

    def list_rooms(self):
        try:
            conn = connect_to_db()
            if not conn:
                raise Exception("Veritabanı bağlantısı sağlanamadı.")

            cursor = conn.cursor()
            cursor.execute("SELECT Room_id, Room_Type, Price, Available FROM Room")
            rooms = cursor.fetchall()

            if not rooms:
                QtWidgets.QMessageBox.information(self, "Bilgi", "Henüz eklenmiş oda yok.")
                return

            room_list_window = QtWidgets.QDialog(self)
            room_list_window.setWindowTitle("Odalar")
            room_list_window.setGeometry(600, 200, 400, 300)

            layout = QtWidgets.QVBoxLayout()

            list_widget = QtWidgets.QListWidget()
            for room in rooms:
                room_id, room_type, price, available = room
                available_status = "Boş" if available else "Dolu"
                item_text = f"Oda No: {room_id}, Tip: {room_type}, Fiyat: {price} TL, Durum: {available_status}"
                item = QtWidgets.QListWidgetItem(item_text)
                list_widget.addItem(item)

                # Odaların düzenlenmesini engelle
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

                # Odaların durumunu değiştirmek için çift tıklama olayı
                item.setData(QtCore.Qt.UserRole, room_id)  # Oda numarasını saklıyoruz

            # Çift tıklama ile oda detaylarını düzenleyeceğiz
            list_widget.itemDoubleClicked.connect(self.open_room_edit_window)

            layout.addWidget(list_widget)
            room_list_window.setLayout(layout)
            room_list_window.exec_()

        except Exception as e:
            print(f"Hata oluştu: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", "Odalar listelenirken bir hata oluştu.")
        finally:
            if conn:
                conn.close()

    def open_room_edit_window(self, item):
        room_id = item.data(QtCore.Qt.UserRole)  # Oda numarasını alıyoruz

        # Seçilen odanın bilgilerini almak için veritabanına sorgu
        try:
            conn = connect_to_db()
            if not conn:
                raise Exception("Veritabanı bağlantısı sağlanamadı.")

            cursor = conn.cursor()
            cursor.execute("SELECT Room_id, Room_Type, Price, Available FROM Room WHERE Room_id = ?", (room_id,))
            room = cursor.fetchone()

            if not room:
                QtWidgets.QMessageBox.warning(self, "Hata", "Oda bilgileri bulunamadı.")
                return

            room_number, room_type, price, available = room
            available_status = "Boş" if available else "Dolu"

            # Oda düzenleme penceresini aç
            edit_window = QtWidgets.QDialog(self)
            edit_window.setWindowTitle(f"Oda Düzenle - Oda No: {room_number}")
            edit_window.setGeometry(700, 250, 400, 300)

            layout = QtWidgets.QVBoxLayout()

            # Oda bilgilerini düzenlemek için etiketler ve giriş kutuları
            form_layout = QtWidgets.QFormLayout()
            form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
            form_layout.setFormAlignment(QtCore.Qt.AlignCenter)

            room_number_entry = QtWidgets.QLineEdit(str(room_number))
            room_number_entry.setFixedSize(250, 30)
            room_number_entry.setReadOnly(True)

            room_type_entry = QtWidgets.QLineEdit(room_type)
            room_type_entry.setFixedSize(250, 30)

            price_entry = QtWidgets.QLineEdit(str(price))
            price_entry.setFixedSize(250, 30)

            available_combobox = QtWidgets.QComboBox()
            available_combobox.addItem("Boş", 1)
            available_combobox.addItem("Dolu", 0)
            available_combobox.setCurrentIndex(0 if available == 1 else 1)

            form_layout.addRow("Oda Numarası:", room_number_entry)
            form_layout.addRow("Oda Tipi:", room_type_entry)
            form_layout.addRow("Fiyat:", price_entry)
            form_layout.addRow("Durum:", available_combobox)

            # Düzenleme butonu
            save_button = QtWidgets.QPushButton("Kaydet")
            save_button.clicked.connect(lambda: self.save_room_edit(room_id, room_type_entry.text(), price_entry.text(), available_combobox.currentData()))

            layout.addLayout(form_layout)
            layout.addWidget(save_button)

            edit_window.setLayout(layout)
            edit_window.exec_()

        except Exception as e:
            print(f"Hata oluştu: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", "Oda düzenleme penceresi açılamadı.")
        finally:
            if conn:
                conn.close()

    def save_room_edit(self, room_id, room_type, price, available):
        try:
            conn = connect_to_db()
            if not conn:
                raise Exception("Veritabanı bağlantısı sağlanamadı.")

            cursor = conn.cursor()

            try:
                price = float(price)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Hata", "Fiyat geçerli bir sayı olmalıdır.")
                return

            cursor.execute(""" 
                UPDATE Room 
                SET Room_Type = ?, Price = ?, Available = ? 
                WHERE Room_id = ?
            """, (room_type, price, available, room_id))

            conn.commit()
            QtWidgets.QMessageBox.information(self, "Başarılı", "Oda bilgileri başarıyla güncellendi.")

        except Exception as e:
            print(f"Hata oluştu: {e}")
            QtWidgets.QMessageBox.critical(self, "Hata", "Oda düzenlenirken bir hata oluştu.")
        finally:
            if conn:
                conn.close()

# Müşteri Yönetim Penceresi
class CustomerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri Yönetimi")
        self.setGeometry(200, 200, 900, 400)

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
            ["ID", "Müşteri Adı", "Cinsiyet", "Yaş", "Telefon", "E-posta"])
        self.customer_table.horizontalHeader().setStretchLastSection(True)
        self.customer_table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        # Tablo hücrelerinin düzenlenmesini engelle
        self.customer_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

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
            self.show_customer_form(name, gender, age, phone, email, customer_id)
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
                        cursor.execute("DELETE FROM Customer WHERE Customer_id = ?", (customer_id,))
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
                cursor.execute("SELECT Customer_id, Name, Gender, Age, Phone, Email FROM Customer")
                rows = cursor.fetchall()

                self.customer_table.setRowCount(0)  # Eski veriyi temizle
                for row_data in rows:
                    row = self.customer_table.rowCount()
                    self.customer_table.insertRow(row)
                    for column, data in enumerate(row_data):
                        self.customer_table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
            except Exception as e:
                print(f"Müşteri listesi yüklenirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", "Müşteri listesi yüklenirken hata oluştu.")
            finally:
                conn.close()

    def show_customer_form(self, name="", gender="", age="", phone="", email="", customer_id=None):
        # Müşteri ekleme/düzenleme formu
        form_dialog = QtWidgets.QDialog(self)
        form_dialog.setWindowTitle("Müşteri Formu")
        form_dialog.setFixedSize(300, 200)

        layout = QtWidgets.QFormLayout(form_dialog)
        name_entry = QtWidgets.QLineEdit(name)
        gender_entry = QtWidgets.QComboBox()
        gender_entry.addItem("Erkek")
        gender_entry.addItem("Kadın")
        gender_entry.setCurrentText(gender if gender else "Erkek")
        age_entry = QtWidgets.QLineEdit(age)
        phone_entry = QtWidgets.QLineEdit(phone)
        email_entry = QtWidgets.QLineEdit(email)

        layout.addRow("Müşteri Adı:", name_entry)
        layout.addRow("Cinsiyet:", gender_entry)
        layout.addRow("Yaş:", age_entry)
        layout.addRow("Telefon:", phone_entry)
        layout.addRow("E-posta:", email_entry)

        save_button = QtWidgets.QPushButton("Kaydet", form_dialog)
        save_button.clicked.connect(lambda: self.save_customer(
            name_entry.text(), gender_entry.currentText(),
            age_entry.text(), phone_entry.text(), email_entry.text(), form_dialog, customer_id
        ))

        layout.addWidget(save_button)
        form_dialog.exec_()

    def save_customer(self, name, gender, age, phone, email, dialog, customer_id=None):
        # Veri doğrulama
        if not name or not age or not phone or not email:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Tüm alanlar doldurulmalıdır.")
            return

        if not age.isdigit() or int(age) <= 0:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Geçerli bir yaş girin.")
            return

        if not phone.isdigit() or len(phone) != 10:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Geçerli bir telefon numarası girin.")
            return

        if '@' not in email:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Geçerli bir e-posta adresi girin.")
            return

        # Veritabanına kaydetme
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                if customer_id:
                    cursor.execute("""UPDATE Customer SET Name = ?, Gender = ?, Age = ?, Phone = ?, Email = ? 
                                      WHERE Customer_id = ?""",
                                   (name, gender, age, phone, email, customer_id))
                else:
                    cursor.execute("""INSERT INTO Customer (Name, Gender, Age, Phone, Email) 
                                      VALUES (?, ?, ?, ?, ?)""",
                                   (name, gender, age, phone, email))
                conn.commit()
                self.load_customers()
                dialog.accept()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Müşteri bilgileri başarıyla kaydedildi.")
            except Exception as e:
                print(f"Müşteri bilgisi kaydedilirken hata oluştu: {e}")
                QtWidgets.QMessageBox.critical(self, "Hata", f"Müşteri bilgisi kaydedilirken hata oluştu: {e}")
            finally:
                conn.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Hata", "Veritabanına bağlanırken bir hata oluştu.")

# PyQt5 Uygulama Başlatıcı
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())