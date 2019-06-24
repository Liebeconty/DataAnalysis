class DataClean:
    #删除多列数据
    def drop_multiple_col(col_names_list, df): 
        df.drop(col_names_list, axis=1, inplace=True)
        return df
    #转换Dtypes
    def change_dtypes(col_int, col_float, df): 
        df[col_int] = df[col_int].astype('int32')
        df[col_float] = df[col_float].astype('float32')
    #将分类变量转换为数值变量
    def convert_cat2num(df):
        num_encode = {'col_1' : {'YES':1, 'NO':0},
                      'col_2'  : {'WON':1, 'LOSE':0, 'DRAW':0}}  
        df.replace(num_encode, inplace=True)
    #检查缺失的数据
    def check_missing_data(df):
        return df.isnull().sum().sort_values(ascending=False)
    #删除列中的字符串
    def remove_col_str(df):
        df['col_1'].replace('\n', '', regex=True, inplace=True)
        df['col_1'].replace(' &#.*', '', regex=True, inplace=True)
    #删除列中的空格
    def remove_col_white_space(df):
        # remove white space at the beginning of string 
        df[col] = df[col].str.lstrip()
    #将两列字符串数据（在一定条件下）拼接起来
    def concat_col_str_condition(df):
        mask = df['col_1'].str.endswith('pil', na=False)
        col_new = df[mask]['col_1'] + df[mask]['col_2']
        col_new.replace('pil', ' ', regex=True, inplace=True)
    #转换时间戳（从字符串类型转换为日期「DateTime」格式）
    def convert_str_datetime(df): 
        df.insert(loc=2, column='timestamp', value=pd.to_datetime(df.transdate, format='%Y-%m-%d %H:%M:%S.%f'))

