import os.path
from aqt import mw

class Editor:
    def __init__(self, config, content):
        self.content = content
        self.config = config

        self.f = config["note"]["fields"]

    def onFocusLost(self, updated, note, index):

        allFields = mw.col.models.fieldNames(note.model())
        field = allFields[index]

        # Value of the lost-focus field
        jp = note[field].strip()

        if field != self.f["japanese"] or not jp:
            return updated

        self.fillTranslation(note, jp)
        self.fillSound(note, jp)

        return True # updated

    def fillTranslation(self, note, jp):
        refs = ["romaji", "sense"]

        if all(note[self.f[ref]] != "" for ref in refs):
            return # Don't need to update

        try:
            tr = self.content.translate(jp)
        except Exception as exc:
            print("Unable to translate '{}': {}".format(jp, exc))
            return

        self.fill(note, "romaji", tr["romaji"])
        self.fill(note, "sense", "<br>".join(tr["senses"]))


    def fillSound(self, note, jp):
        refs = ["audio"]

        if all(note[self.f[ref]] != "" for ref in refs):
            return # Don't need to update

        try:
            sound, format = self.content.speak(jp)
        except Exception as exc:
            print("Unable to synthesize sound '{}': {}".format(jp, exc))
        else:
            media_dir = mw.col.media.dir()
            filename = "{}.{}".format(jp, format)
            filepath = os.path.join(media_dir, filename)

            with open(filepath, "wb") as fp:
                fp.write(sound.read())

            self.fill(note, "audio", "[sound:{}]".format(filename))

    def fill(self, note, field_ref, value):
        """Fill the specific field, referenced by its name, if it's empty"""

        field = self.f[field_ref]

        if note[field] == "":
            note[field] = value
