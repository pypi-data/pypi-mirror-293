from typing import List

from matplotlib import pyplot as plt
import numpy as np
import torch

from sihl.heads import AnomalyDetection

from .common import get_images, plot_to_numpy


@get_images.register(AnomalyDetection)
def _(head, config, input, target, features) -> List[np.ndarray]:
    prediction = head(features)
    image = head.normalize(features[0])
    teacher_output = head.teacher_project(features).to("cpu")
    student_output = head.student(image)
    st_teacher = student_output[:, : head.out_channels].to("cpu")
    st_teacher = (st_teacher - st_teacher.mean()) / st_teacher.std()
    st_autoencoder = student_output[:, head.out_channels :].to("cpu")
    ae_output = head.autoencoder(image).to("cpu")

    distance_st, distance_ae, distance_stae = head.compute_distances(features)
    anomaly_local = distance_st.mean(dim=1)
    anomaly_global = distance_stae.mean(dim=1)
    anomaly_local = (
        0.1 * (anomaly_local - head.q_st_start) / (head.q_st_end - head.q_st_start)
    ).to("cpu")
    anomaly_global = (
        0.1 * (anomaly_global - head.q_ae_start) / (head.q_ae_end - head.q_ae_start)
    ).to("cpu")

    images = (input.permute(0, 2, 3, 1) * 255).to(torch.uint8).to("cpu").numpy()
    visualizations = []
    for batch, image in enumerate(images):
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 10), dpi=100)
        for ax in axes:
            for subax in ax:
                subax.axis("off")
        axes[0][0].title.set_text("Input")
        axes[0][0].imshow(image)
        axes[0][1].title.set_text("Target")
        if target is not None:
            axes[0, 1].imshow(target[batch].to("cpu"), cmap="gray")
        axes[0][2].title.set_text("Prediction")
        if prediction is not None:
            axes[0][2].imshow(prediction[batch].to("cpu"), cmap="gray", vmin=0, vmax=1)

        axes[1][0].title.set_text("autoencoder")
        axes[1][0].imshow(ae_output[batch].mean(0), cmap="seismic", vmin=-1, vmax=1)
        axes[1][1].title.set_text("student (autoencoder)")
        axes[1][1].imshow(
            st_autoencoder[batch].mean(0), cmap="seismic", vmin=-1, vmax=1
        )
        axes[1][2].title.set_text("Global anomaly")
        axes[1][2].imshow(anomaly_global[batch], cmap="gray", vmin=0, vmax=1)

        axes[2][0].title.set_text("teacher")
        axes[2][0].imshow(
            teacher_output[batch].mean(0), cmap="seismic", vmin=-1, vmax=1
        )
        axes[2][1].title.set_text("student (teacher)")
        axes[2][1].imshow(st_teacher[batch].mean(0), cmap="seismic", vmin=-1, vmax=1)
        axes[2][2].title.set_text("Local anomaly")
        axes[2][2].imshow(anomaly_local[batch], cmap="gray", vmin=0, vmax=1)

        fig.tight_layout()
        visualizations.append(plot_to_numpy(fig))
        plt.close()
    return visualizations
