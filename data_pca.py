
from data_src import sales, sales_shape
from sklearn.decomposition import PCA

pca = PCA(n_components = 5)
sales_pca_shape = sales_shape[:2] + (5,)
sales_pca = pca.fit_transform(sales.reshape((-1, 33))).reshape(sales_pca_shape)

pca_total = PCA(n_components = 100)
total_sales_pca = pca_total.fit_transform(sales.reshape(sales_shape[0], -1))
total_sales_pca_shape = total_sales_pca.shape
