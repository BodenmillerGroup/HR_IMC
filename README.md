## High-resolution imaging mass cytometry: (HR-IMC)



This project stores details of both **PSF creation** and Richardson-Lucy **deconvolution** for high-resolution imaging mass cytometry (**HR-IMC**). Additional scripts relating to HR-IMC's performance assessment and application are provided.



## Overview
Here we provide a python script designed for processing high-resolution Imaging Mass Cytometry (IMC) data. It applies Richardson-Lucy deconvolution with a custom PSF to improve image resolution to 333 nm. The script takes oversampled multi-layer TIFF images as input, processes them layer by layer, and outputs the enhanced images. Please note that there is no additional data processing step following the acquisition process. The input is the raw .tiff image extracted (typically via Steinbock) from the .mcd file produced at acquisition. 

If the user has generated oversampled data for 500 nm resolution, this can be specified using the `resolution = 500` argument. The user can also alter iteration number and signal inflection point. 


## System Requirements
- **Operating System**: Linux or macOS (Windows may work but is untested)
- **CPU**: Multi-core processor (recommended: 8+ cores)
- **RAM**: At least 32GB (recommended: 64GB+ for large datasets)
- **Storage**: Sufficient disk space for temporary files and output images


## Installation Guide

1. **Install Python** (version 3.7 or higher recommended):
   ```sh
   sudo apt update && sudo apt install python3 python3-pip -y  # For Debian/Ubuntu
   ````
   or download from https://www.python.org/downloads/

2. **Install required Python packages:**
   ```sh
   pip install numpy tifffile scipy scikit-image opencv-python
   ```

On a standard desktop computer, installation should take approximately 5-10 minutes.




## Instructions to Run on Demo Data

The test image contains a zoom-in of smooth muscle actin fibres captured with our oversampling technique. Our deconvolution pipeline acts to recover fine sub-micron structural details. We visualise Histone H3 (nuclear), SMA and ATP5A (mitochondrial) markers. The expected output can be downloaded for visual comparison. 

1. **Download the test image (Demo.tif)**: Ensure you have a directory containing `.tif` files.
2. **Modify the script's input and output directory paths**:
   ```python
   input_dir = "/path/to/demo/data/"
   output_dir = "/path/to/output/"
   ```
3. **Run the script**:
   ```sh
   python HR_IMC_Deconvolution.py
   ```

Expected Run Time: **less than a minute**

*The same instructions apply to run this script on your own data set. Keep in mind that large datasets (~1000 images) can take several hours to run, depending on hardware capabilities. The iteration number can be altered to refine data (<20 recommended)*


## Data availability
Provided scripts are based on high-resolution imaging mass cytometry (HR-IMC) data available at Zenodo (https://doi.org/10.5281/zenodo.17077712).


## Alternative resolutions
In this code, we only provide deconvolution strategies for 333 and 500 nm step sizes. In order to tailor the worflow to alternative resolutions, the laser scanning patterns need to be modelled in a vector-based graphics system or calculated in an computational grid-based simulation with a 2D circular kernal. Intersectional areas can be calculated and weighted PSFs formulated accordingly. 


## High-resolution IMC (HR-IMC) workflow

**Panel Design**
1. Select antibodies with strong signal
    * Use markers validated in classical IMC
    * Recommended signal-to-noise ratio: SNR > 5
    * Average signal intensity: ≥ 10 counts
2. Optimize antibody concentration

**Laser Energy Optimization**
1. Define test regions
    * Select multiple adjacent regions of interest (ROIs)
    * Assign one laser energy setting per ROI
2. Repeated ablation of the same region
    * Within each ROI, repeatedly ablate the exact same region using the same laser energy
    * This simulates the repeated passes required for HR-IMC oversampling
3. Number of ablation rounds
    * Number of ablation rounds = (1 µm / target resolution)² + 1 (e.g. 5 for 0.5 µm)
    * Perform one additional ablation round to evaluate remaining signal
4. Select optimal energy: Choose the highest laser energy that still preserves tissue signal across all rounds
5. Determine x₀ for image deconvolution
    * Fit an inverse sigmoidal decay model to signal intensity vs. number of laser passes
    * Extract x₀ (inflection point) representing 50% signal loss

**HR-IMC Data Acquisition**
1. Set laser step size to desired resolution (e.g. 0.5 µm for 500 nm resolution)
2. Adjust laser energy based on laser energy optimization
3. Export acquisition as MCD files

**Image Deconvolution & Reconstruction**
1. Download HR-IMC deconvolution algorithm (HRIMC_multiple_resolutions.py)
2. Extract TIFF files
    * Use steinbock to convert .mcd files to TIFF
3. Run deconvolution
    * Input: TIFF images from the img/ directory
    * Set: input path, output directory, x₀ value from laser optimization
    * Execute the script to generate high-resolution reconstructed images

**Image Segmentation**
1. Quality control: Remove markers with poor signal or low SNR
2. Segment cells using steinbock
    * Adjust expected pixel size (default: 1 µm, HR-IMC example: 0.5 µm)
3. Downstream analysis


## Informational overview
For more information, please consult our _Nature Methods_ publication: [High-resolution imaging mass cytometry to map subcellular structures](https://www.nature.com/articles/s41592-025-02889-8) 
The guidelines from above are also outlined in Extended Data Figure 5.


## License information
<sub>
MIT License  
*Copyright (c) 2025 [Bodenmiller lab]  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*
<sub>

