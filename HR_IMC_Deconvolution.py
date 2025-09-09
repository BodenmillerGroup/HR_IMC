# %%
import os
import numpy as np
from tifffile import imread, imwrite
from scipy.ndimage import gaussian_filter
from skimage.restoration import richardson_lucy
from skimage.util import img_as_uint
import cv2


def RLD_HRIMC_circle(input_dir, output_dir, x0, iterations):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Loop through all TIFF files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".tiff") or filename.endswith(".tif"):
            # Read the TIFF file
            tiff_path = os.path.join(input_dir, filename)
            scan_data = imread(tiff_path)
            
            # Normalize each layer of the TIFF and apply transformations
            processed_layers = []
            original_layers = []
            for layer in range(scan_data.shape[0]):
                layer_data = scan_data[layer, :, :]
                Passes = np.array([7,6,5,8,7,
                                   7,8,7,6,6,
                                   7,9,8,7,8,
                                   8,7,7,6,6,
                                   7,6,6,5,5,
                                   6,6,5,5,4,
                                   4,6,4,5,3,
                                   4,5,6,6,5,
                                   4,5,5,4,3,
                                   4,4,3,6,5,
                                   4,5,5,4,4,
                                   3,3,4,4,3,
                                   3,2,4,3,2,
                                   2,1,1,3,2,
                                   2,1,1,3,3,
                                   2,2,2,2,1,
                                   1,1,1,3,2,
                                   1,2,2,1,1,
                                   2,1,1,4,3,
                                   2,1])

                Contributions = np.array([0.02,0.00108,0.00108,0.0034,0.0196,
                                       0.0196,0.0034,0.0034,0.0196,0.0196,
                                       0.0034,0.00223,0.00223,0.00223,0.0034,
                                       0.0034,0.0034,0.0034,0.0034,0.0034,
                                       0.0196,0.00106,0.0196,0.00106,0.0196,
                                       0.00108,0.00106,0.00106,0.00106,0.00106,
                                       0.00108,0.0196,0.00106,0.0196,0.00106,
                                       0.0196,0.0196,0.0034,0.0034,0.0196,
                                       0.0196,0.0034,0.0034,0.0196,0.0196,
                                       0.0034,0.0034,0.0196,0.00223,0.00223,
                                       0.00223,0.0034,0.0034,0.0034,0.0034,
                                       0.0034,0.0034,0.0196,0.00108,0.0196,
                                       0.00106,0.0196,0.00108,0.00106,0.00106,
                                       0.00106,0.00106,0.00108,0.0196,0.00106,
                                       0.0196,0.00106,0.0196,0.0034,0.0034,
                                       0.0196,0.0196,0.0034,0.0034,0.0196,
                                       0.0196,0.0034,0.0034,0.00223,0.00223,
                                       0.00223,0.0034,0.0034,0.0034,0.0034,
                                       0.00108,0.00196,0.00108,0.00219,0.00219,
                                       0.00219,0.00219])

                Contributions = Contributions / Contributions.sum()
                I0 = np.max(layer_data)
                Passes = I0 - I0/(1+ np.exp(-(Passes - x0)))
                y_array = Passes*Contributions
                total_sum = np.sum(y_array)

                result = list((
                    (y_array[3] + y_array[4] + y_array[11] + y_array[14] + y_array[15] + y_array[20])/ total_sum, 
                    (y_array[0] + y_array[5] + y_array[6] + y_array[7] + y_array[8] + y_array[12] + y_array[16] + y_array[17] + y_array[22])/ total_sum, 
                    (y_array[9] + y_array[10] + y_array[13] + y_array[18] + y_array[19] + y_array[24])  / total_sum,
                    (y_array[31] + y_array[36] + y_array[37] + y_array[38] + y_array[39] + y_array[48] + y_array[51] + y_array[52] + y_array[57])/ total_sum, 

                    (y_array[33] + y_array[40] + y_array[41] + y_array[42] + y_array[43] + y_array[49] + y_array[53] + y_array[54] + y_array[59])/ total_sum, 

                    (y_array[35] + y_array[44] + y_array[45] + y_array[46] + y_array[47] + y_array[50] + y_array[55] + y_array[56] + y_array[61])/ total_sum, 
                    (y_array[68] + y_array[73] + y_array[74] + y_array[75] + y_array[83] + y_array[86])/ total_sum, 
                    (y_array[70] + y_array[76] + y_array[77] + y_array[78] + y_array[79] + y_array[84] + y_array[87] + y_array[88] + y_array[91])/ total_sum, 
                    (y_array[72] + y_array[80] + y_array[81] + y_array[82] + y_array[85] + y_array[89])/ total_sum, 
                    ))

                kernel = np.array(result / np.sum(result))
                kernel = kernel.reshape(3, 3)

            
            
                # Normalize the data
                layer_data = (layer_data - layer_data.min()) / (layer_data.max() - layer_data.min())
                  
                layer_data_denoise = layer_data
                #Clip values to remove 0s (handled badly by RLD)
                layer_data_denoise = np.clip(layer_data_denoise, 1e-4, None)
                
                # Richardson-Lucy deconvolution
                deconvolved_image = richardson_lucy(layer_data_denoise, kernel, iterations=iterations)
                
                # Convert to 16-bit
                deconvolved_image_uint16 = img_as_uint(deconvolved_image)
                processed_layers.append(deconvolved_image_uint16)
                original_layers.append(layer_data_denoise)
            # Stack all processed layers into a single multi-layer TIFF
            processed_tiff = np.stack(processed_layers, axis=0)
            scan_data = np.stack(scan_data, axis=0)
            
            #Removing a 2 pixel (1um), border to account for border effect (remove if necessary)
            processed_tiff_cropped = processed_tiff[:, 3:-3, 3:-3]
            scan_data = scan_data[:, 3:-3, 3:-3]

            
            # Save the processed TIFF to the output directory
            output_path = os.path.join(output_dir, filename)
            imwrite(output_path, processed_tiff_cropped)
            
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_new{ext}"
            output_path = os.path.join(input_dir, new_filename)
            imwrite(output_path, scan_data)
    
    print(f"Processing complete. Files saved in {output_dir}")


# %%
input_dir = "/mnt/central_nas/projects/Pladioc/SRIMC_project/IF/IMC_data/img_HPF/"
output_dir = "/mnt/central_nas/projects/Pladioc/SRIMC_project/IF/IMC_data/processed/"

# %%
RLD_HRIMC_circle(input_dir, output_dir, x0 = 7, iterations = 4)



