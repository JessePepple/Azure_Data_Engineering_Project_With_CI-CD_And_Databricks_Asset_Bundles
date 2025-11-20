class reuse:
    def dropColumns(self,df,columns):
        df = df.drop(*columns)
        return df
