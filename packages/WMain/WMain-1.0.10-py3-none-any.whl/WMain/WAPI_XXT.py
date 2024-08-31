from WMain.WRequests import WSession
from WMain.WUrl import WUrl
from WMain.WFile import create_path
import re


class WAPI_XXT_Session:
    URL_API_COURSE_LIST_DATA = (
        "https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata"
    )

    URL_MAIN = "https://chaoxing.com"
    WURL_FILE_LIST = WUrl(
        "https://mooc2-ans.chaoxing.com/mooc2-ans/coursedata/stu-datalist"
    )
    WURL_API_FILE_DOWNLOAD = WUrl(
        "https://mooc2-ans.chaoxing.com/mooc2-ans/coursedata/batchDownload"
    )
    XPATH_TEACHER_NAME = '//*[@class="course-info"]/p[2]/@title'
    XPATH_CLASS_NAME = (
        '//*[@class="course-info"]//*[@class="course-name overHidden2"]/@title'
    )
    XPATH_CLAZZ_ID = '//*[@class="clazzId"]/@value'
    XPATH_COURSE_ID = '//*[@class="courseId"]/@value'
    XPATH_FILE_TITLE = '//*[@class="dataBody_td"]/@dataname'
    XPATH_FILE_DATA_ID = '//*[@class="dataBody_td"]/@id'
    XPATH_FILE_T = '//*[@class="dataBody_td"]/@t'
    XPATH_FILE_TYPE = '//*[@class="dataBody_td"]/@type'
    RE_FILE_PAGE_NUM = re.compile('id="totalPages" value="(.*?)"')
    FILE_TYPE_FLODER = "afolder"

    def __init__(self, session: WSession):
        self.session = session
        self.downloading_filename = ""

    def login_by_cookie_str(self, cookie_str: str):
        self.session.load_cookies_str(cookie_str)
        self.flush()

    def login_by_cookie_editor(self, file: str):
        self.session.load_cookie_editor(file)
        self.flush()

    def flush(self):
        self._flush_class_teacher_classId_courseId_list()

    def _flush_class_teacher_classId_courseId_list(self) -> dict:
        data = {
            "courseType": "1",
            "courseFolderId": "0",
            "query": "",
            "pageHeader": "-1",
            "superstarClass": "0",
        }
        resp = self.session.post(self.URL_API_COURSE_LIST_DATA, data=data)
        teacher_list = resp.xpath(self.XPATH_TEACHER_NAME)
        clazz_list = resp.xpath(self.XPATH_CLASS_NAME)
        clazz_id_list = resp.xpath(self.XPATH_CLAZZ_ID)
        course_id_list = resp.xpath(self.XPATH_COURSE_ID)
        self.class_to_teacher_clazzId_courseId = {}
        for i in zip(clazz_list, teacher_list, clazz_id_list, course_id_list):
            self.class_to_teacher_clazzId_courseId[i[0]] = [i[1], i[2], i[3]]

    def _get_page_file_list(self, page: int) -> list:
        self.WURL_FILE_LIST["pages"] = str(page)
        resp = self.session.get(self.WURL_FILE_LIST)
        file_title_list = resp.xpath(self.XPATH_FILE_TITLE)
        file_data_id_list = resp.xpath(self.XPATH_FILE_DATA_ID)
        file_type_list = resp.xpath(self.XPATH_FILE_TYPE)
        return list(zip(file_title_list, file_data_id_list, file_type_list))

    def _get_page_num(self) -> int:
        self.WURL_FILE_LIST["pages"] = 1
        return int(
            self.RE_FILE_PAGE_NUM.findall(self.session.get(self.WURL_FILE_LIST).text)[0]
        )

    def _get_file_list(self) -> list:
        file_list = []
        for i in range(self._get_page_num()):
            file_list += self._get_page_file_list(i + 1)
        return file_list

    def _set_file_courseId_clazzId(self, class_name: str):
        self.WURL_FILE_LIST.params.clear()
        self.WURL_FILE_LIST.params_to_params_str()
        v = self.class_to_teacher_clazzId_courseId[class_name]
        self.WURL_FILE_LIST["courseid"] = v[2]
        self.WURL_FILE_LIST["clazzid"] = v[1]

    def download_course_file(self, class_name: str, save_path: str, types: list = None):
        self._set_file_courseId_clazzId(class_name)
        self._download_file(self._get_file_list(), save_path, types)

    def _download_file(self, file_list: list, save_path: str, types: list = None):
        save_path = save_path.rstrip("/") + "/"
        create_path(save_path)
        for file_title, file_data_id, file_type in file_list:
            if file_type == self.FILE_TYPE_FLODER:
                _download_path = save_path + file_title + "/"
                self.WURL_FILE_LIST["dataName"] = file_title
                self.WURL_FILE_LIST["dataId"] = file_data_id
                self._download_file(self._get_file_list(), _download_path, types)
            else:
                if types and file_type not in types:
                    continue
                self.WURL_FILE_LIST["dataName"] = file_title
                self.WURL_FILE_LIST["dataId"] = file_data_id
                self.WURL_API_FILE_DOWNLOAD["classId"] = self.WURL_FILE_LIST["clazzid"]
                self.WURL_API_FILE_DOWNLOAD["courseId"] = self.WURL_FILE_LIST[
                    "courseid"
                ]
                self.WURL_API_FILE_DOWNLOAD["dataId"] = self.WURL_FILE_LIST["dataId"]
                download_url = self.session.get(self.WURL_API_FILE_DOWNLOAD).json()[0]
                self.session.ini.headers["Sec-Fetch-Dest"] = "iframe"
                self.session.ini.headers["Sec-Fetch-Site"] = "same-site"
                self.session.ini.headers["Referer"] = self.URL_MAIN
                self.downloading_filename = save_path + file_title
                self.session.get(download_url).save_file(save_path + file_title)
                self.downloading_filename = ""


if __name__ == "__main__":
    s = WSession()
    s.ini.set_proxy(20000)
    xxt = WAPI_XXT_Session(s)
    xxt.login_by_cookie_str(
        """
lv=1; fid=181; _uid=204966268; uf=b2d2c93beefa90dc09742b9df6b00323ca46a41f3cd71e603c5516fee57aa6d4de62abff77a1567e96e415d46f880f7dc49d67c0c30ca5047c5a963e85f1109920eb9746f35d3581ce71fc6e59483dd3f091be6a5a65c4a2a49575c1eeb375ca6e5797318c6b22bd; _d=1718339278472; UID=204966268; vc=3CF4AB941B07FA89650875E0FC5BE7E1; vc2=1EA3BE19493F146E5FC909F73B6F7CD4; vc3=KrzMc4Vwv0XJdHIVqAGPosXZ3RfreuvVPN6hoHSJ9awBPW8zhocdrubwPhCzttqWTwysvvGBXTNgkfmDtsmH5VYuM2EW%2BQn4pVbTraLwHww%2BiXCIgU9hMzrhcjSrCJhTSqUN1FhcR5DFJvz3eEXy72eGpCYRuDm50Edq2lgq12k%3D01a8bdb53d2443a3198a4d0f71192f41; cx_p_token=58b6a1b90684c7914368f3fbdc207ed5; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMDQ5NjYyNjgiLCJsb2dpblRpbWUiOjE3MTgzMzkyNzg0NzQsImV4cCI6MTcxODk0NDA3OH0.haenkRzjtOQJslBhIyEr7LCaYZq8D9u1rtbdHILzW2o; xxtenc=94d6652cc8d263012b3b4e2df8eb88dd; DSSTASH_LOG=C_38-UN_920-US_204966268-T_1718339278474; orgfid=43843; registerCode=00010048000100010018; createSiteSource=num3; wfwfid=181; workRoleBenchId=0; siteType=2; styleId=; spaceFidEnc=4027ADFFD9B03F5B10118A8EF09B58CD; jrose=0DC89CAE9FCE1A9900F7729428060FC4.ans; spaceFid=181; spaceRoleId=3; tl=1; _industry=5; 242285967cpi=214358913; 242285967ut=s; 242285967t=1718767682442; 242285967enc=59efd982a50d9928ce8c800cee60620a; source=num2; wfwEnc=3935AE32EECDA3A04179505AFEFBF13B"""
    )
    xxt.download_course_file("2024计算机控制系统", "./xxt/download", ["pdf", "ppt"])
