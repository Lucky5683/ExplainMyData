import polars as pl
import io

def get_data_context(df: pl.DataFrame) -> dict:
    """
    Returns a summary of the metadata for the given Polars DataFrame.
    This metadata includes column names, data types, and the first 3 rows as a sample.
    """
    columns = df.columns
    # Convert Polars data types to strings for easy serialization
    data_types = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
    
    # Get the first 3 rows as a list of dictionaries
    sample_data = df.head(3).to_dicts()
    
    return {
        "columns": columns,
        "data_types": data_types,
        "sample_data": sample_data
    }

def load_file(file_obj, filename: str) -> pl.DataFrame:
    """
    Loads an uploaded file (CSV or Excel) into a Polars DataFrame.
    """
    if filename.endswith('.csv'):
        return pl.read_csv(file_obj)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        return pl.read_excel(file_obj)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")