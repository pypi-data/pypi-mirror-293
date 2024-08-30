__all__ = ['VideoCropper']

import subprocess
import cv2
import numpy as np
import fire
import os

def get_video_duration(input_file):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout)

def extract_frame(input_file, output_file, timestamp):
    cmd = [
        'ffmpeg',
        '-ss', str(timestamp),
        '-i', input_file,
        '-vframes', '1',
        '-y',
        output_file
    ]
    subprocess.run(cmd, check=True)

def find_crop_params(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)

    cropped = image[y:y+h, x:x+w]

    mask = cv2.inRange(cropped, np.array([17, 17, 17]), np.array([17, 17, 17]))
    mask_inv = cv2.bitwise_not(mask)

    contours, _ = cv2.findContours(mask_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    inner_max_contour = max(contours, key=cv2.contourArea)
    inner_x, inner_y, inner_w, inner_h = cv2.boundingRect(inner_max_contour)

    final_x = x + inner_x
    final_y = y + inner_y
    final_w = inner_w
    final_h = inner_h

    return f'{final_w}:{final_h}:{final_x}:{final_y}'

def crop_frame(input_file, output_file, timestamp, crop_params):
    cmd = [
        'ffmpeg',
        '-ss', str(timestamp),
        '-i', input_file,
        '-vframes', '1',
        '-filter:v', f'crop={crop_params}',
        '-y',
        output_file
    ]
    subprocess.run(cmd, check=True)

def crop_video(input_file, output_file, crop_params):
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-filter:v', f'crop={crop_params}',
        '-c:a', 'copy',
        '-y',
        output_file
    ]
    subprocess.run(cmd, check=True)

def display_frame(image_path):
    image = cv2.imread(image_path)
    cv2.imshow("Cropped Frame", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class VideoCropper:
    def process(self, input_file, output_dir=None, auto_crop=False):
        """
        Process a video file to crop it automatically or interactively.

        Args:
        input_file (str): Path to the input video file.
        output_dir (str, optional): Directory to save output files. Defaults to the same directory as the input file.
        auto_crop (bool, optional): If True, crop the video automatically without user confirmation. Defaults to False.

        Returns:
        str: Path to the cropped video file.
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        if output_dir is None:
            output_dir = os.path.dirname(input_file) or '.'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        extracted_frame = os.path.join(output_dir, f"{base_name}_extracted_frame.png")
        output_frame = os.path.join(output_dir, f"{base_name}_cropped_frame.png")
        output_video = os.path.join(output_dir, f"{base_name}_cropped.mp4")

        # Get video duration
        duration = get_video_duration(input_file)

        # Extract a frame from the middle of the video
        middle_timestamp = duration / 2
        extract_frame(input_file, extracted_frame, middle_timestamp)

        print(f"Frame extracted as {extracted_frame}")

        # Find crop parameters
        crop_params = find_crop_params(extracted_frame)
        print(f"Detected crop parameters: {crop_params}")

        # Crop the extracted frame
        crop_frame(input_file, output_frame, middle_timestamp, crop_params)

        print(f"Cropped frame saved as {output_frame}")

        if not auto_crop:
            print("Displaying cropped frame for review. Press any key to close the image.")
            display_frame(output_frame)
            confirmation = input("Do you want to proceed with cropping the entire video? (y/n): ")
            if confirmation.lower() != 'y':
                print("Video cropping cancelled.")
                return None

        crop_video(input_file, output_video, crop_params)
        print(f"Cropped video saved as {output_video}")
        return output_video

def main():
    fire.Fire(VideoCropper)

if __name__ == "__main__":
    main()