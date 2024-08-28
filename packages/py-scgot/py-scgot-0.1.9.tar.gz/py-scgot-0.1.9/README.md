Modelling and Deciphering Cell Dynamics with Time-series or Snapshot Single Cell Dataset by Graphical Optimal Transport(GOT)
First release. 
- [x] Velocity (snapshot)
- [x] Velocity (time-series)
- [x] Trajectory
- [x] Cell Fate
- [x] Global Gene Regulatory Network
- [x] Local Gene Regulatory Network
- [ ] GRN Decomposition
- [ ] Perturbation

## Installation
### Installation with pip
To install with pip, run the following from a terminal:
```
conda create -n pyGOT python==3.10.0
pip install py-scgot
```

### Installation from GitHub
To clone the repository and install manually, run the following from a terminal:

```
git clone git@github.com:Witiy/pyGOT.git
cd pyGOT
conda create -n pyGOT python==3.10.0
python setup.py install
```

## Usage
### Velocity
#### snapshot
```
import pygot
embedding_key = 'X_pca'
velocity_key = 'velocity_pca'
model = pygot.tl.got_without_time_pipeline(adata, embedding_key, cell_type_key='leiden', kernel='dpt',
                                  cytotrace=True, scale=True, plot=True, basis='umap',
                                  x_centric=False, v_centric_iter_n=500, linear=True)
pygot.tl.velocity(adata, model.func, time_vary=False)
pygot.tl.velocity_graph(adata, embedding_key=embedding_key, velocity_key=velocity_key)
pygot.pl.velocity_embedding_stream(adata)
```

#### time-series
```
import pygot
import torch
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
embedding_key = 'X_pca'
velocity_key = 'velocity_pca'
time_key = 'Day' # your experimental time label
model, history = pygot.tl.fit_velocity_model(
            adata, time_key, embedding_key, device=device, )
pygot.tl.velocity(adata, model.func, time_key=time_key, time_vary=True)
pygot.tl.velocity_graph(adata, embedding_key=embedding_key, velocity_key=velocity_key)
pygot.pl.velocity_embedding_stream(adata)
```
### Cell Fate
```
snd = pygot.tl.SND(got, adata, embedding_key)
snd.setup_cell_fate(cell_type_key, ['Monocyte', 'Neutrophil'])
snd.calcu_cell_fate(x0_adata, end=2, sample_size=100)
```

## TODO
- [x] Architecture (beautiful interface)
- [x] Cell fate calculation (real data)
- [ ] GRN Decomposition (real data)
- [ ] Systematically evalute method (velocity, cell fate, GRN)
- [ ] Tutorial (website)
- [ ] Document in Code
- [ ] Perturbation


