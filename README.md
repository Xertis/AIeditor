## Программа представляет собой текстовый utf-8 редактор с возможность суммаризации текста, а так же с возможностью поиска ответов в тексте

## Инструкция по пользованию

При первом заходе в приложение открывается похожее на стандартные текстовые редакторы окно

Основные кнопки и поля ввода:
1. Кнопка **open_file**
	Открывает новый файл
	
2. Кнопка **save_file** 
	Сохраняет файл


3.  Поле внутри AI chat нужно для ввода запроса, кнопкой send же запрос отправляется в нейронку, от различных ситуаций использования меняется выбор нейросети:
	**Суммирование текста**
	- **Сценарий:** Текст выделен, отправлено пустое сообщение в диалог с нейронкой, или сообщение с числом.
	- **Действие:** Будет использована нейронка суммаризации.
	- **Ответ:** Нейронка отправит суммированный текст с количеством предложений, равным числу из сообщения пользователя (или 1, если число не указано).
	
	#Warning 
		Под выделенным текстом имеется ввиду текст, который был выделен через ЛКМ
	
	**Ответы на вопросы**
	- **Сценарий:** Отправлено не пустое сообщение с вопросом.
	- **Действие:** В нейронку отправляется весь текст.
	- **Ответ:** Нейронка отвечает на вопрос, основываясь на всем тексте.
	


## Архитектура проекта: 

AIeditor/
│
├── constants.py - Перечисление констант проекта
├── main.py - Файл запуска проекта
│
└── src/
    ├── ai_requests.py - Класс для работы с нейросетью
    └── app/
    │   ├── aieditor.py - Класс с инициализацией главного окна и его методов
    │   └── handlers.py - Класс хендлеров кнопок
    │
    └── sql/
        ├── db_api.py - Класс API для работы с базой данных
        ├── db_tables.py - Объявление таблиц базы данных
        └── queries/
            ├── db_files.py - Методы для управления файлами в бд
            ├── db_requests.py - Методы для управления историей запросов в бд
            └── db_unsave.py - Методы для работы с не сохранённым текстом файла в бд

## Использованные технологии

> 1. SQL - для сохранения недавних состояний файлов
> 2. SQLalchemy - для удобного манипулирования и расширения бд
> 3. PyQT6 - основная библиотека, на которой основано приложение
> 4. Transformers - загрузчик и менеджер нейросетей, для удобной работы с ними
> 5. Sumy - библиотека для суммирования текста
