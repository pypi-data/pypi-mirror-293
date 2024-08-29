import h5py
import numpy as np
from xdas import DataArray
from xdas.virtual import VirtualSource
from datetime import datetime
import xarray as xr
from natsort import natsorted
import glob

def read_Terra15(fname):
  '''
  Open file from Terra15 version 6 using xdas loader
  '''

  with h5py.File(fname, "r") as file:
    ti=np.datetime64(datetime.utcfromtimestamp(file['data_product']['gps_time'][0])).astype('datetime64[ms]')
    tf=np.datetime64(datetime.utcfromtimestamp(file['data_product']['gps_time'][-1])).astype('datetime64[ms]')
    d0 = file.attrs['sensing_range_start']
    dx = file.attrs['dx']
    data = VirtualSource(file['data_product']['data'])
  nt, nd = data.shape
  t = {"tie_indices": [0, nt - 1], "tie_values": [ti, tf]}
  d = {"tie_indices": [0, nd - 1], "tie_values": [d0, d0+ (nd - 1) * dx]}
  return DataArray(data, {"time": t, "distance": d})


def dask_Terra15(fname,**kwargs):
  '''
  Open data using xarray dask 
  '''

  ds=xr.open_mfdataset(fname,engine='h5netcdf',group='/data_product',phony_dims='sort',concat_dim='phony_dim_0',combine='nested',**kwargs)

  ds=ds.rename({'phony_dim_0': 'time'})

  # Convert timestamp in numpy datetime[ns]
  pdt=ds['gps_time'].to_pandas()
  pdt = pdt.astype(int)
  pdt = pdt.apply(lambda x: datetime.utcfromtimestamp(x))
  ds['time']=pdt



  da=xr.open_dataset(natsorted(glob.glob(fname))[0])

  d0 = da.attrs['sensing_range_start']
  dx = da.attrs['dx']

  nt, nd = ds.data.shape

  d = np.arange(d0,d0+(nd)*dx,dx)

  ds=ds.rename({'phony_dim_1': 'distance'})
  ds['distance']=d

  # Copy attributs
  ds.attrs=da.attrs
  ds.attrs['nt']=nt

  # drop unwanted variable
  ds=ds.drop_vars('posix_time')
  ds=ds.drop_vars('gps_time')
  ds=ds.data.rename('velocity')

  return ds