create_trips_table_query = f"""
    drop table if exists trips;
    create table if not exists trips(
        trip_id int8 not null unique
        , start_date timestamp
        , end_date timestamp
        , duration_sec int
        , is_member bool
        , start_station_id int8
        , end_station_id int8
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
        datetime timestamp not null unique
        , year int
        , month int
        , day int
        , day_of_week int
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
    truncate table time;
    insert into time
    select  
    	dt as datetime
        , extract(year from datetime) as year
        , extract(month from datetime) as month
        , extract(day from datetime) as day
        , extract(dow from datetime) as day_of_week
        , extract(hour from datetime) as hour
    from (
        select distinct dt
        from (
            select start_date as dt from trips
            union all
            select end_date as dt from trips
            union all
            select last_updated_dt as dt from gbfs
        )
    );
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

check_primary_key_constraint ="""
    select count(*)
    from (
        select {}, count(*)
        from {}
        group by 1
        having count(*) > 2
    )
"""

sample_query = """
    select 
        g.station_id
        , s.name
        , avg(g.num_bikes_available)
        , sum(t.daily_trip_count)
    from gbfs g
    inner join stations s
        on g.station_id = s.station_id
    inner join (
      select start_station_id, count(*) as daily_trip_count
      from trips
      where cast(start_date as date) = '2021-04-20'
      group by 1
    ) t on t.start_station_id = g.station_id 
    where cast(g.last_updated_dt as date) = '2021-04-20'
    group by 1,2
    limit 5;
"""