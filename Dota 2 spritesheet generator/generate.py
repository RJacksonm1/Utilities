import json
import time
import urllib2
import vdf

from PIL import Image

SPRITE_DESIRED_WIDTH = 16  # Pixels
SPRITE_DESIRED_HEIGHT = 16  # Pixels

ROW_LIMIT = 512 / SPRITE_DESIRED_WIDTH  # Integer value in pixels
_API_KEY = ""  # http://steamcommunity.com/dev/

GetHeroes = [{"name": "Blank", "id": 0}]  # Have the very first entry be blank.
GetHeroes.extend(json.loads(urllib2.urlopen("http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?key=%(key)s" % {"key": _API_KEY}).read())["result"]["heroes"])

parseHeroes = []
for x in xrange(0, len(GetHeroes)):
    found = False
    for item in GetHeroes:
        if item["id"] == x:
            parseHeroes.append(item)
            found = True
    if found == False:
        parseHeroes.append({"name": "FAILBOAT", "id": x})


mod_texture = vdf.loads(open("input/mod_textures.txt", "r").read().replace("TextureData", "\"TextureData\""))  # Case-specific hack due to vdf.py being more strongly syntax'd than Valve's own VDFs.
raw_spritesheet = Image.open("input/minimap_hero_sheet.png")

raw_sprite_data = {}

for entry in mod_texture["sprites/640_hud"]["TextureData"].iteritems():
    if entry[0][:16] == "minimap_heroicon":
        raw_sprite_data[entry[0]] = entry[1]

raw_sprites = {}

for data in raw_sprite_data.iteritems():
    raw_sprites[data[0][17:]] = raw_spritesheet.crop((data[1]["x"], data[1]["y"], data[1]["x"] + data[1]["width"], data[1]["y"] + data[1]["height"]))

output_image_width = ROW_LIMIT * SPRITE_DESIRED_WIDTH
output_image_height = ((len(parseHeroes) / ROW_LIMIT) * SPRITE_DESIRED_HEIGHT)
if len(parseHeroes) % ROW_LIMIT != 0:
    output_image_height += SPRITE_DESIRED_HEIGHT

output_image = Image.new("RGBA", (output_image_width, output_image_height))

last_x = 0
last_y = 0
for hero in parseHeroes:
    if hero["id"] == 0:
        output_image.paste(raw_sprites.get(hero["name"], Image.open("input/all_class.png")).resize((SPRITE_DESIRED_WIDTH, SPRITE_DESIRED_HEIGHT), Image.BILINEAR), (last_x, last_y))
    else:
        output_image.paste(raw_sprites.get(hero["name"], Image.open("input/default.png")).resize((SPRITE_DESIRED_WIDTH, SPRITE_DESIRED_HEIGHT), Image.BILINEAR), (last_x, last_y))
    last_x += SPRITE_DESIRED_WIDTH
    if last_x == ROW_LIMIT * SPRITE_DESIRED_WIDTH:
        last_x = 0
        last_y += SPRITE_DESIRED_HEIGHT

output_image.save("output/output_{}.png".format(time.mktime(time.gmtime())), "PNG")
print "Done"
