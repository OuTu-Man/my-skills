import re


class Tools:
    @staticmethod
    def convert_text_from_dict(text: str, data: dict):
        """
        Replace all '<.*>' in text
        e.g submit_btn = "//button[.='<button_text>']", data = {"button_text": "Submit"}
        submit_btn = convert_text_from_dict(submit_btn, data)
        submit_btn = "//button[.='Submit']
        @param text: text need to convert
        @param data: a map store all possible values can be converted
        @return: converted text
        """
        r = re.compile("[<>]+").findall(text)
        if len(r) == 0:
            return text

        r = re.compile("(<.*?>)").findall(text)
        keys = data.keys()

        for v in r:
            key = v.replace("<", "").replace(">", "")
            if key in keys:
                after = str(data[key])
                text = text.replace(v, after)

        return text
