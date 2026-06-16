# -*- coding: utf-8 -*-
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AUTO-GENERATED — do NOT edit manually.
# Edit RUN_013 - dungeon team.yaml and regenerate with:
#     from app.services.yaml_service import generate_py_from_yaml
#     generate_py_from_yaml(Path("RUNS/RUN_013 - dungeon team.yaml"))
# Generated: 2026-06-16 15:07:27
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_validator import validate_config_or_exit
from batch_transitions import run_batch_generation

# ============================================================
# PROJECT CONFIG
# ============================================================

PROJECT_FOLDER = 'C:\\Users\\abork\\AppData\\Local\\CapCut\\Videos\\dungeon_team\\film'

FORCE_RESOLUTION = (
    1024,
    1024,
)
DEFAULT_RESOLUTION = (
    1024,
    1024,
)

DEFAULT_BACKEND        = 'linux'
DEFAULT_FPS            = 16
DEFAULT_STEPS          = 6
DEFAULT_CFG            = 2
DEFAULT_DURATION       = 2
DEFAULT_BLOCKS_TO_SWAP      = 35
DEFAULT_FRAME_INTERPOLATION = True
DEFAULT_SEED           = None
SKIP_MISSING           = True
SKIP_EXISTED           = True
IMAGE_QUALITY          = 95
ASPECT_RATIO_TOLERANCE = 0.13
ASPECT_RATIO_STRATEGY  = 'most_common'
DEBUG_LOG              = True

POSTPROCESSING = {'enabled': False}

# ── Linux backend paths ─────────────────────────────────────────
CONFIG_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflow_configs\\wan_i2v.yaml'
WORKFLOWS_PATH = 'D:\\streamlit_project\\comfyui_integration\\workflows'
COMFYUI_OUTPUT_FOLDER = 'D:\\ComfyUI\\output\\Wan22_I2V'
API_URL = 'http://127.0.0.1:8189'

USE_TEST_FLOW = False

# ============================================================
# FLOW
# ============================================================

FLOW_FULL = [
    {
        'type': 'scene_break',
        'name': 'PREZENTACJA ZŁEJ KRÓLOWEJ',
    },
    {
        'file': 'zla krolowa.png',
        'backend': 'linux',
        'duration': 5.5,
        'pos': 'Smooth transition on evil queen face',
        'neg': 'NONE',
    },
    {
        'file': 'zla_krolowa_zoom.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'type': 'scene_break',
        'name': 'WKROCZENIE DO PODZIEMI',
    },
    {
        'file': 'Dungeon_entrance_large.png',
        'backend': 'linux',
        'duration': 5.5,
        'pos': 'Sorceress slowly approaches the dungeon entrance',
        'neg': 'NONE',
    },
    {
        'file': 'Dungeon_entrance_small.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'type': 'scene_break',
        'name': 'WALKA Z POTWORAMI',
    },
    {
        'file': 'redwarrior.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """2-second I2V: A fierce female warrior quickly rises from a kneeling position in a powerful upward motion. As she stands up, she swiftly reaches down, grabs the sword lying on the ground with her right hand and lifts it in one continuous, fluid and aggressive movement.

Dynamic, intense and heroic action, realistic physics, strong warrior energy, photorealistic, ultra detailed, cinematic.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'red warrior',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'wampirzyce.jpg',
        'backend': 'linux',
        'duration': 2.5,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """3-second cinematic I2V: Three beautiful, dangerously seductive vampire women stare straight into the camera with raw lust and hunger. They provocatively invite the viewer to approach them — slowly reaching out their hands, licking their lips, smiling with fangs visible, moving their bodies in a tempting, sexual way.

Intense eye contact, seductive body language, erotic and predatory atmosphere. Moody cinematic lighting with deep shadows and red accents, photorealistic, highly detailed.""",
                'neg': '',
            },
        ],
        "chain_prefix": 'Wampirzyce',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'undead.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Undead is approaching the camera waving his sword',
                'neg': '',
            },
        ],
        "chain_prefix": 'undead',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'dungeon_ghost.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Horror 3-second I2V: A vengeful spirit trapped in the painting suddenly comes alive and violently reaches out. It stretches both arms aggressively toward the camera, desperately trying to seize something in front of the painting. Pale, ghostly hands with long fingers clawing forward. Twisted, terrifying facial expression. Slow build-up followed by a fast, frightening lunge. Extremely creepy and tense atmosphere, photorealistic, high detail.',
                'neg': 'static ghost, no movement, arms not reaching, weak gesture, ghost staying inside painting, friendly ghost, bright lighting, no horror, deformed hands, extra limbs, bad anatomy, rubbery motion, blurry, low quality, cartoonish ghost, slow motion only, no lunge, changed pose',
            },
        ],
        "chain_prefix": 'duch nekromantki',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'monster_slaver.jpg',
        'backend': 'linux',
        'duration': 2.5,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Monster is trying to catch naked women next to him. Women are freezed with horror',
                'neg': '',
            },
        ],
        "chain_prefix": 'monster slaver',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'wladczyni ciemnych elfow.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Evil dark elf queen is casting a spell',
                'neg': '',
            },
        ],
        "chain_prefix": 'dark elf queen casting a spell',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'Diablo.png',
        'backend': 'linux',
        'duration': 3,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': 'Red diablo monster is pointing at camera. Demonic woman is touching his belly',
                'neg': '',
            },
        ],
        "chain_prefix": 'diablo',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'wiedzma.jpg',
        'backend': 'linux',
        'duration': 3.5,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Witch slowly raises both arms above her head, dark swirling mist expands and
flows outward around her body, she performs a dramatic magical incantation gesture""",
                'neg': 'static, frozen, no movement',
            },
            {
                'duration': 3,
                'pos': 'Which is casting spell, throwing hand towards camera and smiling cruelly',
                'neg': 'static, frozen, no movement',
            },
        ],
        "chain_prefix": 'wiedzma',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': '',
    },

    {"break": True},

    {
        'file': 'walka z wiedzma 1.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': '',
        'neg': '',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """Cinematic 4-second I2V video: A beautiful sorceress stands in a powerful pose and casts a strong spell. She raises her hands dramatically, magical energy swirls around her, and she releases the spell.

A bright white light suddenly explodes from her hands and body, rapidly expanding and growing in intensity. The light becomes stronger and stronger until it completely fills the entire screen with blinding pure white light by the end of the clip.

Elegant and intense spellcasting motion, glowing magical particles, dramatic light burst, smooth transition from normal lighting to full white screen. Photorealistic, highly detailed, cinematic atmosphere, 4K.""",
                'neg': 'weak light, small light burst, colored light, blue light, golden light, slow light growth, partial white screen, still image at the end, dark screen, no light explosion, bad magic effect, low quality particles, deformed hands, blurry, artifacts, cartoonish, sudden cut, minimal light change',
            },
        ],
        "chain_prefix": 'walka z wiedzma 1',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'walka z wiedzma 2.jpg',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 4,
                'pos': """4-second cinematic I2V: A sorceress is violently hit by a powerful white magic orb in the chest. A massive blinding white flash erupts on impact. Her body starts cracking with glowing lines, then dramatically disintegrates and dissolves into sparkling white particles and light energy. She fades away completely with a look of shock and agony until nothing remains.

Intense magical attack effect, powerful light explosion, smooth disintegration, photorealistic, high emotional impact.""",
                'neg': 'no reaction, survives the hit, minimal light, weak explosion, woman stays intact, bad disintegration, deformed body, low quality particles, sudden cut, no pain, static pose, rubbery motion, blurry, artifacts, cartoonish effect, woman flies away, blood, gore',
            },
            {
                'duration': 3,
                'pos': """3-second cinematic I2V: A sorceress is hit by a devastating spell and violently disintegrates. Her body cracks and explodes into countless glowing fragments. The destruction is fast, brutal and spectacular — limbs and torso break apart, skin and clothes tear away as she collapses inward and dissolves into swirling particles and bright energy dust.

Dynamic, chaotic disintegration in the center of the frame. She completely vanishes by the end, leaving only faint glowing particles. Intense magical destruction, high motion, photorealistic, high detail.""",
                'neg': 'woman flies away, woman runs, woman falls down, body stays intact, survives the spell, minimal destruction, slow disintegration, low detail particles, bad physics, deformed body, cartoonish explosion, leaves the frame, static pose, no destruction, weak effect',
            },
        ],
        "chain_prefix": 'walka z wiedzma 2',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'ZDOBYCIE ARTEFAKTU',
    },
    {
        'file': 'zdobycie artefaktu_1.jpg',
        'backend': 'linux',
        'duration': 3,
        'pos': """Cinematic 3-4 second I2V2I video:

Start frame (Image 1): Empty mysterious chamber with an old wooden doorway on the right side of the frame. The door is slightly open, no one is visible.

A beautiful sorceress slowly and cautiously enters the chamber from the right through the doorway. She steps carefully into the room, moving from the right edge toward the center with alert, graceful steps. She holds her staff ready, head slightly turned, scanning the surroundings with caution.

End frame (Image 2): The sorceress is already inside the chamber, standing in a cautious pose, looking around.

Smooth, tense and atmospheric entrance. Natural, realistic movement with high caution, dark fantasy atmosphere, dramatic cinematic lighting, photorealistic, highly detailed, 4K.""",
        'neg': 'static camera, no entrance, sorceress not entering, already in the room at start, sudden appearance, teleport effect, fast running, jerky animation, bad walking, stiff movement, no caution, overconfident pose, bad anatomy, extra limbs, deformed hands, staff floating, changed pose during movement, wrong door, empty room at the end, low detail, blurry, artifacts, rubbery motion, cartoonish, plastic skin, overexposed, underexposed, different clothing, changed hair, looking directly at camera',
    },
    {
        'file': 'zdobycie artefaktu_2.jpg',
        'backend': 'linux',
        'duration': 4.5,
        'pos': """Cinematic 4.5-second I2V2I video continuation: The sorceress is already standing inside the mysterious chamber. She slowly and cautiously walks forward, moving from the mid-ground closer toward the center of the room, with elegant but alert steps.

As she approaches, a magical staff lying on a stone pedestal begins to levitate slowly. The staff rises into the air, glowing with bright cyan and golden magical energy, surrounded by swirling sparkling particles and ethereal light trails. The staff then gracefully flies toward the sorceress and smoothly lands in her outstretched right hand.

Strong emphasis on beautiful, visible magic effects — glowing runes, floating particles, energy streams. The sorceress maintains a focused, slightly surprised yet powerful expression while accepting the staff. Dark fantasy atmosphere, dramatic cinematic lighting, photorealistic, ultra detailed, 4K.""",
        'neg': 'static scene, no movement, sorceress not walking, staff not levitating, no magic effects, sudden staff appearance, bad levitation, staff teleporting, weak magic, low detail magic, deformed staff, jerky motion, rubbery movement, bad hand catch, changed pose, looking at camera, fast movement, running, low quality, artifacts, blurry particles, cartoonish magic, bright lighting, changed clothing',
    },
    {
        'file': 'zdobycie artefaktu_3.jpg',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'type': 'scene_break',
        'name': 'CZARODZIEJKA RZUCA CZAR TAŃCA',
    },
    {
        'file': 'czarodziejka.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """Cinematic 4-5 second I2V2I video: A beautiful sorceress stands in the exact same elegant pose as in the reference images. Her magical clothing and staff slowly and sensually disappear in a magical way.

The elegant robes and fabric gradually dissolve into glowing sparkling particles and soft light, vanishing piece by piece from her body. Her staff also fades away with magical effects. The disappearance is graceful, smooth and highly seductive.

At the end she stands completely naked in the exact same pose, with nothing on her body. Mesmerizing magical transformation, beautiful glowing particles, soft cinematic lighting, sensual atmosphere, photorealistic, ultra detailed, 4K.""",
        'neg': 'clothing remains, partial nudity, censored, underwear stays, staff remains, sudden disappearance, bad transition, deformed body, extra limbs, blurry, low quality, artifacts, rubbery motion, changed pose, different body, modest clothing, fast transition, cartoonish particles',
    },
    {
        'file': 'naga.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 4,
                'pos': 'Sorceress is leaving dungeon to the entrance in full sun',
                'neg': '',
            },
        ],
        "chain_prefix": 'taniec',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'type': 'scene_break',
        'name': 'CZARODZIEJKA ODCZAROWUJE KRAINĘ',
    },
    {
        'file': 'zamek.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec zamek',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'las.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec las',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'wioska.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec wioska',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'prisoners.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec prisoners',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'city.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec zamek_kopia',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'roadtonowhere.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec roadtonowhere',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'farmers.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec farmers',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'barracks.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec barracks',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'pustynia.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec pustynia',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'fullsun.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec fullsun',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'fullmoon.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec fullmoon',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'vallley.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec valley',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'lake.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec lake',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'rain.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec rain',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'icyforrest.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec icyforrest',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'sky.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec sky',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'underground.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A beautiful sorceress performs a very sensual and hypnotic dance. She moves slowly and gracefully, arching her back, rolling her hips seductively, and sliding her hands over her body. Her movements are fluid, elegant and highly erotic — she caresses her curves, runs fingers through her hair, and looks at the camera with intense, seductive eye contact.

Magical glowing particles and soft light trails follow her movements. Mysterious and enchanting atmosphere, soft cinematic lighting, extremely sensual and feminine dance, photorealistic, ultra detailed, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
            {
                'duration': 3,
                'pos': """Cinematic 5-second I2V video: A seductive sorceress dances in a raw, provocative and highly erotic way. She moves with passion — intense hip swaying, body waves, slow sensual twerking motions, running her hands from her breasts down to her hips and thighs. She arches her back deeply, bites her lip, and gives the camera a dominant, lustful look.

Her dance is teasing and confident, full of sexual energy. Dramatic lighting, magical sparks and glowing effects around her, photorealistic, highly detailed, sensual atmosphere, 4K.""",
                'neg': 'static pose, minimal movement, stiff dance, awkward movement, bad anatomy, deformed body, extra limbs, mutated hands, blurry motion, low quality, artifacts, rubbery motion, jerky movement, unnatural bending, modest dance, shy pose, looking away from camera, closed body language, boring dance, no hip movement, no body waves, flat expression, censored, clothing on body, partial clothing, deformed breasts, plastic skin, cartoonish, overexposed, underexposed, bad lighting, changed background, low detail, poor anatomy, floating particles without reason',
            },
        ],
        "chain_prefix": 'taniec underground',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {
        'type': 'scene_break',
        'name': 'CZARODZIEJKA NA TRONIE',
    },
    {
        'file': 'as_a_qeen.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """Cinematic 4-second I2V video: A regal queen is sitting elegantly on an ornate throne. Suddenly, a magical transformation begins — her luxurious royal dress slowly and sensually dissolves into glowing golden particles and sparkling light. The fabric gracefully fades away piece by piece, revealing her naked body underneath.

She remains seated in the exact same elegant pose on the throne throughout the entire transformation — back straight, hands resting on the armrests, head held high with a majestic expression.

The magical undressing is beautiful, smooth and hypnotic, with shimmering particles and soft glowing effects. At the end she sits completely naked on the throne in the same regal pose. Luxurious, sensual and magical atmosphere, dramatic cinematic lighting, photorealistic, ultra detailed, 4K.""",
        'neg': 'clothing remains, partial clothing, sudden disappearance, bad transition, deformed body, changed pose, standing up, looking away, low quality magic, no particles, cartoonish effects, blurry, artifacts, rubbery motion, modest pose, censorship, extra limbs',
    },
    {
        'file': 'as a qeen naked.png',
        'backend': 'linux',
        'duration': 2,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        'type': 'scene_break',
        'name': 'ZŁA KRÓLOWA UKARANA',
    },
    {
        'file': 'zla krolowa sen 1.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I dream sequence: The evil queen sits regally on a luxurious golden throne in a royal chamber. Slowly and magically her royal dress dissolves into golden sparkling particles, leaving her completely naked. At the same time the environment around her transforms into a dark, cold dungeon. The golden throne gradually turns into a crude stone throne.

Dreamy, surreal and hypnotic transition with soft glowing particles and ethereal light. She remains seated in the exact same majestic pose. Moody, dark fantasy atmosphere, smooth surreal transformation, photorealistic, highly detailed.""",
        'neg': 'clothing remains, dress stays on body, partial clothing, sudden disappearance, no particles, no magic effects, weak dissolution, queen moving, changed pose, looking at camera, throne disappearing, fast undressing, bad anatomy, deformed body, extra limbs, blurry, low quality, artifacts, rubbery motion, cartoonish particles, bright lighting, no dream effect, static scene, no environmental change',
    },
    {
        'file': 'zla krolowa sen 2.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I dream sequence continuation: The completely naked queen remains seated in the exact same majestic pose on the throne.

The luxurious golden throne slowly and magically transforms into a crude, heavy stone throne. At the same time the surrounding environment changes from a dark dungeon corridor into a small, grim prison cell with stone walls, iron bars and chains. The camera continues a slow, subtle push-in, keeping focus on the queen sitting on the now stone throne.

Dreamy, surreal and unsettling transition with soft glowing particles, slight visual distortion and hazy atmosphere. Dark, oppressive and claustrophobic mood, cold lighting, photorealistic, highly detailed.""",
        'neg': 'static scene, no movement, throne stays golden, throne not changing, environment not changing, corridor remains, no cell transformation, queen moving or standing up, changed pose, sudden jump, no particles, weak transition, bad blending, deformed throne, unrealistic stone texture, bright lighting, no dream haze, sharp realistic scene, low detail transition, artifacts, blurry environment, inconsistent lighting',
    },
    {
        'file': 'zla krolowa sen 3.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I dream sequence: The completely naked queen sits motionless on the crude stone throne inside the dark prison cell, maintaining the exact same regal yet vulnerable pose.

Fresh, red-pink whip marks and welts slowly materialize on her skin. The marks appear gradually across her breasts, stomach, and thighs — delicate at first, then becoming more visible and pronounced. The flogging welts emerge as if being inflicted by an invisible force.

The scene is almost static with only very subtle dreamy movement. Soft blur, slight haze and ethereal dream-like distortion throughout the shot, creating an unsettling nightmare atmosphere. Cold, dim lighting, photorealistic skin details, highly emotional and disturbing, ultra detailed.""",
        'neg': 'sudden appearance of marks, violent movement, queen moving, changing pose, throne moving, new objects, bright lighting, no blur, sharp realistic scene, static without dream effect, cartoonish marks, bloody wounds, black bruises, deformed body, low quality, artifacts',
    },
    {
        'file': 'zla krolowa sen 4.png',
        'backend': 'linux',
        'duration': 2,
        'pos': """Cinematic 2-second I2V2I dream sequence finale: Everything in the nightmare begins to rapidly dissolve and disappear. The stone throne, the prison cell walls and the naked queen with whip marks all break apart into swirling dark particles, mist and shadows.

The scene quickly transitions into reality — the queen is now lying on the cold, dirty stone floor of the real dungeon cell. She lies curled on her side with eyes closed. At the very end of the clip she suddenly opens her eyes wide with a strong expression of shock, terror and disorientation, realizing it was only a nightmare.

Fast, chaotic and unsettling dream collapse, dramatic dissolution into darkness, realistic falling onto the floor, intense and frightening awakening moment, cold harsh lighting, photorealistic, highly detailed.""",
        'neg': 'slow dissolution, throne remains, cell remains, queen stays sitting, gradual slow change, calm awakening, no shock, no fear in eyes, bad falling physics, deformed body, changed pose too early, static final pose, low quality, artifacts, blurry, rubbery motion, no particles, weak transition',
    },
    {
        'file': 'zla_krolowa_sen_5.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {
        "chain": [
            {
                'duration': 3,
                'pos': """3-second cinematic I2V: A woman lying on her back suddenly wakes up. She abruptly opens her eyes wide and looks straight up at the camera with intense fear and shock. Her expression is full of terror — wide eyes, raised eyebrows, slightly open mouth, panicked breathing.

Strong emotional reaction, realistic eye movement, subtle body tension. Dark, dramatic lighting, unsettling atmosphere, photorealistic, ultra detailed facial emotions.""",
                'neg': 'closed eyes, slow blinking, calm expression, neutral face, sleepy, relaxed, smiling, looking away, bad eye direction, deformed face, blurry, low quality, artifacts, minimal movement, no fear, cartoonish, plastic skin',
            },
        ],
        "chain_prefix": 'przebudzenie',
        'backend': 'linux',
        'fps': 16,
        'steps': 6,
        'cfg': 2,
        'neg': 'static, frozen, no movement',
    },

    {"break": True},

    {
        'file': 'taniec_zlej_krolowej_1.png',
        'backend': 'linux',
        'duration': 5,
        'pos': """5-second erotic I2V2I: Naked woman dances seductively in a dark dungeon.

Start: back view.
She performs slow, sensual body rolls and hip movements, then gracefully turns to face the camera.

End: front view, standing with both hands raised high above her head, body fully exposed, intense seductive gaze.

Very sensual and provocative dance, smooth transitions, dramatic volumetric lighting, photorealistic, high detail.""",
        'neg': 'static scene, no movement, throne stays golden, throne not changing, environment not changing, corridor remains, no cell transformation, queen moving or standing up, changed pose, sudden jump, no particles, weak transition, bad blending, deformed throne, unrealistic stone texture, bright lighting, no dream haze, sharp realistic scene, low detail transition, artifacts, blurry environment, inconsistent lighting',
    },
    {
        'file': 'taniec_zlej_krolowej_2.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """3-second erotic I2V2I: Naked woman dances seductively in a dark dungeon. She starts on the left side of the frame and slowly moves to the right while dancing. Her movements are very sensual — deep hip rolls, body waves, back arching, caressing her skin.

She ends on the right side with both hands behind her head, posing provocatively. Slow, hypnotic and highly erotic dance, intense eye contact with camera, cinematic volumetric lighting, photorealistic.""",
        'neg': 'static pose, minimal movement, stiff dance, awkward motion, bad anatomy, deformed body, extra limbs, blurry, low quality, clothing on body, censored, jerky movement, rubbery motion, changed pose too fast, no hip movement, looking away, modest dance, poor lighting',
    },
    {
        'file': 'taniec_zlej_krolowej_3.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """4-second erotic I2V2I: Naked woman dances seductively in a dark dungeon.

Start: hands behind head, provocative pose on the left side.
She slowly moves closer to the camera while dancing with intense hip movements, back arching and sensual body waves.

End: Close medium shot (visible from knees up), standing with hands on hips, powerful and teasing stance, looking straight into the camera.

Slow, hypnotic and very erotic dance, cinematic volumetric lighting, photorealistic, high detail.""",
        'neg': 'static pose, minimal movement, stiff dance, bad anatomy, deformed body, extra limbs, blurry motion, low quality, jerky movement, rubbery motion, changed pose too fast, clothing, censored, looking away, modest pose, poor hip movement, bad framing, full body shot at the end, too far from camera',
    },
    {
        'file': 'taniec_zlej_krolowej_4.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """4-second erotic I2V2I: Naked woman dances seductively in a dark dungeon.

Start: standing frontally with hands on hips.
She performs slow, teasing hip movements and body waves, then gracefully turns and moves deeper into the dungeon while dancing.

End: kneeling in the background, back to the camera, in a sensual arched pose.

Smooth, highly provocative and feminine dance, intense sensuality, cinematic volumetric lighting, photorealistic.""",
        'neg': 'static pose, minimal movement, stiff dance, bad anatomy, deformed body, extra limbs, blurry motion, jerky movement, rubbery motion, clothing, censored, sudden turn, bad transition, changed pose too fast, low quality, artifacts, poor hip movement, looking at camera in end frame, wrong position',
    },
    {
        'file': 'taniec_zlej_krolowej_5.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

    {
        'file': 'taniec_zlej_krolowej_1_ultra.png',
        'backend': 'linux',
        'duration': 5,
        'pos': """5-second erotic I2V2I: Naked woman dances seductively in a dark dungeon.

Start: back view.
She performs slow, sensual body rolls and hip movements, then gracefully turns to face the camera.

End: front view, standing with both hands raised high above her head, body fully exposed, intense seductive gaze.

Very sensual and provocative dance, smooth transitions, dramatic volumetric lighting, photorealistic, high detail.""",
        'neg': 'static scene, no movement, throne stays golden, throne not changing, environment not changing, corridor remains, no cell transformation, queen moving or standing up, changed pose, sudden jump, no particles, weak transition, bad blending, deformed throne, unrealistic stone texture, bright lighting, no dream haze, sharp realistic scene, low detail transition, artifacts, blurry environment, inconsistent lighting',
    },
    {
        'file': 'taniec_zlej_krolowej_2_ultra.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """3-second erotic I2V2I: Naked woman dances seductively in a dark dungeon. She starts on the left side of the frame and slowly moves to the right while dancing. Her movements are very sensual — deep hip rolls, body waves, back arching, caressing her skin.

She ends on the right side with both hands behind her head, posing provocatively. Slow, hypnotic and highly erotic dance, intense eye contact with camera, cinematic volumetric lighting, photorealistic.""",
        'neg': 'static pose, minimal movement, stiff dance, awkward motion, bad anatomy, deformed body, extra limbs, blurry, low quality, clothing on body, censored, jerky movement, rubbery motion, changed pose too fast, no hip movement, looking away, modest dance, poor lighting',
    },
    {
        'file': 'taniec_zlej_krolowej_3_ultra.png',
        'backend': 'linux',
        'duration': 3,
        'pos': """4-second erotic I2V2I: Naked woman dances seductively in a dark dungeon.

Start: hands behind head, provocative pose on the left side.
She slowly moves closer to the camera while dancing with intense hip movements, back arching and sensual body waves.

End: Close medium shot (visible from knees up), standing with hands on hips, powerful and teasing stance, looking straight into the camera.

Slow, hypnotic and very erotic dance, cinematic volumetric lighting, photorealistic, high detail.""",
        'neg': 'static pose, minimal movement, stiff dance, bad anatomy, deformed body, extra limbs, blurry motion, low quality, jerky movement, rubbery motion, changed pose too fast, clothing, censored, looking away, modest pose, poor hip movement, bad framing, full body shot at the end, too far from camera',
    },
    {
        'file': 'taniec_zlej_krolowej_4_ultra.png',
        'backend': 'linux',
        'duration': 4,
        'pos': """4-second erotic I2V2I: Naked woman dances seductively in a dark dungeon.

Start: standing frontally with hands on hips.
She performs slow, teasing hip movements and body waves, then gracefully turns and moves deeper into the dungeon while dancing.

End: kneeling in the background, back to the camera, in a sensual arched pose.

Smooth, highly provocative and feminine dance, intense sensuality, cinematic volumetric lighting, photorealistic.""",
        'neg': 'static pose, minimal movement, stiff dance, bad anatomy, deformed body, extra limbs, blurry motion, jerky movement, rubbery motion, clothing, censored, sudden turn, bad transition, changed pose too fast, low quality, artifacts, poor hip movement, looking at camera in end frame, wrong position',
    },
    {
        'file': 'taniec_zlej_krolowej_5_ultra.png',
        'backend': 'linux',
        'duration': 0,
        'pos': 'NONE',
        'neg': 'NONE',
    },
    {"break": True},

]

FLOW = FLOW_FULL

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    config = validate_config_or_exit(globals())
    run_batch_generation(config)
