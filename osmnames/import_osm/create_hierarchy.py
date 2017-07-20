import os

from osmnames.database.functions import exec_sql, exec_sql_from_file, vacuum_database
from osmnames import consistency_check
from osmnames import logger

SQL_DIR = "{}/create_hierarchy/".format(os.path.dirname(__file__))
log = logger.setup(__name__)


def create_hierarchy():
    set_geometry_centers()
    cluster_geometries()

    set_parent_ids()

    drop_geometry_center_indexes()
    consistency_check.missing_parent_ids()


def set_geometry_centers():
    exec_sql_from_file("set_geometry_centers.sql", cwd=SQL_DIR)
    vacuum_database()


def cluster_geometries():
    exec_sql("""
        CLUSTER osm_linestring_center_geom ON osm_linestring;
        CLUSTER osm_polygon_geom ON osm_polygon;
        CLUSTER osm_housenumber_geom ON osm_housenumber;
        CLUSTER osm_point_geom ON osm_point;
    """)


def set_parent_ids():
    exec_sql_from_file("set_parent_ids.sql", cwd=SQL_DIR)
    vacuum_database()


def drop_geometry_center_indexes():
    exec_sql("DROP INDEX osm_linestring_center_geom")
    exec_sql("DROP INDEX osm_polygon_center_geom")
