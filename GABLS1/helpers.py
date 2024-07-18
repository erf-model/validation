import numpy as np
import xarray as xr
import glob
import os
from erftools.postprocessing import AveragedProfiles, Column

Tsim = 32400.

def load_erf_les(dpath='.',output_interval=1.0,Tavg=3600.):
    fpath = f'{dpath}/averaged_profiles.nc'
    try:
        ds = xr.open_dataset(fpath)
        print('Loaded',fpath)
    except:
        print('Processing',dpath)
        pro = AveragedProfiles(f'{dpath}/mean_profiles.dat',
                               f'{dpath}/covar_profiles.dat',
                               f'{dpath}/sfs_profiles.dat',
                               sampling_interval_s=output_interval)
        ds = pro.ds
        assert ds.t[-1] == Tsim
        ds = ds.sel(t=slice(Tsim-Tavg+1e-8,None))
        ds = ds.mean('t')
        ds['hvelmag'] = np.sqrt(ds['u']**2 + ds['v']**2)
        ds.to_netcdf(fpath)
    finally:
        return ds

def load_erf_scm(dpath='.',dt=1.0,Tavg=3600.):
    fpath = f'{dpath}/profiles.nc'
    try:
        ds = xr.open_dataset(fpath)
        print('Loaded',fpath)
    except:
        print('Processing SCM',dpath)
        # select plotfiles
        istart = int(np.round((Tsim - Tavg)/dt))
        pltfiles = glob.glob(f'{dpath}/plt*')
        assert len(pltfiles) > 0
        pltsteps = [int(os.path.split(dpath)[1][3:]) for dpath in pltfiles]
        pltfiles = sorted([dpath for i,dpath in zip(pltsteps,pltfiles) if i > istart])
        assert len(pltfiles) > 0
        # load column data
        df = Column(pltfiles).df
        # ugly way to time-average starting from a multiindex
        if len(pltfiles) > 1:
            df = df.unstack().mean().unstack().T
        ds = df.to_xarray()
        ds = ds.rename_vars(height='z').swap_dims(height='z')
        ds['hvelmag'] = ('z', np.sqrt(ds['x_velocity']**2 + ds['y_velocity']**2).values)
        ds = ds.rename_vars(theta='θ')
        # calculate additional QOIs
        z = ds.coords['z'].values
        zstag = 0.5*(z[1:] + z[:-1])
        dz = np.diff(z)
        Km = 0.5 * (ds['Kmv'].isel(z=slice(0,-1)).values + ds['Kmv'].isel(z=slice(1,None)).values)
        Kh = 0.5 * (ds['Khv'].isel(z=slice(0,-1)).values + ds['Khv'].isel(z=slice(1,None)).values)
        dUdz = ds['x_velocity'].diff('z') / dz
        dUdz = dUdz.rename(z='zstag').assign_coords(zstag=zstag)
        dVdz = ds['y_velocity'].diff('z') / dz
        dVdz = dVdz.rename(z='zstag').assign_coords(zstag=zstag)
        dTdz = ds['θ'].diff('z') / dz
        dTdz = dTdz.rename(z='zstag').assign_coords(zstag=zstag)
        ds["u'w'"] = -Km * dUdz
        ds["v'w'"] = -Km * dVdz
        ds["θ'w'"] = -Kh * dTdz
        # save
        ds.to_netcdf(fpath)
    finally:
        return ds
