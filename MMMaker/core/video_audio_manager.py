import tempfile
from moviepy.editor import *


def extract_audio(video_path):
    """
    :param video_path: 영상에 쓰일 하이라이트 영상 경로
    :return: 영상에서 추출된 오디오 파일 경로
    """

    # Create random file name
    tf = tempfile.NamedTemporaryFile()

    audio_path = os.getcwd() + "video_audio_manager_" + tf.name[4:] + ".wav"

    # Access video file
    video_clip = VideoFileClip(video_path)

    # Extract audio file
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)

    return audio_path


def overwrite_audio(video_path, audio_path):
    """
    :param video_path: 영상에 쓰일 하이라이트 영상 경로
    :param audio_path: 음계가 조정된 오디오 파일 경로
    :return: 조정된 하이라이트 영상 경
    """
    # Access video file and audio file

    # Adjust video speed to sync with audio file

    # Overwrite video audio

    return video_path

