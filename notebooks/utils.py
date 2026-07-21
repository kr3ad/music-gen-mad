import numpy as np
import torch
import matplotlib.pyplot as plt
from transformers import AutoProcessor, AutoFeatureExtractor
import librosa
import torchaudio

def load_process_bulk_audio(paths, sr=16000):
    waveforms = {}
    for path in paths:
        audio, sr = librosa.load(path, sr=sr)  # Analyze the first 10 seconds
        waveforms[path] = audio, sr
    return waveforms

def process_bulk_music_gen(waveforms, processor=AutoProcessor.from_pretrained("facebook/musicgen-small")):
    # Preprocess the audio and an optional text query to guide the cross-attention analysis
    inputs = {}
    for path, item in waveforms.items():
        wf, sr = item
        input = processor(
            audio=wf,
            sampling_rate=sr,
            text=[""],  # Optional text to analyze cross-attention alignments
            return_tensors="pt"
        )
        inputs[path] = input
    return inputs

def process_bulk_wave2vec(waveforms, feature_extractor=AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-960h")):
    inputs = {}
    for path, item in waveforms.items():
        wf, sr = item
        input = feature_extractor(
            wf,
            sampling_rate=sr,
            return_tensors="pt"
        )
        inputs[path] = input
    return inputs

def compute_mad_by_layer(self_attentions, seq_len):
    # 1. Construct the pairwise distance matrix in steps
    num_layers = len(self_attentions)
    num_heads = self_attentions[0].shape[1]
    steps = np.arange(seq_len)
    distance_matrix = np.abs(steps[:, None] - steps[None, :])

    # 2. Convert steps to relative distance
    relative_distance = distance_matrix / seq_len
    distance_tensor = torch.tensor(relative_distance, dtype=torch.float32, device=self_attentions[0].device)

    # 3. Compute Mean Attention Distance in seconds
    mean_distances = np.zeros((num_layers, num_heads))

    for layer_idx in range(num_layers):
        layer_attn = self_attentions[layer_idx][0]

        # Weighted sum of distances in seconds
        weighted_distances = layer_attn * distance_tensor
        token_mean_distances = torch.sum(weighted_distances, dim=-1)
        head_mean_distances = torch.mean(token_mean_distances, dim=-1)

        mean_distances[layer_idx] = head_mean_distances.cpu().numpy()
    return mean_distances

def plot_mad_single(mean_distances_seconds, num_heads, num_layers=24):
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
