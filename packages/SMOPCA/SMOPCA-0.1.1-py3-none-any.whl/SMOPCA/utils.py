import numpy as np
import matplotlib.pyplot as plt
import scanpy as sc
import scipy
from sklearn import metrics
from scipy import sparse


def preprocess_adata(adata_list, filter_gene=25, filter_cell=50, hvg=2000):
    adata_rna, adata_adt = adata_list
    sc.pp.filter_genes(adata_rna, min_cells=filter_gene)
    sc.pp.filter_cells(adata_rna, min_genes=filter_cell)
    adata2 = adata_adt[adata_rna.obs_names].copy()
    sc.pp.highly_variable_genes(adata_rna, flavor="seurat_v3", n_top_genes=hvg)
    sc.pp.normalize_total(adata_rna, target_sum=1e4)
    sc.pp.log1p(adata_rna)
    sc.pp.scale(adata_rna)
    adata1 = adata_rna[:, adata_rna.var['highly_variable']]
    adata2 = clr_normalize_each_cell(adata2)
    sc.pp.scale(adata2)
    pos = np.array(adata1.obsm['spatial'])
    X1, X2 = adata1.X.toarray(), adata2.X
    return X1, X2, pos


def clr_normalize_each_cell(adata, inplace=True):
    """Modified from SpatialGlue code"""
    def seurat_clr(x):
        s = np.sum(np.log1p(x[x > 0]))
        exp = np.exp(s / len(x))
        return np.log1p(x / exp)
    if not inplace:
        adata = adata.copy()
    adata.X = np.apply_along_axis(seurat_clr, 1, (adata.X.A if scipy.sparse.issparse(adata.X) else np.array(adata.X)))
    return adata


def clustering_metric(y, y_pred):
    ami = np.round(metrics.adjusted_mutual_info_score(y, y_pred), 5)
    nmi = np.round(metrics.normalized_mutual_info_score(y, y_pred), 5)
    ari = np.round(metrics.adjusted_rand_score(y, y_pred), 5)
    return ami, nmi, ari


def preprocess_hvg(x_list=[], select_list=[], top=1000):
    assert len(x_list) == len(select_list)
    x_selected_list = []
    for i, x in enumerate(x_list):
        if select_list[i]:
            print("selecting top", top, "hvg for modality", i + 1)
            hvg_ind = geneSelection(x, num_genes=top)
            x_hvg = x[:, hvg_ind]
            x_selected_list.append(x_hvg)
        else:
            x_selected_list.append(x)

    print("normalizing counts")
    x_normalized_list = []
    for i, x_selected in enumerate(x_selected_list):
        adata = sc.AnnData(x_selected)
        adata = normalize(adata, size_factors=True, normalize_input=True, logtrans_input=True)
        x_normalized = adata.X
        x_normalized_list.append(x_normalized)

    return tuple(x_normalized_list)


def normalize(adata, filter_min_counts=True, size_factors=True, normalize_input=True, logtrans_input=True):
    if filter_min_counts:
        sc.pp.filter_genes(adata, min_counts=1)
        sc.pp.filter_cells(adata, min_counts=1)
    if size_factors or normalize_input or logtrans_input:
        adata.raw = adata.copy()
    else:
        adata.raw = adata
    if size_factors:
        sc.pp.normalize_per_cell(adata)
        adata.obs['size_factors'] = adata.obs.n_counts / np.median(adata.obs.n_counts)
    else:
        adata.obs['size_factors'] = 1.0
    if logtrans_input:
        sc.pp.log1p(adata)
    if normalize_input:
        sc.pp.scale(adata)
    return adata


def geneSelection(data, threshold=0, at_least=10, y_offset=.02, x_offset=5, decay=1.5, num_genes=1000):
    """Modified from scMDC code"""
    if sparse.issparse(data):
        zeroRate = 1 - np.squeeze(np.array((data > threshold).mean(axis=0)))
        A = data.multiply(data > threshold)
        A.data = np.log2(A.data)
        meanExpr = np.zeros_like(zeroRate) * np.nan
        detected = zeroRate < 1
        meanExpr[detected] = np.squeeze(np.array(A[:, detected].mean(axis=0))) / (1 - zeroRate[detected])
    else:
        zeroRate = 1 - np.mean(data > threshold, axis=0)
        meanExpr = np.zeros_like(zeroRate) * np.nan
        detected = zeroRate < 1
        mask = data[:, detected] > threshold
        logs = np.zeros_like(data[:, detected]) * np.nan
        logs[mask] = np.log2(data[:, detected][mask])
        meanExpr[detected] = np.nanmean(logs, axis=0)

    lowDetection = np.array(np.sum(data > threshold, axis=0)).squeeze() < at_least
    zeroRate[lowDetection] = np.nan
    meanExpr[lowDetection] = np.nan

    if num_genes is not None:
        up = 10
        low = 0
        for t in range(200):
            nonan = ~np.isnan(zeroRate)
            selected = np.zeros_like(zeroRate).astype(bool)
            selected[nonan] = zeroRate[nonan] > np.exp(-decay * (meanExpr[nonan] - x_offset)) + y_offset
            if np.sum(selected) == num_genes:
                break
            elif np.sum(selected) < num_genes:
                up = x_offset
                x_offset = (x_offset + low) / 2
            else:
                low = x_offset
                x_offset = (x_offset + up) / 2
    else:
        nonan = ~np.isnan(zeroRate)
        selected = np.zeros_like(zeroRate).astype(bool)
        selected[nonan] = zeroRate[nonan] > np.exp(-decay * (meanExpr[nonan] - x_offset)) + y_offset

    return selected


def plot_cluster(labels: np.ndarray, pos: np.ndarray, colorList: list, pointSize=1, show=True):
    assert len(labels) == pos.shape[0]
    xList = pos[:, 0]
    yList = pos[:, 1]
    for i in range(len(xList)):
        plt.plot(xList[i], yList[i], marker='o', color=colorList[labels[i]], markersize=pointSize)
    plt.gca().set_aspect(1)
    if show:
        plt.show()
