        for column in restored_df.columns:
        restored_df[column] = restored_df[column].map(lambda x: x.replace("'", "''") if isinstance(x, str) else x)