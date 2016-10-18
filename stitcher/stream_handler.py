"""
Stream handler module
"""
from abc import ABCMeta, abstractmethod
import cv2
from .formatter import Formatter
from .distortion_corrector.corrector import correct_distortion
from .panorama import Stitcher

class StreamHandler(object):
    """
    Abstract base stream class
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def stitch_streams(self):
        """
        Takes in a list of streams and stitches them into one stream
        """
        pass

    @abstractmethod
    def stitch_corrected_streams(self):
        """
        Takes in a list of streams and stitches them into one stream
        after applying distortion corrections
        """
        pass

class SingleStreamHandler(StreamHandler):
    """
    Stream handler for a single video stream
    """
    def __init__(self, stream):
        self.stream = stream

    def stitch_streams(self):
        if self.stream.validate():
            while self.stream.has_next():
                frame = self.stream.next()
                cv2.imshow("Stream", frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
            Formatter.print_status("[INFO] cleaning up...")
            self.stream.close()
            cv2.destroyAllWindows()
            cv2.waitKey(1)

    def stitch_corrected_streams(self):
        if self.stream.validate():
            while self.stream.has_next():
                frame = correct_distortion(self.stream.next())
                cv2.imshow("Stream", frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
            Formatter.print_status("[INFO] cleaning up...")
            self.stream.close()
            cv2.destroyAllWindows()
            cv2.waitKey(1)

class MultiStreamHandler(StreamHandler):
    """
    Stream handler for multiple video streams
    """
    def __init__(self, streams):
        self.streams = streams

    def stitch_streams(self):
        if all([stream.validate for stream in self.streams]):
            if len(self.streams) < 4:
                stitcher = Stitcher()
                left_stream = self.streams[0]
                right_stream = self.streams[1]
                while left_stream.has_next() and right_stream.has_next():
                    left_frame = left_stream.next()
                    right_frame = right_stream.next()
                    result = stitcher.stitch([left_frame, right_frame])

                    cv2.imshow("Left Stream", left_frame)
                    cv2.imshow("Right Stream", right_frame)
                    cv2.imshow("Stitched Stream", result)

                    # no homograpy could be computed
                    if result is None:
                        Formatter.print_err("[INFO] homography could not be computed")
                        break

                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("q"):
                        break

                # do a bit of cleanup
                Formatter.print_status("[INFO] cleaning up...")
                left_stream.close()
                right_stream.close()
                cv2.destroyAllWindows()
                cv2.waitKey(1)
            else:
                fst_stitcher = Stitcher()
                snd_stitcher = Stitcher()
                combined_stitcher = Stitcher()
                while all([stream.has_next() for stream in self.streams]):
                    frames = [stream.next() for stream in self.streams]
                    left_result = fst_stitcher.stitch([frames[0], frames[1]])
                    right_result = snd_stitcher.stitch([frames[2], frames[3]])
                    result = combined_stitcher.stitch([left_result, right_result])
                    cv2.imshow("Stitched Stream", result)

                    # no homograpy could be computed
                    if result is None:
                        Formatter.print_err("[INFO] homography could not be computed")
                        break

                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("q"):
                        break

                # do a bit of cleanup
                Formatter.print_status("[INFO] cleaning up...")
                for stream in self.streams:
                    stream.close()
                cv2.destroyAllWindows()
                cv2.waitKey(1)

    def stitch_corrected_streams(self):
        if all([stream.validate for stream in self.streams]):
            if len(self.streams) < 4:
                stitcher = Stitcher()
                left_stream = self.streams[0]
                right_stream = self.streams[1]
                while left_stream.has_next() and right_stream.has_next():
                    left_frame = correct_distortion(left_stream.next())
                    right_frame = correct_distortion(right_stream.next())
                    result = stitcher.stitch([left_frame, right_frame])

                    cv2.imshow("Left Stream", left_frame)
                    cv2.imshow("Right Stream", right_frame)
                    cv2.imshow("Stitched Stream", result)

                    # no homograpy could be computed
                    if result is None:
                        Formatter.print_err("[INFO] homography could not be computed")
                        break

                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("q"):
                        break

                # do a bit of cleanup
                Formatter.print_status("[INFO] cleaning up...")
                left_stream.close()
                right_stream.close()
                cv2.destroyAllWindows()
                cv2.waitKey(1)
            else:
                fst_stitcher = Stitcher()
                snd_stitcher = Stitcher()
                combined_stitcher = Stitcher()
                while all([stream.has_next() for stream in self.streams]):
                    frames = [correct_distortion(stream.next()) for stream in self.streams]
                    left_result = fst_stitcher.stitch([frames[0], frames[1]])
                    right_result = snd_stitcher.stitch([frames[2], frames[3]])
                    result = combined_stitcher.stitch([left_result, right_result])
                    cv2.imshow("Stitched Stream", result)

                    # no homograpy could be computed
                    if result is None:
                        Formatter.print_err("[INFO] homography could not be computed")
                        break

                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("q"):
                        break

                # do a bit of cleanup
                Formatter.print_status("[INFO] cleaning up...")
                for stream in self.streams:
                    stream.close()
                cv2.destroyAllWindows()
                cv2.waitKey(1)
