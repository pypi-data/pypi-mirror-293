import os
from typing import List
from WMain.WBasic import get_timestamp10, get_timestamp13
from WMain.WRequests import WSession
from WMain.WAPI_CloudCode import api_cloudcode
from WMain.WUrl import WUrl
import re
from pprint import pprint


class BaiduNetdistF:

    def __init__(self, bd_file):
        self.bd_file = bd_file
        self.path = bd_file["path"]
        self.name = self.path.split("/")[-1]
        self.isdir = bool(bd_file["isdir"])
        if not self.isdir:
            self.size = bd_file["size"]
        else:
            self.size = 0
        self.fs_id = bd_file["fs_id"]

    def __repr__(self) -> str:
        return self.path

    def __str__(self) -> str:
        return self.path

    def __eq__(self, value) -> bool:
        if isinstance(value, BaiduNetdistF):
            return self.name == value.name
        elif isinstance(value, str):
            if value.startswith("/"):
                return self.path == value
            else:
                return self.name == value


class BaiduNetdisk:
    session: WSession = WSession()
    list_url: str = "https://pan.baidu.com/api/list"
    filemanager_url: str = "https://pan.baidu.com/api/filemanager"
    create_url: str = "https://pan.baidu.com/api/create"
    template_variable_url: str = "https://pan.baidu.com/api/gettemplatevariable"
    verify_url: str = "https://pan.baidu.com/share/verify"
    transfer_url: str = "https://pan.baidu.com/share/transfer"
    search_url: str = "https://pan.baidu.com/api/search"

    api_create_url_v2 = "https://pan.baidu.com/rest/2.0/doc/file"

    def __init__(self, cookie_file: str = None, session: WSession = WSession()):
        self.session = session
        if cookie_file is not None:
            self.session.load_cookie_editor(cookie_file)
        self.field = {"bdstoken": None, "token": None}  # 请求需要的域

    def init(self):
        params = {"fields": '["bdstoken","token"]'}
        dic = self.session.get(self.template_variable_url, params=params).resp.json()[
            "result"
        ]
        self.field["token"] = dic["token"]
        self.field["bdstoken"] = dic["bdstoken"]

    def list_iter(self, dir: str, page=1, page_num=1000) -> List[BaiduNetdistF]:
        resp = self.session.get(
            self.list_url, params={"dir": dir, "num": str(page_num), "page": str(page)}
        )
        return [BaiduNetdistF(dic) for dic in dict(resp.json())["list"]]

    def list_all(self, dir: str, page_num=1000) -> List[BaiduNetdistF]:
        r = []
        page = 1
        while 1:
            last_r_size = len(r)
            r += self.list_iter(dir, page, page_num)
            if len(r) - last_r_size < page_num:
                break
            page += 1
        return r

    def del_list(self, file_dir_list: List[str]) -> int:
        del_list_str = '["' + '","'.join(file_dir_list) + '"]'
        params = {
            "bdstoken": self.field["bdstoken"],
            "async": len(file_dir_list),
            "onnest": "fail",
            "opera": "delete",
        }
        data = {"filelist": del_list_str}
        resp = self.session.post(self.filemanager_url, params=params, data=data)
        errno = resp.json()["errno"]
        if errno == 0:
            return True
        else:
            return errno

    def exist(self, file_dir: str, isdir=True) -> bool:
        for file in self.list_all("/" + "/".join(file_dir.split("/")[:-1])):
            if isdir == file.isdir and file == file_dir:
                return True
        return False

    def create_dir(self, dir: str, rename=False):
        params = {"bdstoken": self.field["bdstoken"]}
        data = {"path": dir, "isdir": "1", "block_list": "[]"}
        if not rename and self.exist(dir, True):
            return "文件已存在, 无需创建"
        resp = self.session.post(self.create_url, params=params, data=data)
        if resp.json()["errno"] == 0:
            return True
        else:
            return resp.json()

    def search_iter(self, keyword: str, page=1, page_num=1000) -> List[BaiduNetdistF]:
        page = 1
        params = {
            "order": "time",
            "num": str(page_num),
            "page": str(page),
            "recursion": "1",
            "key": keyword,
        }
        resp = self.session.get(self.search_url, params=params)
        return [BaiduNetdistF(dic) for dic in resp.json()["list"]]

    def search_all(self, keyword: str, page_num=1000) -> List[BaiduNetdistF]:
        r = []
        page = 1
        while 1:
            last_r_size = len(r)
            r += self.search_iter(keyword, page, page_num)
            if len(r) - last_r_size < page_num:
                break
            page += 1
        return r

    def verify(self, verify_params, verify_data):
        count = 0
        while 1:
            # 开始请求安全api
            # 百度设计了防盗链, 必须有referer
            resp = self.session.post(
                self.verify_url, params=verify_params, data=verify_data
            )
            print(verify_data, verify_params, self.verify_url)
            error = resp.json()["errno"]
            if error == 0:
                return
            elif error == -62:
                captcha_url = self.session.get(
                    "https://pan.baidu.com/api/getcaptcha?prod=shareverify"
                ).json()["vcode_img"]
                vcode_str = captcha_url.split("?")[1]
                if count > 5:
                    return False
                vcode = api_cloudcode.Post4_by_bytes(
                    self.session.get(captcha_url).content
                )
                verify_params["t"] = get_timestamp10()
                verify_data["vcode"] = vcode
                verify_data["vcode_str"] = vcode_str
                count += 1
            else:
                return False

    def auto_save(self, url: str, dir="/auto_get", pwd="", verify=False):
        if not url.startswith("https://pan.baidu.com/s/"):
            return "百度网盘url格式错误"
        resp = self.session.get(url)
        self.session.ini.headers["Referer"] = url
        keyword_list = [
            "分享的文件已经被删除",
            "分享的文件已经被取消",
            "因为涉及侵权、色情、反动、低俗等信息，无法访问",
            "链接错误没找到文件",
            "分享文件已过期",
        ]
        for keyword in keyword_list:
            if keyword in resp.text:
                return keyword
        if verify:
            url = resp.url
            url_ = WUrl(url)
            url_params = url_.params
            surl = url_[1] if "surl" not in url_params else url_params["surl"][0]
            if "pwd" in url_params and pwd == "":
                pwd = url_params["pwd"]
            verify_params = {
                "t": get_timestamp10(),
                "surl": surl,
                "bdstoken": self.field["bdstoken"],
            }
            verify_data = {"pwd": pwd, "vcode": "", "vcode_str": ""}
            if not self.verify(verify_params, verify_data):
                return "安全验证失败"

        resp = self.session.get(url)
        resp.save_file("1.html")
        share_uk = re.findall('share_uk:"([0-9]*)"', resp.text)[0]
        share_id = re.findall('shareid:"([0-9]*)"', resp.text)[0]
        fs_id = re.findall('"fs_id":([0-9]*),', resp.text)[0]
        transfer_params = {"shareid": share_id, "from": share_uk, "ondup": "newcopy"}
        transfer_data = {
            "fsidlist": f"[{fs_id}]",
            "path": dir,
        }
        resp = self.session.post(
            self.transfer_url, params=transfer_params, data=transfer_data
        )
        if resp.json()["errno"] == 0:
            result = resp.json()["extra"]["list"][0]
            return f'成功保存到{result["to"]}'
        else:
            return resp.json()


# share_uk:"1100586214790", shareid:"41767244614"

# TEST
if __name__ == "__main__":
    bd = BaiduNetdisk()
    bd.session.ini.set_proxy(7890)
    bd.session.load_cookies_str(
        """PSINO=2;ndut_fmt=1D79F7C27C49DCC205F781D26ED0EF4018E6C6AEBB91193F1AD1918A0B4DF3B7;BAIDUID=75A0DD89BD02948B1C37518081671BE0:SL=0:NR=10:FG=1;BDUSS_BFESS=3ZCVHA3OUtlLTg2NUhEbVFXeDh2d215eW5Bb1ZSS0ZyMFl5M3A1Z3VPbG5sOVptRVFBQUFBJCQAAAAAAAAAAAEAAACuhdCQMTIzxOPU2jEyMTM4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGcKr2ZnCq9mU;PANWEB=1;ZFY=n9xe9UfztVCTxA26Pgteh1ogkCVtGZSdsi67:B1BOfN8:C;delPer=0;XFI=12af81bf-3f34-185d-d979-bde9f708c222;ab_sr=1.0.1_NTk5NTMwMDk3Yjc4MWM1MDE0ZThiMWI4NzkxMjdlNmQxMmZjZWVhZTBjZTQ3Y2UxNWU1NmViODZlNTM0YmQ4OGNkOTgzNzRmMjQwOGU5NmMyOGUyYWFhNGI3ZDY4ZTA1ZjUwNTA3OGY4OWNmZjNiOTNhZTNjOGM2YzZhOGI5YmFjODYzYTZiY2EzNWEwNzc4NDM4NmE0NjNiZjQ5MmRmZDA1MjkxN2Y2ZGNmN2IzOWNjMWJmMmViNGZjYWYwZDRm;BAIDUID_BFESS=75A0DD89BD02948B1C37518081671BE0:SL=0:NR=10:FG=1;STOKEN=73f4943decad772575b7682b374f47c697b991bbc6dec8e27d67eefdd9d8d857;SE_LAUNCH=5%3A1722839228_31%3A28713987;BA_HECTOR=alakah048485akak208l8l809kqs8f1jb0s5t1v;newlogin=1;BIDUPSID=47A4E231E0E46B43AEE15B88EB0AE823;BDCLND=fMDtlpMFKwKwVXQNYitwJuh7ziQmcg6uraZWOpbweqA%3D;BDORZ=AE84CDB3A529C0F8A2B9DCDD1D18B695;BDPASSGATE=IlPT2AEptyoA_yiU4SO_3lIN8eDEUsCD34OtVnti3ECGh67BmhH74bJDF680NyetByCd-YyfmqkCpjrFV6xjg0N_gRsUpiJS5Frkus3Ps2TqK2tk7r-kCbDJMyYUruDxkhUaz4wT_OVEVFoKewPJpuo4isOlre2Hah40skLrg_beZVmpBXb6r7WTX76fRHvYDsi1yujEaVJAVFeBUu4NKDTucloiPy1tx_7bi3Mq3Q45rkoUGv8dL3cA1G85Jppg0PmV1QC7zMGnDkscwnxzLl1ejSa85tD6Mk9d_KvxfMpGVdPeSsCDVDrXBL1vctD1Or2iTAWZmtkGDV9S98sUBph5HsPVCXTEYjUOLdOFvAGmGpM-ulOEIwDLtIMQO10H_QlcZq5CTyoFizOfqBm4gCjo_3T_i0FvM0wOCpePu8gvmHdWBpbht57jc7Jv-p_fT7afE5XiGa4l3G2s-37DDb44K_r82VEbqUuloizSjSr9DwrTWPwJcy-77WxmTWiB9QePNo3XK3O2nr64tQHV84uz-oSUqzaZwyqfRNWpTx9DN-9zobBoInHWvYvtzHx_O4GdvI4n_VDDnD2L81uwpzB9a4A01NJKOtD0JPITwc_IopwyXC9to_Sz3wFfZ7nDv3ltB_qcX8D6GEnfSFFmpbl0ZDLmHJTzvtLgETVYEVCX0lTBBqhiw8NV5oEqPebbPDDFg3Q0PjiopwkjNNWJgmB4AvgzEi25vXzJ3-8NCRnx7xJmwEg46g1r4o8TYv0XbpUwgBlCA5_S62PUCreFoI1OspfegRZzWq_IWF8zu579FugP-nnzEFyXiSrIuQtne-Uk;BDUSS=3ZCVHA3OUtlLTg2NUhEbVFXeDh2d215eW5Bb1ZSS0ZyMFl5M3A1Z3VPbG5sOVptRVFBQUFBJCQAAAAAAAAAAAEAAACuhdCQMTIzxOPU2jEyMTM4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGcKr2ZnCq9mU;csrfToken=6slLRiu9BlVDiCkYPHr6PtHe;H_PS_PSSID=60272_60359_60470_60491_60498_60515_60526_60568;H_WISE_SIDS=110085_299594_603327_298696_301025_607111_307087_277936_610004_610437_609499_612162_612273_611188_613052_613178_613335_612824_613596_613585_612042_613729_613842_613794_614178_614268_613974_612558_614441_614465_614471_609580_610630_612917_614558_614574_614666_614690_614686_614716_614719_614694_309908_614849_614837_614886_614910_614875_614891_614906_614956_615156_615142_615164_615136_613118_614205_613688_615092_615215_615213_615075_613395_614508_615335_615259;H_WISE_SIDS_BFESS=110085_299594_603327_298696_301025_607111_307087_277936_610004_610437_609499_612162_612273_611188_613052_613178_613335_612824_613596_613585_612042_613729_613842_613794_614178_614268_613974_612558_614441_614465_614471_609580_610630_612917_614558_614574_614666_614690_614686_614716_614719_614694_309908_614849_614837_614886_614910_614875_614891_614906_614956_615156_615142_615164_615136_613118_614205_613688_615092_615215_615213_615075_613395_614508_615335_615259;Hm_lvt_95fc87a381fad8fcb37d76ac51fefcea=1717670376;PANPSC=10018276940153916359%3ACU2JWesajwByPfGOomAcr8Wn1hbHg1WZbtDq%2BK%2BOodwOYC6rNtBREiQxbl68m9lcBm6rqQ5QdYLyWDVSifoxLPcv5Xx7XQ9zwhRIQmAoMSKHkrigi2TxuAjHRUw%2FZR6kLvxjdeGWe15rqCNYc2LuOFCHZGOaQdgCY8uG8AM%2BY0Ih6uZoP3DwQ7BnXFvU9LYk9FYxwFKTFsLxviQE%2FB0jTjCo8bcT1HMK;PSCBD=31%3A1;PSTM=1709211960;XFCS=9E78B2F7F2B8D703AC9D1BA138107C0451D4DFB1E03D4BEC6176004D2B74E949;XFT=8eMvuXPrK1hi1Of2cr1z/IOLSvJKF2F3oJJyD6xU8h4="""
    )

    bd.init()
    pprint(bd.list_all("/"))
    pprint(bd.create_dir("/我的资源"))
    # pprint(
    #     bd.auto_save(
    #         "https://pan.baidu.com/s/1gtgxD8FlQ26JEGjmBORnfg?pwd=m9vd", "/auto_get"
    #     )
    # )
    # search_res = bd.search_all("你好")
    # pprint(search_res.__len__())
    # pprint(search_res[:5])
