from typing import Dict

from app.services.link_service import LinkService
from app.services.video_service import VideoService
from app.utils.helpers import RequestAPI
from app.utils.s3 import tmp_folder_clean_up


# Consts
BULK_API_DATA = "https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.json"  # noqa


class GitHubAPI(RequestAPI):
    """for handling all GitHub interactions
    """

    def __init__(self):
        super().__init__()

    def get_all_locations_data(self) -> Dict:
        """fetch json data from repo

        :return:                dict
        """
        r_json = list()
        req = self.request(BULK_API_DATA)

        if req:
            r_json = req.json()

        return r_json

    def create_objects_from_data(self, location_data: Dict) -> None:
        """capture data to mongodb

        :param location_data:           data from repo
        :return:
        """
        data = location_data.get("data")
        existing_video_names = [v.name for v in VideoService.list_videos()]

        for instance in data[:10]:
            # TODO: need unique id here
            name = instance.get("name")
            if name and name not in existing_video_names:
                links = instance.pop("links", [])
                video = VideoService.create_video(**instance)
                LinkService.create_links(video, links)

                tmp_folder_clean_up()

    def main(self) -> None:
        """main
        """
        locations_data = self.get_all_locations_data()
        self.create_objects_from_data(locations_data)
