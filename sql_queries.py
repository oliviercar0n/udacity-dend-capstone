create_trips_table_query = f"""
    drop table if exists trips;
    create table if not exists trips(
        trip_id int8 not null
        , start_date timestamp not null
        , end_date timestamp not null
        , duration_sec int
        , is_member varchar
        , start_station_id int8 not null
        , end_station_id int8 not null
    )
"""

create_gbfs_table_query = f"""
    drop table if exists gbfs;
    create table if not exists gbfs(
        station_id int8
        , is_charging bool 
        , is_installed int8
        , is_renting int8
        , is_returning int8
        , last_reported int8
        , num_bikes_available int8
        , num_bikes_disabled int8
        , num_docks_available int8
        , num_docks_disabled int8
        , num_ebikes_available int8
        , last_updated_dt timestamp
    )
"""

create_stations_table_query = f"""
    drop table if exists stations;
    create table if not exists stations(
        station_id int not null
        , name varchar
        , lat decimal(9,6)
        , lon decimal(9,6)
    )
"""

copy_table_query = """
    copy {}
    from '{}'
    access_key_id '{}'
    secret_access_key '{}'
    format as {}
"""

create_queries = [
    create_trips_table_query,
    create_stations_table_query,
    create_gbfs_table_query
]

check_row_count = """
    select count(*)
    from {}
"""