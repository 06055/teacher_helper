import mysql.connector
from flask import request,Flask,render_template
import re

login = ''
password = ''
id_user = 0
id_subject = 0
spisok_global_predmot = list()
spisok_predm = list()


app = Flask(__name__)




@app.route('/')
def main_window():

    return render_template('main_window.html')


@app.route('/logining')
def log():

    return render_template("parrents_log_reg.html")

def is_valid_email(email):

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


@app.route('/get_login_password', methods = ['POST','GET'])
def take_log_password():
    listok_loginov = list()
    spisok_predmetov = list()
    global id_user
    global get_id_from_window_add_predmet
    global login
    global password
    global spisok_global_predmot

    site_perem = "parrents_log_reg.html"

    rezult = 'Не всі поля заповнені'
    if login == '' and password == '':

        login = request.form['login']
        password = request.form['password']


    if login != '' and password != '':

        
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""SELECT id,name,last_name,number,email FROM user_information WHERE email = '{login}' and password = Sha1('{password}')"""

        cursor.execute(_SQL)
        log_user =  cursor.fetchall()

        if len(log_user) == 1:

            rezult = 'Ви успішно увійшли до облікового запису'
            site_perem = "items_window.html"

            for i in log_user:
                id_user = i[0]
                listok_loginov.append(i)

            _SQL = f"""select teach_predm.id as id_pred,name_predm from teach_predm inner join relatin_teachers_predmet on teach_predm.id=relatin_teachers_predmet.id_predmet WHERE id_user_teacher={id_user}"""
            cursor.execute(_SQL)
            name_predmet = cursor.fetchall()
            for i in name_predmet:
                spisok_predmetov.append(i)
                spisok_global_predmot.append(i)

        else:
            rezult = 'Невірний логін або пароль'
            login = ''
            password = ''


    return render_template(site_perem,therezult = rezult, thelistok_loginov = listok_loginov,thespisok_predmetov = spisok_predmetov)




@app.route('/registration')
def registration():

    return render_template('registration.html')

    
@app.route('/register', methods=['POST'])
def take_reg():
    successful = ''
    
    rezult_gmail = ''
    count = 0
    name = request.form['name']
    last_name = request.form['last_name']
    number = request.form['number']
    gmail = request.form['gmail']
    password = request.form['password']
    done = ''
    password_povtor = request.form['password_povtor']


    if not is_valid_email(gmail):
        return render_template('registration.html', therezult_gmail="Введена невалидная почта", thedone=done)

    if name != '' and last_name != '' and number != '' and gmail != '':
        rezult_login = ''

    
    if password == password_povtor:
        rezult_password = ''
    elif password != password_povtor:
        rezult_password = 'Введенный пароль не совпадает'
    
    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()
    _SQL = """SELECT email FROM user_information"""
    cursor.execute(_SQL)
    rezult = cursor.fetchall()
    for i in rezult:
        if i[0].lower() == gmail.lower():
            count = 1

    if count == 1:
        rezult_gmail = 'Такая почта уже зарегистрирована'
    else:
        if rezult_password == '':
            _SQL = """INSERT INTO user_information(name,last_name,number,email,password) VALUES (%s,%s,%s,%s,SHA1(%s))"""
            
            cursor.execute(_SQL,(name,last_name,number,gmail,password))
            dbc.commit()

            cursor.close()
            dbc.close()
            successful = 'Ваш аккаунт успешно создан'

            done = "yes"

    return render_template('registration.html', therezult_password=rezult_password, therezult_login='', thesuccessful=successful, therezult_gmail=rezult_gmail, thedone=done)

@app.route('/show_teach_predm')
def show_teach_predm():
    #Можно сделать глобальным и не париться 
    global spisok_predm
    
    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()

    _SQL = """SELECT name_predm FROM teach_predm """
    cursor.execute(_SQL)
    rezult = cursor.fetchall()

    for i in rezult:

        spisok_predm.append(i)


    return render_template('items_window.html',thespisok_predm = spisok_predm)




@app.route('/okno_dobavlenia_in_windows')
def okno_dobavlenia_in_windows():
    global id_user
    global spisok_global_predmot
    global id_subject

    spisok_predmets = list()
    spisok_predmeto_imeet = list()
    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()

    _SQL="""SELECT * FROM teach_predm"""

    cursor.execute(_SQL)
    predmets = cursor.fetchall()



    for i in predmets:
        if i in spisok_global_predmot:

            spisok_predmeto_imeet.append(i)

        else:
            spisok_predmets.append(i)

    return render_template('window_add_predmet.html',thespisok_predmets = spisok_predmets, thespisok_predmeto_imeet = spisok_predmeto_imeet, theid_subject = id_subject)


@app.route('/predmet')
def poluchenie_id_from_window():
    global id_user
    get_id_from_window_add_predmet= request.args.get('id')
    successful = 'Сталася помилка'

    if get_id_from_window_add_predmet != '' and id_user != 0:
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """INSERT INTO relatin_teachers_predmet(id_user_teacher,id_predmet) VALUES(%s,%s)"""
        cursor.execute(_SQL,(id_user,get_id_from_window_add_predmet))
        dbc.commit()
        successful = 'Предмет був успішно добавлений'
        radio_yes_no = 'no'
    return render_template('window_add_predmet.html',thesuccessful = successful, theradio_yes_no = radio_yes_no)


@app.route('/show_dobavlenie_predm')
def show_dobavlenie_predm():

    return render_template('menu_dobavlenie.html')



@app.route('/dobavlenie_predm', methods = ['POST'])
def dobavlenie_predm():
    global id_user
    

    get_predmet = request.form['get_predmet']
    if id_user != 0:

        if get_predmet != '':

            dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
            dbc = mysql.connector.connect(**dbconfig)
            cursor = dbc.cursor()

            _SQL = """INSERT INTO teach_predm(name_predm) VALUES (%s)"""
            cursor.execute(_SQL,(get_predmet,))

            dbc.commit()


            cursor.close()
            dbc.close() 
            itog_delete = 'Успішно добавлений предмет'
            radio_yes_no = 'no'


    return render_template('menu_dobavlenie.html',theitog_delete = itog_delete, theradio_yes_no = radio_yes_no)


@app.route('/predmet_show', methods = ['GET'])
def predmet_click():
    global id_user
    global id_subject
    spisok_studentov = list()
    list_name = list()

    id_subject = request.args.get('id_predmet') #Получаю ID по клику на предмет это для того что-бы сделать связь между предметом и студентом


    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
    dbc = mysql.connector.connect(** dbconfig)
    cursor = dbc.cursor()
    if id_subject != 0:

        _SQL = f"""SELECT ts.id, ts.name, ts.last_name, ts.year_st, ts.number_phone, ts.progress_bar FROM relation_predmet_students rs JOIN teach_predm tp ON rs.id_predmet = tp.id JOIN teach_students ts ON rs.id_student = ts.id WHERE rs.id_teacher = {id_user} AND rs.id_predmet = {id_subject}"""

        cursor.execute(_SQL)
        
        studentov_get = cursor.fetchall()

        for i in studentov_get:
            spisok_studentov.append(i)


        _SQL = f"""SELECT name_predm FROM teach_predm WHERE id = {id_subject} """
        cursor.execute(_SQL)
        rezult = cursor.fetchall()
        for g in rezult:
            list_name.append(g)
        list_name = list_name[0]
    return render_template('window_students.html',thespisok_studentov = spisok_studentov, the_id_predmet = id_subject, thelist_name = list_name)



@app.route('/stud_person_information')
def stud_person_information():
    global id_subject
    global id_user
    id_stud = request.args.get('id')
    list_have_zero_done = list()
    list_total_thems = list()
    spisok_person_infa = list()
    list_first_thema = list()
    list_name_thems = list()
    if id_stud != 0:
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL=f"""SELECT * FROM teach_students WHERE id = '{id_stud}' """
        cursor.execute(_SQL)

        info_stud = cursor.fetchall()

        for i in info_stud:
            spisok_person_infa.append(i)

        
        _SQL = f"""SELECT progress_bar FROM relation_sybject_user_predmet_stud WHERE id_predmet = {id_subject} AND id_user = {id_user} AND id_student = {id_stud}"""
        cursor.execute(_SQL)
        rezult_subject = cursor.fetchall()

        for i in rezult_subject:
            list_total_thems.append(i)
            if i[0] == 1:
                list_have_zero_done.append(i)
            else:
                list_first_thema.append(i)

    list_have_zero_done = len(list_have_zero_done)
    list_total_thems = len(list_total_thems)

    _SQL = f"""SELECT id_subject FROM relation_sybject_user_predmet_stud 
            WHERE id_predmet = {id_subject} AND id_user = {id_user} AND id_student = {id_stud} AND progress_bar = 0"""

    cursor.execute(_SQL)
    rezult_name_subj = cursor.fetchall()

    for p in rezult_name_subj:
        _SQL = """SELECT name_subject FROM teach_subject WHERE id = %s"""
        cursor.execute(_SQL, (p[0],))
        rezultat = cursor.fetchall()
        for l in rezultat:
            list_name_thems.append(l[0])

    list_name_thems = list_name_thems[0] if list_name_thems else None


    if list_have_zero_done == list_total_thems:
        list_name_thems = 'Немає тем'

    return render_template('stud_person_information.html', thespisok_person_infa = spisok_person_infa, theid_subject = id_subject, theid_stud = id_stud ,thelist_total_thems = list_total_thems, thelist_have_zero_done = list_have_zero_done, thelist_name_thems = list_name_thems)


@app.route('/dobavlenie_stud', methods=['POST', 'GET'])
def okno_dobavlenia_stud():
    global id_subject
    global id_user
    list_has_stud = list()
    list_studentov = list()
    itog_delete = ''
    message = ''
    radio_yes_no = 'yes'
    dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'database': 'teacher_assistant'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()

    _SQL_check_students = f"SELECT COUNT(*) FROM relation_predmet_students WHERE id_teacher = {id_user}"
    cursor.execute(_SQL_check_students)
    num_students = cursor.fetchone()[0]

    if num_students == 0:
        message = ' '
    else:

        _SQL = f"""SELECT * FROM relation_predmet_students WHERE id_teacher = {id_user}"""
        cursor.execute(_SQL)
        
        perem_stud = cursor.fetchall()
        for i in perem_stud:
            list_studentov.append(i[2])

        list_studentov_str = ', '.join(map(str, list_studentov))

        _SQL = f"""SELECT DISTINCT ts.id, ts.name, ts.last_name, ts.year_st
        FROM teach_students ts
        WHERE ts.id IN ({list_studentov_str})
        AND ts.id NOT IN (
            SELECT rs.id_student
            FROM relation_predmet_students rs
            WHERE rs.id_predmet = {id_subject}
            )
        """

        cursor.execute(_SQL)

        rezult = cursor.fetchall()
        for g in rezult:
            list_has_stud.append(g)

    if request.method == 'POST':

        name = request.form.get('name')
        last_name = request.form.get('last_name')
        years_stud = request.form.get('years_stud')
        number_phone = request.form.get('number_phone')

        if name != '' and last_name != '' and years_stud != '' and number_phone != '':

            _SQL = 'INSERT INTO teach_students(name,last_name,year_st,number_phone,progress_bar) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(_SQL,(name,last_name,years_stud,number_phone,0))
            dbc.commit()
            id_stud = cursor.lastrowid

            _SQL = """INSERT INTO relation_predmet_students(id_predmet,id_student,id_teacher) VALUES(%s,%s,%s)"""
            cursor.execute(_SQL,(id_subject,id_stud,id_user,))
            dbc.commit()
            list_id_thems = list()
            uniquet_list = list()
            _SQL = f"""SELECT id_subject FROM relation_sybject_user_predmet_stud WHERE id_predmet = {id_subject} AND id_user = {id_user} """

            cursor.execute(_SQL)
            rezult = cursor.fetchall()

            for h in rezult:
                list_id_thems.append(h)


            for item in list_id_thems:
                if item not in uniquet_list:
                    uniquet_list.append(item)

            for j in uniquet_list:
                _SQL = """INSERT INTO relation_sybject_user_predmet_stud(id_user,id_predmet,id_student,id_subject,progress_bar) VALUES(%s,%s,%s,%s,%s)"""
                cursor.execute(_SQL,(id_user,id_subject,id_stud,j[0],0))
                print(_SQL)
                dbc.commit()


            itog_delete = 'Успішно добавлений студент'
            radio_yes_no = 'no'

            


    return render_template('window_add_student.html' , theid_subject = id_subject, thelist_has_stud = list_has_stud, themessage = message,theitog_delete = itog_delete, theradio_yes_no = radio_yes_no  )




@app.route('/dobavlenie_students_who_already', methods=['POST', 'GET'])
def dobavlenie_students_who_already():
    global id_subject
    global id_user
    list_id_thems = list()
    uniquet_list = list()
    ID_STUD = request.form.get('id_student')
    if ID_STUD is not None and ID_STUD !=0 and request.method == 'POST':

        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = """INSERT INTO relation_predmet_students(id_predmet,id_student,id_teacher) VALUES(%s,%s,%s)"""
        cursor.execute(_SQL,(id_subject,ID_STUD,id_user,))
        dbc.commit()

        _SQL = f"""SELECT id_subject FROM relation_sybject_user_predmet_stud WHERE id_predmet = {id_subject} AND id_user = {id_user} """

        cursor.execute(_SQL)
        rezult = cursor.fetchall()

        for h in rezult:
            list_id_thems.append(h)

        for item in list_id_thems:
            if item not in uniquet_list:
                uniquet_list.append(item)


        for j in uniquet_list:
            _SQL = """INSERT INTO relation_sybject_user_predmet_stud(id_user,id_predmet,id_student,id_subject,progress_bar) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(_SQL,(id_user,id_subject,ID_STUD,j[0],0))

            dbc.commit()


        itog_delete = 'Успішно добавлений студент'
        radio_yes_no = 'no'
        


    return render_template('window_add_student.html',theitog_delete = itog_delete, theradio_yes_no = radio_yes_no,theid_subject = id_subject )



@app.route('/delete_the_predmet')
def delete_the_predmet():
    global id_user
    global id_subject
    spisok_predmete_delete = list()
    status = 'yes'

    if id_user != 0 and id_subject != 0:

        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""SELECT * FROM teach_predm WHERE id = '{id_subject}' """
        cursor.execute(_SQL)

        rezult_predmet_del = cursor.fetchall()

        for i in rezult_predmet_del:
            id_subject = i[0]
            spisok_predmete_delete.append(i)


    return render_template('window_delete_predmet.html', thespisok_predmete_delete = spisok_predmete_delete, theid_subject = id_subject,thestatus = status)



@app.route('/udalenie_end', methods = ['POST'])
def udalenie_en():
    status = 'yes'
    global id_subject
    global id_user
    perem_render_site = 'window_delete_predmet.html'


    radio_yes_no = request.form['radio_yes_no']

    list_id_teacher = list()

    if radio_yes_no == 'yes':
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""SELECT id_user_teacher FROM relatin_teachers_predmet WHERE id_predmet = {id_subject} """
        cursor.execute(_SQL)
        perem_id_teacher = cursor.fetchall()

        for i in perem_id_teacher:
            list_id_teacher.append(i)

        _SQL = f"""DELETE FROM relation_sybject_user_predmet_stud WHERE  id_predmet = {id_subject}  AND id_user = {id_user} """
        cursor.execute(_SQL)
        print(_SQL)
        dbc.commit()
        print('-------')
        _SQL = f"""DELETE FROM teach_subject WHERE  id_predmet = {id_subject}  AND id_user = {id_user} """
        cursor.execute(_SQL)
        print(_SQL)
        dbc.commit()

        if len(list_id_teacher) == 1:
            _SQL = f"""DELETE FROM relatin_teachers_predmet WHERE  id_predmet = {id_subject}  AND id_user_teacher = {id_user} """
            cursor.execute(_SQL)
            dbc.commit()

            _SQL = f"""DELETE FROM  teach_predm WHERE id ={id_subject} """
            cursor.execute(_SQL)
            dbc.commit()
            del_predmet = 'Успішне видалення'
            perem_render_site = 'items_window.html'

        else:

            _SQL = f"""DELETE FROM relatin_teachers_predmet WHERE  id_predmet = {id_subject}  AND id_user_teacher = {id_user} """
            cursor.execute(_SQL)
            dbc.commit()

            _SQL = f"""SELECT id_student 
            FROM relation_predmet_students 
            WHERE id_predmet = {id_subject}"""
            cursor.execute(_SQL)

            rezult_stud_from_predmet = cursor.fetchall()

            for i in rezult_stud_from_predmet:
                _SQL = f"""SELECT COUNT(id_predmet) FROM relation_predmet_students WHERE id_student = {i[0]}"""

                cursor.execute(_SQL)
                rezult_sviasi_mesdu_stud_and_predmet = cursor.fetchall()

                for g in rezult_sviasi_mesdu_stud_and_predmet:

                        if g[0] == 1:

                            _SQL = f"""DELETE FROM relation_predmet_students WHERE id_student = {i[0]} AND id_predmet = {id_subject}"""
                            cursor.execute(_SQL)
                            dbc.commit()

                            _SQL =f"""DELETE FROM teach_students WHERE id = {i[0]} """
                            cursor.execute(_SQL)
                            dbc.commit()

                        else:
                            _SQL = f"""DELETE FROM relation_predmet_students WHERE id_student = {i[0]} AND id_predmet = {id_subject}"""
                            cursor.execute(_SQL)
                            dbc.commit()

            del_predmet = 'Успішне видалення'
            status = 'net'

    elif radio_yes_no == 'no':
        del_predmet = 'Ви відмінили видалення предмета'
        status = 'no'


    return render_template(perem_render_site,thedel_predmet = del_predmet, theradio_yes_no = radio_yes_no, thestatus = status,theid_subject = id_subject)


@app.route('/window_del_student_show')
def window_del_student_show():
    ID_stud = request.args.get('id')
    list_name_last = list()
    if ID_stud != 0:
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""SELECT name,last_name FROM teach_students WHERE id = {ID_stud}"""
        cursor.execute(_SQL)
        rezult = cursor.fetchall()


        for i in rezult:
            list_name_last.append(i)


    return render_template('window_delete_stud.html', the_ID_stud = ID_stud, thelist_name_last = list_name_last, thestatus = 'yes')




@app.route('/delete_stud_end', methods ={'POST'})
def delete_stud_end():
    global id_subject

    id_stud = request.form['id_stud']
    radio_yes_no = request.form['radio_yes_no']

    if radio_yes_no == 'yes':
        
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','db':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""SELECT COUNT(id_predmet) FROM relation_predmet_students WHERE id_student = {id_stud}"""
        cursor.execute(_SQL)

        rezult_count = cursor.fetchone()

        rezult_count = rezult_count[0]

        if rezult_count == 1:

            _SQL = f"""DELETE FROM relation_predmet_students WHERE id_student = {id_stud} AND id_predmet = {id_subject}"""
            cursor.execute(_SQL)
            dbc.commit()

            _SQL = f"""DELETE FROM relation_sybject_user_predmet_stud WHERE id_student = {id_stud} AND id_predmet = {id_subject}"""
            cursor.execute(_SQL)
            dbc.commit()


            _SQL =f"""DELETE FROM teach_students WHERE id = {id_stud} """
            cursor.execute(_SQL)
            dbc.commit()

        else:
            _SQL = f"""DELETE FROM relation_predmet_students WHERE id_student = {id_stud} AND id_predmet = {id_subject}"""
            cursor.execute(_SQL)
            dbc.commit()

            _SQL = f"""DELETE FROM relation_sybject_user_predmet_stud WHERE id_student = {id_stud} AND id_predmet = {id_subject}"""
            cursor.execute(_SQL)
            dbc.commit()

        itog_delete = 'Успішне видалення'
    else:


        itog_delete = 'Ви видмінили видалення'


    return render_template("window_delete_stud.html", theitog_delete = itog_delete, thestatus = 'no', theid_subject = id_subject  )




@app.route('/window_change_student_show')
def window_change_student_show():
    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()
    list_change_stud = list()
    id_stud_personal = request.args.get('id')


    _SQL = f"""SELECT id,name,last_name,year_st,number_phone FROM teach_students WHERE id = {id_stud_personal} """
    cursor.execute(_SQL)
    rezult = cursor.fetchall()
    for i in rezult:
        list_change_stud.append(i)
    

    return render_template('window_change_stud.html',thelist_change_stud = list_change_stud, theid_stud = id_stud_personal, thestatus = 'yes')



@app.route('/window_change_student', methods = ['POST'])
def window_change_student():
    id_stud = request.form['id_stud']
    name = request.form['name']
    last_name = request.form['last_name']
    years = request.form['years']
    number_phone = request.form['number_phone']

    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()

    _SQL = f"""UPDATE teach_students SET name = %s, last_name = %s, year_st = %s, number_phone = %s WHERE id = {id_stud}"""
    cursor.execute(_SQL,(name,last_name,years,number_phone))
    dbc.commit()
    itog = 'Успішне редагування студента'
    return render_template('window_change_stud.html', theid_stud = id_stud, theitog = itog, thestatus = 'no' )



@app.route('/window_subject')
def window_subject():
    global id_subject
    global id_user
    dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
    dbc = mysql.connector.connect(**dbconfig)
    cursor = dbc.cursor()

    if id_user != 0 and id_subject != 0 :
        list_thems = list()
        _SQL = f"""SELECT id,name_subject FROM teach_subject WHERE id_user = {id_user} AND id_predmet = {id_subject}"""
        cursor.execute(_SQL)
        rezult = cursor.fetchall()
        for i in rezult:
            list_thems.append(i)

    return render_template('subject_window.html' ,theid_subject = id_subject,thelist_thems = list_thems)



@app.route('/window_add_subject_show')
def window_add_subject_show():

    return render_template('window_add_subject.html')




@app.route('/window_add_subject_end', methods = ['POST'])
def window_add_subject_end():
    global id_subject
    global id_user

    name_thema = request.form['name_subject']
    itog_add = 'Сталася помилка'
    back_modal = "yes"
    if name_thema != '' and id_user != 0 and id_subject != 0:
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """INSERT INTO teach_subject(name_subject,id_user,id_predmet) VALUES(%s,%s,%s)"""
        cursor.execute(_SQL,(name_thema,id_user,id_subject))
        dbc.commit()
        id_thema = cursor.lastrowid

        _SQL = f"""SELECT id_student FROM relation_predmet_students WHERE id_predmet = {id_subject} AND id_teacher = {id_user} """
        cursor.execute(_SQL)
        list_id_stud_where_predmet = list()
        rezult = cursor.fetchall()

        if id_user != 0 and id_subject != 0 and id_thema != 0:
            for i in rezult:
                list_id_stud_where_predmet.append(i)

                _SQL = """INSERT INTO relation_sybject_user_predmet_stud(id_user,id_predmet,id_student,id_subject,progress_bar) VALUES(%s,%s,%s,%s,%s)"""
                cursor.execute(_SQL,(id_user,id_subject,i[0],id_thema,0))
                dbc.commit()

            itog_add = "Успішно добавлена тема"
            

    return render_template('window_add_subject.html',theitog_add = itog_add, theback_modal = back_modal, theid_subject = id_subject)




@app.route('/show_person_stud_subject')
def show_person_stud_subject():
    global id_subject
    global id_user
    id_stud_person = request.args.get('id_stud')
    if id_stud_person != 0 and id_stud_person is not None and id_user != 0 and id_user is not None and id_subject != 0 and id_subject is not None:
        list_subject = list()
        list_have_zero_one = list()
        dbconfig = {'host':'127.0.0.1','user':'newusername','password':'newpassword','database':'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()
        _SQL = f"""SELECT id_subject,progress_bar FROM relation_sybject_user_predmet_stud WHERE id_user = {id_user} AND id_predmet = {id_subject} AND id_student = {id_stud_person}"""
        cursor.execute(_SQL)
        rezult_id_subject = cursor.fetchall()
        for id_subj in rezult_id_subject:
            _SQL = f"""SELECT * FROM teach_subject WHERE id ={id_subj[0]} """
            cursor.execute(_SQL)
            rezult_subject = cursor.fetchall()

    
            for i in rezult_subject:
                
                if id_subj[1] == 1:
                    list_have_zero_one.append(i)
                else:
                    list_subject.append(i)

    return render_template('person_subject_for_stud.html', theid_stud_person = id_stud_person, thelist_subject = list_subject, thelist_have_zero_one = list_have_zero_one, thestatus = 'yes')



@app.route('/id_checkbox', methods=['POST'])
def id_checkbox():
    global id_subject
    global id_user
    id_stud_get = request.form.get('id_stud')  
    id_themes = request.form.getlist('id_thems[]')
    itog = 'Ви не вибрали предмет або сталася помилка'
    

    if id_themes and id_stud_get:
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'database': 'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        for i in id_themes:
            _SQL = f"""SELECT progress_bar FROM relation_sybject_user_predmet_stud  
                    WHERE id_user = {id_user} AND id_predmet = {id_subject} AND id_student = {id_stud_get} AND id_subject = {i}"""

            cursor.execute(_SQL)
            rezlt = cursor.fetchall()
            for g in rezlt:
                if g[0] == 0:
                    _SQL = f"""UPDATE relation_sybject_user_predmet_stud SET progress_bar = 1 
                            WHERE id_user = {id_user} AND id_predmet = {id_subject} AND id_student = {id_stud_get} AND id_subject = {i}"""
                    cursor.execute(_SQL)
                    dbc.commit()

                    if len(id_themes) > 1:

                        itog = 'Теми успішно збережено'
                    else:
                        itog = 'Тема успішно збережено'

    return render_template('person_subject_for_stud.html', theid_stud_person=id_stud_get, themodal_yes_no = 'yes', the_itog = itog, thestatus = 'no')



@app.route('/update_thema_show')
def update_thema_show():
    global id_subject
    global id_user
    listok = list()
    id_stud_get = request.args.get('id_student')
    id_person_subj = request.args.get('id_thema')

    if id_stud_get and id_person_subj:
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'database': 'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""SELECT name_subject FROM teach_subject WHERE id = {id_person_subj}"""
        cursor.execute(_SQL)
        name_thema = cursor.fetchall()

        for i in name_thema:
            listok.append(i)

    return render_template('update_person_thema.html', theid_stud_get = id_stud_get, theid_person_subj = id_person_subj, thename_thema= listok, thestatus = 'yes' )


@app.route('/update_thema', methods=['POST'])
def update_thema():
    global id_subject
    global id_user
    id_stud_person = request.form['id_stud_person']
    id_thema = request.form['id_thema']

    print(id_stud_person)
    print(id_thema)

    if id_stud_person and id_thema:
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'database': 'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""UPDATE relation_sybject_user_predmet_stud SET progress_bar = 0 
                WHERE id_user = {id_user} AND id_predmet = {id_subject} AND id_student = {id_stud_person} AND id_subject = {id_thema}"""
        cursor.execute(_SQL)
        dbc.commit()
        itog = 'Тема успішно була відновлена   '

    return render_template('update_person_thema.html', thestatus = 'no', the_itog = itog, theid_stud_get = id_stud_person) 


@app.route('/window_choice_subject')
def window_choice_subject():
    id_subject = request.args.get('id_subject')
    name_subject = request.args.get('name_sabject')


    return render_template('window_choice_subject.html', theid_subject=id_subject, thename_subject=name_subject)



@app.route('/window_change_subject_show')
def window_change_subject_show():
    id_thema = request.args.get('id_sub')
    name_subject = request.args.get('name_subj')

    return render_template('window_change_subject.html', theid_subject=id_thema, thename_subject=name_subject, thestatus = 'yes')



@app.route('/window_change_subject', methods = ['POST'])
def window_change_subject():
    global id_user
    global id_subject
    id_thema = request.form['id_subject']
    name_subject = request.form['name_subject']

    if id_thema and name_subject:
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'database': 'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = """UPDATE teach_subject SET name_subject = %s
                WHERE id_user = {} AND id_predmet = {} AND id = {}""".format(id_user, id_subject, id_thema)

        cursor.execute(_SQL, (name_subject,))
        dbc.commit()
        cursor.close()
        dbc.close()
        itog = 'Ви успішно відредагували'
    return render_template('window_change_subject.html', thestatus = 'no', theitog = itog)




@app.route('/window_delete_subject_show')
def window_delete_subject_show():
    id_subject = request.args.get('id_sub')
    name_subj = request.args.get('name_subj')

    return render_template('window_delete_subject.html', theid_subject=id_subject, thename_subj = name_subj,  thestatus = 'yes')


@app.route('/window_delete_subject', methods = ['POST'])
def window_delete_subject():

    id_thema = request.form['id_sub']
    radio_yes_no = request.form['radio_yes_no']

    if radio_yes_no == 'yes':
        dbconfig = {'host': '127.0.0.1', 'user': 'newusername', 'password': 'newpassword', 'database': 'teacher_assistant'}
        dbc = mysql.connector.connect(**dbconfig)
        cursor = dbc.cursor()

        _SQL = f"""DELETE FROM relation_sybject_user_predmet_stud WHERE id_subject = {id_thema}"""
        cursor.execute(_SQL)
        dbc.commit()

        _SQL = f"""DELETE FROM teach_subject WHERE id = {id_thema}"""
        cursor.execute(_SQL)
        dbc.commit()

        cursor.close()
        dbc.close()
        itog = 'Ви успішно видалили'
    else:
        itog = 'Ви відмінили видалення'


    return render_template('window_change_subject.html', thestatus = 'no', theitog = itog)






if __name__ == '__main__':
    app.run(debug=True)



