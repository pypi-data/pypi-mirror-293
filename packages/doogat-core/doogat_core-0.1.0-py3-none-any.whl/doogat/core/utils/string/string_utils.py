from inflection import camelize as infl_camelize


class StringUtils:
    @staticmethod
    def camelize(text: str) -> str:
        text = text.replace("-", "_")
        text = text.replace(" ", "_")

        return infl_camelize(text)
