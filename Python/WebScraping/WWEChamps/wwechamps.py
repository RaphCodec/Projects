import mechanicalsoup
import pandas as pd
import sqlite3
from datetime import datetime
import tomli
from loguru import logger
from json import dumps
from icecream import ic


def CreateTable(
    df,
    table: str = None,
    primary: str = None,
    parent_table: list = [],
    table_fk_column: list = [],
    parent_fk_column: list = [],
) -> None:
    # Define dtype map to map pandas to SQLite data types
    dtypes_map = {
        "int64": "INTEGER",
        "int32": "INTEGER",
        "int16": "INTEGER",
        "int8": "INTEGER",
        "float64": "REAL",
        "float32": "REAL",
        "object": "TEXT",
        "bool": "INTEGER",
        "datetime64": "TEXT",  # or INTEGER depending on storage preference
        "datetime64[ns]": "TEXT",  # or INTEGER depending on storage preference
        "timedelta64": "TEXT",  # or INTEGER depending on storage preference
        "timedelta64[ns]": "TEXT",  # or INTEGER depending on storage preference
        "category": "TEXT",  # or INTEGER depending on storage preference
    }

    # Generate column definitions excluding the primary key column if provided
    column_definitions = [
        f"{col} {dtypes_map[str(dtype)]}"
        for col, dtype in df.dtypes.items()
        if col != primary
    ]

    # Include the primary key column separately
    if primary:
        column_definitions.insert(0, f"{primary} INTEGER PRIMARY KEY")

    # Join column definitions to create the query
    columns_query = ", ".join(column_definitions)

    # Generate CREATE TABLE query
    query = f"CREATE TABLE IF NOT EXISTS {table} ({columns_query}"

    # adding Foreign Keys
    if parent_table and parent_fk_column and table_fk_column:
        for p_table, p_column, t_column in zip(
            parent_table, parent_fk_column, table_fk_column
        ):
            query += f" ,FOREIGN KEY({t_column}) REFERENCES {p_table}({p_column})"
        query += ");"
    else:
        query += ");"

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

    return

def Upsert(df, table: str, pk: str) -> None:
    # create and connect to sqlite3 database
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    DIT = pd.read_sql(f"Select {pk} FROM {table}", conn)

    #filtering existing and new rows
    df_insert = df[~df[pk].isin(DIT[pk].tolist())]
    df_update = df[df[pk].isin(DIT[pk].tolist())]

    if not df_insert.empty:
        # insert data into table
        cursor.executemany(
            f"""Insert into {table}
                            values({('?,' * len(df_insert.columns))[:-1]})
                            """,
            df_insert.values.tolist(),
        )

        conn.commit()
    logger.info(f"Rows inserted: {len(df_insert)}")

    if not df_update.empty:
        placeholders = ", ".join(
            [f"{col} = ?" for col in df_update.columns if col != pk]
        )
        cursor.executemany(
            f"""UPDATE {table}
                    SET {placeholders}
                    WHERE {pk} = ?
                    """,
            df_update.values.tolist(),
        )

        conn.commit()
    logger.info(f"Rows updated: {len(df)}")

    conn.close  # close conncection


def main():
    # making broswer object and opening url
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)

    # getting all the data
    td = browser.page.find_all("td")
    browser.close()  # closing browser

    data = [value.text.replace("\n", "") for value in td]
    titles(data)
    reigns(data)


def titles(data):
    # slicing list to get data for each wwe championship change
    titles = data[
        data.index("WWWF World Heavyweight Championship") : data.index(
            "Undisputed WWE Universal Championship"
        )
        + 2
    ]

    cols = ["Names", "Years"]
    df_dict = {}

    for idx, key in enumerate(cols):
        df_dict[key] = titles[idx:][::2]

    df = pd.DataFrame(df_dict)

    # creating a column to count order of titles and act as a primary key
    df.insert(loc=0, column="TitleID", value=df.index + 1)

    CreateTable(df, TABLE_5, "TitleID")
    Upsert(df, TABLE_5, "TitleID")


def reigns(data):
    # slicing list to get data for each wwe championship change
    reigns = data[data.index("Buddy Rogers") : data.index("[204]") + 1]

    """deleting specific unnecessary - from data so that it can be converted to 
        a dataframe later.  These are the - found in the No. column on the webpage
         table but have a <td> tag.
        DO NOT TRY TO REPLACE ALL -
        THERE ARE SOME THAT ARE NEEDED TO COMPLETE ROWS"""
    del reigns[reigns.index("Antonio Inoki") + 9]
    del reigns[reigns.index("Ted DiBiase") + 9]
    del reigns[reigns.index("December 3, 1991") + 8]
    del reigns[reigns.index("January 19, 1997") + 8]
    del reigns[reigns.index("June 29, 1998") + 8]
    del reigns[reigns.index("September 14, 1999") + 8]
    del reigns[reigns.index("September 17, 2006") + 8]
    del reigns[reigns.index("June 7, 2009") + 8]
    del reigns[reigns.index("July 17, 2011") + 8]
    del reigns[reigns.index("September 15, 2013") + 8]
    del reigns[reigns.index("April 6, 2014") + 8]
    del reigns[reigns.index("March 29, 2015") + 8]

    # removing unnecssary '†' character so that creating df is possible later
    reigns = list(filter(lambda a: a != "†", reigns))

    """these are table values that identifiy the company name at the time
        However they are not needed and create extra undesired elements in the dataframe"""

    to_remove = [
        "World Wide Wrestling Federation (WWWF)",
        "National Wrestling Alliance: World Wide Wrestling Federation (WWWF)",
        "National Wrestling Alliance: World Wrestling Federation (WWF)",
        "World Wrestling Federation (WWF)",
        "World Wrestling Entertainment (WWE)",
        "WWE: SmackDown",
        "WWE: ECW",
        "WWE: Raw",
        "WWE (unbranded)",
    ]

    # fiding the index numbers for the values in to remove if they are in the reigns list
    indices = [idx for idx, x in enumerate(reigns) if x in to_remove]

    # the column names
    cols = [
        "Champion",
        "Date",
        "Event",
        "Location",
        "Reign",
        "Days",
        "DaysRecog",
        "Notes",
    ]
    # slcing reigns list to remove unwanted values and adding them to an empty list
    reigns_lst = []
    for idx, x in enumerate(indices):
        if idx == 0:
            cop = reigns.copy()
            cop = cop[: x - 1]
            reigns_lst.extend(cop)
        elif x == indices[-1]:
            cop = reigns.copy()
            cop = cop[x + 1 :]
            reigns_lst.extend(cop)
        else:
            cop = reigns.copy()
            cop = cop[indices[idx - 1] + 1 : x - 1]
            reigns_lst.extend(cop)

    # adding list values to corresponding columns in a dictionary
    reigns_dict = {}

    for idx, key in enumerate(cols):
        reigns_dict[key] = reigns_lst[idx:][::9]

    # dict to dataframe
    reigns = pd.DataFrame(reigns_dict)

    reigns = reigns.replace("—", None)  # removing uneeded character
    reigns = reigns.replace("", None)  # removing uneeded character
    reigns[["Days", "DaysRecog"]] = reigns[["Days", "DaysRecog"]].replace(
        regex=",", value=""
    )  # removing uneeded character
    reigns[["Days", "DaysRecog"]] = reigns[["Days", "DaysRecog"]].replace(
        regex="<1", value=".5"
    )  # removing uneeded character
    reigns["Days"] = reigns["Days"].str.rstrip("+")
    reigns["DaysRecog"] = reigns["DaysRecog"].str.rstrip("+")
    reigns["Date"] = pd.to_datetime(reigns["Date"])
    # changing back to str after formatting since sqlite does not have date type
    reigns["Date"] = reigns["Date"].astype(str)

    # creating a column to count order of champs and act as a primary key
    reigns.insert(loc=0, column="ID", value=reigns.index)

    # creating lookup tables
    Champions = pd.DataFrame(data={"Champion": reigns["Champion"].unique()})
    Champions.insert(loc=0, column="ChampionID", value=Champions.index + 1)

    Events = pd.DataFrame(data={"Event": reigns["Event"].unique()})
    Events.insert(loc=0, column="EventID", value=Events.index + 1)

    Locations = pd.DataFrame(data={"Location": reigns["Location"].unique()})
    Locations.insert(loc=0, column="LocationID", value=Locations.index + 1)

    # replacing fact table valeus with look up values
    reigns["Champion"] = reigns["Champion"].map(
        Champions.set_index("Champion")["ChampionID"].to_dict()
    )
    reigns["Event"] = reigns["Event"].map(
        Events.set_index("Event")["EventID"].to_dict()
    )
    reigns["Location"] = reigns["Location"].map(
        Locations.set_index("Location")["LocationID"].to_dict()
    )

    CreateTable(Champions, TABLE_2, "ChampionID")
    CreateTable(Events, TABLE_3, "EventID")
    CreateTable(Locations, TABLE_4, "LocationID")
    CreateTable(
        reigns,
        TABLE_1,
        "ID",
        [TABLE_2, TABLE_3, TABLE_4],
        ["Champion", "Event", "Location"],
        ["ChampionID", "EventID", "LocationID"],
    )

    # inserting data into sqlite3 database
    Upsert(Champions, TABLE_2, "ChampionID")
    Upsert(Events, TABLE_3, "EventID")
    Upsert(Locations, TABLE_4, "LocationID")
    Upsert(reigns, TABLE_1, "ID")


if __name__ == "__main__":
    with open("WWEChamps.config.toml", mode="rb") as fp:
        CONFIG = tomli.load(fp)
    URL = CONFIG["URL"]
    DB = CONFIG["DB"]
    TABLE_1 = CONFIG["TABLE_1"]
    TABLE_2 = CONFIG["TABLE_2"]
    TABLE_3 = CONFIG["TABLE_3"]
    TABLE_4 = CONFIG["TABLE_4"]
    TABLE_5 = CONFIG["TABLE_5"]

    logger.info(f"Using Config:\n{dumps(CONFIG, indent = 4)}\n")
    start = datetime.now()
    logger.info(f"Script Started")

    try:
        main()
        elapsed = datetime.now() - start
        logger.info(
            f"Script Ran Sucessfully. {elapsed.seconds // 3600} hours {elapsed.seconds % 3600 // 60} minutes {elapsed.seconds % 60} seconds elapsed"
        )
    except Exception as e:
        elapsed = datetime.now() - start
        logger.error(
            f"Script Failed. {elapsed.seconds // 3600} hours {elapsed.seconds % 3600 // 60} minutes {elapsed.seconds % 60} seconds elapsed"
        )
        # logger.exception(f'Error: {e}')
        """
        UNCOMMENT THE ABOVE LINE FOR A MORE DETAILED AND MORE FORMATTED ERROR MESSAGE
        """
        from traceback import format_exc

        logger.error(f"Error: {e}")
        logger.error(f"\n{format_exc()}")
