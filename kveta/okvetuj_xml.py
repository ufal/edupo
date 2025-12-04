#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os
import sys
import json

from kveta import okvetuj

def local_name(tag):
    """Vrátí lokální jméno tagu bez namespace (např. '{ns}div2' -> 'div2')."""
    return tag.rsplit('}', 1)[-1] if '}' in tag else tag

def remove_elements(root, names):
    for parent in list(root.iter()):
        for child in list(parent):
            if local_name(child.tag) in names:
                # preserve tail text
                if child.tail:
                    # append it after the removed node
                    idx = list(parent).index(child)
                    if idx > 0:
                        # merge tail with previous sibling's tail
                        prev = list(parent)[idx - 1]
                        prev.tail = (prev.tail or "") + child.tail
                    else:
                        # merge with parent's text
                        parent.text = (parent.text or "") + child.tail
                parent.remove(child)

def collect_and_remove_headPoems(div2):
    """
    Najde všechny headPoem elementy uvnitř div2, sbírá jejich text (itertext),
    pak je odstraní z div2. Vrátí spojený text headPoem (nebo None).
    """
    #poems = []
    ## Najdeme všechny headPoem prvky (může jich být více)
    #for hp in [e for e in div2.iter() if local_name(e.tag) == "headPoem"]:
    #    poems.append(''.join(hp.itertext()).strip())
    #    # najít rodiče a odstranit hp
    #    # rodiče můžeme najít iterací přes elementy a kontrolou jejich přímých dětí
    #    for parent in div2.iter():
    #        if hp in list(parent):
    #            #parent.remove(hp)
    #            break
    #if poems:
    #    return "\n\n".join(poems)
    #return None

    head_poem = div2.find(".//headPoem")
    if head_poem is None:
        head_poem = div2.find(".//headPoemAdd")
    if head_poem is None:
        head_poem = div2.find(".//headPoemIncAdd")
    head_poem_text = None

    if head_poem is not None:
        head_poem_text = "".join(head_poem.itertext()).strip()
        for parent in div2.iter():
            children = list(parent)
            for i, child in enumerate(children):
                if child is head_poem:
                    # Preserve tail text by attaching it to the previous sibling or parent
                    if head_poem.tail:
                        if i > 0:
                            # Attach tail to previous sibling
                            prev = children[i - 1]
                            prev.tail = (prev.tail or "") + head_poem.tail
                        else:
                            # No previous sibling — attach tail to parent text
                            parent.text = (parent.text or "") + head_poem.tail
                    # Remove element
                    parent.remove(head_poem)
                    break
    return head_poem_text

def extract_div2_text(xml_file, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # collect metadata
    metadata = dict()
    for tag in ("surname", "name", "date", "titleColl", "born", "died", "nomedeplume", "gender"):
        metadata[tag] = "".join(root.find(".//"+tag).itertext()).strip()
    identity = metadata["surname"]+", "+metadata["name"]
    p_author = {"identity": identity, "name": identity, "born": metadata["born"], "died": metadata["died"], "zena": None}
    if metadata["nomedeplume"]:
        p_author["name"] = metadata["nomedeplume"]
    if metadata["gender"] == "F":
        p_author["zena"] = "1"
    biblio = {"b_title": metadata["titleColl"], "p_title": "", "year": metadata["date"]}

    # Najdeme všechny div2 elementy (bez ohledu na namespace)
    div2_elements = [e for e in root.iter() if local_name(e.tag) == "div2"]
    total = len(div2_elements)
    digits = max(3, len(str(total)))  # minimálně 3 číslice pro hezké názvy (volitelné)

    for i, div2 in enumerate(div2_elements, start=1):
        # 1) vyjmout a uložit headPoem(y)
        head_poem_text = collect_and_remove_headPoems(div2)

        # 2) odstranit všechny bordely mimo verše (včetně obsahu)
        remove_elements(div2, {"pageNum", "pageNumAdd", "graphic", "list", "speaker", "stage", "datelinePoem", "datelinePoemAdd", "datelineChapter", "datelineChapterAdd", "headPoem", "headPoemAdd", "subheadPoem", "subheadPoemAdd", "headPoemIncAdd", "headChapter", "subheadChapter", "headChapterAdd", "subheadChapterAdd", "dedicationPoem", "dedicationChapter", "noteAuthor", "noteOther", "biblCit", "epigraph", "quiteEpi", "biblEpi"})

        # 3) z div2 získat text (itertext zachová obsah <foreign> i ostatní texty)
        main_text = ''.join(div2.itertext()).strip()

        # 4) okvetuj
        output, k = okvetuj(main_text)
        output[0]['p_author'] = p_author
        output[0]['biblio'] = biblio
        if head_poem_text:
            output[0]['biblio']['p_title'] = head_poem_text
        else:
            print("Warning: <headPoem> not found.", file=sys.stderr)

        # 5) uložit soubory
        idx_str = str(i).zfill(digits)
        json_path = os.path.join(output_dir, f"{idx_str}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            print(f"{idx_str}.json", file=sys.stderr)
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Použití: python extract_div2.py vstup.xml [output_dir]")
        sys.exit(1)
    xml_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) >= 3 else "output"
    extract_div2_text(xml_file, out_dir)



