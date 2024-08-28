import matplotlib.pyplot as plt
import matplotlib
import scanpy as sc
import numpy as np

def plot_trajectory(adata, traj, time_key, basis='pumap', title='', **kwargs):
    
    marker = matplotlib.markers.MarkerStyle('o', fillstyle='none')
    fig, ax = plt.subplots(1,1, **kwargs)
    ax.axis('off')
    sc.pl.embedding(adata, basis=basis, color=time_key, ax=ax, show=False, title=title)
    for i in range(traj.shape[1]):
        ax.plot(traj[:,i,0], traj[:,i,1], color='black',alpha=.3, linewidth=1)
    ax.scatter(traj[0,:,0], traj[0,:,1], color='blue', s=10, label='start')
    ax.scatter(traj[-1,:,0], traj[-1,:,1], color='red', s=10, label='end', marker=marker)
    plt.legend()
'''
def plot_checkpoint_traj(adata, cell_idx, manipulator : FateManipulator, t_end, encoder=None, embedding_key='pca', basis='pumap', 
                         show_traj=False, s=5, linewidth=1, ax=None, fig=None):
    
    xt = adata[cell_idx].obsm['X_'+embedding_key]
    t_start = manipulator.check_t_start(cell_idx)
    checkpoint_traj, _ = manipulator.simulator.simulation(xt,  t_start=t_start, t_end=t_end, encoder=encoder)
    print(checkpoint_traj.shape)
    if ax == None:
        fig, ax = plt.subplots(1,1, figsize=(12, 8))
    if show_traj:
        for i in range(checkpoint_traj.shape[1]):
            ax.plot(checkpoint_traj[:,i,0], checkpoint_traj[:,i,1], alpha=0.2, linewidth=linewidth, color='black')
    sc.pl.embedding(adata, basis=basis, ax=ax, show=False)

    c = np.array(np.linspace(t_start, t_end, checkpoint_traj.shape[0]))

    c = np.array([[c[i]] * checkpoint_traj.shape[1] for i in range(len(c))]).flatten()
    start_state = checkpoint_traj[0,:,:]
    
    #checkpoint_traj = checkpoint_traj[1:,:,:]
    checkpoint_traj = checkpoint_traj.reshape(-1, checkpoint_traj.shape[-1])

    cax = ax.scatter(checkpoint_traj[:,0], checkpoint_traj[:,1],  s=s, c=c, cmap='viridis')

    #ax.scatter(start_state[:,0], start_state[:,1],  s=s, c='blue', label='start')
    #plt.legend()
    plt.title('Simulated trajectory of checkpoints')
    plt.colorbar(
                cax, ax=ax, pad=0.01, fraction=0.08, aspect=30, 
            )
    #cbar = fig.colorbar(s)
    
        
    #cbar.set_label("infered timepoints")
'''