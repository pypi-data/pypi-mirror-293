<div style="text-align: center;">
  <img src="../docs/images/ncut.svg" alt="NCUT" style="width: 80%; filter: brightness(60%) grayscale(100%);"/>
</div>

### [🌐Documentation](https://ncut-pytorch.readthedocs.io/) | [🤗HuggingFace Demo](https://huggingface.co/spaces/huzey/ncut-pytorch)


## NCUT: Nyström Normalized Cut

**Normalized Cut**, aka. spectral clustering, is a graphical method to analyze data grouping in the affinity eigenvector space. It has been widely used for unsupervised segmentation in the 2000s.

**Nyström Normalized Cut**, is a new approximation algorithm developed for large-scale graph cuts,  a large-graph of million nodes can be processed in under 10s (cpu) or 2s (gpu).  


---

## Installation & Quick Start

PyPI install, our package is based on PyTorch, please [install PyTorch](https://pytorch.org/get-started/locally/) first

```shell
pip install ncut-pytorch
```


Minimal example on how to run NCUT:

```py linenums="1"
import torch
from ncut_pytorch import NCUT, rgb_from_tsne_3d

model_features = torch.rand(20, 64, 64, 768)  # (B, H, W, C)

inp = model_features.reshape(-1, 768)  # flatten
eigvectors, eigvalues = NCUT(num_eig=100, device='cuda:0').fit_transform(inp)
tsne_x3d, tsne_rgb = rgb_from_tsne_3d(eigvectors, device='cuda:0')

eigvectors = eigvectors.reshape(20, 64, 64, 100)  # (B, H, W, num_eig)
tsne_rgb = tsne_rgb.reshape(20, 64, 64, 3)  # (B, H, W, 3)
```

We have implemented some backbone models, they can be used as feature extractors, Here is a list of available models:

```py
from ncut_pytorch.backbone import list_models
print(list_models())
[
  'SAM2(sam2_hiera_t)', 'SAM2(sam2_hiera_s)', 'SAM2(sam2_hiera_b+)', 'SAM2(sam2_hiera_l)', 
  'SAM(sam_vit_b)', 'SAM(sam_vit_l)', 'SAM(sam_vit_h)', 'MobileSAM(TinyViT)', 
  'DiNOv2reg(dinov2_vits14_reg)', 'DiNOv2reg(dinov2_vitb14_reg)', 'DiNOv2reg(dinov2_vitl14_reg)', 'DiNOv2reg(dinov2_vitg14_reg)', 
  'DiNOv2(dinov2_vits14)', 'DiNOv2(dinov2_vitb14)', 'DiNOv2(dinov2_vitl14)', 'DiNOv2(dinov2_vitg14)', 
  'DiNO(dino_vitb8)', 'DiNO(dino_vits8)', 'DiNO(dino_vitb16)', 'DiNO(dino_vits16)', 
  'CLIP(ViT-B-16/openai)', 'CLIP(ViT-B-16/laion2b_s34b_b88k)', 
  'CLIP(eva02_base_patch14_448/mim_in22k_ft_in1k)', 
  'CLIP(convnext_base_w_320/laion_aesthetic_s13b_b82k)', 
  'MAE(vit_base)', 'ImageNet(vit_base)'
]
```

A example that run with a real backbone model:

```py linenums="1"
import torch
from ncut_pytorch import NCUT, rgb_from_tsne_3d
from ncut_pytorch.backbone import load_model, extract_features

model = load_model(model_name="SAM(sam_vit_b)")
images = torch.rand(20, 1024, 1024, 3)
model_features = extract_features(images, model, node_type='attn', layer=6)
# model_features = model(images)['attn'][6]  # this also works

inp = model_features.reshape(-1, 768)  # flatten
eigvectors, eigvalues = NCUT(num_eig=100, device='cuda:0').fit_transform(inp)
tsne_x3d, tsne_rgb = rgb_from_tsne_3d(eigvectors, device='cuda:0')

eigvectors = eigvectors.reshape(20, 64, 64, 100)  # (B, H, W, num_eig)
tsne_rgb = tsne_rgb.reshape(20, 64, 64, 3)  # (B, H, W, 3)
```


---

> paper in prep, Yang 2024
>
> AlignedCut: Visual Concepts Discovery on Brain-Guided Universal Feature Space, Huzheng Yang, James Gee\*, Jianbo Shi\*,2024
> 
> Normalized Cuts and Image Segmentation, Jianbo Shi and Jitendra Malik, 2000
