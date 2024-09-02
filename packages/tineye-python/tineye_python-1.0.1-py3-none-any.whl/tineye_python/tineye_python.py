import requests
import json
import os

class TinEyeAPIRequest:
    def __init__(self, api_url='https://tineye.com/api/v1/result_json/', api_key=''):
        self.api_url = api_url
        self.api_key = api_key

    def search_data(self, image, offset=0, limit=100, sort='score', order='desc', save_to_file=None, **kwargs):
        headers = {
            "host": "tineye.com",
            "connection": "keep-alive",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "accept": "application/json, text/plain, */*",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "origin": "https://tineye.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://tineye.com/search",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9"
        }

        if image.startswith('http://') or image.startswith('https://'):
            boundary = "----WebKitFormBoundaryA6RKEYWOfKJIfYaK"
            payload = f"--{boundary}\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n{image}\r\n--{boundary}--\r\n"
            headers["content-type"] = f"multipart/form-data; boundary={boundary}"
            response = requests.post(self.api_url, data=payload, headers=headers)
        else:
            files = {
                "image": open(image, "rb")
            }
            response = requests.post(self.api_url, files=files, headers=headers)

        json_response = self._parse_response(response.json())

        if save_to_file:
            with open(save_to_file, 'w') as f:
                json.dump(json.loads(json_response), f, indent=4)
            print(f"JSON output saved to {save_to_file}")
        else:
            print(json_response)

    def _parse_response(self, data):
        response = {
            "matches": [],
            "stats": {}
        }
        if 'matches' in data:
            for match in data["matches"]:
                response["matches"].append({
                    "image_url": match["image_url"],
                    "domain": match["domain"],
                    "score": match["score"],
                    "width": match["width"],
                    "height": match["height"],
                    "size": match["size"],
                    "format": match["format"],
                    "filesize": match["filesize"],
                    "overlay": match["overlay"],
                    "backlinks": self._parse_backlinks(match["backlinks"]),
                    "tags": match.get("tags", [])
                })
        if 'stats' in data:
            response["stats"] = {
                "num_matches": data["num_matches"],
                "num_filtered_matches": data["num_filtered_matches"],
                "num_collection_matches": data["num_collection_matches"],
                "num_stock_matches": data["num_stock_matches"],
                "num_unavailable_matches": data["num_unavailable_matches"],
                "str_num_matches": data["str_num_matches"],
                "str_search_time": data["str_search_time"],
                "query_source": data["query_source"]
            }
        return json.dumps(response, indent=4)

    def _parse_backlinks(self, backlinks):
        parsed_backlinks = []
        for backlink in backlinks:
            parsed_backlinks.append({
                "url": backlink["url"],
                "backlink": backlink["backlink"],
                "crawl_date": backlink["crawl_date"],
                "source_id": backlink["source_id"],
                "image_name": backlink["image_name"]
            })
        return parsed_backlinks
