# Teacher Helper / Помічник вчителя

Teacher Helper – це веб-додаток на Flask для керування інформацією про студентів та предмети. Програма дозволяє реєструвати батьків/користувачів і їхніх дітей, додавати/оновлювати/видаляти записи про студентів і предмети, а також призначати предмети конкретним студентам. Для взаємодії з базою даних використовується MySQL (через `mysql-connector-python`【4†L79-L84】). Інтерфейс зроблено на шаблонах HTML, CSS та JavaScript для зручного користування.

Teacher Helper is a Flask-based web application for managing information about students and subjects. The application allows user (parent/teacher) registration and login, adding/updating/deleting student and subject records, and assigning subjects to specific students. It uses a MySQL database (via `mysql-connector-python`【4†L79-L84】) for data storage. The user interface is built with HTML, CSS, and JavaScript for an easy-to-use experience.

## Можливості / Features

- Реєстрація батьків/учасників системи та авторизація через веб-інтерфейс.  
- Додавання, оновлення та видалення інформації про студентів.  
- Додавання, оновлення та видалення предметів (курсів), пов’язаних з викладачами.  
- Призначення предметів студентам через зв’язки база даних.  
- Зручний графічний інтерфейс на Flask з формами для введення даних.  

- User registration and login via a web interface.  
- Add, update, and delete student records.  
- Add, update, and delete subjects (courses) associated with teachers.  
- Assign subjects to students using database relationships.  
- User-friendly Flask web interface with forms for data entry.  

## Початок роботи / Getting Started

Перед тим як запускати проєкт, виконайте наступні кроки налаштування.

Before running the project, perform the following setup steps.

1. **Вимоги / Prerequisites:** Переконайтеся, що у вас встановлено Python (версія 3.9 або новіша, Flask підтримує Python 3.9+)【6†L15-L18】. Також потрібен сервер MySQL та відповідні таблиці.  
   - Встановіть Flask:  
     ```bash
     pip install Flask
     ```  
     (Flask – популярний фреймворк для веб-додатків на Python【6†L104-L108】.)
   - Встановіть MySQL Connector:  
     ```bash
     pip install mysql-connector-python
     ```  
     (Пакет `mysql-connector-python` потрібен для з’єднання з базою даних MySQL【4†L79-L84】.)
   - Перевірте, що у вас налаштовано MySQL та створено базу даних (за замовчуванням назва `teacher_assistant`). Задайте відповідного користувача та пароль, або змініть налаштування у файлі `main.py` (див. далі).

2. **Клонування репозиторію / Clone the repository:**  
   ```bash
   $ git clone https://github.com/<your-username>/teacher_helper.git
   $ cd teacher_helper
   ```  
   Скачайте код проєкту з GitHub та перейдіть до папки проекту.

3. **Налаштування підключення / Configure database connection:**  
   Відкрийте файл `main.py` і знайдіть словник `dbconfig`. Змініть поля `user`, `password`, `host`, `database` під вашу конфігурацію MySQL (ім'я бази даних, користувач, пароль тощо). Переконайтеся, що база даних і потрібні таблиці існують (назви таблиць можна знайти у коді, наприклад `user_information`, `teach_subject`, `teach_predm` тощо).

   Edit the `dbconfig` dictionary in `main.py` to match your MySQL setup (`user`, `password`, `host`, `database`). Ensure that the database (default `teacher_assistant`) and required tables exist. Create them manually if needed, according to the code’s table names (e.g., `user_information`, `teach_subject`, `teach_predm`, etc.).

4. **Запуск додатку / Run the application:**  
   ```bash
   $ python main.py
   ```  
   Після запуску програма стартує на локальному сервері (зазвичай `http://127.0.0.1:5000/`).  
   After running `main.py`, the application will start on the local server (usually `http://127.0.0.1:5000/`).

## Приклад використання / Usage Example

Після запуску відкрийте браузер і перейдіть за адресою `http://127.0.0.1:5000/`. Наприклад:

- Щоб зареєструвати нового користувача (батька/викладача), натисніть на **Registration** і заповніть форму.  
- Авторизуйтеся через форму входу, використовуючи email та пароль.  
- Після входу ви зможете бачити список предметів (**Subjects**) та додавати нові.  
- Через меню **Students** можна додати нових студентів та призначити їм предмети.  

After starting the app, open your web browser and go to `http://127.0.0.1:5000/`. For example:

- To register a new user (parent/teacher), click **Registration** and fill in the form.  
- Log in using your email and password.  
- After login, you can see the **Subjects** list and add new subjects.  
- Under the **Students** menu, you can add new students and assign subjects to them.  

## Внесок / Contributing

Ви можете зробити внесок у проєкт, відкривши issue на GitHub або запропонувавши Pull Request. Будь ласка, дотримуйтесь загальноприйнятих практик кодування та коментуйте зміни.  

Contributions are welcome! Feel free to open an issue or submit a Pull Request on GitHub. Please follow standard coding conventions and comment your changes.

## Ліцензія / License

Проєкт розповсюджується під ліцензією **MIT License**. Зміст ліцензії дозволяє вільно використовувати, копіювати та модифікувати програмне забезпечення【8†L32-L40】.  

This project is licensed under the **MIT License**【8†L32-L40】, which permits free use, copying, and modification of the software.

## Автор / Author

Автор

GitHub: https://github.com/06055

Проєкт створений з навчальною метою для вивчення Python та Pygame. Ліцензія: MIT — можна використовувати, поширювати та змінювати з вказанням автора.

Author

GitHub: https://github.com/06055

This project was created for learning purposes to practice Python and Pygame. License: MIT — free to use, distribute, and modify with attribution.

