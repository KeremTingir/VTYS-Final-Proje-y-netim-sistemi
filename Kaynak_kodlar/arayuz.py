import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QLabel, QLineEdit, QFormLayout, QDateTimeEdit,
    QDialogButtonBox, QMessageBox, QInputDialog
)
from PyQt5.QtCore import QDateTime
from fonksiyonlar import * 

class ProjectManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.conn, self.cursor = connect_to_database()  # Bağlantıyı burada aç
        if not self.conn or not self.cursor:
            QMessageBox.critical(self, "Hata", "Veritabanına bağlanırken bir hata oluştu. Uygulama kapatılıyor.")
            sys.exit(1)
        
        self.setWindowTitle("Proje Yönetimi")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        # Sol tarafta projeler
        self.project_table = QTableWidget(self)
        self.project_table.setColumnCount(3)  # Proje tablosu için 3 sütun
        self.project_table.setHorizontalHeaderLabels(["Proje Adı", "Başlangıç Tarihi", "Bitiş Tarihi"])
        self.layout.addWidget(self.project_table)

        # Proje ekle butonu
        self.add_project_button = QPushButton("Proje Ekle", self)
        self.add_project_button.clicked.connect(self.show_add_project_dialog)
        self.layout.addWidget(self.add_project_button)

        # Proje güncelle butonu
        self.update_project_button = QPushButton("Proje Güncelle", self)
        self.update_project_button.clicked.connect(self.show_update_project_dialog)
        self.layout.addWidget(self.update_project_button)
        
        # Proje sil butonu
        self.delete_project_button = QPushButton("Proje Sil", self)
        self.delete_project_button.clicked.connect(self.show_delete_project_dialog)
        self.layout.addWidget(self.delete_project_button)
        
        # Proje ara butonu
        self.search_project_button = QPushButton("Proje Ara", self)
        self.search_project_button.clicked.connect(self.show_search_project_dialog)
        self.layout.addWidget(self.search_project_button)

        # Sağ tarafta görevler
        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(4)  # Görev tablosu için 4 sütun
        self.task_table.setHorizontalHeaderLabels(["Proje Adı", "Görev Adı", "Atanan Kişi", "Görev Durumu"])
        self.layout.addWidget(self.task_table)

        # Görev ekle butonu
        self.add_task_button = QPushButton("Görev Ekle", self)
        self.add_task_button.clicked.connect(self.show_add_task_dialog)
        self.layout.addWidget(self.add_task_button)
        
        # Çalışanı Listele butonu
        self.list_tasks_button = QPushButton("Çalışan Görevleri Listele", self)
        self.list_tasks_button.clicked.connect(self.show_list_tasks_dialog)
        self.layout.addWidget(self.list_tasks_button)
        
        self.show()
    
    def show_add_project_dialog(self):
        dialog = AddProjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            project_name = dialog.project_name_input.text()
            start_date = dialog.start_date_input.date().toString("yyyy-MM-dd")
            end_date = dialog.end_date_input.date().toString("yyyy-MM-dd")

            # Fonksiyonları kullanarak veritabanına ekleme işlemleri
            add_project(project_name, start_date, end_date)
        
            self.add_project(project_name, start_date, end_date)
            
        # Diyalog penceresini kapat
        dialog.close()

    def add_project(self, project_name, start_date, end_date):
        row_position = self.project_table.rowCount()
        self.project_table.insertRow(row_position)
        self.project_table.setItem(row_position, 0, QTableWidgetItem(project_name))
        self.project_table.setItem(row_position, 1, QTableWidgetItem(start_date))
        self.project_table.setItem(row_position, 2, QTableWidgetItem(end_date))

    def show_update_project_dialog(self):
        selected_row = self.project_table.currentRow()
        if selected_row == -1:
            return

        selected_project_name = self.project_table.item(selected_row, 0).text()
        selected_start_date = self.project_table.item(selected_row, 1).text()
        selected_end_date = self.project_table.item(selected_row, 2).text()

        dialog = UpdateProjectDialog(self, selected_project_name, selected_start_date, selected_end_date)
        if dialog.exec_() == QDialog.Accepted:
            updated_project_name = dialog.project_name_input.text()
            updated_start_date = dialog.start_date_input.date().toString("yyyy-MM-dd")
            updated_end_date = dialog.end_date_input.date().toString("yyyy-MM-dd")

            # Fonksiyonları kullanarak veritabanında güncelleme işlemleri
            update_project(self.conn, self.cursor, selected_project_name, updated_project_name, updated_start_date, updated_end_date)
        
            self.update_project(selected_row, updated_project_name, updated_start_date, updated_end_date)

    def update_project(self, row, updated_project_name, updated_start_date, updated_end_date):
        self.project_table.setItem(row, 0, QTableWidgetItem(updated_project_name))
        self.project_table.setItem(row, 1, QTableWidgetItem(updated_start_date))
        self.project_table.setItem(row, 2, QTableWidgetItem(updated_end_date))

    def show_delete_project_dialog(self):
        selected_row = self.project_table.currentRow()
        if selected_row == -1:
            return

        selected_project_name = self.project_table.item(selected_row, 0).text()

        reply = QMessageBox.question(self, "Proje Sil", f"Seçili projeyi silmek istiyor musunuz?\n\nProje Adı: {selected_project_name}",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Fonksiyonları kullanarak veritabanında silme işlemleri
            delete_project(self.conn, self.cursor, selected_project_name)
            
            self.delete_project(selected_row)

    def delete_project(self, row):
        self.project_table.removeRow(row)
        
    def show_search_project_dialog(self):
        project_name, ok_pressed = QInputDialog.getText(self, 'Proje Ara', 'Proje Adı:')
        if ok_pressed:
            self.search_project(project_name)
    
    def search_project(self, project_name):
        self.project_table.clearContents()  # Mevcut içeriği temizle

        projects = search_project(self.conn, self.cursor, project_name)

        for project in projects:
            row_position = self.project_table.rowCount()
            self.project_table.insertRow(row_position)
            self.project_table.setItem(row_position, 0, QTableWidgetItem(project["ProjeAdi"]))
            self.project_table.setItem(row_position, 1, QTableWidgetItem(project["BaslangicTarihi"]))
            self.project_table.setItem(row_position, 2, QTableWidgetItem(project["BitisTarihi"]))
    
    def show_add_task_dialog(self):
        selected_row = self.project_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir proje seçin.")
            return

        selected_project_name = self.project_table.item(selected_row, 0).text()

        dialog = AddTaskDialog(self, selected_project_name)
        if dialog.exec_() == QDialog.Accepted:
            task_name = dialog.task_name_input.text()
            assigned_person = dialog.assigned_person_input.text()

            # Fonksiyonları kullanarak veritabanında ekleme işlemleri
            self.add_task(selected_project_name, task_name, assigned_person)

    def add_task(self, project_name, task_name, assigned_person):
        # Projeyi veritabanında arayarak ID'sini alalım
        project_id = get_project_id(self.conn, self.cursor, project_name)

        # Çalışanı veritabanında arayarak ID'sini alalım
        employee_id = get_employee_id(self.conn, self.cursor, assigned_person)

        # Eğer proje veya çalışan bulunamazsa uyarı verip işlemi iptal edelim
        if project_id is None or employee_id is None:
            QMessageBox.warning(self, "Uyarı", "Proje veya çalışan bulunamadı. Görev eklenemedi.")
            return

        # Görev ekleme fonksiyonunu kullanarak veritabanında ekleme işlemleri
        add_task(self.conn, self.cursor, task_name, project_id, employee_id)

        # Arayüzü güncelleme işlemleri
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)
        self.task_table.setItem(row_position, 0, QTableWidgetItem(project_name))
        self.task_table.setItem(row_position, 1, QTableWidgetItem(task_name))
        self.task_table.setItem(row_position, 2, QTableWidgetItem(assigned_person))
        self.task_table.setItem(row_position, 3, QTableWidgetItem("Devam Ediyor"))  # Default durum
  
    def show_list_tasks_dialog(self):
        person_name, ok_pressed = QInputDialog.getText(self, 'Çalışan Görevleri Listele', 'Çalışan Adı Soyadı:')
        if ok_pressed:
            dialog = ListTasksDialog(self, person_name, self.conn, self.cursor)
            dialog.exec_()
            
    def closeEvent(self, event):
            reply = QMessageBox.question(self, 'Uygulama Kapatılıyor',
                                         'Uygulamayı kapatmak istediğinizden emin misiniz?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
 
     
class AddProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Proje Ekle")

        self.layout = QFormLayout(self)

        self.label = QLabel("Proje Adı:", self)
        self.project_name_input = QLineEdit(self)
        self.layout.addRow(self.label, self.project_name_input)

        self.label_start_date = QLabel("Başlangıç Tarihi:", self)
        self.start_date_input = QDateTimeEdit(self)
        self.start_date_input.setDateTime(QDateTime.currentDateTime())
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDateTime.currentDateTime().date())
        self.layout.addRow(self.label_start_date, self.start_date_input)

        self.label_end_date = QLabel("Bitiş Tarihi:", self)
        self.end_date_input = QDateTimeEdit(self)
        self.end_date_input.setDateTime(QDateTime.currentDateTime())
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDateTime.currentDateTime().date())
        self.layout.addRow(self.label_end_date, self.end_date_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)

     # Diyalog penceresi kapatıldığında çalışacak fonksiyon
    def closeEvent(self, event):
        self.accept()
    
class UpdateProjectDialog(QDialog):
    def __init__(self, parent=None, project_name="", start_date="", end_date=""):
        super().__init__(parent)

        self.setWindowTitle("Proje Güncelle")

        self.layout = QFormLayout(self)

        self.label = QLabel("Proje Adı:", self)
        self.project_name_input = QLineEdit(self)
        self.project_name_input.setText(project_name)
        self.layout.addRow(self.label, self.project_name_input)

        self.label_start_date = QLabel("Başlangıç Tarihi:", self)
        self.start_date_input = QDateTimeEdit(self)
        self.start_date_input.setDateTime(QDateTime.fromString(start_date, "yyyy-MM-dd"))
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        self.start_date_input.setCalendarPopup(True)
        self.layout.addRow(self.label_start_date, self.start_date_input)

        self.label_end_date = QLabel("Bitiş Tarihi:", self)
        self.end_date_input = QDateTimeEdit(self)
        self.end_date_input.setDateTime(QDateTime.fromString(end_date, "yyyy-MM-dd"))
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        self.end_date_input.setCalendarPopup(True)
        self.layout.addRow(self.label_end_date, self.end_date_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)

class AddTaskDialog(QDialog):
    def __init__(self, parent=None, project_name=""):
        super().__init__(parent)

        self.setWindowTitle("Görev Ekle")

        self.layout = QFormLayout(self)

        self.label_project = QLabel("Proje Adı:", self)
        self.project_input = QLineEdit(self)
        self.project_input.setText(project_name)
        self.project_input.setReadOnly(True)
        self.layout.addRow(self.label_project, self.project_input)

        self.label_task_name = QLabel("Görev Adı:", self)
        self.task_name_input = QLineEdit(self)
        self.layout.addRow(self.label_task_name, self.task_name_input)

        self.label_assigned_person = QLabel("Atanan Personel:", self)
        self.assigned_person_input = QLineEdit(self)
        self.layout.addRow(self.label_assigned_person, self.assigned_person_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)

class ListTasksDialog(QDialog):
    def __init__(self, parent=None, selected_person="", conn=None, cursor=None):
        super().__init__(parent)

        self.setWindowTitle(f"{selected_person} Görev Listesi")

        self.layout = QVBoxLayout(self)

        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(4)  # Görev tablosu için 4 sütun
        self.task_table.setHorizontalHeaderLabels(["Proje Adı", "Görev Adı", "Atanan Kişi", "Görev Durumu"])
        self.layout.addWidget(self.task_table)

        self.populate_task_table(selected_person, conn, cursor)

    def populate_task_table(self, selected_person, conn, cursor):
        tasks = get_employee_tasks(conn, cursor, selected_person)

        for task in tasks:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(task["project_name"]))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(task["task_name"]))
            self.task_table.setItem(row_position, 2, QTableWidgetItem(task["assigned_person"]))
            status_item = QTableWidgetItem(task["status"])
            self.task_table.setItem(row_position, 3, status_item)

            # Görev durumu güncelleme butonu ekle
            update_button = QPushButton("Durumu Güncelle", self)
            update_button.clicked.connect(lambda _, row=row_position, task_id=task["task_id"]: self.show_update_status_dialog(row, task_id))
            self.task_table.setCellWidget(row_position, 4, update_button)

    def show_update_status_dialog(self, row, task_id):
        dialog = UpdateStatusDialog(self, row, task_id, self.conn, self.cursor)
        if dialog.exec_() == QDialog.Accepted:
            updated_status = dialog.status_input.text()
            self.update_task_status(row, task_id, updated_status)

    def update_task_status(self, row, task_id, updated_status):
        self.task_table.setItem(row, 3, QTableWidgetItem(updated_status))
        update_task_status(self.conn, self.cursor, task_id, updated_status)
    
class UpdateStatusDialog(QDialog):
    def __init__(self, parent=None, row=None, task_id=None, conn=None, cursor=None):
        super().__init__(parent)

        self.setWindowTitle("Görev Durumu Güncelle")

        self.layout = QFormLayout(self)

        self.label_status = QLabel("Yeni Durum:", self)
        self.status_input = QLineEdit(self)
        self.layout.addRow(self.label_status, self.status_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)

        self.row = row
        self.task_id = task_id
        self.conn = conn
        self.cursor = cursor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectManagementApp()
    sys.exit(app.exec_())
