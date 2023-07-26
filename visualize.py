import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D

def get_outliers(df,anomalies_pred):
    df = df.reset_index()
    df['anomaly'] = anomalies_pred
    outliers = df.loc[df['anomaly']==-1]
    outlier_index = list(outliers.index)
    return outlier_index

def dim_reduction(df):
    pca = PCA(n_components=3)  # Reduce to k=3 dimensions
    scaler = StandardScaler()
    X = scaler.fit_transform(df)
    X_reduce = pca.fit_transform(X)
    return X_reduce

def plot_data(X_reduce, outlier_index):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_zlabel("x_composite_3")# Plot the compressed data points

    ax.scatter(X_reduce[:, 0], X_reduce[:, 1], zs=X_reduce[:, 2], s=4, lw=1, label="inliers",c="green")# Plot x's for the ground truth outliers

    ax.scatter(X_reduce[outlier_index,0],X_reduce[outlier_index,1], X_reduce[outlier_index,2], lw=2, s=60, marker="x", c="red", label="outliers")

    ax.legend()
    
    plt.show()

def main(df, anomalies_pred):
    X_reduce = dim_reduction(df)
    outlier_index = get_outliers(df, anomalies_pred)
    plot_data(X_reduce, outlier_index)
