import re
from pathlib import Path
from build_standalone_report import render_report
from docx import Document

def generate_dino():
    src_path = Path("Dino_Ballecer_Round_by_Round_Game_Preparation.md")
    dest_path = Path("Dino_Ballecer_Round_by_Round_Game_Preparation_R4-9.md")
    content = src_path.read_text(encoding="utf-8")
    
    # split before Round 1 and after Round 4
    parts = content.split("## Round 1 ")
    header = parts[0]
    
    body_parts = content.split("## Round 4 ")
    body = "## Round 4 " + body_parts[1]
    
    # Update title in header
    header = header.replace("# Dino Ballecer — Round-by-Round Game Preparation", "# Dino Ballecer — Round-by-Round Game Preparation (Rounds 4–9)")
    header = header.replace("covering all nine rounds, **22–27 June 2026**", "covering Rounds 4–9, **24–27 June 2026**")
    header = header.replace("It gives deep round-by-round preparation for Rounds 1–2 and 4–9. Round 3 (FM Arlan Cabe, a PHI compatriot) is deliberately kept to a brief public-file card under the shared-information integrity gate — not a preparation target.", "It gives deep round-by-round preparation for Rounds 4–9.")
    
    # Filter out R1, R2, R3 from dashboard table
    lines = header.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith("| R1 ·") or line.strip().startswith("| R2 ·") or line.strip().startswith("| R3 ·"):
            continue
        new_lines.append(line)
    header = "\n".join(new_lines)
    
    # Write to destination
    dest_path.write_text(header + "\n" + body, encoding="utf-8")
    print("Wrote", dest_path)

def generate_arlan():
    src_path = Path("Arlan_Cabe_Round_by_Round_Game_Preparation.md")
    dest_path = Path("Arlan_Cabe_Round_by_Round_Game_Preparation_R4-9.md")
    content = src_path.read_text(encoding="utf-8")
    
    # split before Round 1 and after Round 4
    parts = content.split("## Round 1 ")
    header = parts[0]
    
    body_parts = content.split("## Round 4 ")
    body = "## Round 4 " + body_parts[1]
    
    # Update title in header
    header = header.replace("# Arlan Cabe — Round-by-Round Game Preparation", "# Arlan Cabe — Round-by-Round Game Preparation (Rounds 4–9)")
    header = header.replace("covering all nine rounds, **22–27 June 2026**", "covering Rounds 4–9, **24–27 June 2026**")
    header = header.replace("It gives deep round-by-round preparation for Rounds 1–2 and 4–9. Round 3 (Dino Ballecer, a PHI compatriot who shares a coach) is deliberately kept to a brief public-file note under the shared-information integrity gate — not a preparation target, mirroring Dino's own playbook.", "It gives deep round-by-round preparation for Rounds 4–9.")
    
    # Filter out R1, R2, R3 from dashboard table
    lines = header.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith("| R1 ·") or line.strip().startswith("| R2 ·") or line.strip().startswith("| R3 ·"):
            continue
        new_lines.append(line)
    header = "\n".join(new_lines)
    
    # Write to destination
    dest_path.write_text(header + "\n" + body, encoding="utf-8")
    print("Wrote", dest_path)

def compile_docx(stem, title, break_before):
    source = Path(f"{stem}.md")
    output = Path(f"{stem}.docx")
    render_report(source, output, title)
    
    doc = Document(str(output))
    broken = []
    for par in doc.paragraphs:
        text = par.text.strip()
        style = par.style.name if par.style else ""
        if style.startswith(("Heading", "Title")) and any(text.startswith(b) for b in break_before):
            par.paragraph_format.page_break_before = True
            broken.append(text[:48])
    doc.save(str(output))
    print(f"saved -> {output.name}  (page breaks before {len(broken)} headings)")

if __name__ == "__main__":
    generate_dino()
    generate_arlan()
    
    break_before = (
        "Tournament-Wide Gates",
        "Systems Library",
        "Round 4", "Round 5", "Round 6", "Round 7", "Round 8", "Round 9",
        "Appendix",
    )
    compile_docx("Dino_Ballecer_Round_by_Round_Game_Preparation_R4-9", "Dino Ballecer — Round-by-Round Game Preparation (Rounds 4-9)", break_before)
    compile_docx("Arlan_Cabe_Round_by_Round_Game_Preparation_R4-9", "Arlan Cabe — Round-by-Round Game Preparation (Rounds 4-9)", break_before)
