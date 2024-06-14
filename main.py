import mysql.connector
from PyQt5 import QtWidgets, QtGui

import Admin
import RA
import zakaz

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="bd"
)

cursor = db.cursor()


class ReAv(QtWidgets.QMainWindow, RA.Ui_Dialog):
    def __init__(self):
        super(ReAv, self).__init__()
        self.ad = None
        self.setupUi(self)


        self.pushButton_reg.pressed.connect(self.reg)
        self.pushButton_Aut.pressed.connect(self.avt)

        self.setMinimumSize(400, 400)



    def reg(self):
        login = self.lineEdit_login.text()
        password = self.lineEdit_passw.text()
        fio = self.lineEdit_fio.text()
        email = self.lineEdit_email.text()

        cursor.execute(f'INSERT INTO user_info VALUES ("{login}", "{password}", "{fio}", "{email}")')
        db.commit()

    def avt(self):
        loginAu = self.lineEdit_loginAu.text()
        PassAu = self.lineEdit_PassAu.text()

        cursor.execute(f'SELECT fio FROM user_info WHERE login = "{loginAu}" AND password = "{PassAu}"')
        x = cursor.fetchall()

        if len(x) == 0:
            return

        if "0987" == PassAu and "1" == loginAu:
            self.ad = admin()
            self.ad.show()
            self.hide()

        else:
            self.ct = Zakaz()
            self.ct.show()
            self.hide()

class admin(QtWidgets.QMainWindow, Admin.Ui_MainWindow):
    def __init__(self):
        super(admin, self).__init__()
        self.setupUi(self)

        self.pushButton_all_zakaz.pressed.connect(self.all_zak)
        self.pushButton_naiti.pressed.connect(self.naiti)
        self.pushButton_filter.pressed.connect(self.Filter)
        self.pushButton_izmenit.pressed.connect(self.updata_status)
        self.pushButton_del_sotr.pressed.connect(self.del_sotr)
        self.pushButton_dop_sotr.pressed.connect(self.dop_sotr)
        self.pushButton_dop_tov.pressed.connect(self.add_tov)
        self.pushButton_del_tov.pressed.connect(self.del_tov)
        self.fullname_customers()
        self.pushButton_dop_prodaja.pressed.connect(self.add_prodaja)
        self.pushButton_del_prodaja.pressed.connect(self.del_prodaja)

        cursor.execute(f'select `id`,`FullName`,`Phone`, `Tovar`, `kol`, `OrderDate`,`OrderStatus` from Customers')
        zak = cursor.fetchall()
        self.tableWidget_zakaz.clear()
        self.tableWidget_zakaz.setRowCount(len(zak))
        for i in range(len(zak)):
            for j in range(7):
                self.tableWidget_zakaz.setItem(i, j, QtWidgets.QTableWidgetItem(str(zak[i][j])))

        self.tableWidget_zakaz.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Товар", "Количество(шт)", "Дата заказа", "Статус заказа"])

        cursor.execute(f'select `ArticleNumber`,`ProductName`,`Category`,`Price`,`DateOfManufacture`,`ExpiryDate`,`Manufacturer`,`CountryOfOrigin` from Products ')
        tov = cursor.fetchall()
        self.tableWidget_tovar.clear()
        self.tableWidget_tovar.setRowCount(len(tov))
        for i in range(len(tov)):
            for j in range(8):
                self.tableWidget_tovar.setItem(i, j, QtWidgets.QTableWidgetItem(str(tov[i][j])))

        self.tableWidget_tovar.setHorizontalHeaderLabels(["Артикул", "Наименование", "Категория", "Цена", "Дата изготовления", "Срок годности", "Производитель", "Страна производства"])

        cursor.execute(f'select `FullName`,`DateOfBirth`,`Phone`,`Address` from Employees ')
        sotr = cursor.fetchall()
        print(sotr[0])
        self.tableWidget_sotrydnik.clear()
        self.tableWidget_sotrydnik.setRowCount(len(sotr))
        for i in range(len(sotr)):
            for j in range(4):
                self.tableWidget_sotrydnik.setItem(i, j, QtWidgets.QTableWidgetItem(str(sotr[i][j])))

        self.tableWidget_sotrydnik.setHorizontalHeaderLabels(["ФИО", "Дата рождения", "Телефон", "Адресс"])

        cursor.execute(f'select `Klient`,`employees`,`tovar`,`dataProdaji`,`sposob` from Prodaji ')
        sotr = cursor.fetchall()
        print(sotr[0])
        self.tableWidget_prodaji.clear()
        self.tableWidget_prodaji.setRowCount(len(sotr))
        for i in range(len(sotr)):
            for j in range(5):
                self.tableWidget_prodaji.setItem(i, j, QtWidgets.QTableWidgetItem(str(sotr[i][j])))

        self.tableWidget_prodaji.setHorizontalHeaderLabels(["Клиент", "Сотрудник", "Товары и их кол-во", "Дата продажи", "Способ оплаты"])

    def fullname_customers(self):
        cursor.execute(f'select `FullName` from Customers ')
        clients = cursor.fetchall()
        self.comboBox_klient.clear()
        for client in clients:
             self.comboBox_klient.addItem(client[0])


    def all_zak(self):
        cursor.execute(f'select `id`,`FullName`,`Phone`, `Tovar`, `kol`, `OrderDate`,`OrderStatus` from Customers')
        zak = cursor.fetchall()
        self.tableWidget_zakaz.clear()
        self.tableWidget_zakaz.setRowCount(len(zak))
        for i in range(len(zak)):
            for j in range(7):
                self.tableWidget_zakaz.setItem(i, j, QtWidgets.QTableWidgetItem(str(zak[i][j])))

        self.tableWidget_zakaz.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Товар", "Количество(шт)", "Дата заказа", "Статус заказа"])


    def Filter(self):
        filter = self.comboBox_klient.currentText()
        cursor.execute(f'select `id`,`FullName`,`Phone`, `Tovar`, `kol`, `OrderDate`,`OrderStatus` from Customers WHERE FullName = "{filter}"')
        zak = cursor.fetchall()
        print(zak[0])

        self.tableWidget_zakaz.clear()
        self.tableWidget_zakaz.setRowCount(len(zak))
        for i in range(len(zak)):
            for j in range(7):
                self.tableWidget_zakaz.setItem(i, j, QtWidgets.QTableWidgetItem(str(zak[i][j])))

        self.tableWidget_zakaz.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Товар", "Количество(шт)", "Дата заказа", "Статус заказа"])


    def naiti(self):
        text_to_find = self.lineEdit_stroka_poiska.text()
        if not text_to_find:
            return

        rows = self.tableWidget_zakaz.rowCount()
        for row in range(rows):
            for column in range(self.tableWidget_zakaz.columnCount()):
                item = self.tableWidget_zakaz.item(row, column)
                if item and text_to_find.lower() in item.text().lower():
                    for col in range(self.tableWidget_zakaz.columnCount()):
                        self.tableWidget_zakaz.item(row, col).setBackground(QtGui.QColor("#42aaff"))
                    return


    def updata_status(self):
        id = self.lineEdit_id.text()
        status = self.lineEdit_status.text()
        cursor.execute(f'UPDATE `Customers` SET `OrderStatus` = "{status}" WHERE `id` = "{id}" ')
        db.commit()

        cursor.execute(f'select `id`,`FullName`,`Phone`, `Tovar`, `kol`, `OrderDate`,`OrderStatus` from Customers')
        zak = cursor.fetchall()
        self.tableWidget_zakaz.clear()
        self.tableWidget_zakaz.setRowCount(len(zak))
        for i in range(len(zak)):
            for j in range(7):
                self.tableWidget_zakaz.setItem(i, j, QtWidgets.QTableWidgetItem(str(zak[i][j])))

        self.tableWidget_zakaz.setHorizontalHeaderLabels(["ID", "ФИО", "Телефон", "Товар", "Количество(шт)", "Дата заказа", "Статус заказа"])

    def add_tov(self):
        art = self.lineEdit_articyl_tov.text()
        name = self.lineEdit_name_tov.text()
        kateg = self.lineEdit_katagory_tov.text()
        cena = self.lineEdit_price_tov.text()
        data = self.lineEdit_dataofman_tov.text()
        exp = self.lineEdit_expirydata_tov.text()
        man = self.lineEdit_manyfacture_tov.text()
        ountr = self.lineEdit_ountry_tov.text()
        cursor.execute(f'INSERT INTO Products VALUES ("{art}", "{name}", "{kateg}", "{cena}",  "{data}", "{exp}", "{man}", "{ountr}")')
        db.commit()

        cursor.execute(f'select `ArticleNumber`,`ProductName`,`Category`,`Price`,`DateOfManufacture`,`ExpiryDate`,`Manufacturer`,`CountryOfOrigin` from Products ')
        tov = cursor.fetchall()
        self.tableWidget_tovar.clear()
        self.tableWidget_tovar.setRowCount(len(tov))
        for i in range(len(tov)):
            for j in range(8):
                self.tableWidget_tovar.setItem(i, j, QtWidgets.QTableWidgetItem(str(tov[i][j])))

        self.tableWidget_tovar.setHorizontalHeaderLabels(["Артикул", "Наименование", "Категория", "Цена", "Дата изготовления", "Срок годности", "Производитель",
             "Страна производства"])


    def del_tov(self):
        artycl = self.lineEdit_articyl_tov.text()
        cursor.execute(f' DELETE FROM Products WHERE ArticleNumber = "{artycl}" ')
        db.commit()

        cursor.execute(f'select `ArticleNumber`,`ProductName`,`Category`,`Price`,`DateOfManufacture`,`ExpiryDate`,`Manufacturer`,`CountryOfOrigin` from Products ')
        tov = cursor.fetchall()
        self.tableWidget_tovar.clear()
        self.tableWidget_tovar.setRowCount(len(tov))
        for i in range(len(tov)):
            for j in range(8):
                self.tableWidget_tovar.setItem(i, j, QtWidgets.QTableWidgetItem(str(tov[i][j])))

        self.tableWidget_tovar.setHorizontalHeaderLabels(["Артикул", "Наименование", "Категория", "Цена", "Дата изготовления", "Срок годности", "Производитель",
             "Страна производства"])


    def dop_sotr(self):
        fio = self.lineEdit_fio_sotr.text()
        data = self.lineEdit_databirth_sotr.text()
        tel = self.lineEdit_phone_sotr.text()
        adress = self.lineEdit_address_sotr.text()

        cursor.execute(f'INSERT INTO Employees VALUES ("{fio}", "{data}", "{tel}", "{adress}")')
        db.commit()

        cursor.execute(f'select `FullName`,`DateOfBirth`,`Phone`,`Address` from Employees ')
        sotr = cursor.fetchall()
        print(sotr[0])
        self.tableWidget_sotrydnik.clear()
        self.tableWidget_sotrydnik.setRowCount(len(sotr))
        for i in range(len(sotr)):
            for j in range(4):
                self.tableWidget_sotrydnik.setItem(i, j, QtWidgets.QTableWidgetItem(str(sotr[i][j])))

        self.tableWidget_sotrydnik.setHorizontalHeaderLabels(["ФИО", "Дата рождения", "Телефон", "Адресс"])

    def del_sotr(self):
        fio = self.lineEdit_fio_sotr.text()
        cursor.execute(f' DELETE FROM Employees WHERE FullName = "{fio}" ')
        db.commit()

        cursor.execute(f'select `FullName`,`DateOfBirth`,`Phone`,`Address` from Employees ')
        sotr = cursor.fetchall()
        print(sotr[0])
        self.tableWidget_sotrydnik.clear()
        self.tableWidget_sotrydnik.setRowCount(len(sotr))
        for i in range(len(sotr)):
            for j in range(4):
                self.tableWidget_sotrydnik.setItem(i, j, QtWidgets.QTableWidgetItem(str(sotr[i][j])))

        self.tableWidget_sotrydnik.setHorizontalHeaderLabels(["ФИО", "Дата рождения", "Телефон", "Адресс"])

    def add_prodaja(self):
        fioklienta = self.lineEdit_klient.text()
        fiosotr = self.lineEdit_sotr.text()
        tovar = self.lineEdit_tov_and_kol.text()
        dataprod = self.lineEdit_data_prodaji.text()
        oplata = self.lineEdit_sposob_oplat.text()

        cursor.execute(f'INSERT INTO Prodaji VALUES ("{fioklienta}", "{fiosotr}", "{tovar}", "{dataprod}", "{oplata}")')
        db.commit()

        cursor.execute(f'select `Klient`,`employees`,`tovar`,`dataProdaji`,`sposob` from Prodaji ')
        sotr = cursor.fetchall()
        print(sotr[0])
        self.tableWidget_prodaji.clear()
        self.tableWidget_prodaji.setRowCount(len(sotr))
        for i in range(len(sotr)):
            for j in range(5):
                self.tableWidget_prodaji.setItem(i, j, QtWidgets.QTableWidgetItem(str(sotr[i][j])))

        self.tableWidget_prodaji.setHorizontalHeaderLabels(
            ["Клиент", "Сотрудник", "Товары и их кол-во", "Дата продажи", "Способ оплаты"])

    def del_prodaja(self):
        fio = self.lineEdit_klient.text()
        cursor.execute(f' DELETE FROM Prodaji WHERE Klient = "{fio}" ')
        db.commit()

        cursor.execute(f'select `Klient`,`employees`,`tovar`,`dataProdaji`,`sposob` from Prodaji ')
        sotr = cursor.fetchall()
        print(sotr[0])
        self.tableWidget_prodaji.clear()
        self.tableWidget_prodaji.setRowCount(len(sotr))
        for i in range(len(sotr)):
            for j in range(5):
                self.tableWidget_prodaji.setItem(i, j, QtWidgets.QTableWidgetItem(str(sotr[i][j])))

        self.tableWidget_prodaji.setHorizontalHeaderLabels(
            ["Клиент", "Сотрудник", "Товары и их кол-во", "Дата продажи", "Способ оплаты"])

class Zakaz(QtWidgets.QMainWindow, zakaz.Ui_MainWindow):
    def __init__(self):
        super(Zakaz, self).__init__()
        self.setupUi(self)

        self.pushButton_ofzakaz.pressed.connect(self.add_zakaz)
        self.product_name()

    def product_name(self):
        cursor.execute(f'select `ProductName` from Products ')
        tovar = cursor.fetchall()
        self.comboBox_prodyct.clear()
        for tov in tovar:
            self.comboBox_prodyct.addItem(tov[0])

    def add_zakaz(self):
        fio = self.lineEdit_fio.text()
        tel = self.lineEdit_phone.text()
        tov = self.comboBox_prodyct.currentText()
        kol = self.lineEdit_kol.text()
        cursor.execute(f'INSERT INTO Customers VALUES (`id`,"{fio}", "{tel}", "{tov}", "{kol}",utc_date(), "Новый")')
        db.commit()

        self.showMessageBox("")


    def showMessageBox(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Заказ оформлен")
        msg.setInformativeText(message)
        msg.setWindowTitle("Информация")
        msg.exec_()





App = QtWidgets.QApplication([])
window = ReAv()
window.show()
App.exec()