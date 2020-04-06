def __init__(self, subtitle, encoding="UTF-8"):
        super().__init__()

        subtitlefile = QFile(subtitle)

        if not subtitlefile.open(QIODevice.ReadOnly | QIODevice.Text):
            return

        text = QTextStream(subtitlefile)
        text.setCodec(encoding)

        subtitletext = text.readAll()

        # ('sıra', 'saat', 'dakika', 'saniye', 'milisaniye', 'saat', 'dakika', 'saniye', 'milisaniye', 'birincisatır', 'ikincisatır')
        compile = re.compile(r"(\d.*)\n(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})\n(\W.*|\w.*)\n(\w*|\W*|\w.*|\W.*)\n")
        self.sublist = compile.findall(subtitletext) 