# TODO: check if duplicate section names exist
def check_metadata():
    pass


def process_section(section, value):
    children = []
    images = []
    sections = {}
    for key in value.keys():
        if key == "images":
            images = value[key]
        else:
            children.append(key)
            s_sections = process_section(key, value[key])
            sections.update(s_sections)
            children.extend(s_sections[key]["children"])
            images.extend(s_sections[key]["images"])

    sections[section] = {"children": children, "images": images}
    return sections
