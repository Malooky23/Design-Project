# preprocess_data.py
import pandas as pd
import os
from country_mappings import SWEDISH_TO_ENGLISH_COUNTRIES, COUNTRY_COORDS


def process_raw_file(file_path, name_col, gender=None):
    """
    Helper function to read and process a single raw CSV file.
    This function is based on the logic from your original utils.py.
    """
    print(f"Processing {file_path}...")
    try:
        # Using low_memory=False is fine for this one-time script
        df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}. Skipping.")
        return pd.DataFrame()

    # Standardize column names
    df = df.rename(columns={df.columns[0]: name_col, df.columns[1]: 'Total'})
    df.columns = df.columns.str.replace('\n', ' ')

    # Melt from wide to long format
    id_vars = [name_col, 'Total']
    country_cols = [col for col in df.columns if col not in id_vars]
    df_long = df.melt(id_vars=id_vars, value_vars=country_cols,
                      var_name='country', value_name='count')

    # Drop the 'Total' column, it's not needed in the long format
    df_long = df_long.drop(columns=['Total'], errors='ignore')

    # Clean the 'count' column efficiently
    df_long['count'] = df_long['count'].astype(
        str).str.replace(',', '', regex=False)
    df_long['count'] = pd.to_numeric(
        df_long['count'], errors='coerce').fillna(0).astype(int)

    # Filter out zero counts
    df_long = df_long[df_long['count'] > 0].copy()

    # Add gender and aggregate to prevent double-counting from source data
    if gender:
        df_long['gender'] = gender
        group_cols = [name_col, 'gender', 'country']
        df_long = df_long.groupby(group_cols, as_index=False)['count'].sum()
    else:  # For surnames
        group_cols = [name_col, 'country']
        df_long = df_long.groupby(group_cols, as_index=False)['count'].sum()

    print(f"Finished processing {file_path}. Found {len(df_long)} records.")
    return df_long


def main():
    """
    Main function to run the entire preprocessing pipeline.
    """
    # Ensure the data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # --- 1. PROCESS FIRST NAMES ---
    print("--- Processing First Names ---")
    # NOTE: Your provided file was 'women-copy.csv'. Ensure your actual files are named as below.
    men_df = process_raw_file('data/men1.csv', 'name', gender='M')
    women_df = process_raw_file('data/women1.csv', 'name', gender='F')

    if men_df.empty and women_df.empty:
        print("No first name data found. Aborting.")
        return

    names_df = pd.concat([men_df, women_df], ignore_index=True)

    print("Mapping country names and adding coordinates...")
    names_df['country'] = names_df['country'].map(SWEDISH_TO_ENGLISH_COUNTRIES)
    names_df = names_df.dropna(subset=['country'])

    coords = names_df['country'].map(COUNTRY_COORDS)
    names_df['lat'] = coords.apply(
        lambda x: x[0] if isinstance(x, tuple) else None)
    names_df['lon'] = coords.apply(
        lambda x: x[1] if isinstance(x, tuple) else None)
    names_df = names_df.dropna(subset=['lat', 'lon'])

    # Optimize data types to reduce memory usage and increase loading speed
    names_df['name'] = names_df['name'].astype('category')
    names_df['gender'] = names_df['gender'].astype('category')
    names_df['country'] = names_df['country'].astype('category')
    names_df['count'] = names_df['count'].astype('uint32')
    names_df['lat'] = names_df['lat'].astype('float32')
    names_df['lon'] = names_df['lon'].astype('float32')

    names_df = names_df[['name', 'gender', 'country', 'count', 'lat', 'lon']]

    # Save the final dataframe to a Parquet file
    output_path = 'data/processed_names.parquet'
    names_df.to_parquet(output_path, index=False)
    print(f"\n✅ Successfully saved processed first names to {output_path}")

    # --- 2. PROCESS SURNAMES ---
    print("\n--- Processing Surnames ---")
    surnames_df = process_raw_file('data/surname1.csv', 'lastname')

    if not surnames_df.empty:
        surnames_df['country'] = surnames_df['country'].map(
            SWEDISH_TO_ENGLISH_COUNTRIES)
        surnames_df = surnames_df.dropna(subset=['country'])

        print("Ranking surnames by country...")
        surnames_df['rank'] = surnames_df.groupby('country')['count'].rank(
            method='dense', ascending=False).astype(int)
        last_names_df = surnames_df[['country', 'rank', 'lastname']].sort_values(by=[
                                                                                 'country', 'rank'])

        # Optimize dtypes
        last_names_df['country'] = last_names_df['country'].astype('category')
        last_names_df['lastname'] = last_names_df['lastname'].astype(
            'category')
        last_names_df['rank'] = last_names_df['rank'].astype('uint16')

        # Save to Parquet
        output_path_surnames = 'data/processed_surnames.parquet'
        last_names_df.to_parquet(output_path_surnames, index=False)
        print(
            f"✅ Successfully saved processed surnames to {output_path_surnames}")
    else:
        print("No surname data found or processed.")

    print("\nPreprocessing complete.")


if __name__ == '__main__':
    main()
