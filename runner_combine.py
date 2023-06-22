from calcutil.alpha_performance_evaluating_util import PerformanceEvaluatingUtils
from calcutil.alpha_performance_evaluator import PerformanceEvaluator
from data.dataloader import DataLoader
import logging
from sklearn.cluster import KMeans
from kneed import KneeLocator
from matplotlib import pyplot as plt
import pandas as pd

from data.dataprocessor import DataProcessor

alpha_perfmc_cfg_list = [
]

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    data_loader = DataLoader()
    alpha_performance_evaluating_utils = PerformanceEvaluatingUtils(data_loader)
    performance_evaluator = PerformanceEvaluator(alpha_performance_evaluating_utils)
    all_weights = performance_evaluator.load(alpha_perfmc_cfg_list).dropna()

    C = all_weights.corr()
    kmeans_kwargs = {
                     "init": "random",
                     "n_init": 10,
                     "max_iter": 300,
                     "random_state": 42,
    }

    sse = []
    for k in range(1, 21):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(C)
        sse.append(kmeans.inertia_)

    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 21), sse)
    plt.xticks(range(1, 21))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()

    kl = KneeLocator(range(1, 21), sse, curve = "convex", direction = "decreasing")
    elbow = kl.elbow

    kmeans = KMeans(n_clusters=elbow, **kmeans_kwargs)
    kmeans.fit(C)
    fitted_labels = pd.concat([pd.Series(kmeans.feature_names_in_, name="alpha"), pd.Series(kmeans.labels_, name="label")], axis=1).sort_values("label")
    print(fitted_labels)

    output = None
    all_labels = list(fitted_labels["label"].drop_duplicates())
    for label in all_labels:
        current_label = list(fitted_labels[fitted_labels["label"] == label]["alpha"])
        if output is None:
            output = all_weights[current_label].fillna(0).mean(axis=1)
        else:
            output += all_weights[current_label].fillna(0).mean(axis=1)
    output = output / len(all_labels)
    DataProcessor.write_alpha_data_all(output.rename("weight").reset_index(), "combined" + "_" + "kmeans")
