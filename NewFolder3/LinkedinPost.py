import requests


class LinkedinPost:
    def __init__(self) -> None:
        pass
        access_token = "AQVu4b6yzTOgJPYc2AMbN7GvAsllXspThZh9_suAwuJ7Ri3Vh_dGr9xbcxeEDNTN3B7pKuiFoC1O4DJSU2xiY_YhYymumhOVDLqAAtLvkUEm7CZuGVt6Vq2tUcu4R28y1wGrRwK2NkK5IMdMBNvqm_xf2trnqRELn7fBkLDj0lox4Ov_w3VWHIM94mxlClf05lwXIACgf-5_n1Qc_uXJSB0_yW7GL7nKZGMWtjdLog8-M5UiYbCecCW6HCduOzucBg3ciVbSoyjvUa92z1LhDcXV2NIwyMbwKPTzruBoLbxQqP8m3K4WMKGNOVm2Gf59xZcSr_xjlO-wX78XpykkDrSj4lqZ_A"
        self.headers = {'Content-Type': 'application/json',
           'X-Restli-Protocol-Version': '2.0.0',
           'Authorization': 'Bearer ' + access_token}


    def geturn(self, headers):
        response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
        user_info = response.json()
        return user_info

    def post_lindedin(self, user_urn="urn:li:person:f0UuztlisG", message="", link="", link_text=""):
        headers = self.headers
        post_url = 'https://api.linkedin.com/v2/ugcPosts'
        post_data = {
        "author": user_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": message
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": message
                            },
                            "originalUrl": link,
                            "title": {
                                "text": link_text
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
            }
        }
        response = requests.post(url=post_url, headers=headers, json=post_data)
        print(response.json())

LinkedinPost().post_lindedin(message="Read the blogs #lastevents.space lastevents.space", link="https://www.lastevents.space/blog/read", link_text="")