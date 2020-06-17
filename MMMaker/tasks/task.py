from __future__ import absolute_import

from celery import Celery

from app.memes.models import Task
from core.file_manager import downloader, uploader
from core.pitch_controller import adjust_sounds, EXAMPLE_MUSIC
from core.video_merger import merge_videos
from core.highlight_extractor import extract_highlights
from core.video_effect_manager import apply_effects


app = Celery('task')


@app.task()
def make_meme_task(pk):
    meme = Task.objects.prefetch_related('task_resources').get(pk=pk)
    resources = meme.task_resources.all()

    try:
        meme.status = Task.STATUS_STARTED
        meme.save(update_fields=['status'])

        file_urls = [resource.file_url for resource in resources ]
        file_paths = downloader(file_urls)
        meme.status = Task.STATUS_DOWNLOAD
        meme.save(update_fields=['status'])

        max_highlights, min_highlights = extract_highlights(file_paths)
        meme.status = Task.STATUS_EXTRACT_HIGHLIGHT
        meme.save(update_fields=['status'])

        videos = adjust_sounds(max_highlights, min_highlights, EXAMPLE_MUSIC)
        meme.status = Task.STATUS_ADJUST_SOUNDS
        meme.save(update_fields=['status'])

        videos = apply_effects(videos)
        meme.status = Task.STATUS_APPLY_EFFECTS
        meme.save(update_fields=['status'])

        file_path = merge_videos(videos)
        meme.status = Task.STATUS_MERGE_VIDEOS
        meme.save(update_fields=['status'])

        result_url = uploader(file_path)
        meme.status = Task.STATUS_UPLOADER
        meme.save(update_fields=['status'])

        meme.result_url = result_url
        meme.status = Task.STATUS_COMPLETE
        meme.save(update_fields=['result_url', 'status'])

    except Exception as e:
        meme.status = Task.STATUS_FAILED
        meme.save(update_fields=['status'])