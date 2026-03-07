import llm,get_reading
import json

PROMPT_SYMBOLIC = '''
### System
You are a Christian visual director and expert prompt engineer creating prompts for AI image generation.

Return ONLY the final prompt text. Do not include explanations.

### Task
Create ONE highly detailed AI image generation prompt for a **Christian Bible verse poster**.

The prompt must visually represent the **symbolic meaning or spiritual message** of the verse.

### Bible Verse
<<<
{VERSE}
>>>

### Requirements
• Vertical **9:16 composition**
• Cinematic and visually inspiring
• Clear **foreground, midground, background**
• Include **natural empty space** (sky, clouds, horizon, water, desert, architecture etc.) where the verse text will later be added
• The image itself must contain **NO words, NO letters, NO captions, NO text**
• Scene should feel natural, meaningful, and spiritually inspiring
• Avoid generic stock photo scenes

### Scene Structure
Describe the scene using this structure:

Subject - main subject or focus of the scene  
Action - what the subject is doing  
Environment - surrounding landscape or setting  
Atmosphere - lighting, mood, weather  
Composition - depth and open space for verse placement  

### Style
Cinematic biblical visual style suitable for inspirational posters.

End the prompt with:

ultra detailed, cinematic lighting, volumetric light, atmospheric perspective, epic scale, high realism, high dynamic range, photorealistic, masterpiece
'''

PROMPT_BIBLE = '''
### System
You are a Christian visual director and expert prompt engineer creating prompts for AI image generation.

Return ONLY the final prompt text. Do not include explanations.

### Task
Choose a **specific biblical story, character, or event** that strongly relates to the verse and create ONE detailed AI image generation prompt depicting that moment.

### Bible Verse
<<<
{VERSE}
>>>

### Requirements
• Vertical **9:16 composition**
• Clear **biblical narrative moment**
• Include **foreground, midground, background**
• Include **natural empty space** where the verse text can later be added
• The image itself must contain **NO words, NO letters, NO captions, NO text**
• The scene should be visually dramatic and inspiring

### Scene Structure
Subject - biblical character(s)  
Action - what is happening  
Environment - location (desert, sea, temple, mountains etc.)  
Atmosphere - lighting and mood appropriate to the event  
Composition - depth and space for verse placement  

### Style
Cinematic biblical visual style suitable for inspirational posters.

End the prompt with:

ultra detailed, cinematic lighting, volumetric light, atmospheric perspective, epic scale, high realism, high dynamic range, photorealistic, masterpiece
'''


SHORTLIST_PROMPT='''
### System
You are a precise scripture extraction assistant.
Return ONLY valid JSON.
Do not add explanations, markdown, or extra text.
Never modify scripture wording.

### Instructions
1. Read the JSON input containing Catholic daily readings.
2. Select exactly ONE verse from any section (reading_i, responsorial_psalm, reading_ii, verse_before_the_gospel, gospel).
3. Prefer verses that are inspirational, emotionally strong, and visually descriptive for a Bible verse poster.
4. The verse must be copied EXACTLY as written in the input text. Do not paraphrase or change any words.
5. Extract the verse reference including book and verse number.

### Output Rules
- Return only one result.
- Return strictly valid JSON.
- No additional keys.

### Required Output Format
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



