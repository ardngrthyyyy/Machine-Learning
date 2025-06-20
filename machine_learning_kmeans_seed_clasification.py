import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Load data dan pre processing
data = pd.read_csv('/content/Seed_Data.csv')
y = data['target'].values
data = data.drop(columns='target')
data.rename(columns={
    'A': 'area',
    'P': 'perimeter',
    'C': 'compactness',
    'LK': 'length of kernel',
    'WK': 'width of kernel',
    'LKG': 'length of kernel groove'
}, inplace=True)
data.head(10)

# Berdasarkan korelasi dan pengetahuan domain, hapus 'perimeter' dan 'lebar kernel'
data_drop = data.drop(columns=['perimeter', 'width of kernel'])
X = data_drop.values
data_drop

# Correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(pd.DataFrame(X, columns=data_drop.columns).corr(), square=True, annot=True, cbar=False, cmap='BuGn')
plt.title("Correlation Heatmap of Selected Features")
plt.show()

# Implementasi Manual
def manual_kmeans(X, k=3, max_iters=100, tol=1e-4, random_state=42):
    np.random.seed(random_state)
    n_samples, n_features = X.shape
    centroids = X[np.random.choice(n_samples, k, replace=False)]
    clusters = np.zeros(n_samples, dtype=int)
    for _ in range(max_iters):
        for i in range(n_samples):
            distances = np.linalg.norm(X[i] - centroids, axis=1)
            clusters[i] = np.argmin(distances)
        new_centroids = np.array([X[clusters == idx].mean(axis=0) if np.any(clusters == idx) else centroids[idx] for idx in range(k)])
        if np.linalg.norm(new_centroids - centroids) < tol:
            break
        centroids = new_centroids
    return clusters, centroids
def manual_accuracy_score(true_labels, pred_labels):
    return np.mean(true_labels == pred_labels)
def manual_confusion_matrix(true_labels, pred_labels, n_classes=3):
    matrix = np.zeros((n_classes, n_classes), dtype=int)
    for t, p in zip(true_labels, pred_labels):
        matrix[t, p] += 1
    return matrix

from collections import Counter
def manual_mode(labels):
    if len(labels) == 0:
        return None
    count = Counter(labels)
    return count.most_common(1)[0][0]
def relabel_clusters(true_labels, cluster_assignments, n_clusters=3):
    new_labels = np.zeros_like(cluster_assignments)
    for cluster_id in range(n_clusters):
        mask = cluster_assignments == cluster_id
        if np.any(mask):
            common_label = manual_mode(true_labels[mask])
            new_labels[mask] = common_label
    return new_labels
def calculate_inertia(X, k, centroids, clusters):
    inertia = 0
    for i in range(k):
        cluster_points = X[clusters == i]
        inertia += np.sum(np.linalg.norm(cluster_points - centroids[i], axis=1) ** 2)
    return inertia

def manual_elbow_method(X, max_k=7):
    inertias = []
    for k in range(1, max_k + 1):
        clusters, centroids = manual_kmeans(X, k=k)
        inertia = calculate_inertia(X, k, centroids, clusters)
        inertias.append(inertia)
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_k + 1), inertias, 'o-', color='#4c72b0')
    plt.xlabel('Number of Clusters k')
    plt.ylabel('Inertia (Sum of Squared Distances)')
    plt.title('Elbow Method For Optimal k')
    plt.grid(True)
    plt.show()

manual_elbow_method(X, max_k=7)
# Jalankan KMeans dengan k=3
clusters, centroids = manual_kmeans(X, k=3)
labels = relabel_clusters(y, clusters, n_clusters=3)

# Hitung confusion matrix
matrix = manual_confusion_matrix(y, labels, n_classes=3)
print("Confusion Matrix:")
print(matrix)

# Visualize confusion matrix menggunakan seaborn heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(matrix.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=[0,1,2], yticklabels=[0,1,2])
plt.xlabel('True Label')
plt.ylabel('Predicted Label')
plt.title('Confusion Matrix Heatmap')
plt.show()

# Hitung accuracy
accuracy = manual_accuracy_score(y, labels)
print(f"Manual KMeans Accuracy: {accuracy:.4f}")

n_classes = matrix.shape[0]
precision = np.zeros(n_classes)
recall = np.zeros(n_classes)
for i in range(n_classes):
    TP = matrix[i, i]
    FP = matrix[:, i].sum() - TP
    FN = matrix[i, :].sum() - TP
    precision[i] = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    recall[i] = TP / (TP + FN) if (TP + FN) > 0 else 0.0
# Show precision and recall per class
for i in range(n_classes):
    print(f"Precision for class {i}: {precision[i]:.4f}")
    print(f"Recall for class {i}: {recall[i]:.4f}")
