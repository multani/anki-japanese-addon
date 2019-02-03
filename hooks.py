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
        value = note[field].strip()

        if field == self.f["japanese"] and value:
            jp = note[field]
            tr = self.content.translate(jp)

            note[self.f["romaji"]] = tr["romaji"]
            note[self.f["sense"]] = "<br>".join(tr["senses"])

            sound, format = self.content.speak(jp)
            if sound is not None:
                media_dir = mw.col.media.dir()
                filename = "{}.{}".format(jp, format)
                filepath = os.path.join(media_dir, filename)

                with open(filepath, "wb") as fp:
                    fp.write(sound.read())

                note[self.f["audio"]] = "[sound:{}]".format(filename)

            updated = True

        return updated
