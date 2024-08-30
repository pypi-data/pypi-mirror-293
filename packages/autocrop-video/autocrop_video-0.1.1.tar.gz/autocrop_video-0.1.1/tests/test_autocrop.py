import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from autocrop.main import VideoCropper, get_video_duration, find_crop_params

import numpy as np
import cv2

class TestAutocrop(unittest.TestCase):

    def setUp(self):
        self.cropper = VideoCropper()
        self.test_video = "test_video.mp4"
        self.test_frame = "test_frame.png"

    @patch('autocrop.main.subprocess.run')
    def test_get_video_duration(self, mock_run):
        mock_run.return_value = MagicMock(stdout="10.5")
        duration = get_video_duration(self.test_video)
        self.assertEqual(duration, 10.5)
        mock_run.assert_called_once()

    @patch('autocrop.main.cv2.imread')
    @patch('autocrop.main.cv2.cvtColor')
    @patch('autocrop.main.cv2.threshold')
    @patch('autocrop.main.cv2.findContours')
    @patch('autocrop.main.cv2.boundingRect')
    @patch('autocrop.main.cv2.inRange')
    def test_find_crop_params(self, mock_inRange, mock_boundingRect, mock_findContours, mock_threshold, mock_cvtColor, mock_imread):
        # Create a mock image with a black background and a white rectangle
        mock_image = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_image[20:80, 10:90] = 255  # White rectangle from (10, 20) to (90, 80)

        mock_imread.return_value = mock_image

        # Set up the expected grayscale image
        expected_gray = cv2.cvtColor(mock_image, cv2.COLOR_BGR2GRAY)
        mock_cvtColor.return_value = expected_gray

        # Manually set the return value of the threshold to ensure it returns a tuple
        expected_thresh = np.ones_like(expected_gray) * 255
        mock_threshold.return_value = (1, expected_thresh)  # Mock the return of the threshold function

        # Adjust for different versions of findContours
        expected_contours = [np.array([[10, 20], [10, 80], [90, 80], [90, 20]])]
        if cv2.__version__.startswith('4'):
            mock_findContours.return_value = (expected_contours, None)
        else:
            mock_findContours.return_value = (None, expected_contours, None)

        # Mock boundingRect to return the expected cropping coordinates
        mock_boundingRect.side_effect = [(10, 20, 80, 60), (0, 0, 80, 60)]
        mock_inRange.return_value = expected_thresh

        crop_params = find_crop_params(self.test_frame)
        self.assertEqual(crop_params, "80:60:10:20")


    @patch('autocrop.main.get_video_duration')
    @patch('autocrop.main.extract_frame')
    @patch('autocrop.main.find_crop_params')
    @patch('autocrop.main.crop_frame')
    @patch('autocrop.main.crop_video')
    @patch('autocrop.main.cv2.imread')
    @patch('autocrop.main.cv2.imshow')
    @patch('autocrop.main.cv2.waitKey')
    @patch('autocrop.main.cv2.destroyAllWindows')
    @patch('builtins.input', return_value='y')
    def test_process(self, mock_input, mock_destroyAllWindows, mock_waitKey, mock_imshow, mock_imread,
                     mock_crop_video, mock_crop_frame, mock_find_crop_params, mock_extract_frame, mock_get_duration):
        mock_get_duration.return_value = 10.0
        mock_find_crop_params.return_value = "100:200:10:20"
        mock_imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

        with tempfile.TemporaryDirectory() as tmpdirname:
            input_file = os.path.join(tmpdirname, "input.mp4")
            open(input_file, 'a').close()  # Create an empty file

            output_file = self.cropper.process(input_file, tmpdirname)

            self.assertIsNotNone(output_file)
            self.assertTrue(output_file.endswith("_cropped.mp4"))

            mock_get_duration.assert_called_once()
            mock_extract_frame.assert_called_once()
            mock_find_crop_params.assert_called_once()
            mock_crop_frame.assert_called_once()
            mock_crop_video.assert_called_once()

    @patch('autocrop.main.get_video_duration')
    @patch('autocrop.main.extract_frame')
    @patch('autocrop.main.find_crop_params')
    @patch('autocrop.main.crop_frame')
    @patch('autocrop.main.crop_video')
    def test_process_auto_crop(self, mock_crop_video, mock_crop_frame, mock_find_crop_params, mock_extract_frame, mock_get_duration):
        mock_get_duration.return_value = 10.0
        mock_find_crop_params.return_value = "100:200:10:20"

        with tempfile.TemporaryDirectory() as tmpdirname:
            input_file = os.path.join(tmpdirname, "input.mp4")
            open(input_file, 'a').close()  # Create an empty file

            output_file = self.cropper.process(input_file, tmpdirname, auto_crop=True)

            self.assertIsNotNone(output_file)
            self.assertTrue(output_file.endswith("_cropped.mp4"))

            mock_get_duration.assert_called_once()
            mock_extract_frame.assert_called_once()
            mock_find_crop_params.assert_called_once()
            mock_crop_frame.assert_called_once()
            mock_crop_video.assert_called_once()

if __name__ == '__main__':
    unittest.main()