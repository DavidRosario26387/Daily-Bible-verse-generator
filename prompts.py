import llm,get_reading
import json

PROMPT_SYMBOLIC = """
### System
You generate high-quality image prompts for Bible verse posters.

Return ONLY the final prompt. No explanations.

### Verse
{VERSE}

### Task
Create ONE clear, visually strong scene that represents the core meaning of the verse (symbolic or literal).

### Requirements
- Focus on ONE main subject (avoid clutter)
- Scene must be inspiring, peaceful or powerful
- Composition must include natural negative space (sky, light, wall, horizon) for text placement
- No text in image
- Do NOT mention Bible references or verse numbers in the prompt
- Avoid complex storytelling

### Output style (must follow)
- 2-4 sentences only
- First sentence = main scene
- Second = environment + mood
- Third = lighting + composition
- Optional fourth = artistic details

### Style suffix (append exactly)
ultra detailed, cinematic lighting, volumetric divine light rays, atmospheric haze, rich color depth, 9:16 portrait orientation, high dynamic range, photorealistic, masterpiece quality, Christian inspirational fine art
"""

PROMPT_BIBLE = """
You generate high-quality biblical image prompts.

Return ONLY the final prompt.

Verse:
{VERSE}

Task:
Create ONE clear scene from a real biblical moment that reflects the verse.

Rules:
- One subject, one action (no clutter)
- Historically accurate (ancient Israel / Roman era)
- No text in image
- Must include natural negative space (sky/light/background)

Structure (strict):
1. Subject + action
2. Environment + setting
3. Lighting + composition
4. Style + color + quality

Style constraints (append naturally, not as a list):
photorealistic, cinematic lighting, warm natural color palette, soft volumetric light, shallow depth of field, high dynamic range, ultra detailed, 9:16 vertical composition, clean framing, professional photography, masterpiece quality
"""


SHORTLIST_PROMPT = """
### Input
{JSON}

### Task
Select exactly ONE verse that is most inspiring and suitable for a poster. It shoudl also be short and accomodatable within an image, choose one inspiring, impactful verse from this.
Take only from reading 1, reading 2 or gospel no where else.
### Rules
- Only ONE verse
- Copy EXACT text
- No paraphrasing
- Prefer short, powerful, visually meaningful lines

### Output
{"reading":"exact verse text","verse":"Book Chapter:Verse"}

Return ONLY JSON.
"""

def return_verse():
    tmrw_reading=get_reading.get_tmrw_reading()
    final_prompt=SHORTLIST_PROMPT.replace("{JSON}",tmrw_reading)
    response = llm.call_llm(final_prompt, expect_json=True)
    data = json.loads(response)
    verse_text = data["reading"]
    verse_reference = data["verse"]
    return verse_text, verse_reference

def return_img_prompt1(verse):
    prompt1=PROMPT_BIBLE.replace("{VERSE}",verse)
    p1=llm.call_llm(prompt1)
    return p1

def return_img_prompt2(verse):
    prompt2=PROMPT_SYMBOLIC.replace("{VERSE}",verse)
    p2=llm.call_llm(prompt2)
    return p2