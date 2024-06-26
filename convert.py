import os
import subprocess
import logging
from tqdm import tqdm

# Set up logging output
logging.basicConfig(filename='conversion.log', level=logging.INFO)

# Input folder path
input_folder = '/mnt/speech-corpus/humiao/xwlb_crawling/xwlb'

# Output folder path
output_folder = '/mnt/speech-corpus/humiao/xwlb_crawling/xwlb_m4a'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the list of files in the input folder
files = os.listdir(input_folder)

# Iterate through each file in the input folder with a progress bar
for filename in tqdm(files, desc="Converting files", unit="file"):
    # Construct the input and output file paths
    input_file = os.path.join(input_folder, filename)
    output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.m4a")

    # Construct the FFmpeg command
    ffmpeg_cmd = f'ffmpeg -i "{input_file}" -c:a aac -vn "{output_file}"'

    # Run the FFmpeg command and capture only the stderr output
    completed_process = subprocess.run(ffmpeg_cmd, shell=True, stderr=subprocess.PIPE)

    # Check if there were any errors, and log them if present
    if completed_process.returncode != 0:
        logging.error(f"Error converting {filename}: {completed_process.stderr.decode('utf-8')}")
    else:
        logging.info(f"Conversion successful for {filename}. M4a file created.")
