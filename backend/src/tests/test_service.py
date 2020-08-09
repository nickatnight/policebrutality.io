from src.tests.utils import BaseTestCase
from src.services.link_service import LinkService
from src.services.video_service import VideoService


class VideoServiceTestCase(BaseTestCase):
    def test_video_update(self):
        v = {
            "state": "California",
            "city": "San Diego",
            "edit_at": "meh",
            "date": "2020-06-01",
            "date_text": "June 1st",
            "pbid": "ca-sandiego-1",
            "description": "test test",
        }
        video = VideoService.create_video(**v)
        LinkService.create_link(
            video,
            {
                "url": "http://shitpissfuckcuntcocksuckermotherfuckertitsfartterdandtwat.com",
                "text": "",
            },
        )

        VideoService.update_video(
            "ca-sandiego-1",
            {
                "tags": ["tag1", "tag2"],
                "description": "Updated description",
                "links": [{"url": "htts://theannoyingsite.com", "text": "Got eem"}],
            },
        )
        links = LinkService.list_links()
        exists = links(link="htts://theannoyingsite.com").first()
        video = VideoService.get_video(pbid="ca-sandiego-1")

        self.assertTrue(exists)
        self.assertTrue(["tag1", "tag2"], [t.name for t in video.tags])
        self.assertTrue(video.description, "Updated description")
