#from fuzzywuzzy import fuzz
from collections import defaultdict

def find_similar_categories(series, cutoff=90):
  series = series.astype(str)  # Convert series to string
  unique_categories = series.unique()
  category_counts = series.value_counts()

  real_categories = []
  fake_categories = {}

  for category in unique_categories:
    if category in real_categories or category in fake_categories: continue

    similar_categories = [cat for cat in unique_categories if fuzz.token_sort_ratio(category, cat) > cutoff and category != cat]

    if len(similar_categories) > 0:
      real_categories.append(category)
      for similar_cat in similar_categories:
        fake_categories[similar_cat] = category

    else: real_categories.append(category)

  return real_categories, fake_categories

def string_metric(column, df, dictionary=False, fake_duplicates=False):
  lengths = column.str.len();
  unique_values = column.nunique();
  if (unique_values < 0.2*len(df)):
    return category_metric(column, df, fake_duplicates);

  return {
    'DType': column.dtype,
    'CType': 'STRING',
    'Average Length': round(lengths.mean(), 2),
    'Min Length': lengths.min(),
    'Max Length': lengths.max(),
    'Unique values': column.nunique() if not dictionary else column.unique().tolist(),
    'Null values': column.isnull().sum(),
    'Total values': len(df),
  };

def category_metric(column, df, fake_duplicates=False):
  lengths = column.str.len();
  unique_values = column.nunique();
  if unique_values <= 500: unique_values = column.unique().tolist();

  #if fake_duplicates: _, fake = find_similar_categories(column, 90);

  ret = {
    'DType': column.dtype,
    'CType': 'ENUM',
    'Average Length': round(lengths.mean(), 2),
    'Min Length': lengths.min(),
    'Max Length': lengths.max(),
    'Unique values': unique_values,
    'Null values': column.isnull().sum(),
    'Total values': len(df),
  };

  #if fake_duplicates: ret['Fake duplicates'] = fake;
  return ret;

def int_metric(column, df, dictionary=False):
  unique_values = column.nunique();
  if (unique_values < 0.1*len(df)):
    return int_category_metric(column, df);

  return {
    'DType': column.dtype,
    'CType': 'INT',
    'Average value': round(column.mean(),2),
    'Min value': column.min(),
    'Max value': column.max(),
    'Std deviation': round(column.std(),2),
    'Null values': column.isnull().sum(),
    'Unique values': column.nunique() if not dictionary else column.unique().tolist(),
    'Total values': len(df),
  };

def int_category_metric(column, df):
  unique_values = column.nunique();
  if unique_values <= 500: unique_values = column.unique().tolist();
  #if unique_values <= 100: unique_values = column.value_counts().to_dict();

  return {
    'DType': column.dtype,
    'CType': 'ENUM_INT',
    'Unique values': unique_values,
    'Null values': column.isnull().sum(),
    'Total values': len(df),
  };

def float_metric(column, df, dictionary):
  return {
    'DType': column.dtype,
    'CType': 'FLOAT',
    'Average value': round(column.mean(),2),
    'Min value': column.min(),
    'Max value': column.max(),
    'Std deviation': round(column.std(),2),
    'Null values': column.isnull().sum(),
    'Unique values': column.nunique() if not dictionary else column.unique(),
    'Total values': len(df),
  };

def print_metric(columnName, metric):
  print('"'+columnName+'":');
  print('  {');
  for k in metric:
    print('    '+k+':', str(metric[k])+',');
  print('  }');

def print_metrics(df, dictionary=False, fake_duplicates=False):
  for i in range(len(list(df.columns))):
    columnName = list(df.columns)[i];
    column = df[columnName];
    dtype = df.dtypes.iloc[i]
    if dtype == 'object': print_metric(columnName, string_metric(column, df, dictionary, fake_duplicates));
    elif dtype == 'int64': print_metric(columnName, int_metric(column, df, dictionary));
    elif dtype == 'float64': print_metric(columnName, float_metric(column, df, dictionary));
