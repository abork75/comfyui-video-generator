"""
BatchFadeBlend — ComfyUI custom node
=====================================
Blends two IMAGE batches with a concave per-frame weight curve:

    w(i) = 1 - (i / fade_frames) ^ curve_power

Frame i < fade_frames  →  corrected * w(i) + original * (1 - w(i))
Frame i >= fade_frames →  original (untouched)

w=1.0 at frame 0, fades slowly at first, drops sharply near fade_frames,
then stays at 0 (full original) for the rest of the video.
"""

import torch


class BatchFadeBlend:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_corrected": ("IMAGE",),
                "images_original":  ("IMAGE",),
                "fade_frames": ("INT",   {"default": 76,  "min": 1,   "max": 9999, "step": 1}),
                "curve_power": ("FLOAT", {"default": 3.0, "min": 0.5, "max": 10.0, "step": 0.5}),
            }
        }

    RETURN_TYPES    = ("IMAGE",)
    RETURN_NAMES    = ("images",)
    FUNCTION        = "blend"
    CATEGORY        = "video/color"
    DESCRIPTION     = "Blend corrected and original image batches with a concave fade curve."

    def blend(self, images_corrected, images_original, fade_frames, curve_power):
        N      = fade_frames
        total  = images_original.shape[0]
        corr_n = images_corrected.shape[0]

        result = images_original.clone().float()
        corr   = images_corrected.float()

        for i in range(min(N, total)):
            w = 1.0 - (i / N) ** curve_power
            # images_corrected may cover fewer frames than images_original
            ci = min(i, corr_n - 1)
            result[i] = corr[ci] * w + result[i] * (1.0 - w)

        return (result,)


NODE_CLASS_MAPPINGS        = {"BatchFadeBlend": BatchFadeBlend}
NODE_DISPLAY_NAME_MAPPINGS = {"BatchFadeBlend": "Batch Fade Blend"}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
