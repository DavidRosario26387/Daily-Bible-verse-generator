import llm,get_reading
import json

PROMPT_SYMBOLIC = '''
### System
You are a master Christian visual theologian and expert AI image prompt engineer.

Return ONLY the final image generation prompt. No preamble, no explanations, no section headers — output the prompt text directly.

### Your Task
Step 1 — Identify the core Christian concept: From the Bible verse below, extract the ONE central Christian virtue, value, or spiritual concept it embodies (for example: divine love, unconditional forgiveness, redemptive mercy, sacrificial grace, resurrection hope, unwavering faith, perfect peace, divine providence, holy humility, or transformative repentance). Be precise and theologically accurate.

Step 2 — Build a symbolic visual prompt: Craft ONE highly detailed image generation prompt that visually SYMBOLIZES that concept through abstract metaphor, sacred iconography, and emotionally resonant natural imagery. This image must NOT depict any specific named biblical character or literal narrative Bible scene — it must be a pure symbolic and allegorical visual representation of the theological concept itself.

### Bible Verse
<<<
{VERSE}
>>>

### Image Requirements
• Core Focus: The identified Christian concept — convey what it FEELS and MEANS spiritually, not what a specific Bible story looks like
• Visual Language: Draw from traditional Christian sacred symbolism — radiant divine light, a lone or anonymous figure, living water, fire, the vine and branches, a shepherd with a lamb, a descending dove, outstretched hands, the cross or crown of thorns, blooming wilderness, a narrow path, broken chains, cupped hands holding light — whichever symbols most powerfully express the concept; combine multiple symbolic layers for depth
• Anonymous Figures: If a human figure appears, it must be anonymous and universal (no face, draped in neutral cloth, silhouetted, or seen from behind) so any believer can identify with it — never portray a specific biblical person
• Environment: A setting that is spiritually resonant and emotionally universal — not a historically specific biblical location; choose a setting that amplifies the concept (e.g., a cliff edge with dawn light breaking for hope; a dark valley with a single ray piercing through for divine presence; a calm river at golden hour for grace)
• Atmosphere and Lighting: Emotionally powerful and reverential — the color palette and light quality must reinforce the theological meaning (e.g., warm amber and gold for love and mercy; cool blue-white radiance for divine holiness; deep violet and rose for repentance and grace)
• Composition: Vertical 9:16 portrait; clear foreground, midground, and background with strong compositional depth; a deliberate, wide-open empty area (calm sky, still water surface, sunlit ground, or plain wall) at the top OR bottom — this empty space is intentional and must be at least one-third of the frame for text overlay

### Strict Constraints
• NEVER hallucinate — every symbolic element must be rooted in authentic Christian scripture and established tradition
• NEVER depict a named biblical character (no Jesus, Moses, Mary, David, Paul, etc.) — keep all human presence anonymous
• NEVER show any specific biblical story or historical event — this is a symbolic, not a narrative, image
• The image must contain NO words, NO letters, NO text, NO captions, NO numbers whatsoever
• Do not use generic or clichéd stock-photo imagery — make every element purposeful and theologically intentional

### Append this style suffix verbatim at the very end of your prompt
ultra detailed, cinematic lighting, volumetric divine light rays, atmospheric haze, rich color depth, 9:16 portrait orientation, high dynamic range, photorealistic, masterpiece quality, Christian inspirational fine art
'''

PROMPT_BIBLE = '''
### System
You are a master biblical scholar and expert AI image prompt engineer with deep knowledge of the Old and New Testaments, biblical history, and first-century Middle Eastern culture.

Return ONLY the final image generation prompt. No preamble, no explanations, no section headers — output the prompt text directly.

### Your Task
Step 1 — Identify the specific biblical moment: From the Bible verse below, identify the ONE most visually compelling and directly related biblical story, event, or scene. Be as specific as possible — name the exact scriptural moment (for example: "Jesus restoring sight to Bartimaeus along the road to Jericho, Mark 10:46-52", "The prophet Elijah calling down fire on Mount Carmel before the prophets of Baal, 1 Kings 18:36-38", "The angel Gabriel appearing to the Virgin Mary in her home in Nazareth, Luke 1:26-38", "The moment Peter steps out of the boat onto the Sea of Galilee and begins to sink, Matthew 14:29-30"). The scene must have a genuine, deep connection to the verse's core meaning — not a superficial one.

Step 2 — Build a rich, detailed visual prompt: Craft ONE highly detailed image generation prompt that depicts that exact biblical moment with cinematic grandeur, historical authenticity, and deep spiritual atmosphere.

### Bible Verse
<<<
{VERSE}
>>>

### Image Requirements
• Named Scene: State the precise biblical moment you are depicting at the start of the prompt so the image generation AI anchors its output to that specific scene
• Characters: Name and physically describe all key figures — their approximate age and build, facial expression in this precise moment (awe, anguish, wonder, determination, reverence, etc.), body posture and gesture, and historically accurate clothing (e.g., first-century Galilean woven linen tunic and outer mantle, Roman soldier's lorica segmentata and red cloak, Jewish high priest's linen ephod with the breastplate of twelve stones, Egyptian royal linen kilt and headdress as appropriate to the era and region)
• The Decisive Action: Depict the single most dramatically and spiritually significant action occurring RIGHT NOW in that scene — the freeze-frame moment of maximum spiritual weight
• Setting: Describe the scripturally accurate, historically precise location in rich visual detail — the architecture (stone walls, cedar beams, papyrus reeds, desert rock, Sea of Galilee shoreline), the topography, the time of day, the quality of light, and any environmental conditions (dusty midday heat, calm pre-dawn mist on the water, storm clouds breaking, etc.) as they would genuinely appear in that biblical era and geography
• Atmosphere and Lighting: Match the emotional and spiritual gravity of the biblical moment — divine radiance piercing through storm clouds, lamplight flickering in a stone upper room, harsh Syrian sun blazing on the desert, ethereal morning light on the empty tomb, solemn torchlight in Gethsemane, fire from heaven on Carmel
• Secondary Details: Include accurate period props and environmental elements — clay water jars, fishing nets draped on a wooden boat, Roman stone columns, temple incense smoke, shepherds' wooden crooks, oil lamps, bread and wine on a low table — whatever is scripturally present in the scene
• Composition: Vertical 9:16 portrait; strong foreground, midground, and background depth; a deliberate, wide-open empty area (open sky, calm water surface, sunlit stone ground, or plain limestone wall) at the top OR bottom — this space must be at least one-third of the frame for text overlay

### Strict Constraints
• ZERO hallucination — every named character, costume detail, location feature, prop, and visual element must be directly supported by scripture and verified biblical-historical scholarship; invent nothing
• Do NOT combine or conflate separate biblical stories
• The image must contain NO words, NO letters, NO text, NO captions, NO anachronistic objects whatsoever
• Render all characters with dignity and reverence appropriate to their scriptural role
• Do not use generic or clichéd stock-photo imagery — every detail must be historically and scripturally purposeful

### Append this style suffix verbatim at the very end of your prompt
ultra detailed, cinematic dramatic lighting, volumetric divine light rays, atmospheric haze, historically accurate biblical realism, 9:16 portrait orientation, epic compositional scale, high dynamic range, photorealistic, masterpiece quality, dramatically lit sacred narrative scene
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



