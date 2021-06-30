create_trips_table_query = f"""
    drop table if exists trips;
    create table if not exists trips(
        trip_id int8 not null primary key
        , start_date timestamp not null
        , end_date timestamp not null
        , duration_sec int
        , is_member bool
        , start_station_id int8 not null
        , end_station_id int8 not null
    )
"""

create_gbfs_table_query = f"""
    drop table if exists gbfs;
    create table if not exists gbfs(
        station_id int8 primary key
        , is_charging bool 
        , is_installed bool
        , is_renting bool
        , is_returning bool
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

create_time_table_query = f"""
    drop table if exists time;
    create table if not exists time(
        datetime timestamp not null primary key
        , hour int
        , month int
        , day int
        , day_of_week int,
        , hour int
    )
"""

copy_table_query = """
    copy {}
    from '{}'
    access_key_id '{}'
    secret_access_key '{}'
    format as {}
"""

copy_time_query = """
    select
        datetime
        , extract(year from datetime) as year
        , extract(month from datetime) as year
        , extract(day from datetime) as year
        , extract(day_of_week from datetime) as year
        , extract(hour from datetime) as year
    from (
        select distinct datetime
        from (
            select start_date as datetime from trips
            union all
            select end_date as datetime from trips
            union all
            select last_updated_dt as datetime from gbfs
        )
    )
"""

create_queries = [
    create_trips_table_query,
    create_stations_table_query,
    create_gbfs_table_query,
    create_time_table_query
]

check_row_count = """
    select count(*)
    from {}
"""