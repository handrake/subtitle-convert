from copy import deepcopy
from pycaption.base import BaseWriter, CaptionNode
from datetime import timedelta
from lxml import etree

class TextWriter(BaseWriter):
    def write(self, captions):  # pylint: disable=arguments-differ
        transcripts = []

        for lang in captions.get_languages():
            lang_transcript = ""

            for caption in captions.get_captions(lang):
                lang_transcript = self._strip_text(caption.nodes, lang_transcript)
            transcripts.append(lang_transcript)

        return '\n'.join(transcripts)

    @staticmethod
    def _strip_text(nodes, lang_transcript):
        for node in nodes:
            if node.type_ == CaptionNode.TEXT:
                lang_transcript += node.content +"\n\n"
            elif node.type_ == CaptionNode.BREAK and lang_transcript[-1] == "\n":
                lang_transcript = lang_transcript[:-1]
        return lang_transcript

class AtsWriter(BaseWriter):
    def _format_timestamp(self, value):  # pylint: disable=no-self-use
        datetime_value = timedelta(milliseconds=(int(value / 1000)))

        str_value = ""
        if hasattr(datetime_value, "hours"):
            str_value += str(datetime_value.hours).zfill(2)
        if hasattr(datetime_value, "minutes"):
            str_value += str(datetime_value.minutes).zfill(2)
        if hasattr(datetime_value, "seconds"):
            str_value += str(datetime_value.seconds).zfill(2)
        if hasattr(datetime_value, "microseconds"):
            str_value += str(round(datetime_value.microseconds * 30.0 / 10**6)).zfill(2)
        else:
            str_value += "00"

        return str_value.lstrip("0")

    def _create_xml_header(self):  # pylint: disable=no-self-use
        base_xml = etree.Element("ISS")

        project_tree = etree.SubElement(base_xml, "Project")
        project_tree.set("Title", "프로젝트명")

        track_list = etree.SubElement(project_tree, "TrackList")

        track = etree.SubElement(track_list, "Track")
        track.set("Name", "기본 트랙")
        track.set("StyleName", "해설자")

        channel_define_list = etree.SubElement(track, "ChannelDefineList")

        channel_define = etree.SubElement(channel_define_list, "ChannelDefine")
        channel_define.set("Name", "기본 채널")
        channel_define.set("StyleName", "지명, 인명 자막")
        channel_define.set("Left", "10")
        channel_define.set("Top", "320")
        channel_define.set("Right", "710")
        channel_define.set("Bottom", "470")

        st_item_list = etree.SubElement(track, "StItemList")

        return base_xml, st_item_list, track

    def write(self, caption_set):  # pylint: disable=arguments-differ
        caption_set = deepcopy(caption_set)

        ats_captions = []

        base_xml, st_item_list, track = self._create_xml_header()

        for lang in caption_set.get_languages():
            ats_captions.extend(
                self._recreate_lang(caption_set.get_captions(lang))
            )

        for item in ats_captions:
            st_item_list.append(item)

        track.set("RowCount", str(len(ats_captions)*2))

        doc = etree.ElementTree(base_xml)

        return etree.tostring(doc, pretty_print=True, encoding='UTF-8',
                              xml_declaration=True, method='xml')

    def _build_st_item(self, row_count, start, text):
        item = etree.Element("StItem")
        item.set("Row", str(row_count))
        item.set("TC", self._format_timestamp(start))
        item.set("Memo", "")
        st_text_list = etree.SubElement(item, "StTextList")
        st_text = etree.SubElement(st_text_list, "StText")
        st_text.set("StyleName", "지명, 인명 자막")
        st_text.set("Mark", "")
        st_text.text = text
        return item

    def _recreate_lang(self, captions):
        ats_cells = []
        row_count = 0

        prev_caption = None

        for caption in captions:
            new_content = ''
            for node in caption.nodes:
                new_content = self._recreate_line(new_content, node)

            new_content = new_content.strip()
            while '\n\n' in new_content:
                new_content = new_content.replace('\n\n', '\n')

            new_content = '|'.join(map(str.strip, new_content.split('\n')))

            if prev_caption:
                print(caption.start - prev_caption.end, new_content)

            if prev_caption and caption.start - prev_caption.end > 336000:
                blank_item = self._build_st_item(row_count, prev_caption.end, "")
                ats_cells.append(blank_item)
                row_count += 1

            item = self._build_st_item(row_count, caption.start, new_content)
            ats_cells.append(item)

            prev_caption = caption
            row_count += 1

        return ats_cells

    def _recreate_line(self, ats, line):  # pylint: disable=no-self-use
        if line.type_ == CaptionNode.TEXT:
            return ats + '%s ' % line.content
        elif line.type_ == CaptionNode.BREAK:
            return ats + '\n'
        return ats
