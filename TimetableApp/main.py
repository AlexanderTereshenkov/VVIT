import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout,
QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox, QScrollArea, QLineEdit, QLabel)


class EditWindow(QWidget):
    def __init__(self):
        super(EditWindow, self).__init__()
        self.vl = QVBoxLayout(self)

        self.subName = QLineEdit()
        self.time = QLineEdit()
        self.task = QLineEdit()
        self.numb = QLineEdit()
        self.name = QLineEdit()
        self.pairCount = QLineEdit()
        self.week = QLineEdit()

        self.vl.addWidget(self.subName)
        self.vl.addWidget(self.time)
        self.vl.addWidget(self.task)
        self.vl.addWidget(self.numb)
        self.vl.addWidget(self.name)
        self.vl.addWidget(self.pairCount)
        self.vl.addWidget(self.week)
        self.update_button = QPushButton("Изменить", self)
        self.update_button.clicked.connect(lambda: self.update_table())
        self.vl.addWidget(self.update_button)

    def set_text(self, text):
        self.t = text
        if(text[0] != '-'):
            self.subName.setText(text[0])
            self.time.setText(text[1])
            self.task.setText(text[2])
            self.numb.setText(text[3])
            self.name.setText(text[4])
            self.pairCount.setText(str(text[7]))
            self.week.setText(text[6])
        else:
            self.subName.setText('Название предмета')
            self.time.setText('Время проведения')
            self.task.setText('пракика/лаб./лекция')
            self.numb.setText('Аудитория')
            self.name.setText('Преподаватель')
            self.pairCount.setText(str(text[7]))
            self.week.setText('четная/нечетная')

    def update_table(self):
        w = MainWindow()
        new_table = [self.subName.text(), self.time.text(), self.task.text(), self.numb.text(), self.name.text(),
                     self.pairCount.text(), self.week.text()]
        w.change_table(new_table, self.t)
        QMessageBox.about(self, "", "Успешно")


class EditTeacherWindow(QWidget):
    def __init__(self):
        super(EditTeacherWindow, self).__init__()
        self.vvbox = QVBoxLayout(self)

        self.t_name = QLineEdit()
        self.s_name = QLineEdit()
        self.s_task = QLineEdit()

        self.vvbox.addWidget(self.t_name)
        self.vvbox.addWidget(self.s_name)
        self.vvbox.addWidget(self.s_task)

        self.ok_btn = QPushButton("Ок")
        self.ok_btn.clicked.connect(lambda: self.update_teacher())
        self.vvbox.addWidget(self.ok_btn)

    def set_text(self, text):
        self.old_t = text
        if text[0] != '-':
            self.t_name.setText(text[0])
            self.s_name.setText(text[1])
            self.s_task.setText(text[2])
        else:
            self.t_name.setText("Имя преподавателя")
            self.s_name.setText("Название предмета")
            self.s_task.setText("пракика/лаб./лекция")

    def update_teacher(self):
        new_t = [self.t_name.text(), self.s_name.text(), self.s_task.text(), self.old_t[3]]
        w = MainWindow()
        w.update_teacher(new_t, self.old_t)
        QMessageBox.about(self, "", "Успешно")


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect_to_DB()
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self.create_shedule_tab()


    def connect_to_DB(self):
        self.conn = psycopg2.connect(
            database="timetable",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

    def create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.shedule_tab1 = QWidget()
        self.teacher_tab = QWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area_1 = QScrollArea()
        self.scroll_area_2 = QScrollArea()

        self.tabs.addTab(self.scroll_area, "Четная неделя")
        self.tabs.addTab(self.scroll_area_1, "Нечетная неделя")
        self.tabs.addTab(self.scroll_area_2, "Преподаватели")

        self.m_gbox = QGroupBox("Понедельник")
        self.t_gbox = QGroupBox("Вторник")
        self.w_gbox = QGroupBox("Среда")
        self.th_gbox = QGroupBox("Четверг")
        self.f_gbox = QGroupBox("Пятница")
        self.st_gbox = QGroupBox("Суббота")

        self.m1_gbox = QGroupBox("Понедельник")
        self.t1_gbox = QGroupBox("Вторник")
        self.w1_gbox = QGroupBox("Среда")
        self.th1_gbox = QGroupBox("Четверг")
        self.f1_gbox = QGroupBox("Пятница")
        self.st1_gbox = QGroupBox("Суббота")

        self.teacher_gbox = QGroupBox("Преподаватели")

        self.teacher_box = QVBoxLayout()
        self.teacher_hbox = QHBoxLayout()
        self.upd_teacher = QHBoxLayout()

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()
        self.shbox5 = QHBoxLayout()
        self.shbox6 = QHBoxLayout()
        self.shbox_button = QHBoxLayout()

        self.svbox1 = QVBoxLayout()
        self.shbox11 = QHBoxLayout()
        self.shbox22 = QHBoxLayout()
        self.shbox33 = QHBoxLayout()
        self.shbox44 = QHBoxLayout()
        self.shbox55 = QHBoxLayout()
        self.shbox66 = QHBoxLayout()
        self.shbox_button1 = QHBoxLayout()

        self.svbox2 = QVBoxLayout()

        self.teacher_box.addLayout(self.teacher_hbox)
        self.teacher_hbox.addWidget(self.teacher_gbox)
        self.teacher_box.addLayout(self.upd_teacher)

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)
        self.svbox.addLayout(self.shbox5)
        self.svbox.addLayout(self.shbox6)
        self.svbox.addLayout(self.shbox_button)

        self.svbox1.addLayout(self.shbox11)
        self.svbox1.addLayout(self.shbox22)
        self.svbox1.addLayout(self.shbox33)
        self.svbox1.addLayout(self.shbox44)
        self.svbox1.addLayout(self.shbox55)
        self.svbox1.addLayout(self.shbox66)
        self.svbox1.addLayout(self.shbox_button1)

        self.shbox11.addWidget(self.m1_gbox)
        self.shbox22.addWidget(self.t1_gbox)
        self.shbox33.addWidget(self.w1_gbox)
        self.shbox44.addWidget(self.th1_gbox)
        self.shbox55.addWidget(self.f1_gbox)
        self.shbox66.addWidget(self.st1_gbox)

        self.shbox1.addWidget(self.m_gbox)
        self.shbox2.addWidget(self.t_gbox)
        self.shbox3.addWidget(self.w_gbox)
        self.shbox4.addWidget(self.th_gbox)
        self.shbox5.addWidget(self.f_gbox)
        self.shbox6.addWidget(self.st_gbox)

        self.create_week_table()
        self.create_teacher_table()

        self.update_shedule_button = QPushButton("Обновить")
        self.update_shedule_button1 = QPushButton("Обновить")
        self.update_tc_btn = QPushButton("Обновить")
        self.add_btn = QPushButton("Добавить")
        self.shbox_button.addWidget(self.update_shedule_button)
        self.shbox_button1.addWidget(self.update_shedule_button1)
        self.upd_teacher.addWidget(self.update_tc_btn)
        self.upd_teacher.addWidget(self.add_btn)

        self.shedule_tab.setLayout(self.svbox)
        self.scroll_area.setWidget(self.shedule_tab)
        self.shedule_tab1.setLayout(self.svbox1)
        self.scroll_area_1.setWidget(self.shedule_tab1)

        self.teacher_tab.setLayout(self.teacher_box)
        self.scroll_area_2.setWidget(self.teacher_tab)

        self.update_shedule_button.clicked.connect(lambda: self.update_layout())
        self.update_shedule_button1.clicked.connect(lambda: self.update_layout())
        self.update_tc_btn.clicked.connect(lambda: self.update_layout())
        self.add_btn.clicked.connect(lambda: self.change_teacher(['-', '-', '-', '-1']))


    def create_week_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(7)
        self.monday_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.monday_table = self.update_day_table("Понедельник", self.monday_table, 'четная')
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.m_gbox.setLayout(self.mvbox)

        self.t_table = QTableWidget()
        self.t_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.t_table.setColumnCount(7)
        self.t_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.t_table = self.update_day_table('Вторник', self.t_table, 'четная')
        self.tvbox = QVBoxLayout()
        self.tvbox.addWidget(self.t_table)
        self.t_gbox.setLayout(self.tvbox)

        self.w_table = QTableWidget()
        self.w_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.w_table.setColumnCount(6)
        self.w_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.w_table = self.update_day_table('Среда', self.w_table, 'четная')
        self.wvbox = QVBoxLayout()
        self.wvbox.addWidget(self.w_table)
        self.w_gbox.setLayout(self.wvbox)

        self.th_table = QTableWidget()
        self.th_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.th_table.setColumnCount(7)
        self.th_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.th_table = self.update_day_table('Четверг', self.th_table, 'четная')
        self.thvbox = QVBoxLayout()
        self.thvbox.addWidget(self.th_table)
        self.th_gbox.setLayout(self.thvbox)

        self.f_table = QTableWidget()
        self.f_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.f_table.setColumnCount(7)
        self.f_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.f_table = self.update_day_table('Пятница', self.f_table, 'четная')
        self.fvbox = QVBoxLayout()
        self.fvbox.addWidget(self.f_table)
        self.f_gbox.setLayout(self.fvbox)

        self.st_table = QTableWidget()
        self.st_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.st_table.setColumnCount(7)
        self.st_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.st_table = self.update_day_table('Суббота', self.st_table, 'четная')
        self.stvbox = QVBoxLayout()
        self.stvbox.addWidget(self.st_table)
        self.st_gbox.setLayout(self.stvbox)

        self.monday_table1 = QTableWidget()
        self.monday_table1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table1.setColumnCount(7)
        self.monday_table1.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.monday_table1 = self.update_day_table("Понедельник", self.monday_table1, 'нечетная')
        self.mvbox1 = QVBoxLayout()
        self.mvbox1.addWidget(self.monday_table1)
        self.m1_gbox.setLayout(self.mvbox1)

        self.t1_table = QTableWidget()
        self.t1_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.t1_table.setColumnCount(7)
        self.t1_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.t1_table = self.update_day_table('Вторник', self.t1_table, 'нечетная')
        self.tvbox1 = QVBoxLayout()
        self.tvbox1.addWidget(self.t1_table)
        self.t1_gbox.setLayout(self.tvbox1)

        self.w1_table = QTableWidget()
        self.w1_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.w1_table.setColumnCount(7)
        self.w1_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.w1_table = self.update_day_table('Среда', self.w1_table, 'нечетная')
        self.wvbox1 = QVBoxLayout()
        self.wvbox1.addWidget(self.w1_table)
        self.w1_gbox.setLayout(self.wvbox1)

        self.th1_table = QTableWidget()
        self.th1_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.th1_table.setColumnCount(7)
        self.th1_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.th1_table = self.update_day_table('Четверг', self.th1_table, 'нечетная')
        self.thvbox1 = QVBoxLayout()
        self.thvbox1.addWidget(self.th1_table)
        self.th1_gbox.setLayout(self.thvbox1)

        self.f1_table = QTableWidget()
        self.f1_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.f1_table.setColumnCount(7)
        self.f1_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.f1_table = self.update_day_table('Пятница', self.f1_table, 'нечетная')
        self.fvbox1 = QVBoxLayout()
        self.fvbox1.addWidget(self.f1_table)
        self.f1_gbox.setLayout(self.fvbox1)

        self.st1_table = QTableWidget()
        self.st1_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.st1_table.setColumnCount(7)
        self.st1_table.setHorizontalHeaderLabels(["Предмет", "Время", "", "Кабинет", "Преподаватель", "", ""])
        self.st1_table = self.update_day_table('Суббота', self.st1_table, 'нечетная')
        self.stvbox1 = QVBoxLayout()
        self.stvbox1.addWidget(self.st1_table)
        self.st1_gbox.setLayout(self.stvbox1)

    def update_layout(self):
        self.vbox.removeWidget(self.tabs)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self.create_shedule_tab()

    def update_day_table(self, day, monday_table, week):
        self.cursor.execute("SELECT DISTINCT(s.name), tt.room_numb, tt.start_time, tc.full_name, tt.task, tt.paire_count, tt.week, "
                            "tt.id, tt.day_name "
                       "FROM subject s, timetable tt, teacher tc "
                       "WHERE tt.day_name=%s AND tt.week=%s AND s.id = tt.subject AND tc.subject=s.id "
                       "AND tc.task=tt.task "
                       "ORDER BY tt.paire_count", (day, week))
        records = list(self.cursor.fetchall())
        records2 = self.make_table_list(records)
        monday_table.setRowCount(5)
        for i in range(5):
            if records2[i] == 'Пар нет':
                monday_table.setItem(i, 0, QTableWidgetItem('-'))
                monday_table.setItem(i, 1, QTableWidgetItem('-'))
                monday_table.setItem(i, 2, QTableWidgetItem('-'))
                monday_table.setItem(i, 3, QTableWidgetItem('-'))
                monday_table.setItem(i, 4, QTableWidgetItem('-'))
                joinButton = QPushButton("Добавить")
                monday_table.setCellWidget(i, 5, joinButton)
            else:
                temp = records2[i]
                monday_table.setItem(i, 0, QTableWidgetItem(temp[0]))
                monday_table.setItem(i, 1, QTableWidgetItem(temp[1]))
                monday_table.setItem(i, 2, QTableWidgetItem(temp[2]))
                monday_table.setItem(i, 3, QTableWidgetItem(temp[3]))
                monday_table.setItem(i, 4, QTableWidgetItem(temp[5]))
                joinButton = QPushButton("Изменить")
                monday_table.setCellWidget(i, 5, joinButton)
                deleteButton = QPushButton("Удалить")
                monday_table.setCellWidget(i, 6, deleteButton)
                deleteButton.clicked.connect(lambda ch, id_delete=records2[i][7]: self.delete_row(id_delete))

            if records2[i][4] == 'четная':
                s = 'четная'
            elif records2[i][4] == 'нечетная':
                s = 'нечетная'
            else:
                s = '-'
            if records2[i] == 'Пар нет':
                sc = i + 1
                right_id = -1
            else:
                sc = records2[i][6]
                right_id = records2[i][7]

            joinButton.clicked.connect(lambda ch, num=i, week=s, table=monday_table, subject_count=sc,
                                              id=right_id, dayD=day:
                                       self.change_day_from_table(num, week, table, subject_count, id, dayD))

            monday_table.resizeRowsToContents()
        return monday_table

    def change_day_from_table(self, rowNum, week, monday_table, subject_count, id, day):
        row = list()
        for i in range(monday_table.columnCount()):
            try:
                row.append(monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            if row.count(None) == 2:
                del row[-1]
            row.append(week)
            row.append(subject_count)
            row.append(rowNum)
            row.append(id)
            row.append(day)
            self.w = EditWindow()
            self.w.set_text(row)
            self.w.show()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def change_table(self, nt, old_table):
        subName = nt[0]
        time = nt[1]
        task = nt[2]
        numb = nt[3]
        name = nt[4]
        pairCount = nt[5]
        week = nt[6]
        t_id = str(old_table[9])
        if t_id != "-1":
            self.cursor.execute("SELECT * FROM subject WHERE subject.name=%s", (subName, ))
            sub = list(self.cursor.fetchall())
            print(sub)
            if sub:
                self.cursor.execute("SELECT teacher.full_name FROM teacher WHERE teacher.full_name=%s AND "
                                    "teacher.task=%s", (name, task))
                if len(self.cursor.fetchall()) == 0:
                    self.cursor.execute("DELETE FROM teacher WHERE teacher.subject=%s AND teacher.task=%s", (sub[0][0], task))
                    self.conn.commit()
                    self.cursor.execute("INSERT INTO teacher(full_name, subject, task) VALUES "
                                        "(%s, %s, %s)", (name, sub[0][0], task))
                    self.conn.commit()

                self.cursor.execute("UPDATE timetable SET subject=subject.id, "
                                    "week=%s, "
                                    "room_numb=%s, "
                                    "start_time=%s, "
                                    "task=%s, "
                                    "paire_count=%s "
                                    "FROM subject "
                                    "WHERE subject.name=%s and timetable.id=%s;", (week, numb, time, task, pairCount,
                                                                                  subName, t_id))
                self.conn.commit()
            else:
                self.cursor.execute("SELECT * FROM subject")
                max_id = self.cursor.fetchall()
                self.cursor.execute("INSERT INTO subject (name) values (%s, %s)", (len(max_id)+1, subName))
                self.conn.commit()
                self.cursor.execute("SELECT subject.id FROM subject WHERE subject.name=%s", (subName,))
                sub_id = self.cursor.fetchall()
                self.cursor.execute("SELECT teacher.full_name FROM teacher WHERE teacher.full_name=%s", (name,))
                if len(self.cursor.fetchall()) == 0:
                    self.cursor.execute("INSERT INTO teacher(full_name, subject, task) values"
                                        " (%s, %s, %s)", (name, sub_id[0][0], task))
                    self.conn.commit()
                self.cursor.execute("UPDATE timetable SET subject=subject.id, "
                                    "week=%s, "
                                    "room_numb=%s, "
                                    "start_time=%s, "
                                    "task=%s, "
                                    "paire_count=%s "
                                    "FROM subject "
                                    "WHERE subject.name=%s and timetable.id=%s;", (week, numb, time, task, pairCount,
                                                                                  subName, t_id))
                self.conn.commit()

        else:
            days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
            self.cursor.execute("SELECT subject.id FROM subject WHERE subject.name=%s", (subName, ))
            sub_id = self.cursor.fetchall()
            if len(sub_id) == 0:
                self.cursor.execute("SELECT * FROM subject")
                max_id = self.cursor.fetchall()
                self.cursor.execute("INSERT INTO subject VALUES (%s, %s)", (len(max_id)+1, subName))
                self.conn.commit()
                self.cursor.execute("SELECT subject.id FROM subject WHERE subject.name=%s", (subName,))
                sub_id = self.cursor.fetchall()
            self.cursor.execute("INSERT INTO teacher(full_name, subject, task) values"
                                " (%s, %s, %s)", (name, sub_id[0][0], task))
            self.conn.commit()
            self.cursor.execute("INSERT INTO timetable(day_name, subject, week, room_numb, start_time, "
                                "task, paire_count, day_count) values "
                                "(%s, %s, %s, %s, %s, %s, %s, %s)", (old_table[10], sub_id[0][0],
                                                                     week, numb, time, task, pairCount, days.index(old_table[10])+1))
            self.conn.commit()

    def make_table_list(self, records):
        s = ['Пар нет', 'Пар нет', 'Пар нет', 'Пар нет', 'Пар нет']
        t = records
        k = 1
        if len(t) == 0:
            return s
        else:
            u = 0
            for i in range(5):
                if k == t[u][5]:
                    s[i] = [t[u][0], t[u][2], t[u][4], t[u][1], t[u][6], t[u][3], t[u][5], t[u][7], t[u][8]]
                    k += 1
                    if u < len(t) - 1:
                        u += 1
                else:
                    k += 1
        return s

    def delete_row(self, id_delete):
        self.cursor.execute("DELETE FROM timetable WHERE timetable.id = %s", (id_delete, ))
        self.conn.commit()

    def create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["Имя", "Предмет", "", "", ""])
        self.cursor.execute("SELECT * from teacher")
        teachers = self.cursor.fetchall()
        self.teacher_table = self.create_tc_table(self.teacher_table, teachers)
        self.teacherbox = QVBoxLayout()
        self.teacherbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.teacherbox)

    def create_tc_table(self, table, teachers):
        table.setRowCount(len(teachers))
        text = ['-', '-', '-']
        for i in range(len(teachers)):
            self.cursor.execute("SELECT subject.name FROM subject where subject.id=%s", (teachers[i][2], ))
            subjects = self.cursor.fetchall()
            table.setItem(i, 0, QTableWidgetItem(teachers[i][1]))
            table.setItem(i, 1, QTableWidgetItem(subjects[0][0]))
            table.setItem(i, 2, QTableWidgetItem(teachers[i][3]))
            update_btn = QPushButton("Измнеить")
            delete_btn = QPushButton("Удалить")
            table.setCellWidget(i, 3, update_btn)
            table.setCellWidget(i, 4, delete_btn)
            delete_btn.clicked.connect(lambda ch, t_id=teachers[i][0]: self.delete_teacher(t_id))
            text = [teachers[i][1], subjects[0][0], teachers[i][3], teachers[i][0]]
            update_btn.clicked.connect(lambda ch, text_t=text: self.change_teacher(text_t))
        table.resizeRowsToContents()
        return table

    def change_teacher(self, text):
        self.w2 = EditTeacherWindow()
        self.w2.set_text(text)
        self.w2.show()

    def delete_teacher(self, t_id):
        self.cursor.execute("DELETE FROM teacher WHERE teacher.id=%s", (t_id, ))
        self.conn.commit()

    def update_teacher(self, new_t, old_t):
        t_name = new_t[0]
        s_name = new_t[1]
        s_task = new_t[2]
        s_id = new_t[3]
        sub_id = 0
        if s_id == -1:
            self.cursor.execute("SELECT * FROM subject where subject.name=%s", (s_name, ))
            subs = self.cursor.fetchall()
            if len(subs) == 0:
                self.cursor.execute("SELECT * FROM subject")
                new_id = self.cursor.fetchall()
                sub_id = len(new_id) + 1
                self.cursor.execute("INSERT INTO subject (id, name) VALUES (%s, %s)", (sub_id, s_name))
                self.conn.commit()
            self.cursor.execute("SELECT * FROM teacher")
            max_t_id = self.cursor.fetchall()
            self.cursor.execute("INSERT INTO teacher(id, full_name, subject, task) VALUES (%s, %s, %s, %s)"
                                , (len(max_t_id) + 1, t_name, sub_id, s_task))
            self.conn.commit()
        else:
            self.cursor.execute("SELECT * FROM subject where subject.name=%s", (s_name, ))
            subs = self.cursor.fetchall()
            if len(subs) == 0:
                self.cursor.execute("SELECT * FROM subject")
                new_id = self.cursor.fetchall()
                sub_id = len(new_id) + 1
                self.cursor.execute("INSERT INTO subject (id, name) VALUES (%s, %s)", (sub_id, s_name))
                self.conn.commit()
            self.cursor.execute("SELECT * FROM teacher WHERE teacher.full_name=%s", (t_name, ))
            teachers = self.cursor.fetchall()
            if len(teachers) == 0:
                self.cursor.execute("SELECT * FROM teacher")
                max_id = 0
                max_t_id = self.cursor.fetchall()
                for elem in max_t_id:
                    if elem[0] > max_id:
                        max_id = elem[0]

                self.cursor.execute("SELECT * FROM subject where subject.name=%s", (s_name,))
                subs = self.cursor.fetchall()
                self.cursor.execute("INSERT INTO teacher(id, full_name, subject, task) VALUES "
                                    "(%s, %s, %s, %s)", (max_id+1, t_name, subs[0][0], s_task))
                self.conn.commit()
            self.cursor.execute("SELECT * FROM subject where subject.name=%s", (s_name,))
            subs = self.cursor.fetchall()
            self.cursor.execute("UPDATE teacher SET full_name=%s"
                                ", subject=%s, task=%s WHERE teacher.id=%s", (t_name, subs[0][0],
                                                                                              s_task, s_id))
            self.conn.commit()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
