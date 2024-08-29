"""Main module."""

import numpy as np
import os
import rasterio
from pyproj import CRS
from shapely.geometry import box

# Local application/library specific imports
from .download.urbanwatch import get_geotif_urbanwatch
from .download.mbfp import get_geojson_links, find_row_for_location
from .download.osm import load_geojsons_from_openstreetmap
from .download.utils import download_file
from .download.oemj import save_oemj_as_geotiff
from .download.nasadem import (
    download_nasa_dem,
    interpolate_dem,
    get_utm_crs
)
from .download.gee import (
    initialize_earth_engine,
    get_roi,
    get_image_collection,
    save_geotiff
)
from .geo.utils import (
    initialize_geod,
    calculate_distance,
    normalize_to_one_meter,
    setup_transformer,
    transform_coords,
    convert_land_cover_array,
    load_geojsons_from_multiple_gz,
    swap_coordinates,
    filter_buildings,
    create_building_polygons
)
from .geo.grid import (
    group_and_label_cells, 
    process_grid,
    calculate_grid_size,
    create_coordinate_mesh,
    create_cell_polygon,
    create_land_cover_grid_from_geotiff_polygon
)
from .utils.visualization import (
    plot_grid, 
    get_land_cover_classes,
    visualize_land_cover_grid
)

def get_grid_land_cover(rectangle_vertices, meshsize, source = 'Urbanwatch'):

    # Initialize Earth Engine
    initialize_earth_engine()

    if source == 'Urbanwatch':
        roi = get_roi(rectangle_vertices)
        collection_name = "projects/sat-io/open-datasets/HRLC/urban-watch-cities"
        image = get_image_collection(collection_name, roi)
        save_geotiff(image, "land_cover.tif")
    elif source == 'OpenEarthMapJapan':
        save_oemj_as_geotiff(rectangle_vertices, "land_cover.tif")    
    
    land_cover_classes = get_land_cover_classes(source)

    land_cover_grid_str = create_land_cover_grid_from_geotiff_polygon("land_cover.tif", meshsize, land_cover_classes, rectangle_vertices)
    color_map = {cls: [r/255, g/255, b/255] for (r,g,b), cls in land_cover_classes.items()}
    # color_map['No Data'] = [0.5, 0.5, 0.5]
    visualize_land_cover_grid(land_cover_grid_str, meshsize, color_map, land_cover_classes)
    land_cover_grid_int = convert_land_cover_array(land_cover_grid_str, land_cover_classes)

    return land_cover_grid_int

def get_grid_building_height(rectangle_vertices, meshsize, output_dir, source = 'Microsoft Building Footprints'):

    if source == 'Microsoft Building Footprints':
        # print_flush(f"Testing get_geojson_links with output_dir: {output_dir}")
        df_links = get_geojson_links(output_dir)

        # Find and download files
        filenames = []
        for vertex in rectangle_vertices:
            lat, lon = vertex
            row = find_row_for_location(df_links, lat, lon)
            if row is not None:
                location = row["Location"]
                quadkey = row["QuadKey"]
                filename = os.path.join(output_dir, f"{location}_{quadkey}.gz")
                if filename not in filenames:
                    filenames.append(filename)
                    download_file(row["Url"], filename)
            else:
                print("No matching row found.")

        # Load and process GeoJSON data
        geojson_data = load_geojsons_from_multiple_gz(filenames)
        swap_coordinates(geojson_data)
    elif source == 'OpenStreetMap':
        geojson_data = load_geojsons_from_openstreetmap(rectangle_vertices)

    # Calculate grid and normalize vectors
    geod = initialize_geod()
    vertex_0, vertex_1, vertex_3 = rectangle_vertices[0], rectangle_vertices[1], rectangle_vertices[3]

    dist_side_1 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_1[1], vertex_1[0])
    dist_side_2 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_3[1], vertex_3[0])

    side_1 = np.array(vertex_1) - np.array(vertex_0)
    side_2 = np.array(vertex_3) - np.array(vertex_0)

    u_vec = normalize_to_one_meter(side_1, dist_side_1)
    v_vec = normalize_to_one_meter(side_2, dist_side_2)

    origin = np.array(rectangle_vertices[0])
    grid_size, adjusted_meshsize = calculate_grid_size(side_1, side_2, u_vec, v_vec, meshsize)  

    print(f"Calculated grid size: {grid_size}")
    print(f"Adjusted mesh size: {adjusted_meshsize}")

    # Create the grid
    grid = np.zeros(grid_size)

    # Setup transformer and plotting extent
    transformer = setup_transformer(CRS.from_epsg(4326), CRS.from_epsg(3857))
    extent = [min(coord[1] for coord in rectangle_vertices), max(coord[1] for coord in rectangle_vertices),
              min(coord[0] for coord in rectangle_vertices), max(coord[0] for coord in rectangle_vertices)]
    plotting_box = box(extent[2], extent[0], extent[3], extent[1])

    # Filter polygons and create building polygons
    filtered_buildings = filter_buildings(geojson_data, plotting_box)
    building_polygons, idx = create_building_polygons(filtered_buildings)

    # Calculate building heights for each grid cell
    buildings_found = 0
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            cell = create_cell_polygon(origin, i, j, adjusted_meshsize, u_vec, v_vec)
            for k in idx.intersection(cell.bounds):
                polygon, height = building_polygons[k]
                if cell.intersects(polygon) and cell.intersection(polygon).area > cell.area/2:
                    grid[i, j] = height
                    buildings_found += 1
                    break

    # Plot the results
    plot_grid(grid, origin, adjusted_meshsize, u_vec, v_vec, transformer, CRS.from_epsg(3857),
              rectangle_vertices, 'building_height', buildings=filtered_buildings)

    return grid#, buildings_found

def get_grid_dem(rectangle_vertices, meshsize, output_dir, api_key, **kwargs):
    geod = initialize_geod()

    center_lat = sum(vertex[0] for vertex in rectangle_vertices) / len(rectangle_vertices)
    center_lon = sum(vertex[1] for vertex in rectangle_vertices) / len(rectangle_vertices)
    dst_crs = get_utm_crs(center_lat, center_lon)

    vertex_0 = rectangle_vertices[0]
    vertex_1 = rectangle_vertices[1]
    vertex_3 = rectangle_vertices[3]

    dist_side_1 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_1[1], vertex_1[0])
    dist_side_2 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_3[1], vertex_3[0])

    side_1 = np.array(vertex_1) - np.array(vertex_0)
    side_2 = np.array(vertex_3) - np.array(vertex_0)

    u_vec = normalize_to_one_meter(side_1, dist_side_1)
    v_vec = normalize_to_one_meter(side_2, dist_side_2)

    origin = np.array(rectangle_vertices[0])
    grid_size = calculate_grid_size(side_1, side_2, u_vec, v_vec, meshsize)

    cell_coords = create_coordinate_mesh(origin, grid_size, meshsize, u_vec, v_vec)

    cell_coords_flat = cell_coords.reshape(2, -1).T
    transformer = setup_transformer(CRS.from_epsg(4326), dst_crs)
    transformed_coords = np.array([transform_coords(transformer, lon, lat) for lat, lon in cell_coords_flat])

    transformed_coords = np.array([coord for coord in transformed_coords if coord is not None])

    all_coords = np.array(rectangle_vertices)
    buffer = 0.01
    bbox = [
        min(all_coords[:, 1]) - buffer,
        min(all_coords[:, 0]) - buffer,
        max(all_coords[:, 1]) + buffer,
        max(all_coords[:, 0]) + buffer
    ]

    dem_data = download_nasa_dem(bbox, api_key)

    interpolated_dem = interpolate_dem(dem_data, transformed_coords, dst_crs)
    dem_grid = interpolated_dem.reshape(grid_size[::-1]).T

    plot_grid(dem_grid, origin, meshsize, u_vec, v_vec, transformer, dst_crs, rectangle_vertices, 'dem')

    return dem_grid

# Main function to handle land cover, building height, and DEM
def get_grid_data(rectangle_vertices, data_type, meshsize=4, output_dir='output', **kwargs):
    if data_type == 'land_cover':
        land_cover_classes = kwargs.pop('land_cover_classes', None)
        if land_cover_classes is None:
            raise ValueError("land_cover_classes is required for land_cover analysis")
        return get_grid_land_cover(rectangle_vertices, land_cover_classes, meshsize, output_dir, **kwargs)
    elif data_type == 'building_height':
        return get_grid_building_height(rectangle_vertices, meshsize, output_dir, **kwargs)
    elif data_type == 'dem':
        api_key = kwargs.pop('api_key', None)
        if api_key is None:
            raise ValueError("api_key is required for DEM analysis")
        return get_grid_dem(rectangle_vertices, meshsize, output_dir, api_key, **kwargs)
    else:
        raise ValueError("Invalid data_type. Choose 'land_cover', 'building_height', or 'dem'.")
    
def create_3d_voxel(building_height_grid_ori, land_cover_grid_ori, dem_grid_ori, tree_grid_ori, voxel_size=2.0):

    # Prepare grids
    building_height_grid = np.flipud(building_height_grid_ori.copy())
    land_cover_grid = np.flipud(land_cover_grid_ori.copy()) + 1
    dem_grid = np.flipud(dem_grid_ori.copy()) - np.min(dem_grid_ori)
    building_nr_grid = group_and_label_cells(np.flipud(building_height_grid_ori.copy()))
    dem_grid = process_grid(building_nr_grid, dem_grid)
    tree_grid = np.flipud(tree_grid_ori.copy())

    # Ensure all input grids have the same shape
    assert building_height_grid.shape == land_cover_grid.shape == dem_grid.shape == tree_grid.shape, "Input grids must have the same shape"

    # Get the dimensions of the input grids
    rows, cols = building_height_grid.shape

    # Calculate the maximum height needed for the 3D array
    max_height = int(np.ceil(np.max(building_height_grid + dem_grid + tree_grid) / voxel_size))

    # Create an empty 3D array
    voxel_grid = np.zeros((rows, cols, max_height), dtype=np.int32)

    # Fill the 3D array
    for i in range(rows):
        for j in range(cols):
            ground_level = int(dem_grid[i, j] / voxel_size)
            building_height = int(building_height_grid[i, j] / voxel_size)
            tree_height = int(tree_grid[i, j] / voxel_size)
            land_cover = land_cover_grid[i, j]

            # Fill underground cells with -1
            voxel_grid[i, j, :ground_level] = -1

            # Set ground level cell to land cover
            voxel_grid[i, j, ground_level] = land_cover

            # Fill tree crown with value -2
            if tree_height > 0:
                tree_start = ground_level + 2
                tree_end = ground_level + tree_height
                voxel_grid[i, j, tree_start:tree_end+1] = -2

            # Fill building with value -3
            if building_height > 0:
                voxel_grid[i, j, ground_level+1:ground_level+building_height+1] = -3

    return voxel_grid