# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

""" YoloV5 base detector class. """

# Importing basic libraries

import numpy as np
from tqdm import tqdm
import supervision as sv
import torch
from torch.hub import load_state_dict_from_url
from yolov5.utils.general import non_max_suppression, scale_coords

class YOLOV5Base:
    """
    Base detector class for YOLO V5. This class provides utility methods for
    loading the model, generating results, and performing single and batch image detections.
    """
    
    # Placeholder class-level attributes to be defined in derived classes
    IMAGE_SIZE = None
    STRIDE = None
    CLASS_NAMES = None
    TRANSFORM = None

    def __init__(self, weights=None, device="cpu", url=None):
        """
        Initialize the YOLO V5 detector.
        
        Args:
            weights (str, optional): 
                Path to the model weights. Defaults to None.
            device (str, optional): 
                Device for model inference. Defaults to "cpu".
            url (str, optional): 
                URL to fetch the model weights. Defaults to None.
        """
        self.model = None
        self.device = device
        self._load_model(weights, self.device, url)
        self.model.to(self.device)

    def _load_model(self, weights=None, device="cpu", url=None):
        """
        Load the YOLO V5 model weights.
        
        Args:
            weights (str, optional): 
                Path to the model weights. Defaults to None.
            device (str, optional): 
                Device for model inference. Defaults to "cpu".
            url (str, optional): 
                URL to fetch the model weights. Defaults to None.
        Raises:
            Exception: If weights are not provided.
        """
        if weights:
            checkpoint = torch.load(weights, map_location=torch.device(device))
        elif url:
            checkpoint = load_state_dict_from_url(url, map_location=torch.device(self.device))
        else:
            raise Exception("Need weights for inference.")
        self.model = checkpoint["model"].float().fuse().eval()  # Convert to FP32 model

    def results_generation(self, preds, img_id, id_strip=None):
        """
        Generate results for detection based on model predictions.
        
        Args:
            preds (numpy.ndarray): 
                Model predictions.
            img_id (str): 
                Image identifier.
            id_strip (str, optional): 
                Strip specific characters from img_id. Defaults to None.

        Returns:
            dict: Dictionary containing image ID, detections, and labels.
        """
        results = {"img_id": str(img_id).strip(id_strip)}
        results["detections"] = sv.Detections(
            xyxy=preds[:, :4],
            confidence=preds[:, 4],
            class_id=preds[:, 5].astype(int)
        )
        results["labels"] = [
            f"{self.CLASS_NAMES[class_id]} {confidence:0.2f}"
            for confidence, class_id in zip(results["detections"].confidence, results["detections"].class_id)
        ]
        return results

    def single_image_detection(self, img, img_size=None, img_path=None, conf_thres=0.2, id_strip=None):
        """
        Perform detection on a single image.
        
        Args:
            img (torch.Tensor): 
                Input image tensor.
            img_size (tuple): 
                Original image size.
            img_path (str): 
                Image path or identifier.
            conf_thres (float, optional): 
                Confidence threshold for predictions. Defaults to 0.2.
            id_strip (str, optional): 
                Characters to strip from img_id. Defaults to None.

        Returns:
            dict: Detection results.
        """
        if img_size is None:
            img_size = img.permute((1, 2, 0)).shape # We need hwc instead of chw for coord scaling
        preds = self.model(img.unsqueeze(0).to(self.device))[0]
        preds = torch.cat(non_max_suppression(prediction=preds, conf_thres=conf_thres), axis=0)
        preds[:, :4] = scale_coords([self.IMAGE_SIZE] * 2, preds[:, :4], img_size).round()
        return self.results_generation(preds.cpu().numpy(), img_path, id_strip)

    def batch_image_detection(self, dataloader, conf_thres=0.2, id_strip=None):
        """
        Perform detection on a batch of images.
        
        Args:
            dataloader (DataLoader): 
                DataLoader containing image batches.
            conf_thres (float, optional): 
                Confidence threshold for predictions. Defaults to 0.2.
            id_strip (str, optional): 
                Characters to strip from img_id. Defaults to None.

        Returns:
            list: List of detection results for all images.
        """
        results = []
        with tqdm(total=len(dataloader)) as pbar:
            for batch_index, (imgs, paths, sizes) in enumerate(dataloader):
                imgs = imgs.to(self.device)
                predictions = self.model(imgs)[0].detach().cpu()
                predictions = non_max_suppression(predictions, conf_thres=conf_thres)

                batch_results = []
                for i, pred in enumerate(predictions):
                    if pred.size(0) == 0:  
                        continue
                    pred = pred.numpy()
                    size = sizes[i].numpy()
                    path = paths[i]
                    original_coords = pred[:, :4].copy()
                    pred[:, :4] = scale_coords([self.IMAGE_SIZE] * 2, pred[:, :4], size).round()
                    # Normalize the coordinates for timelapse compatibility
                    normalized_coords = [[x1 / size[1], y1 / size[0], x2 / size[1], y2 / size[0]] for x1, y1, x2, y2 in pred[:, :4]]
                    res = self.results_generation(pred, path, id_strip)
                    res["normalized_coords"] = normalized_coords
                    batch_results.append(res)
                pbar.update(1)
                results.extend(batch_results)
            return results
