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
### System
You generate historically grounded Bible scene image prompts.

Return ONLY the final prompt. No explanations.

### Verse
{VERSE}

### Task
Choose ONE real biblical moment, character, or setting that directly matches the verse.

### Requirements
- Must be a real event/person/place from the Bible
- Do NOT mix multiple stories
- Keep scene simple and focused (1 main action)
- Clothing, environment and props must be historically plausible (ancient Israel / Roman era)
- No text in image
- Include natural empty space for verse placement

### Output style (must follow)
- 2-4 sentences only
- Sentence 1: main subject + action
- Sentence 2: environment + setting
- Sentence 3: lighting + composition
- Sentence 4 (optional): realism details

### Style suffix (append exactly)
ultra detailed, cinematic dramatic lighting, volumetric divine light rays, atmospheric haze, historically accurate biblical realism, 9:16 portrait orientation, epic compositional scale, high dynamic range, photorealistic, masterpiece quality, dramatically lit sacred narrative scene
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