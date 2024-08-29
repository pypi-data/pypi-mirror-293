import pandas as pd

def get_distribution(df: pd.DataFrame, target_col: str, numeric_columns: list[str]=[]) -> pd.DataFrame:
    '''
    Get DataFrame distribution for a given target column.

    Parameters
    ----------
    df : pandas.DataFrame
      DataFrame to get distribution from.
    target_col : str
      Target column name.
    numeric_columns : list[str]
      List of numeric columns to get distribution from.

    Returns
    -------
    pandas.DataFrame
      DataFrame with distribution for the given target column.
      For categorical columns, the distribution follows the format: number of occurrences / total number of occurrences (percentage).
      For numeric columns, the distribution follows the format: mean (standard deviation).
    '''

    total = df.shape[0]
    columns = df.loc[:, df.columns != target_col].columns.to_list()

    dfs_by_target_col_classes = {}
    values_target_col = df[target_col].value_counts().index.to_list()
    values_target_col.sort()

    for value in values_target_col:
        dfs_by_target_col_classes[value] = df[df[target_col] == value]

    data = {'Attributes': [], 'Total': []}

    for value_target_col in values_target_col:
        data[f'{target_col}:{value_target_col}'] = []

    for col in columns:
        if (col in numeric_columns):
            mean = df[col].mean()
            std = df[col].std()
            data['Attributes'].append(col)
            data['Total'].append(f'{mean:.1f} ({std:.1f})')

            for df_by_target_col_key in dfs_by_target_col_classes.keys():
                mean_by_target_col = dfs_by_target_col_classes[df_by_target_col_key][col].mean()
                std_by_target_col = dfs_by_target_col_classes[df_by_target_col_key][col].std()
                std_by_target_col = std_by_target_col if pd.notna(std_by_target_col) else 0

                data[f'{target_col}:{df_by_target_col_key}'].append(
                    f'{mean_by_target_col:.1f} ({std_by_target_col:.1f})')
        else:
            value_counts_total = df[col].value_counts()
            value_index = value_counts_total.index.to_list()
            value_index.sort()

            for index in value_index:
                data['Attributes'].append(f'{col}:{index}')
                data['Total'].append(
                    f'{value_counts_total[index]}/{total} ({(value_counts_total[index]/total) * 100:.1f})')

                for df_by_target_col_key in dfs_by_target_col_classes.keys():
                    total_by_target_col_class = dfs_by_target_col_classes[df_by_target_col_key].shape[0]
                    value_counts_total_by_target_col = dfs_by_target_col_classes[df_by_target_col_key][col].value_counts()

                    if index in value_counts_total_by_target_col.index.to_list():
                        data[f'{target_col}:{df_by_target_col_key}'].append(
                            f'{value_counts_total_by_target_col[index]}/{total_by_target_col_class} ({(value_counts_total_by_target_col[index]/total_by_target_col_class)  * 100:.1f})')
                    else:
                        data[f'{target_col}:{df_by_target_col_key}'].append('-')

    return pd.DataFrame(data)
