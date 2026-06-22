import pathlib

p = pathlib.Path("main.typ")
content = p.read_text(encoding="utf-8")

# Let's locate the sections
start_diyun = content.find("= דיון ומסקנות")
idx_curie = content.find("== מדידת טמפרטורת קירי")
idx_ratio = content.find("== ניתוח יחס ההשנאה והפרשי מופע (שאלות 8 ו-9)")
idx_coils = content.find("== השוואת פרמטרי הסליל המשני (השראות והתנגדות)")

if all(x != -1 for x in [start_diyun, idx_curie, idx_ratio, idx_coils]):
    # Extract Curie section
    curie_section = content[idx_curie:idx_ratio]
    # Extract Ratio section
    ratio_section = content[idx_ratio:idx_coils]
    
    # Reassemble with swapped order: Ratio first, then Curie
    new_content = (
        content[:start_diyun]
        + "= דיון ומסקנות\n"
        + ratio_section
        + curie_section
        + content[idx_coils:]
    )
    p.write_text(new_content, encoding="utf-8")
    print("Swapped sections successfully")
else:
    print("Failed to find section indices:", start_diyun, idx_curie, idx_ratio, idx_coils)
