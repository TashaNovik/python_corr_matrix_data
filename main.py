import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

df = pd.read_csv('Marvel_Movies_Dataset.csv', sep=',')
print(df.info())
print(df.head())
print(df.shape)
print(df.columns)
print(df.describe())

# Проверить датафрейм на наличие пропусков:
# получились пропуски здесь Director (2)=0.852941
print(df.isnull().mean().sort_values(ascending=False))
# Отбросить пропущенные значения из датафрейма:
df = df.dropna(subset=['Director (2)'])
# Проверить датафрейм на наличие пропусков:
print('Проверить датафрейм на наличие пропусков:')
print(df.isnull().mean().sort_values(ascending=False))

#Далее рассмотрим числовые признаки:
# Будем смотреть эти значения только для колонок с числовым типом:
# Получаем часть датафрейма с колонками только числового типа:
numerical_df = df.select_dtypes(include=['number'])
# Минимум, максимум, среднее и медианное значения.
# Минимальное значение:
print(numerical_df.min())
# Максимальное значение:
print(numerical_df.max())
# Среднее значение:
print(numerical_df.mean())
# Медианное значение:
print(numerical_df.median())
# Отклонение от среднего значения:
print(numerical_df.std())

#Посмотрим, есть ли выбросы с аномальными значениями в данных:
# create a histogram
hist = df['Rotten Tomatoes - Audience (scored out of 100%)'].hist()
figure = hist.get_figure()
figure.savefig('histogram.png')

#Распределение на гистограмме скошено влево, у нас есть выбросы
# Применим математическую трансформацию к данным

df['Rotten Tomatoes - Audience (scored out of 100%)'] = stats.boxcox(df['Rotten Tomatoes - Audience (scored out of 100%)'])[0]
hist = df['Rotten Tomatoes - Audience (scored out of 100%)'].hist()
figure = hist.get_figure()
figure.savefig('histogram_after.png')

# Проверим близость распределения к нормальному:
sm.qqplot(df['Rotten Tomatoes - Audience (scored out of 100%)'], line='s')  # 'ваша_колонка' - имя столбца с данными
plt.savefig('Проверка_распределения_на_нормальность.png')
plt.show()

# Удалить дубликаты:
df = df.drop_duplicates(inplace=True)

# Рассчитать матрицу корреляции для числовых значений датафрейма:
corr_matrix = numerical_df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm') # annot=True отображает значения коэффициентов на карте
plt.savefig('Корреляция_числовых_признаков.png')
plt.show()



