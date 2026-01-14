from io import StringIO
import polars as pl

# add your mapping/enrichments/resolving in here
def clean_date_column(df: pl.DataFrame) -> pl.DataFrame:
    """
    Convert date column from yyyy/mm/dd to yyyy-mm-dd format.
    """
    df = df.with_columns(
        pl.col('date_of_birth').str.replace_all('/', '-').alias('date_of_birth')
    )
    return df

def map_func(item):
    """
    Reads a CSV file, cleans it, and returns the cleaned DataFrame.
    Optionally writes to an output path.
    
    Cleaning operations:
    - Converting dates from yyyy/mm/dd to yyyy-mm-dd format
    - Converting names to title case
    """
    
    # Read CSV
    csv = StringIO(item)
    df = pl.read_csv(csv, truncate_ragged_lines=True)    
    # Clean date of birth (replace / with -)
    df = clean_date_column(df)
    
    # Clean names to title case
    df = df.with_columns([
        pl.col('first_name').str.strip_chars().str.to_titlecase().alias('first_name'),
        pl.col('surname').str.strip_chars().str.to_titlecase().alias('surname')
    ])

    return df.write_csv().encode("utf-8")

if __name__ == "__main__":
    test_data = pl.read_csv('data/sanctioned_individuals.csv')
    item = test_data.write_csv()
    cleaned_df = map_func(item)
    with open('data/sanctioned_individuals_cleaned.csv', 'wb') as f:
        f.write(cleaned_df)
