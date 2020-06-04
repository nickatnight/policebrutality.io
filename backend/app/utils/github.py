from typing import Dict, List

from app.services.video_service import VideoService
from app.utils.helpers import RequestAPI, Identifier


# Consts
API_BASE = "https://api.github.com/repos/2020PB/police-brutality/"
API_REPORTS = f"{API_BASE}contents/reports"


class GitHubAPI(RequestAPI):
    """for handling all GitHub interactions
    """

    def __init__(self):
        super().__init__()

    def get_states_list(self) -> List[Dict]:
        """get top level data (by state)

        :return:                list of items from github api
        """
        r_json = list()
        req = self.request(API_REPORTS)

        if req:
            r_json = req.json()

        return r_json

    def get_raw_content(self, report_list: List[Dict]) -> None:
        """fetch the the raw .md content for each state

        :param report_list:     api data form github
        :return:                None
        """
        for report in report_list:
            state = report.get("name", "").strip(".md")
            content = self.request(report.get("download_url")).content
            self.parse_state_data(content, state)

    def parse_state_data(self, state_content: bytes, state: str) -> None:
        """iterate .md data line by line, and create object for each viedo link

        :param state_content:       byte string
        :param state:
        :return:                    None
        """
        split_line = state_content.decode("utf-8").split("\n")
        data = dict()
        cp_data = dict()
        for line in split_line:
            line_elem = line.split(" ")
            line_elem = list(filter(None, line_elem))
            if line_elem:
                if line_elem[0] == Identifier.CITY:
                    del cp_data
                    cp_data = dict()
                    city = " ".join(line_elem[1:])
                    data["city"] = city.strip()
                elif line_elem[0] == Identifier.TITLE:
                    data["title"] = " ".join(line_elem[1:])
                elif line_elem[0] == Identifier.LINK and data:
                    data["link"] = line_elem[1]
                    data["state"] = state
                    cp_data = data.copy()
                    cp_data.pop("link")
                    if not VideoService.get_video(link=line_elem[1]):
                        VideoService.create_video(**data)
                    del data
                    data = dict()
                elif line_elem[0] == Identifier.LINK:
                    cp_data["link"] = line_elem[1]
                    if not VideoService.get_video(link=line_elem[1]):
                        VideoService.create_video(**cp_data)

    def main(self) -> None:
        """main
        """
        state_list = self.get_states_list()
        self.get_raw_content(state_list)
