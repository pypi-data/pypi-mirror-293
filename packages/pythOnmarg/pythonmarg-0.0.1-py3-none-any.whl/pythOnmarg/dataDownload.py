import pandas as pd
import xlrd
import geopandas as gpd
import os
import re
import zipfile
import tempfile
from urllib.request import urlopen
from io import BytesIO

"""
The pythOnmarg package handles the loading and merging of Public Health Ontario's
"Ontario Marginalization Index" dataset - no downloads necessary!
"""

# -----------------------------------------------------------------------------

def om_data(year, level):
    """
    Gets a dataframe of OnMarg data for selected year and level.

    Parameters
    ----------
    year : int
        Year of data to pull from.
    level : str
        Geographic level summarized to.

    Raises
    ------
    Exception
        Raises an exception if an invalid year or level was provided.

    Returns
    -------
    df : OnMarg data
        Returns a dataframe of OnMarg data.

    """
    
    year = str(year)
    
    # Ensure year is valid and get url
    if year == "2001":
        raise Exception("This year has not yet been implemented")
    elif year == "2006":
        raise Exception("This year has not yet been implemented")
    elif year == "2011":
        url = "https://www.publichealthontario.ca/-/media/Data-Files/index-on-marg-2011.xlsx?la=en&sc_lang=en&hash=88EFEB83D1A1DFC5A90517AE2E71C855"
    elif year == "2016":
        url = "https://www.publichealthontario.ca/-/media/Data-Files/index-on-marg-2016.xls?sc_lang=en&rev=be5ab11ce0cc4fe5ab99ee66d359fd00&hash=8AE291D54B3AD013A106D27139218CE8"
    elif year == "2021":
        url = "https://www.publichealthontario.ca/-/media/Data-Files/index-on-marg.xlsx?rev=c778f01c70294d779131bbdb50c23049&sc_lang=en"
    else:
        raise Exception("There is no record for year: " + year)
    
    # Ensure level is valid
    valid_levels = ["DAUID", "CTUID", "CSDUID", "CCSUID", "CDUID", "CMAUID", "PHUUID", "LHINUID", "LHIN_SRUID"]
    
    if level not in valid_levels:
        raise Exception("There is no level: " + level)
    
    # Determine page format depending on year and level
    if level == "DAUID":
        prefix = "DA"
    else:
        prefix = level
        
    if year == "2011" or level == "DAUID":
        page = prefix + "_" + year
    else:
        page = year + "_" + prefix
    
    # Read and return data
    df = pd.read_excel(url, sheet_name=page)
    
    return df

# -----------------------------------------------------------------------------

def om_geo(year, level):
    """
    Gets a dataframe of OnMarg data for selected year and level, joined with
    geographic data from Stats Canada.

    Parameters
    ----------
    year : int
        Year of data to pull from.
    level : str
        Geographic level summarized to.

    Raises
    ------
    Exception
        Raises an exception if an invalid year or level was provided.

    Returns
    -------
    gdf : OnMarg data
        Returns a geodataframe of OnMarg data.

    """
    
    # Get the name of the shapefile in the directory
    def getFileName(filenames):
        for name in filenames:
            if re.search(".shp$", name):
                return name
        raise Exception("Error: Shapefile not found in download")
    
    # ---
    
    # Extract contents from a zip file
    def extract_data(url, filename=None):
        
        resp = urlopen(url)
        stat_zip = zipfile.ZipFile(BytesIO(resp.read()))
        
        with tempfile.TemporaryDirectory() as tempdir:
            stat_zip.extractall(tempdir)
            if filename is None:
                filenames = os.listdir(tempdir)
                filename = getFileName(filenames)
            filepath = tempdir + "\\" + filename
            geo_dat = gpd.read_file(filepath)
        
        return geo_dat
    
    # ---
    
    # Create 'Index' summary column
    def make_sum_col(df):
        names = list(df.columns)
        q_cols = [col for col in names if '_q_' in col]
        q_mean = df[q_cols].mean(axis=1)
        return df.assign(index_avg=q_mean)
    
    # ---
    
    # Process data from 2011 to 2016
    def process_2011_2016(year, level, stat_url):
        marg_dat = om_data(year=year, level=level)
        geo_dat = extract_data(stat_url)
        
        # Aggregate data if DAUID is not selected
        if level != 'DAUID':
            geo_dat = gpd.GeoDataFrame(geo_dat)
            geo_dat = geo_dat.to_crs(epsg=2962)
            geo_dat = geo_dat.dissolve(by=level, as_index=False)
        
        # Merge OnMarg data with Stats Canada data
        marg_dat[level] = marg_dat[level].astype(float)
        geo_dat[level] = geo_dat[level].astype(float)
        total_dat = marg_dat.merge(geo_dat, on=level, how='left')
        
        # Create GeoDataFrame
        total_dat = make_sum_col(total_dat)
        gdf = gpd.GeoDataFrame(total_dat)
        gdf.to_crs(epsg=2962)
    
        return gdf
    
    # ---
    
    # Process data from 2021
    def process_2021(level, shp_url_1, shp_url_2):
        marg_dat = om_data(year=year, level=level)
        
        # Transform data to follow 2011/2016 formatting
        geo_dat_1 = extract_data(shp_url_1, '2021_92-151_X.csv')
        geo_dat_1 = geo_dat_1[geo_dat_1['PRNAME_PRNOM'] == 'Ontario']
        geo_dat_1 = geo_dat_1.rename(columns={
            'DAUID_ADIDU' : 'DAUID',
            'PRUID_PRIDU' : 'PRUID',
            'PRNAME_PRNOM' : 'PRNAME',
            'CDUID_DRIDU' : 'CDUID',
            'CDNAME_DRNOM' : 'CDNAME',
            'CDTYPE_DRGENRE' : 'CDTYPE',
            'CCSUID_SRUIDU' : 'CCSUID',
            'CCSNAME_SRUNOM' : 'CCSNAME',
            'CSDUID_SDRIDU' : 'CSDUID',
            'CSDNAME_SDRNOM' : 'CSDNAME',
            'CSDTYPE_SDRGENRE' : 'CSDTYPE',
            'ERUID_REIDU' : 'ERUID',
            'ERNAME_RENOM' : 'ERNAME',
            'SACCODE_CSSCODE' : 'SACCODE',
            'SACTYPE_CSSGENRE' : 'SACTYPE',
            'CMAUID_RMRIDU' : 'CMAUID',
            'CMAPUID_RMRPIDU' : 'CMAPUID',
            'CMANAME_RMRNOM' : 'CMANAME',
            'CMATYPE_RMRGENRE' : 'CMATYPE',
            'CTUID_SRIDU' : 'CTUID',
            'CTNAME_SRNOM' : 'CTNAME',
            'ADAUID_ADAIDU' : 'ADAUID'
        })[[
            'DAUID',
            'PRUID',
            'PRNAME',
            'CDUID',
            'CDNAME',
            'CDTYPE',
            'CCSUID',
            'CCSNAME',
            'CSDUID',
            'CSDNAME',
            'CSDTYPE',
            'ERUID',
            'ERNAME',
            'SACCODE',
            'SACTYPE',
            'CMAUID',
            'CMAPUID',
            'CMANAME',
            'CMATYPE',
            'CTUID',
            'CTNAME',
            'ADAUID'
        ]]
        geo_dat_1 = geo_dat_1.drop_duplicates()
        
        geo_dat_2 = extract_data(shp_url_2)
        geo_dat_2.drop(columns=['PRUID'])
        
        # Merge Stats Canada data
        geo_dat_1['DAUID'] = geo_dat_1['DAUID'].astype(float)
        geo_dat_2['DAUID'] = geo_dat_2['DAUID'].astype(float)
        geo_dat = geo_dat_1.merge(geo_dat_2, on='DAUID', how='right')
        
        # Aggregate data if DAUID is not selected
        if level != 'DAUID':
            geo_dat = gpd.GeoDataFrame(geo_dat)
            geo_dat = geo_dat.to_crs(epsg=2962)
            geo_dat = geo_dat.dissolve(by=level, as_index=False)
        
        # Merge OnMarg data with Stats Canada data
        marg_dat[level] = marg_dat[level].astype(float)
        geo_dat[level] = geo_dat[level].astype(float)
        total_dat = marg_dat.merge(geo_dat, on=level, how='left')
        
        # Create GeoDataFrame
        total_dat = make_sum_col(total_dat)
        gdf = gpd.GeoDataFrame(total_dat)
        gdf.to_crs(epsg=2962)
        
        return gdf
    
    year = str(year)
    
    # Get data from year
    if year == "2001":
        raise Exception("This year has not yet been implemented")
    elif year == "2006":
        raise Exception("This year has not yet been implemented")
    elif year == "2011":
        stat_url = "https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gda_000a11a_e.zip"
        total_dat = process_2011_2016(year=year, level=level, stat_url=stat_url)
    elif year == "2016":
        stat_url = "https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lda_000b16a_e.zip"
        total_dat = process_2011_2016(year=year, level=level, stat_url=stat_url)
    elif year == "2021":
        stat_url_1 = "https://www12.statcan.gc.ca/census-recensement/2021/geo/aip-pia/attribute-attribs/files-fichiers/2021_92-151_X.zip"
        stat_url_2 = "https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000b21a_e.zip"
        total_dat = process_2021(level=level, shp_url_1=stat_url_1, shp_url_2=stat_url_2)
    else:
        raise Exception("There is no record for year: " + year)
    
    return total_dat