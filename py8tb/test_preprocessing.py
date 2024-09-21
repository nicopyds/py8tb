from py8tb.preprocessing import get_photos_df

path_indexed_files = "/Users/nicolaepopescul/Desktop/code/streams/20240622_python_8tb/data/df_2024_06_30_18_08_37.parquet.gzip"
def test_get_photos_df():
    photos = get_photos_df(df = None, path = path_indexed_files)
    assert photos["FileType"].unique()[0] == "photo", "You have other file types in your df"
