import llm,get_reading
import json

PROMPT_SYMBOLIC = '''
### System
You are a Christian visual director and expert prompt engineer creating prompts for AI image generation.

Return ONLY the final image generation prompt. Do not include explanations, preamble, or section headers.

### Task
Create ONE highly detailed AI image generation prompt that visually represents the **deep Christian spiritual meaning** behind the Bible verse below.

The image must be **about the verse** — capturing its theological and emotional depth through symbolic Christian visual storytelling.

### Bible Verse
<<<
{VERSE}
>>>

### Strict Rules
• Base the scene entirely on the verse — no invented theology or unscriptural imagery
• Strictly **never hallucinate** — every element must be consistent with Christian scripture and tradition
• The image itself must contain **NO words, NO letters, NO text, NO captions** whatsoever
• Leave a clearly visible **empty region** (either top, bottom, or a calm open area) so that verse text can be overlaid later — this empty space must be an intentional compositional choice, such as an open sky, still water surface, sunlit ground, or plain wall
• Vertical **9:16 portrait composition**
• Do NOT use generic stock-photo clichés

### Scene Requirements
• Subject: the central spiritual symbol or figure that embodies the verse's meaning
• Action: what is happening that reflects the verse
• Environment: a setting that deepens the verse's meaning (e.g., garden, mountaintop, sea, temple, wilderness)
• Atmosphere: lighting and mood that match the emotional tone of the verse (e.g., golden hour, divine rays, gentle mist)
• Composition: clear foreground, midground, and background; deliberate open/empty space for text placement

### Style
Cinematic biblical visual style, photorealistic, suitable for a Christian inspirational poster.

End your prompt with:
ultra detailed, cinematic lighting, volumetric light rays, atmospheric perspective, epic scale, high realism, high dynamic range, photorealistic, masterpiece
'''

PROMPT_BIBLE = '''
### System
You are a Christian visual director and expert prompt engineer creating prompts for AI image generation.

Return ONLY the final image generation prompt. Do not include explanations, preamble, or section headers.

### Task
First, identify ONE specific Bible topic — a character, story, concept, scenario, or event — that is **deeply and meaningfully related** to the verse below. Then create ONE detailed AI image generation prompt depicting that biblical moment or concept in a visually striking and spiritually accurate way.

### Bible Verse
<<<
{VERSE}
>>>

### Strict Rules
• The chosen biblical topic must have a genuine, deep connection to the verse's meaning — not superficial
• Strictly **never hallucinate** — every depicted element must be scripturally accurate and consistent with the Bible
• The image itself must contain **NO words, NO letters, NO text, NO captions** whatsoever
• Leave a clearly visible **empty region** (either top, bottom, or a calm open area) so that verse text can be overlaid later — this empty space must be an intentional compositional choice, such as an open sky, still water surface, sunlit ground, or plain wall
• Vertical **9:16 portrait composition**
• Do NOT depict scenes or details that contradict scripture

### Scene Requirements
• Subject: the biblical character(s) or central figure from the chosen story or event
• Action: the key dramatic or spiritual moment that echoes the verse's message
• Environment: the scripturally accurate location (desert, sea of Galilee, Jerusalem temple, Garden of Gethsemane, etc.)
• Atmosphere: lighting and mood true to the biblical narrative (divine radiance, solemn dusk, burning midday, etc.)
• Composition: clear foreground, midground, and background; deliberate open/empty space for text placement

### Style
Cinematic biblical visual style, photorealistic, dramatically lit, suitable for a Christian inspirational poster.

End your prompt with:
ultra detailed, cinematic lighting, volumetric light rays, atmospheric perspective, epic scale, high realism, high dynamic range, photorealistic, masterpiece
'''


SHORTLIST_PROMPT='''
### System
You are a precise scripture extraction assistant.
Return ONLY valid JSON. Do not add explanations, markdown, or extra text.
Never modify scripture wording — use the exact words from the input.

### Task
From the Catholic daily readings provided below (which may include reading_i, responsorial_psalm, reading_ii, verse_before_the_gospel, and gospel), select **strictly one** verse that is:
- The most touching and spiritually inspiring verse across all the readings
- Relatable, moving, and meaningful — something people commonly treasure or are deeply moved by
- A strong candidate for a Bible verse image (visually evocative, emotionally resonant)
- Usable on its own without needing surrounding context to be understood

### Rules
- Select **exactly one** verse — not a passage, not multiple sentences unless they form a single numbered verse
- Copy the verse text **exactly** as it appears in the input — do not paraphrase, summarize, or change any word
- Extract the verse reference in the format: Book Chapter:Verse (e.g., John 3:16)
- Return strictly valid JSON with no extra keys, no markdown fences, no explanation

### Output Format
{"reading":"exact verse text","verse":"Book Chapter:Verse"}

### Input
<<<
{JSON}
>>>

### Example Output
{"reading":"The LORD is my shepherd; there is nothing I shall want.","verse":"Psalm 23:1"}
'''

def return_verse():
    tmrw_reading=get_reading.get_tmrw_reading()
    final_prompt=SHORTLIST_PROMPT.replace("{JSON}",tmrw_reading)
    response = llm.call_llm(final_prompt, expect_json=True)
    data = json.loads(response)
    verse_text = data["reading"]
    verse_reference = data["verse"]
    return verse_text, verse_reference

def return_img_prompt1(verse):
    prompt1=PROMPT_SYMBOLIC.replace("{VERSE}",verse)
    p1=llm.call_llm(prompt1)
    return p1

def return_img_prompt2(verse):
    prompt2=PROMPT_BIBLE.replace("{VERSE}",verse)
    p2=llm.call_llm(prompt2)
    return p2



