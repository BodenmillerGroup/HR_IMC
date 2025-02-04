## High-resolution imaging mass cytometry: (HR-IMC)



This project stores details of both **PSF creation** and Richardson-Lucy **deconvolution** for high-resolution imaging mass cytometry (**HR-IMC**). 

Additional scripts relating to HR-IMC's performance assessment and application will be shared upon request prior to publication. All code will be publicly shared upon publication.



## Overview
Here we provide a python script designed for processing high-resolution Imaging Mass Cytometry (IMC) data. It applies Richardson-Lucy deconvolution with a custom PSF to improve image resolution to 333 nm. The script takes oversampled multi-layer TIFF images as input, processes them layer by layer, and outputs the enhanced images.

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

The test image contains several nuclei measured with two channels (ATP5A & Iridium) to visualize mitochondria and nuclei. The expected output can be downloaded for visual comparison. 

1. **Download the test image (Demo.tif)**: Ensure you have a directory containing `.tif` files.
2. **Modify the script's input and output directory paths**:
   ```python
   input_dir = "/path/to/demo/data/"
   output_dir = "/path/to/output/"
   ```
3. **Run the script**:
   ```sh
   python RLD_HRIMC_circle.py
   ```

Expected Run Time: **5-10 minutes**


_The same instructions apply to run this script on your own data set. Keep in mind that large datasets (~1000 images) can take several hours to run, depending on hardware capabilities_


