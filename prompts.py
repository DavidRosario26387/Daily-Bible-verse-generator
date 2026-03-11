import llm,get_reading
import json

PROMPT_SYMBOLIC = '''
### System
You are a prompt engineer for image generation, give one detailed prompt i should use for this verse.

Return ONLY the final image generation prompt. No preamble, no explanations, no section headers — output the prompt text directly.

### Bible Verse
<<<
{VERSE}
>>>

### Your Task

Generate a prompt that i can use to generate a visually stunning and accurate image that i can use for this verse above.
Identify one deep christian concept for this image and give a prompt explaining the image generation requirement in great detail.
Explain a good image that can be generated for this this verse and that i can use in poster card. The image should be motivating and inspiring for people who watch it.
It should include christian details, and be accurate according to scripture
remember image should not hallucinate, ensure you add that in the prompt, it should be accurate according to bible.

Mention everything and give a detailed prompt that i can use directly
Include everything like lighting, scene, background etc in the prompt and explain in great detail accordance to bible. Also allow some free space in that image where i can later add the verse
the free space can be given subtly as sky, ground, wall etc where i will add verse later. no text should be there in the image.


### Strict Constraints
NEVER hallucinate
No text allowed
Image should be accurate according to bible.

### Append this style suffix verbatim at the very end of your prompt
ultra detailed, cinematic lighting, volumetric divine light rays, atmospheric haze, rich color depth, 9:16 portrait orientation, high dynamic range, photorealistic, masterpiece quality, Christian inspirational fine art
'''

PROMPT_BIBLE = '''
### System
You are a prompt engineer for image generation, give one detailed prompt i should use for this verse.

Return ONLY the final image generation prompt. No preamble, no explanations, no section headers — output the prompt text directly.

### Bible Verse
<<<
{VERSE}
>>>

### Your Task

Identify one bible scenario that best suits this verse above, choose one moment, character, event, miracle, scenario or place that is most relevant for this verse
and generate a prompt that i can use to generate a good, visually stunning and inspiring image for this verse. The prompt should explain the image scenario in great detail.
No hallucination allowed, everything in that image should be accurate according to bible. Mention everything and give a detailed prompt that i can use directly
Include everything like lighting, scene, background etc in the prompt and explain in great detail accordance to bible. Also allow some free space in that image where i can later add the verse
the free space can be given subtly as sky, ground, wall etc where i will add verse later. no text should be there in the image.

### Strict Constraints
• ZERO hallucination — every named character, costume detail, location feature, prop, and visual element must be directly supported by scripture and verified biblical-historical scholarship; invent nothing
• Do NOT combine separate biblical stories
• The image must contain NO words, NO letters, NO text, NO captions whatsoever

### Append this style suffix verbatim at the very end of your prompt
ultra detailed, cinematic dramatic lighting, volumetric divine light rays, atmospheric haze, historically accurate biblical realism, 9:16 portrait orientation, epic compositional scale, high dynamic range, photorealistic, masterpiece quality, dramatically lit sacred narrative scene
'''


SHORTLIST_PROMPT='''
### Input
<<<
{JSON}
>>>
### System
You are a Bible verse selector, choose any one verse from this above bible readings for today.

### Task
From the Catholic daily readings provided above (which may include reading_i, responsorial_psalm, reading_ii, verse_before_the_gospel, and gospel), 
select **strictly one** verse that is most inspiring, touching or commonly used in verse cards, I want to make a verse card that has this words and share.
so choose one verse that moves people and has deep spiritual meaning from bible. choose only from the input given above.

### Rules
- Select **exactly one** verse — not a passage, not multiple sentences unless they form a single numbered verse
- Copy the verse text **exactly** as it appears in the input — do not paraphrase, summarize, or change any word
- Extract the verse reference in the format: Book Chapter:Verse (e.g., John 3:16)
- Return strictly valid JSON with no extra keys, no markdown fences, no explanation

### Output Format
{"reading":"exact verse text","verse":"Book Chapter:Verse"}

Return ONLY valid JSON. Do not add explanations, markdown, or extra text.

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
    prompt1=PROMPT_BIBLE.replace("{VERSE}",verse)
    p1=llm.call_llm(prompt1)
    return p1

def return_img_prompt2(verse):
    prompt2=PROMPT_SYMBOLIC.replace("{VERSE}",verse)
    p2=llm.call_llm(prompt2)
    return p2



