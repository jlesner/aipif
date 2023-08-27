
import json
# from common.ContextAware import ContextAware

class WebApi():

    def sanitize(self, s):
        return s.translate(
            str.maketrans("'\"\\{}/", "      ")
        )


if __name__ == "__main__":
    wa = WebApi()
    test_string = "🌕🍒🦎🍓🚂🎷 This's a \"test\" with\\slashes.{}/"
    print(wa.sanitize(test_string)) 

