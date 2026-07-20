import numpy as np
import torch
import matplotlib.pyplot as plt
from transformers import AutoProcessor
import librosa

def load_process_bulk_audio(paths, processor=AutoProcessor.from_pretrained("facebook/musicgen-small")):
    inputs = {}
    for path in paths:
        audio, sr = librosa.load(path, sr=32000, duration=60.0)  # Analyze the first 10 seconds

        # Preprocess the audio and an optional text query to guide the cross-attention analysis
        input = processor(
            audio=audio,
            sampling_rate=sr,
            text=[""],  # Optional text to analyze cross-attention alignments
            padding=True,
            return_tensors="pt"
        )
        inputs[path] = input
    return inputs

def compute_mad_by_layer(self_attentions, seq_len):
    # MusicGen's EnCodec frame rate is exactly 50 Hz (50 tokens per second)
    frame_rate = 50.0

    # 1. Construct the pairwise distance matrix in steps
    num_layers = len(self_attentions)
    num_heads = self_attentions[0].shape[1]
    steps = np.arange(seq_len)
    distance_matrix = np.abs(steps[:, None] - steps[None, :])

    # 2. Convert steps directly to seconds: 1 step = 0.02 seconds (20ms)
    distance_in_seconds = distance_matrix / frame_rate
    distance_tensor_sec = torch.tensor(distance_in_seconds, dtype=torch.float32, device=self_attentions[0].device)

    # 3. Compute Mean Attention Distance in seconds
    mean_distances_seconds = np.zeros((num_layers, num_heads))

    for layer_idx in range(num_layers):
        layer_attn = self_attentions[layer_idx][0]

        # Weighted sum of distances in seconds
        weighted_distances = layer_attn * distance_tensor_sec
        token_mean_distances = torch.sum(weighted_distances, dim=-1)
        head_mean_distances = torch.mean(token_mean_distances, dim=-1)

        mean_distances_seconds[layer_idx] = head_mean_distances.cpu().numpy()
    return mean_distances_seconds

def plot_mad(mean_distances_seconds, num_heads, num_layers=24):
    plt.figure(figsize=(10, 6))

    # for layer in range(num_layers):
    #     x_coords = [layer] * num_heads
    #     y_coords = mean_distances_seconds[layer]
    #     plt.scatter(x_coords, y_coords, color='forestgreen', alpha=0.4, edgecolors='none')

    layer_averages_sec = np.mean(mean_distances_seconds, axis=1)
    plt.plot(range(num_layers), layer_averages_sec, color='darkorange', linewidth=2.5, marker='o', label='Layer Average')

    plt.title("Mean Attention Distance in Seconds across MusicGen Layers", fontsize=14, fontweight='bold')
    plt.xlabel("Decoder Layer", fontsize=12)
    plt.ylabel("Temporal Attention Distance (Seconds)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    return plt
