class ICONS:
    def  __init__(self):
        self.icons = {
            "wait": "⌛",
            "success": "✅",
            "error": "❌",
            "info": "⎚-⎚",
            "warning": "https://th.bing.com/th/id/OIP.Fgxrs6VT6FPZP-HvmC9K-QHaHa?rs=1&pid=ImgDetMain",
            "loading": "https://i.pinimg.com/originals/7d/2b/9b/7d2b9b7c6e2e4e4a9e3f6d0b9e4c4a3b.gif",
            "manga": "🌸",
            "anime": "❟❛❟",
            "ban": "https://emojicombos.com/images/emoji/apple/128/1f6ab.png",
            "new": "🆕",
        }

    def get_icons(self, arg):
        return self.icons[arg]