from modules.code_reader.code_reader import CodeReader


def main():
    code_reader = CodeReader("https://github.com/berdebotond/GoCineAPI")
    code = code_reader.get_code()
    code_summery = code_reader.get_code_summery()
    print(code)
    print(code_summery)


if __name__ == '__main__':
    main()