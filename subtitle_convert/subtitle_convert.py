from pycaption.base import BaseWriter, CaptionNode

class TextWriter(BaseWriter):
    def write(self, captions):
        transcripts = []

        for lang in captions.get_languages():
            lang_transcript = ""

            for caption in captions.get_captions(lang):
                lang_transcript = self._strip_text(caption.nodes, lang_transcript)
            transcripts.append(lang_transcript)

        return '\n'.join(transcripts)

    def _strip_text(self, nodes, lang_transcript):
        for node in nodes:
            if node.type_ == CaptionNode.TEXT:
                lang_transcript += node.content +"\n\n"
            elif node.type_ == CaptionNode.BREAK and lang_transcript[-1] == "\n":
                lang_transcript = lang_transcript[:-1]
        return lang_transcript
