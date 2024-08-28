import torch.optim as optim
import numpy as np
import torch
from tqdm import tqdm



def mean_distance_loss(vectors):
    """
    :param vectors: (N, d) 
    :return: mean pair-wised l2 distance 
    """
    n = vectors.size(0)
    dist_matrix = torch.cdist(vectors, vectors)  # 计算所有向量对之间的距离
    loss = torch.sum(dist_matrix) / (n * (n - 1))  # 计算平均距离
    return loss
def vector_similarity_loss(vectors):
    
    """
    
    :param vectors: (N, d) tensor
    :return: mean pair-wised cosine 
    """
    n = vectors.size(0)
    norm_vectors = torch.nn.functional.normalize(vectors, p=2, dim=1)  # 归一化向量
    similarity_matrix = torch.mm(norm_vectors, norm_vectors.T)  # 计算余弦相似度矩阵
    # 将对角线上的相似度设置为0
    mask = torch.eye(n, device=vectors.device).bool()
    similarity_matrix[mask] = 0
    # 平均相似度损失，越大越好，因此用 1 - 平均相似度来最小化
    loss = torch.sum(1 - similarity_matrix) / (n * (n - 1))
    return loss
class BasicVelocityFunction(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 16),
            torch.nn.CELU(),
            torch.nn.Linear(16, 32),
            torch.nn.CELU(),
            torch.nn.Linear(32, output_dim)
        )
        
    def forward(self, x):
        return self.net(x)
    def _initialize_weights(self):
        for layer in self.net:
            if isinstance(layer, nn.Linear):
                nn.init.kaiming_uniform_(layer.weight, nonlinearity='celu')
                if layer.bias is not None:
                    nn.init.constant_(layer.bias, 0)

class DecomposeVelocityFunction(torch.nn.Module):
    def __init__(self, input_dim, output_dim, n_lineages):
        super().__init__()
        self.vector_lineages = torch.nn.ModuleList([
            BasicVelocityFunction(input_dim, output_dim) for _ in range(n_lineages)
        ])
        self.vector_growth = BasicVelocityFunction(input_dim, output_dim)
        
        self.n_lineages = n_lineages

    def forward(self, v, x, idx, t):
        v_g = self.vector_growth(x)
        v_ls = torch.zeros_like(v)
        #mean_v_l = torch.zeros(self.n_lineages, x.shape[1])
        mean_v_g = [[] for i in range(self.n_lineages)]
        mean_v_l = [[] for i in range(self.n_lineages)]
        loss_orth, loss_recon = 0., 0.
        
        for i in range(self.n_lineages):
            selected = (idx == i)

            v_l = self.vector_lineages[i](x[selected])
            
            for j in range(np.min(t), np.max(t) + 1):
                mean_v_l[i].append(v_l[t[selected] == j].mean(dim=0))
                mean_v_g[i].append(v_g[selected][t[selected] == j].mean(dim=0))

            loss_orth += torch.mean(torch.sum(v_g[selected] * v_l, dim=1) ** 2)
            loss_recon += torch.mean((v[selected] - (v_g[selected] + v_l))**2)
            v_ls[selected] = v_l
        
        loss_sim = 0
        max_t = np.min([len(a) for a in mean_v_g])
        for j in range(max_t):
            #loss_oppo -= vector_similarity_loss(torch.stack([mean_v_l[i][j] for i in range(self.n_lineages)]))
            loss_sim += mean_distance_loss(torch.stack([mean_v_g[i][j] for i in range(self.n_lineages)]))
        
        loss_sim /= max_t

        return loss_recon, loss_orth, loss_sim

    @torch.no_grad()
    def inference(self, x, idx):
        v_g = self.vector_growth(x)
        v_ls = torch.zeros_like(v_g)
        for i in range(self.n_lineages):
            selected = (idx == i)
            v_l = self.vector_lineages[i](x[selected])
            v_ls[selected] = v_l
        return v_g, v_ls

def preprocess_adata(adata, lineages, embedding_key, velocity_key, lineage_key, time_key, device):
    t = adata.obs[time_key].to_numpy().astype(int)
    idx = np.zeros(len(adata))
    for i, l in enumerate(lineages):
        idx[adata.obs[lineage_key] == l] = i
    idx = idx.astype(int)
    
    vs = torch.tensor(adata.obsm[velocity_key]).float().to(device)
    x = torch.tensor(adata.obsm[embedding_key]).float().to(device)
    return x, vs, idx, t




class Decomposition:
    def __init__(self, lineages, time_key,  embedding_key='X_pca', velocity_key='velocity_pca', lineage_key='future_cell_type', 
                          device=None):
        if device is None:
            device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.device = device
        self.lineages, self.time_key, self.embedding_key, self.velocity_key, self.lineage_key = \
            lineages, time_key, embedding_key, velocity_key, lineage_key
        

    def fit(self, adata, num_epochs=15000):
        
        input_dim, output_dim, m = adata.obsm[self.embedding_key].shape[1], adata.obsm[self.velocity_key].shape[1], len(self.lineages)
        
        self.decom_func = DecomposeVelocityFunction(input_dim, output_dim, m).to(device)

        x, vs, idx, t = preprocess_adata(adata, self.lineages, self.embedding_key, self.velocity_key, self.lineage_key, self.time_key, self.device)

        self.decom_func.train()
    
        ##pre-train
        print('Pre-train growth vector field')
        optimizer = optim.SGD(self.decom_func.vector_growth.parameters(), lr=0.01, weight_decay=0.01) 
        pbar = tqdm(range(num_epochs//20 + 1) )
        for epoch in pbar:
            optimizer.zero_grad()
            
            v_g = self.decom_func.vector_growth(x)
            
            loss = torch.mean((vs-v_g)**2)
            loss.backward()
            optimizer.step()
            

            if (epoch+1) % 100 == 0:
                pbar.set_description(f'Epoch [{epoch+1}/{num_epochs//20}], Loss : {loss.item():.4f}  ')



        print('Pre-train lineage vector field')
        optimizer = optim.SGD(self.decom_func.vector_lineages.parameters(), lr=0.01, weight_decay=0.01) 
        
        pbar = tqdm(range(num_epochs//20 + 1))
        for epoch in pbar:
            optimizer.zero_grad()
            l_recon, l_orth, l_sim = self.decom_func(vs, x, idx, t)
            loss = l_recon + 0.15 * l_orth + 0.05 * l_sim
            loss.backward()
            optimizer.step()

            if (epoch+1) % 100 == 0:
                pbar.set_description(f'Epoch [{epoch+1}/{num_epochs//20}], Loss : {loss.item():.4f}  ')

        
        #train
        print('Starting decomposing velocity into growth(shared) and lineage(specified) velocity..')
        optimizer = optim.SGD(self.decom_func.parameters(), lr=0.003, weight_decay=0.01)
        
        pbar = tqdm(range(num_epochs))

        for epoch in pbar:
            optimizer.zero_grad()
            l_recon, l_orth, l_sim = self.decom_func(vs, x, idx, t)
            loss = l_recon + 0.15*l_orth + 0.05 * l_sim
            loss.backward()
            optimizer.step()
            
            if (epoch+1) % 10 == 0:
                
                pbar.set_description(f'Epoch [{epoch+1}/{num_epochs}], Loss : {loss.item():.4f}  Recon : {l_recon.item():.4f}  Orth : {l_orth.item():.4f}  Sim: {l_sim.item() :.4f}')
                
        self.decom_func.eval()

    def decompose_velocity(self, adata, num_epochs=15000):
        self.decom_func.eval()
        x, vs, idx, t = preprocess_adata(adata, self.lineages, self.embedding_key, self.velocity_key, self.lineage_key, self.time_key, self.device)
        with torch.no_grad():
            v_g, v_l = self.decom_func.inference(x, idx)
        scores = torch.stack([torch.norm(v_g, dim=1), torch.norm(v_l, dim=1)], dim=1)
        #scores = torch.stack([torch.sum(v_g * vs, dim=1) / (torch.norm(v_g, dim=1) * torch.norm(vs, dim=1)), torch.sum(v_l * vs, dim=1) / (torch.norm(v_l, dim=1) * torch.norm(vs, dim=1)) ], dim=1)
        scores /= torch.sum(scores, dim=1)[:, None]
        vkey = self.velocity_key.split('_')[0]
        basis = self.velocity_key.split('_')[1]
        adata.obsm[vkey + '_growth_' + basis] = v_g.detach().cpu().numpy()
        adata.obsm[vkey + '_lineages_' + basis] = v_l.detach().cpu().numpy()
        adata.obs[['growth', 'lineages']] = scores.detach().cpu().numpy()