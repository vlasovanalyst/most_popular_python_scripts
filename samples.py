### 📁 1–5. Работа с файлами и путями

# 1. Быстро посчитать строки в большом CSV без открытия
   sum(1 for _ in open('data.csv'))
   

# 2. Список всех CSV/Excel файлов в папке
   from pathlib import Path
   files = list(Path('data/').rglob('*.csv'))
   

# 3. Автозагрузка последнего файла в папке
   latest = max(Path('data/').glob('*.csv'), key=lambda f: f.stat().st_mtime)
   

# 4. Автоархивация старых файлов
   import shutil
   shutil.make_archive('backup', 'zip', 'data/')
   

# 5. Проверка валидности пути к файлу
   import os
   os.path.exists('file.csv')
   

---

### 📊 6–10. Быстрые EDA и отчёты

# 6. Быстрый отчёт с `pandas_profiling`
   import pandas_profiling
   df.profile_report().to_file('report.html')
   

# 7. Отчёт с `Sweetviz`
   import sweetviz as sv
   sv.analyze(df).show_html()
   

# 8. Список уникальных значений и их частоты
   df['column'].value_counts()
   

# 9. Добавление флага "праздничный день" (для РФ)
import holidays
ru_holidays = holidays.Russia()
df['is_holiday'] = df['date'].isin(ru_holidays)

# 10. Поиск выбросов по IQR
def detect_outliers_iqr(series):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return series[(series < (q1 - 1.5*iqr)) | (series > (q3 + 1.5*iqr))]



---

### 📈 11–15. Визуализация данных

# 11. Гистограмма по всем числовым колонкам
df.hist(figsize=(12,8))


# 12. Корреляционная матрица с тепловой картой
import seaborn as sns
sns.heatmap(df.corr(), annot=True)


# 13. Top-N барчарт
df['col'].value_counts().nlargest(10).plot(kind='bar')


# 14. Pairplot для быстрого анализа
sns.pairplot(df.sample(500))


# 15. Быстрая визуализация категориального признака
def plot_bar(df, col):
    df[col].value_counts().plot(kind='bar')
    plt.title(f'Распределение {col}')
    plt.show()


---

### 🧹 16–20. Очистка и предобработка

# 16. Удаление всех колонок, где >30% пропусков
df.dropna(thresh=len(df)*0.7, axis=1, inplace=True)


# 17. Заполнение пропусков медианой для числовых колонок
df.fillna(df.median(numeric_only=True), inplace=True)


# 18. Преобразование строк в дату
pd.to_datetime(df['date'], errors='coerce')


# 19. Удаление неинформативных признаков
df = df.loc[:, df.nunique() > 1]

# 20. Упрощение текстов — приведение к нижнему регистру и удаление спецсимволов
df['text'] = df['text'].str.lower().str.replace(r'\W+', ' ', regex=True)


---

### 📆 21–25. Работа с датами

# 21. Выделить день/месяц/год из даты
df['year'] = df['date'].dt.year

# 22. Создать колонку "дата + 7 дней"
df['date_plus_7'] = df['date'] + pd.Timedelta(days=7)


# 23. Группировка по неделям
df.groupby(df['date'].dt.to_period('W'))['value'].sum()


# 24. Расчёт разницы между датами в днях
(df['end'] - df['start']).dt.days


# 25. Сегментация по времени суток
df['hour'] = df['date'].dt.hour
df['period'] = pd.cut(df['hour'], bins=[0,6,12,18,24], labels=['ночь','утро','день','вечер'])

### 🔍 26–30. SQL-подобные штуки

# 26. Объединение таблиц по merge
pd.merge(df1, df2, on='user_id', how='left')

# 27. Имитация GROUP BY + HAVING
df.groupby('user_id').agg({'value':'sum'}).query('value > 1000')

# 28. Фильтрация по подзапросу
active_users = df[df['status'] == 'active']['user_id'].unique()
df[df['user_id'].isin(active_users)]

# 29. TOP 1 по группе (аналог ROW\_NUMBER = 1)
df.sort_values('value', ascending=False).drop_duplicates('group')

# 30. Простое выполнение SQL на pandas с `pandasql`
from pandasql import sqldf
sqldf("SELECT * FROM df WHERE value > 100")

---

### 🧪 31–35. A/B и метрики

# 31. Подсчёт ARPU, ARPPU, CR
arpu = df['revenue'].sum() / df['user_id'].nunique()


# 32. Конверсия по шагам воронки
df.groupby('step')['user_id'].nunique().pct_change()


# 33. Z-тест разницы конверсий
from statsmodels.stats.proportion import proportions_ztest
proportions_ztest([30, 45], [1000, 1000])


# 34. Доверительный интервал среднего
import scipy.stats as st
st.t.interval(alpha=0.95, df=len(x)-1, loc=x.mean(), scale=st.sem(x))

# 35. Визуализация распределений в группах
sns.violinplot(x='group', y='metric', data=df)


### 🛠️ 36–40. Автоматизация и лайфхаки

# 36. Автообработка Excel-файлов со множеством листов
pd.read_excel('file.xlsx', sheet_name=None)


# 37. Оповещение в Telegram по результатам анализа
import requests
requests.post(f'https://api.telegram.org/bot<TOKEN>/sendMessage', data={'chat_id':123, 'text':'Анализ готов!'})


# 38. Сохранение графиков автоматически в PDF
import matplotlib.pyplot as plt
plt.savefig('report.pdf')

# 39. Простой API-запрос и парсинг JSON

import requests
r = requests.get('https://api.example.com/data')
data = r.json()


# 40. Планировщик на каждый день — с `schedule`
import schedule, time
schedule.every().day.at("09:00").do(run_analysis)
while True:
    schedule.run_pending()
    time.sleep(60)
