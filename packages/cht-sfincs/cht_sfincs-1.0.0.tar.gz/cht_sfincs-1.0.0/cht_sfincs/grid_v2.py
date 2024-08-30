# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:24:49 2022

@author: ormondt
"""
import time
import os
import numpy as np
from matplotlib import path
from pyproj import CRS, Transformer
import shapely

import xugrid as xu
import xarray as xr
import warnings
import geopandas as gpd
np.warnings = warnings

import pandas as pd

import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import export_image

class SfincsGrid:
    def __init__(self, model):
        self.model = model
        self.x0 = None
        self.y0 = None
        self.dx = None
        self.dy = None
        self.rotation = None
        self.nr_cells = 0
        self.nr_refinement_levels = 1
        self.version = 0
        self.data = None
        self.type = "regular"
        self.exterior = gpd.GeoDataFrame()

    def read(self, file_name=None):
        if file_name == None:
            if not self.model.input.variables.qtrfile: 
                self.model.input.variables.qtrfile = "sfincs.nc"
            file_name = os.path.join(self.model.path, self.model.input.variables.qtrfile)
        self.data = xu.open_dataset(file_name)
        self.data.close()
        self.type = "quadtree"
        self.nr_cells = self.data.dims['mesh2d_nFaces']
        self.get_exterior()
        crd_dict = self.data["crs"].attrs
        if "projected_crs_name" in crd_dict:
            self.model.crs = CRS(crd_dict["projected_crs_name"])
        elif "geographic_crs_name" in crd_dict:
            self.model.crs = CRS(crd_dict["geographic_crs_name"])
        else:
            print("Could not find CRS in quadtree netcdf file")    

    def write(self, file_name=None, version=0):
        if file_name == None:
            if not self.model.input.variables.qtrfile: 
                self.model.input.variables.qtrfile = "sfincs.nc"
            file_name = os.path.join(self.model.path, self.model.input.variables.qtrfile)
        attrs = self.data.attrs
        ds = self.data.ugrid.to_dataset()
        ds.attrs = attrs
        ds.to_netcdf(file_name)

    def build(self,
              x0,
              y0,
              nmax,
              mmax,
              dx,
              dy,
              rotation,
              refinement_polygons=None):

        print("Building mesh ...")

        # Always quadtree !
        self.type = "quadtree"

        start = time.time()

        print("Getting cells ...")

        self.x0 = x0
        self.y0 = y0
        self.dx = dx
        self.dy = dy
        self.nmax = nmax
        self.mmax = mmax
        self.rotation = rotation
        self.cosrot = np.cos(rotation*np.pi/180)
        self.sinrot = np.sin(rotation*np.pi/180)
        self.refinement_polygons = refinement_polygons

        # Make regular grid
        self.get_regular_grid()
 
        # Initialize data arrays 
        self.initialize_data_arrays()

        # Refine all cells 
        if refinement_polygons is not None:
            self.refine_mesh()

        # Initialize data arrays
        self.initialize_data_arrays()

        # Get all neighbor arrays (mu, mu1, mu2, nu, nu1, nu2)
        self.get_neighbors()

        # Get uv points
        self.get_uv_points()

        # Create xugrid dataset 
        self.to_xugrid()
        
#        self.get_exterior()

        self.clear_temporary_arrays()

        print("Time elapsed : " + str(time.time() - start) + " s")

    def set_bathymetry(self, bathymetry_sets, quiet=True):
        
        from cht.bathymetry.bathymetry_database import bathymetry_database

        if not quiet:
            print("Getting bathymetry data ...")

        nlev = self.nr_refinement_levels
        
        # Check if coordinates already exists
        xy = self.data.grid.face_coordinates
        zz = np.full(self.nr_cells, np.nan)
                        
        # Loop through all levels
        for ilev in range(nlev):

            if not quiet:
                print("Processing bathymetry level " + str(ilev + 1) + " of " + str(nlev) + " ...")
            
            ifirst = self.ifirst[ilev]
            if ilev<nlev - 1:
                ilast = self.ifirst[ilev + 1]
            else:
                ilast = self.nr_cells - 1
            
            # Make blocks off cells in this level only
            cell_indices_in_level = np.arange(ifirst, ilast + 1, dtype=int)
                  
            xz  = xy[cell_indices_in_level, 0]
            yz  = xy[cell_indices_in_level, 1]
            dxmin = self.dx/2**ilev

            if self.data.grid.crs.is_geographic:
                dxmin = dxmin * 111000.0

            zgl = bathymetry_database.get_bathymetry_on_points(xz,
                                                               yz,
                                                               dxmin,
                                                               self.model.crs,
                                                               bathymetry_sets)
            zz[cell_indices_in_level] = zgl

        ugrid2d = self.data.grid
        self.data["z"] = xu.UgridDataArray(xr.DataArray(data=zz, dims=[ugrid2d.face_dimension]), ugrid2d)

    def snap_to_grid(self, polyline, max_snap_distance=1.0):
        if len(polyline) == 0:
            return gpd.GeoDataFrame()
        geom_list = []
        for iline, line in polyline.iterrows():
            geom = line["geometry"]
            if geom.geom_type == 'LineString':
                geom_list.append(geom)
        gdf = gpd.GeoDataFrame({'geometry': geom_list})    
        print("Snapping to grid ...")
        snapped_uds, snapped_gdf = xu.snap_to_grid(gdf, self.data.grid, max_snap_distance=max_snap_distance)
        print("Snapping to grid done.")
        snapped_gdf = snapped_gdf.set_crs(self.model.crs)
        return snapped_gdf

    def face_coordinates(self):
        # if self.data is None:
        #     return None, None
        xy = self.data.grid.face_coordinates
        return xy[:, 0], xy[:,1]

    def get_exterior(self):
        try:
            indx = self.data.grid.edge_node_connectivity[self.data.grid.exterior_edges, :]
            x = self.data.grid.node_x[indx]
            y = self.data.grid.node_y[indx]
            # Make linestrings from numpy arrays x and y
            linestrings = [shapely.LineString(np.column_stack((x[i], y[i]))) for i in range(len(x))]
            # Merge linestrings
            merged = shapely.ops.linemerge(linestrings)
            # Merge polygons
            polygons = shapely.ops.polygonize(merged)
    #        polygons = shapely.simplify(polygons, self.dx)
            self.exterior = gpd.GeoDataFrame(geometry=list(polygons), crs=self.model.crs)
        except:
            self.exterior = gpd.GeoDataFrame()    

    def get_datashader_dataframe(self):
        # Create a dataframe with line elements
        x1 = self.data.grid.edge_node_coordinates[:,0,0]
        x2 = self.data.grid.edge_node_coordinates[:,1,0]
        y1 = self.data.grid.edge_node_coordinates[:,0,1]
        y2 = self.data.grid.edge_node_coordinates[:,1,1]
        transformer = Transformer.from_crs(self.model.crs,
                                            3857,
                                            always_xy=True)
        x1, y1 = transformer.transform(x1, y1)
        x2, y2 = transformer.transform(x2, y2)
        self.df = pd.DataFrame(dict(x1=x1, y1=y1, x2=x2, y2=y2))

    def map_overlay(self, file_name, xlim=None, ylim=None, color="black", width=800):
        if self.data is None:
            # No grid (yet)
            return False
        try:
            if not hasattr(self, "df"):
                self.df = None
            if self.df is None: 
                self.get_datashader_dataframe()

            transformer = Transformer.from_crs(4326,
                                        3857,
                                        always_xy=True)
            xl0, yl0 = transformer.transform(xlim[0], ylim[0])
            xl1, yl1 = transformer.transform(xlim[1], ylim[1])
            xlim = [xl0, xl1]
            ylim = [yl0, yl1]
            ratio = (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
            height = int(width * ratio)
            cvs = ds.Canvas(x_range=xlim, y_range=ylim, plot_height=height, plot_width=width)
            agg = cvs.line(self.df, x=['x1', 'x2'], y=['y1', 'y2'], axis=1)
            img = tf.shade(agg)
            path = os.path.dirname(file_name)
            if not path:
                path = os.getcwd()
            name = os.path.basename(file_name)
            name = os.path.splitext(name)[0]
            export_image(img, name, export_path=path)
            return True
        except Exception as e:
            return False

    # # Let's move this to cht_tiling
    # def make_index_tiles(self, path, zoom_range=None, format=0):
        
    #     import math
    #     from cht.tiling.tiling import deg2num
    #     from cht.tiling.tiling import num2deg
    #     import cht.misc.fileops as fo
        
    #     npix = 256
        
    #     if not zoom_range:
    #         zoom_range = [0, 13]

    #     cosrot = math.cos(-self.rotation*math.pi/180)
    #     sinrot = math.sin(-self.rotation*math.pi/180)       

    #     # Compute lon/lat range
    #     xmin = np.amin(self.x) - 10*self.dx
    #     xmax = np.amax(self.x) + 10*self.dx
    #     ymin = np.amin(self.y) - 10*self.dy
    #     ymax = np.amax(self.y) + 10*self.dy
    #     transformer = Transformer.from_crs(self.crs,
    #                                         CRS.from_epsg(4326),
    #                                         always_xy=True)
    #     lon_min, lat_min = transformer.transform(xmin, ymin)
    #     lon_max, lat_max = transformer.transform(xmax, ymax)
    #     lon_range = [lon_min, lon_max]
    #     lat_range = [lat_min, lat_max]        
        
    #     transformer_a = Transformer.from_crs(CRS.from_epsg(4326),
    #                                             CRS.from_epsg(3857),
    #                                             always_xy=True)
    #     transformer_b = Transformer.from_crs(CRS.from_epsg(3857),
    #                                             self.crs,
    #                                             always_xy=True)
        
    #     i0_lev = []
    #     i1_lev = []
    #     nmax_lev = []
    #     mmax_lev = []
    #     nm_lev = []
    #     for level in range(self.nr_refinement_levels):
    #         i0 = self.level_index[level]
    #         if level<self.nr_refinement_levels - 1:
    #             i1 = self.level_index[level + 1]
    #         else:
    #             i1 = self.nr_cells   
    #         i0_lev.append(i0)    
    #         i1_lev.append(i1)    
    #         nmax_lev.append(np.amax(self.n[i0:i1]) + 1)
    #         mmax_lev.append(np.amax(self.m[i0:i1]) + 1)
    #         mm = self.m[i0:i1]
    #         nn = self.n[i0:i1]
    #         nm_lev.append(mm*nmax_lev[level] + nn)

    #     for izoom in range(zoom_range[0], zoom_range[1] + 1):
            
    #         print("Processing zoom level " + str(izoom))
        
    #         zoom_path = os.path.join(path, str(izoom))
        
    #         dxy = (40075016.686/npix) / 2 ** izoom
    #         xx = np.linspace(0.0, (npix - 1)*dxy, num=npix)
    #         yy = xx[:]
    #         xv, yv = np.meshgrid(xx, yy)
        
    #         ix0, iy0 = deg2num(lat_range[0], lon_range[0], izoom)
    #         ix1, iy1 = deg2num(lat_range[1], lon_range[1], izoom)
        
    #         for i in range(ix0, ix1 + 1):
            
    #             path_okay = False
    #             zoom_path_i = os.path.join(zoom_path, str(i))
            
    #             for j in range(iy0, iy1 + 1):
            
    #                 file_name = os.path.join(zoom_path_i, str(j) + ".dat")
            
    #                 # Compute lat/lon at ll corner of tile
    #                 lat, lon = num2deg(i, j, izoom)
            
    #                 # Convert to Global Mercator
    #                 xo, yo   = transformer_a.transform(lon,lat)
            
    #                 # Tile grid on local mercator
    #                 x = xv[:] + xo + 0.5*dxy
    #                 y = yv[:] + yo + 0.5*dxy
            
    #                 # Convert tile grid to crs of SFINCS model
    #                 x, y = transformer_b.transform(x, y)

    #                 # Now rotate around origin of SFINCS model
    #                 x00 = x - self.x0
    #                 y00 = y - self.y0
    #                 xg  = x00*cosrot - y00*sinrot
    #                 yg  = x00*sinrot + y00*cosrot

    #                 indx = np.full((npix, npix), -999, dtype=int)

    #                 for ilev in range(self.nr_refinement_levels):
    #                     nmax = nmax_lev[ilev]
    #                     mmax = mmax_lev[ilev]
    #                     i0   = i0_lev[ilev]
    #                     i1   = i1_lev[ilev]
    #                     dx   = self.dx/2**ilev
    #                     dy   = self.dy/2**ilev
    #                     iind = np.floor(xg/dx).astype(int)
    #                     jind = np.floor(yg/dy).astype(int)
    #                     # Now check whether this cell exists on this level
    #                     ind  = iind*nmax + jind
    #                     ind[iind<0]   = -999
    #                     ind[jind<0]   = -999
    #                     ind[iind>=mmax] = -999
    #                     ind[jind>=nmax] = -999

    #                     ingrid = np.isin(ind, nm_lev[ilev], assume_unique=False) # return boolean for each pixel that falls inside a grid cell
    #                     incell = np.where(ingrid)                                # tuple of arrays of pixel indices that fall in a cell

    #                     if incell[0].size>0:
    #                         # Now find the cell indices
    #                         try:
    #                             cell_indices = binary_search(nm_lev[ilev], ind[incell[0], incell[1]]) + i0_lev[ilev]
    #                             indx[incell[0], incell[1]] = cell_indices
    #                         except:
    #                             pass

    #                 if np.any(indx>=0):                        
    #                     if not path_okay:
    #                         if not os.path.exists(zoom_path_i):
    #                             fo.mkdir(zoom_path_i)
    #                             path_okay = True
                                
    #                     # And write indices to file
    #                     fid = open(file_name, "wb")
    #                     fid.write(indx)
    #                     fid.close()

    def get_regular_grid(self):
        # Build initial grid with one level
        ns = np.linspace(0, self.nmax - 1, self.nmax, dtype=int)
        ms = np.linspace(0, self.mmax - 1, self.mmax, dtype=int)
        self.m, self.n = np.meshgrid(ms, ns)
        self.n = np.transpose(self.n).flatten()
        self.m = np.transpose(self.m).flatten()
        self.nr_cells = self.nmax * self.mmax
        self.level = np.zeros(self.nr_cells, dtype=int)
        self.nr_refinement_levels = 1
        # Determine ifirst and ilast for each level
        self.find_first_cells_in_level()
        # Compute cell center coordinates self.x and self.y
        self.compute_cell_center_coordinates()

    def refine_mesh(self): 
        # Loop through rows in gdf and create list of polygons
        # Determine maximum refinement level

        start = time.time()
        print("Refining ...")

        self.ref_pols = []
        for irow, row in self.refinement_polygons.iterrows():
            iref = row["refinement_level"]
            polygon = {"geometry": row["geometry"], "refinement_level": iref}
            self.ref_pols.append(polygon)

        # Loop through refinement polygons and start refining
        for polygon in self.ref_pols:
            # Refine, reorder, find first cells in level
            self.refine_in_polygon(polygon)

        print("Time elapsed : " + str(time.time() - start) + " s")

    def refine_in_polygon(self, polygon):
        # Finds cell to refine and calls refine_cells

        # Loop through refinement levels for this polygon
        for ilev in range(polygon["refinement_level"]):

            # Refine cells in refinement polygons
            # Compute grid spacing for this level
            dx = self.dx/2**ilev
            dy = self.dy/2**ilev
            nmax = self.nmax * 2**ilev
            mmax = self.mmax * 2**ilev
            # Add buffer of 0.5*dx around polygon
            polbuf = polygon["geometry"]
            # Rotate polbuf to grid (this is needed to find cells that could fall within polbuf)
            coords = polbuf.exterior.coords[:]
            npoints = len(coords)
            polx = np.zeros(npoints)
            poly = np.zeros(npoints)

            for ipoint, point in enumerate(polbuf.exterior.coords[:]):
                # Cell centres
                polx[ipoint] =   self.cosrot*(point[0] - self.x0) + self.sinrot*(point[1] - self.y0)
                poly[ipoint] = - self.sinrot*(point[0] - self.x0) + self.cosrot*(point[1] - self.y0)

            # Find cells cells in grid that could fall within polbuf 
            n0 = int(np.floor(np.min(poly) / dy)) - 1
            n1 = int(np.ceil(np.max(poly) / dy)) + 1
            m0 = int(np.floor(np.min(polx) / dx)) - 1
            m1 = int(np.ceil(np.max(polx) / dx)) + 1

            n0 = min(max(n0, 0), nmax - 1)
            n1 = min(max(n1, 0), nmax - 1)
            m0 = min(max(m0, 0), mmax - 1)
            m1 = min(max(m1, 0), mmax - 1)

            # Compute cell centre coordinates of cells in this level in this block
            nn, mm = np.meshgrid(np.arange(n0, n1 + 1), np.arange(m0, m1 + 1))
            nn = np.transpose(nn).flatten()
            mm = np.transpose(mm).flatten()

            xcor = np.zeros((4, np.size(nn)))
            ycor = np.zeros((4, np.size(nn)))
            xcor[0,:] = self.x0 + self.cosrot * (mm + 0) * dx - self.sinrot * (nn + 0) * dy
            ycor[0,:] = self.y0 + self.sinrot * (mm + 0) * dx + self.cosrot * (nn + 0) * dy
            xcor[1,:] = self.x0 + self.cosrot * (mm + 1) * dx - self.sinrot * (nn + 0) * dy
            ycor[1,:] = self.y0 + self.sinrot * (mm + 1) * dx + self.cosrot * (nn + 0) * dy
            xcor[2,:] = self.x0 + self.cosrot * (mm + 1) * dx - self.sinrot * (nn + 1) * dy
            ycor[2,:] = self.y0 + self.sinrot * (mm + 1) * dx + self.cosrot * (nn + 1) * dy
            xcor[3,:] = self.x0 + self.cosrot * (mm + 0) * dx - self.sinrot * (nn + 1) * dy
            ycor[3,:] = self.y0 + self.sinrot * (mm + 0) * dx + self.cosrot * (nn + 1) * dy

            # Create np array with False for all cells
            inp = np.zeros(np.size(nn), dtype=bool)
            # Loop through 4 corner points
            # If any corner points falls within the polygon, inp is set to True
            for j in range(4):
                inp0 = inpolygon(np.squeeze(xcor[j,:]),
                                 np.squeeze(ycor[j,:]),
                                 polygon["geometry"])
                inp[np.where(inp0)] = True
            in_polygon = np.where(inp)[0]

            # Indices of cells in level within polbuf
            nn_in = nn[in_polygon]
            mm_in = mm[in_polygon]
            nm_in = nmax * mm_in + nn_in

            # Find existing cells of this level in nmi array
            n_level = self.n[self.ifirst[ilev]:self.ilast[ilev] + 1]
            m_level = self.m[self.ifirst[ilev]:self.ilast[ilev] + 1]
            nm_level = m_level * nmax + n_level

            # Find indices all cells to be refined
            ind_ref = binary_search(nm_level, nm_in)

            ind_ref=ind_ref[ind_ref>=0]

            # ind_ref = ind_ref[ind_ref < np.size(nm_level)]
            if not np.any(ind_ref):
                continue
            # Index of cells to refine
            ind_ref += self.ifirst[ilev]

            self.refine_cells(ind_ref, ilev)

    def refine_cells(self, ind_ref, ilev):
        # Refine cells with index ind_ref

        # First find lower-level neighbors (these will be refined in the next iteration)
        if ilev>0:
            ind_nbr = self.find_lower_level_neighbors(ind_ref, ilev)
        else:
            ind_nbr = np.empty(0, dtype=int)    

        # n and m indices of cells to be refined
        n = self.n[ind_ref]
        m = self.m[ind_ref]

        # New cells
        nnew = np.zeros(4 * len(ind_ref), dtype=int)
        mnew = np.zeros(4 * len(ind_ref), dtype=int)
        lnew = np.zeros(4 * len(ind_ref), dtype=int) + ilev + 1
        nnew[0::4] = n*2      # lower left
        nnew[1::4] = n*2 + 1  # upper left
        nnew[2::4] = n*2      # lower right
        nnew[3::4] = n*2 + 1  # upper right
        mnew[0::4] = m*2      # lower left
        mnew[1::4] = m*2      # upper left
        mnew[2::4] = m*2 + 1  # lower right
        mnew[3::4] = m*2 + 1  # upper right
        # Add new cells to grid
        self.n = np.append(self.n, nnew)
        self.m = np.append(self.m, mnew)
        self.level = np.append(self.level, lnew)
        # Remove old cells from grid
        self.n = np.delete(self.n, ind_ref)
        self.m = np.delete(self.m, ind_ref)
        self.level = np.delete(self.level, ind_ref)        
        self.nr_cells = len(self.n)
        # Update nr_refinement_levels at max of ilev + 2 and self.nr_refinement_levels
        self.nr_refinement_levels = np.maximum(self.nr_refinement_levels, ilev + 2)
        # Reorder cells
        self.reorder()
        # Update ifirst and ilast
        self.find_first_cells_in_level()
        # Compute cell center coordinates self.x and self.y
        self.compute_cell_center_coordinates()

        if np.any(ind_nbr):
            self.refine_cells(ind_nbr, ilev - 1)

    def initialize_data_arrays(self):
        # Set indices of neighbors to -1
        self.mu  = np.zeros(self.nr_cells, dtype=np.int8)
        self.mu1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.mu2 = np.zeros(self.nr_cells, dtype=int) - 1
        self.md  = np.zeros(self.nr_cells, dtype=np.int8)
        self.md1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.md2 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nu  = np.zeros(self.nr_cells, dtype=np.int8)
        self.nu1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nu2 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nd  = np.zeros(self.nr_cells, dtype=np.int8)
        self.nd1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nd2 = np.zeros(self.nr_cells, dtype=int) - 1

        # Set initial depth
        self.z = np.zeros(self.nr_cells, dtype=float)
        # Set initial SFINCS mask to zeros
        self.mask = np.zeros(self.nr_cells, dtype=np.int8)
        # Set initial SnapWave mask to zeros
        self.snapwave_mask = np.zeros(self.nr_cells, dtype=np.int8)

    def get_neighbors(self):
        # Get mu, mu1, mu2, nu, nu1, nu2 for all cells   

        start = time.time()

        print("Finding neighbors ...")

        # Get nm indices for all cells
        nm_all = np.zeros(self.nr_cells, dtype=int)
        for ilev in range(self.nr_refinement_levels):
            nmax = self.nmax * 2**ilev + 1
            i0 = self.ifirst[ilev]
            i1 = self.ilast[ilev] + 1
            n = self.n[i0:i1]
            m = self.m[i0:i1]
            nm_all[i0:i1] = m * nmax + n

        # Loop over levels
        for ilev in range(self.nr_refinement_levels):

            nmax = self.nmax * 2**ilev + 1

            # First and last cell in this level
            i0 = self.ifirst[ilev]
            i1 = self.ilast[ilev] + 1

            # Initialize arrays for this level
            mu = np.zeros(i1 - i0, dtype=int)
            mu1 = np.zeros(i1 - i0, dtype=int) - 1
            mu2 = np.zeros(i1 - i0, dtype=int) - 1
            nu = np.zeros(i1 - i0, dtype=int)
            nu1 = np.zeros(i1 - i0, dtype=int) - 1
            nu2 = np.zeros(i1 - i0, dtype=int) - 1

            # Get n and m indices for this level
            n = self.n[i0:i1]
            m = self.m[i0:i1]
            nm = nm_all[i0:i1]

            # Now look for neighbors 
                           
            # Same level

            # Right
            nm_to_find = nm + nmax
            inb = binary_search(nm, nm_to_find)
            mu1[inb>=0] = inb[inb>=0] + i0

            # Above
            nm_to_find = nm + 1
            inb = binary_search(nm, nm_to_find)
            nu1[inb>=0] = inb[inb>=0] + i0

            ## Coarser level neighbors
            if ilev>0:

                nmaxc = self.nmax * 2**(ilev - 1) + 1   # Number of cells in coarser level in n direction 

                i0c = self.ifirst[ilev - 1]  # First cell in coarser level                
                i1c = self.ilast[ilev - 1] + 1 # Last cell in coarser level

                nmc = nm_all[i0c:i1c] # Coarser level nm indices
                nc = n // 2 # Coarser level n index of this cells in this level
                mc = m // 2 # Coarser level m index of this cells in this level 

                # Right
                nmc_to_find = (mc + 1) * nmaxc + nc
                inb = binary_search(nmc, nmc_to_find)
                inb[np.where(even(m))[0]] = -1
                # Set mu and mu1 for inb>=0
                mu1[inb>=0] = inb[inb>=0] + i0c
                mu[inb>=0] = -1

                # Above
                nmc_to_find = mc * nmaxc + nc + 1
                inb = binary_search(nmc, nmc_to_find)
                inb[np.where(even(n))[0]] = -1
                # Set nu and nu1 for inb>=0
                nu1[inb>=0] = inb[inb>=0] + i0c
                nu[inb>=0] = -1

            # Finer level neighbors
            if ilev<self.nr_refinement_levels - 1:

                nmaxf = self.nmax * 2**(ilev + 1) + 1 # Number of cells in finer level in n direction

                i0f = self.ifirst[ilev + 1]  # First cell in finer level
                i1f = self.ilast[ilev + 1] + 1 # Last cell in finer level
                nmf = nm_all[i0f:i1f] # Finer level nm indices

                # Right

                # Lower row
                nf = n * 2 # Finer level n index of this cells in this level
                mf = m * 2 + 1 # Finer level m index of this cells in this level
                nmf_to_find = (mf + 1) * nmaxf + nf
                inb = binary_search(nmf, nmf_to_find)
                mu1[inb>=0] = inb[inb>=0] + i0f
                mu[inb>=0] = 1

                # Upper row
                nf = n * 2 + 1# Finer level n index of this cells in this level
                mf = m * 2 + 1 # Finer level m index of this cells in this level
                nmf_to_find = (mf + 1) * nmaxf + nf
                inb = binary_search(nmf, nmf_to_find)
                mu2[inb>=0] = inb[inb>=0] + i0f
                mu[inb>=0] = 1

                # Above

                # Left column
                nf = n * 2 + 1 # Finer level n index of this cells in this level
                mf = m * 2 # Finer level m index of this cells in this level
                nmf_to_find = mf * nmaxf + nf + 1
                inb = binary_search(nmf, nmf_to_find)
                nu1[inb>=0] = inb[inb>=0] + i0f
                nu[inb>=0] = 1

                # Right column
                nf = n * 2 + 1 # Finer level n index of this cells in this level
                mf = m * 2 + 1 # Finer level m index of this cells in this level
                nmf_to_find = mf * nmaxf + nf + 1
                inb = binary_search(nmf, nmf_to_find)
                nu2[inb>=0] = inb[inb>=0] + i0f
                nu[inb>=0] = 1

            # Fill in mu, mu1, mu2, nu, nu1, nu2 for this level
            self.mu[i0:i1] = mu
            self.mu1[i0:i1] = mu1
            self.mu2[i0:i1] = mu2
            self.nu[i0:i1] = nu
            self.nu1[i0:i1] = nu1
            self.nu2[i0:i1] = nu2

        print("Time elapsed : " + str(time.time() - start) + " s")

        # Making global model
        # Check if CRS is geographic
        if self.model.crs.is_geographic:
            # Now check if mmax * dx is 360
            if self.mmax * self.dx > 359 and self.mmax * self.dx < 361:
                # We have a global model
                # Loop through all points
                for ilev in range(self.nr_refinement_levels):                    
                    i0 = self.ifirst[ilev]
                    i1 = self.ilast[ilev] + 1
                    nmaxf = self.nmax * 2**ilev + 1
                    mf = self.mmax * 2**ilev - 1
                    nmf = nm_all[i0:i1]
                    # Loop through all cells
                    for i in range(i0, i1):
                        if self.m[i] > 0:
                            # This cell is not on the left of the model
                            break
                        # Now find matching cell on the right
                        # nm index of cell on RHS of grid
                        nmf_to_find = mf * nmaxf + self.n[i]
                        iright = np.where(nmf==nmf_to_find)[0]
                        if iright.size > 0:
                            iright = iright + i0
                            self.mu[iright] = 0
                            self.mu1[iright] = i
                            self.mu2[iright] = -1




        print("Setting neighbors left and below ...")

        # Right
       
        iok1 = np.where(self.mu1>=0)[0]
        # Same level
        iok2 = np.where(self.mu==0)[0]
        # Indices of cells that have a same level neighbor to the right
        iok = np.intersect1d(iok1, iok2)
        # Indices of neighbors
        imu = self.mu1[iok]
        self.md[imu] = 0
        self.md1[imu] = iok

        # Coarser
        iok2 = np.where(self.mu==-1)[0]
        # Indices of cells that have a coarse level neighbor to the right
        iok = np.intersect1d(iok1, iok2)
        # Odd
        iok_odd  = iok[np.where(odd(self.n[iok]))]
        iok_even = iok[np.where(even(self.n[iok]))]
        imu = self.mu1[iok_odd]
        self.md[imu] = 1
        self.md1[imu] = iok_odd
        imu = self.mu1[iok_even]
        self.md[imu] = 1
        self.md2[imu] = iok_even

        # Finer
        # Lower
        iok1 = np.where(self.mu1>=0)[0]
        # Same level
        iok2 = np.where(self.mu==1)[0]
        # Indices of cells that have finer level neighbor to the right
        iok = np.intersect1d(iok1, iok2)
        imu = self.mu1[iok]
        self.md[imu] = -1
        self.md1[imu] = iok
        # Upper
        iok1 = np.where(self.mu2>=0)[0]
        # Same level
        iok2 = np.where(self.mu==1)[0]
        # Indices of cells that have finer level neighbor to the right
        iok = np.intersect1d(iok1, iok2)
        imu = self.mu2[iok]
        self.md[imu] = -1
        self.md1[imu] = iok

        # Above
        iok1 = np.where(self.nu1>=0)[0]
        # Same level
        iok2 = np.where(self.nu==0)[0]
        # Indices of cells that have a same level neighbor above
        iok = np.intersect1d(iok1, iok2)
        # Indices of neighbors
        inu = self.nu1[iok]
        self.nd[inu] = 0
        self.nd1[inu] = iok

        # Coarser
        iok2 = np.where(self.nu==-1)[0]
        # Indices of cells that have a coarse level neighbor to the right
        iok = np.intersect1d(iok1, iok2)
        # Odd
        iok_odd  = iok[np.where(odd(self.m[iok]))]
        iok_even = iok[np.where(even(self.m[iok]))]
        inu = self.nu1[iok_odd]
        self.nd[inu] = 1
        self.nd1[inu] = iok_odd
        inu = self.nu1[iok_even]
        self.nd[inu] = 1
        self.nd2[inu] = iok_even

        # Finer
        # Left
        iok1 = np.where(self.nu1>=0)[0]
        # Same level
        iok2 = np.where(self.nu==1)[0]
        # Indices of cells that have finer level neighbor above
        iok = np.intersect1d(iok1, iok2)
        inu = self.nu1[iok]
        self.nd[inu] = -1
        self.nd1[inu] = iok
        # Upper
        iok1 = np.where(self.nu2>=0)[0]
        # Same level
        iok2 = np.where(self.nu==1)[0]
        # Indices of cells that have finer level neighbor to the right
        iok = np.intersect1d(iok1, iok2)
        inu = self.nu2[iok]
        self.nd[inu] = -1
        self.nd1[inu] = iok

        print("Time elapsed : " + str(time.time() - start) + " s")

    def get_uv_points(self):

        start = time.time()
        print("Getting uv points ...")

        # Get uv points (do we actually need to do this?)
        self.uv_index_z_nm  = np.zeros((self.nr_cells*4), dtype=int)
        self.uv_index_z_nmu = np.zeros((self.nr_cells*4), dtype=int)
        self.uv_dir         = np.zeros((self.nr_cells*4), dtype=int)
        # Loop through points (SHOULD TRY TO VECTORIZE THIS, but try to keep same order of uv points
        nuv = 0
        for ip in range(self.nr_cells):
            if self.mu1[ip]>=0:
                self.uv_index_z_nm[nuv] = ip        
                self.uv_index_z_nmu[nuv] = self.mu1[ip]     
                self.uv_dir[nuv] = 0
                nuv += 1
            if self.mu2[ip]>=0:
                self.uv_index_z_nm[nuv] = ip        
                self.uv_index_z_nmu[nuv] = self.mu2[ip]     
                self.uv_dir[nuv] = 0     
                nuv += 1
            if self.nu1[ip]>=0:
                self.uv_index_z_nm[nuv] = ip        
                self.uv_index_z_nmu[nuv] = self.nu1[ip]     
                self.uv_dir[nuv] = 1     
                nuv += 1
            if self.nu2[ip]>=0:
                self.uv_index_z_nm[nuv] = ip
                self.uv_index_z_nmu[nuv] = self.nu2[ip]
                self.uv_dir[nuv] = 1
                nuv += 1
        self.uv_index_z_nm  = self.uv_index_z_nm[0 : nuv]
        self.uv_index_z_nmu = self.uv_index_z_nmu[0 : nuv]
        self.uv_dir         = self.uv_dir[0 : nuv]
        self.nr_uv_points   = nuv

        print("Time elapsed : " + str(time.time() - start) + " s")

    def reorder(self):
        # Reorder cells
        # Sort cells by level, then m, then n
        i = np.lexsort((self.n, self.m, self.level))
        self.n = self.n[i]
        self.m = self.m[i]
        self.level = self.level[i]

    def find_first_cells_in_level(self):
        # Find first cell in each level
        self.ifirst = np.zeros(self.nr_refinement_levels, dtype=int)
        self.ilast = np.zeros(self.nr_refinement_levels, dtype=int)
        for ilev in range(0, self.nr_refinement_levels):
            # Find index of first cell with this level
            self.ifirst[ilev] = np.where(self.level == ilev)[0][0]
            # Find index of last cell with this level
            if ilev<self.nr_refinement_levels - 1:
                self.ilast[ilev] = np.where(self.level == ilev + 1)[0][0] - 1
            else:
                self.ilast[ilev] = self.nr_cells - 1

    def compute_cell_center_coordinates(self):
        # Compute cell center coordinates
        # Loop through refinement levels
        dx = self.dx/2**self.level
        dy = self.dy/2**self.level
        self.x = self.x0 + self.cosrot * (self.m + 0.5) * dx - self.sinrot * (self.n + 0.5) * dy
        self.y = self.y0 + self.sinrot * (self.m + 0.5) * dx + self.cosrot * (self.n + 0.5) * dy

    def get_ugrid2d(self):

        tic = time.perf_counter()

        n = self.n
        m = self.m
        level = self.level

        nmax       = self.nmax * 2**(self.nr_refinement_levels - 1) + 1

        face_nodes_n = np.full((8,self.nr_cells), -1, dtype=int)
        face_nodes_m = np.full((8,self.nr_cells), -1, dtype=int)
        face_nodes_nm = np.full((8,self.nr_cells), -1, dtype=int)

        # HIghest refinement level 
        ifac = 2**(self.nr_refinement_levels - level - 1)
        dxf = self.dx / 2**(self.nr_refinement_levels - 1)
        dyf = self.dy / 2**(self.nr_refinement_levels - 1)

        face_n = n * ifac
        face_m = m * ifac

        # First do the 4 corner points
        face_nodes_n[0, :] = face_n
        face_nodes_m[0, :] = face_m
        face_nodes_n[2, :] = face_n
        face_nodes_m[2, :] = face_m + ifac
        face_nodes_n[4, :] = face_n + ifac
        face_nodes_m[4, :] = face_m + ifac
        face_nodes_n[6, :] = face_n + ifac
        face_nodes_m[6, :] = face_m

        # Find cells with refinement below
        i = np.where(self.nd==1)
        face_nodes_n[1, i] = face_n[i]
        face_nodes_m[1, i] = face_m[i] + ifac[i]/2
        # Find cells with refinement to the right
        i = np.where(self.mu==1)
        face_nodes_n[3, i] = face_n[i] + ifac[i]/2
        face_nodes_m[3, i] = face_m[i] + ifac[i]
        # Find cells with refinement above
        i = np.where(self.nu==1)
        face_nodes_n[5, i] = face_n[i] + ifac[i]
        face_nodes_m[5, i] = face_m[i] + ifac[i]/2
        # Find cells with refinement to the left
        i = np.where(self.md==1)
        face_nodes_n[7, i] = face_n[i] + ifac[i]/2
        face_nodes_m[7, i] = face_m[i]

        # Flatten
        face_nodes_n = face_nodes_n.transpose().flatten()
        face_nodes_m = face_nodes_m.transpose().flatten()

        # Compute nm value of nodes        
        face_nodes_nm = nmax * face_nodes_m + face_nodes_n
        nopoint = max(face_nodes_nm) + 1
        # Set missing points to very high number
        face_nodes_nm[np.where(face_nodes_n==-1)] = nopoint

        # Get the unique nm values
        xxx, index, irev = np.unique(face_nodes_nm, return_index=True, return_inverse=True)
        j = np.where(xxx==nopoint)[0][0] # Index of very high number
        # irev2 = np.reshape(irev, (self.nr_cells, 8))
        # face_nodes_all = irev2.transpose()
        face_nodes_all = np.reshape(irev, (self.nr_cells, 8)).transpose()
        face_nodes_all[np.where(face_nodes_all==j)] = -1

        face_nodes = np.full(face_nodes_all.shape, -1)  # Create a new array filled with -1
        for i in range(face_nodes.shape[1]):
            idx = np.where(face_nodes_all[:,i] != -1)[0]
            face_nodes[:len(idx), i] = face_nodes_all[idx, i]  

        # Now get rid of all the rows where all values are -1
        # Create a mask where each row is True if not all elements in the row are -1
        mask = (face_nodes != -1).any(axis=1)

        # Use this mask to index face_nodes
        face_nodes = face_nodes[mask]

        node_n = face_nodes_n[index[:j]]
        node_m = face_nodes_m[index[:j]]
        node_x = self.x0 + self.cosrot*(node_m*dxf) - self.sinrot*(node_n*dyf)
        node_y = self.y0 + self.sinrot*(node_m*dxf) + self.cosrot*(node_n*dyf)

        toc = time.perf_counter()

        print(f"Got rid of duplicates in {toc - tic:0.4f} seconds")

        tic = time.perf_counter()

        nodes = np.transpose(np.vstack((node_x, node_y)))
        faces = np.transpose(face_nodes)
        fill_value = -1

        ugrid2d = xu.Ugrid2d(nodes[:, 0], nodes[:, 1], fill_value, faces)

        ugrid2d.set_crs(self.model.crs)

        # Set datashader df to None
        self.df = None 

        toc = time.perf_counter()

        print(f"Made XUGrid in {toc - tic:0.4f} seconds")

        return ugrid2d

    def cut_inactive_cells(self):

        print("Removing inactive cells ...")

        # In the xugrid data, the indices are 1-based, so we need to subtract 1 
        n = self.data["n"].values[:] - 1
        m = self.data["m"].values[:] - 1
        level = self.data["level"].values[:] - 1
        z = self.data["z"].values[:]
        mask = self.data["mask"].values[:]
        swmask = self.data["snapwave_mask"].values[:]

        indx = np.where((mask + swmask)>0)
            
        self.nr_cells = np.size(indx)
        self.n        = n[indx]
        self.m        = m[indx]
        self.level    = level[indx]
        self.z        = z[indx] 
        self.mask     = mask[indx]
        self.snapwave_mask = swmask[indx]

        # Set indices of neighbors to -1
        self.mu  = np.zeros(self.nr_cells, dtype=np.int8)
        self.mu1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.mu2 = np.zeros(self.nr_cells, dtype=int) - 1
        self.md  = np.zeros(self.nr_cells, dtype=np.int8)
        self.md1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.md2 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nu  = np.zeros(self.nr_cells, dtype=np.int8)
        self.nu1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nu2 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nd  = np.zeros(self.nr_cells, dtype=np.int8)
        self.nd1 = np.zeros(self.nr_cells, dtype=int) - 1
        self.nd2 = np.zeros(self.nr_cells, dtype=int) - 1

        self.find_first_cells_in_level()
        self.get_neighbors() 
        self.get_uv_points()
        self.to_xugrid()
        self.get_exterior()
 
    def to_xugrid(self):    

        print("Making XUGrid ...")

        # Create the grid
        ugrid2d = self.get_ugrid2d()

        # Create the dataset
        self.data = xu.UgridDataset(grids=ugrid2d)

        # Add attributes
        attrs = {"x0": self.x0,
                 "y0": self.y0,
                 "nmax": self.nmax,
                 "mmax": self.mmax,
                 "dx": self.dx,
                 "dy": self.dy,
                 "rotation": self.rotation,
                 "nr_levels": self.nr_refinement_levels}
        self.data.attrs = attrs

        # Now add the data arrays
        self.data["crs"] = self.model.crs.to_epsg()
        self.data["crs"].attrs = self.model.crs.to_cf()
        self.data["level"] = xu.UgridDataArray(xr.DataArray(data=self.level + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["z"] = xu.UgridDataArray(xr.DataArray(data=self.z, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["mask"] = xu.UgridDataArray(xr.DataArray(data=self.mask, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["snapwave_mask"] = xu.UgridDataArray(xr.DataArray(data=self.snapwave_mask, dims=[ugrid2d.face_dimension]), ugrid2d)

        self.data["n"] = xu.UgridDataArray(xr.DataArray(data=self.n + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["m"] = xu.UgridDataArray(xr.DataArray(data=self.m + 1, dims=[ugrid2d.face_dimension]), ugrid2d)

        self.data["mu"]  = xu.UgridDataArray(xr.DataArray(data=self.mu, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["mu1"] = xu.UgridDataArray(xr.DataArray(data=self.mu1 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["mu2"] = xu.UgridDataArray(xr.DataArray(data=self.mu2 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["md"]  = xu.UgridDataArray(xr.DataArray(data=self.md, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["md1"] = xu.UgridDataArray(xr.DataArray(data=self.md1 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["md2"] = xu.UgridDataArray(xr.DataArray(data=self.md2 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)

        self.data["nu"]  = xu.UgridDataArray(xr.DataArray(data=self.nu, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["nu1"] = xu.UgridDataArray(xr.DataArray(data=self.nu1 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["nu2"] = xu.UgridDataArray(xr.DataArray(data=self.nu2 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["nd"]  = xu.UgridDataArray(xr.DataArray(data=self.nd, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["nd1"] = xu.UgridDataArray(xr.DataArray(data=self.nd1 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)
        self.data["nd2"] = xu.UgridDataArray(xr.DataArray(data=self.nd2 + 1, dims=[ugrid2d.face_dimension]), ugrid2d)

        # Get rid of temporary arrays
        self.clear_temporary_arrays()

    def clear_temporary_arrays(self):
        pass

    def find_lower_level_neighbors(self, ind_ref, ilev):

        # ind_ref are the indices of the cells that need to be refined

        n = self.n[ind_ref]
        m = self.m[ind_ref]

        n_odd = np.where(odd(n))
        m_odd = np.where(odd(m))
        n_even = np.where(even(n))
        m_even = np.where(even(m))
        
        ill   = np.intersect1d(n_even, m_even)
        iul   = np.intersect1d(n_odd, m_even)
        ilr   = np.intersect1d(n_even, m_odd)
        iur   = np.intersect1d(n_odd, m_odd)

        n_nbr = np.zeros((2, np.size(n)), dtype=int)        
        m_nbr = np.zeros((2, np.size(n)), dtype=int)

        # LL
        n0 = np.int32(n[ill] / 2)
        m0 = np.int32(m[ill] / 2)
        n_nbr[0, ill] = n0 - 1
        m_nbr[0, ill] = m0
        n_nbr[1, ill] = n0
        m_nbr[1, ill] = m0 - 1
        # UL
        n0 = np.int32((n[iul] - 1) / 2)
        m0 = np.int32(m[iul] / 2)
        n_nbr[0, iul] = n0 + 1
        m_nbr[0, iul] = m0
        n_nbr[1, iul] = n0
        m_nbr[1, iul] = m0 - 1
        # LR
        n0 = np.int32(n[ilr] / 2)
        m0 = np.int32((m[ilr] - 1) / 2)
        n_nbr[0, ilr] = n0 - 1
        m_nbr[0, ilr] = m0
        n_nbr[1, ilr] = n0
        m_nbr[1, ilr] = m0 + 1
        # UR
        n0 = np.int32((n[iur] - 1) / 2)
        m0 = np.int32((m[iur] - 1) / 2)
        n_nbr[0, iur] = n0 + 1
        m_nbr[0, iur] = m0
        n_nbr[1, iur] = n0
        m_nbr[1, iur] = m0 + 1

        nmax = self.nmax * 2**(ilev - 1) + 1

        n_nbr = n_nbr.flatten()
        m_nbr = m_nbr.flatten()
        nm_nbr = m_nbr * nmax + n_nbr
        nm_nbr = np.sort(np.unique(nm_nbr, return_index=False))

        # Actual cells in the coarser level 
        n_level = self.n[self.ifirst[ilev - 1]:self.ilast[ilev - 1] + 1]
        m_level = self.m[self.ifirst[ilev - 1]:self.ilast[ilev - 1] + 1]
        nm_level = m_level * nmax + n_level

        # Find  
        ind_nbr = binary_search(nm_level, nm_nbr)
        ind_nbr = ind_nbr[ind_nbr>=0]

        if np.any(ind_nbr):
            ind_nbr += self.ifirst[ilev - 1]

        return ind_nbr

def odd(num):
    return np.mod(num, 2) == 1

def even(num):
    return np.mod(num, 2) == 0

def inpolygon(xq, yq, p):
    shape = xq.shape
    xq = xq.reshape(-1)
    yq = yq.reshape(-1)
    q = [(xq[i], yq[i]) for i in range(xq.shape[0])]
    p = path.Path([(crds[0], crds[1]) for i, crds in enumerate(p.exterior.coords)])
    return p.contains_points(q).reshape(shape)

def binary_search(val_array, vals):    
    indx = np.searchsorted(val_array, vals) # ind is size of vals 
    not_ok = np.where(indx==len(val_array))[0] # size of vals, points that are out of bounds
    indx[np.where(indx==len(val_array))[0]] = 0 # Set to zero to avoid out of bounds error
    is_ok = np.where(val_array[indx] == vals)[0] # size of vals
    indices = np.zeros(len(vals), dtype=int) - 1
    indices[is_ok] = indx[is_ok]
    indices[not_ok] = -1
    return indices


def gdf2list(gdf_in):
   gdf_out = []
   for feature in gdf_in.iterfeatures():
      gdf_out.append(gpd.GeoDataFrame.from_features([feature]))
   return gdf_out
