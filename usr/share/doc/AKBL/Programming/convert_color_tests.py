

def hex_to_rgb(hex_string):
    """
        Convert hex color hex_strings to an RGB list.
        Ex:  `0000FF` to `[0, 0, 255]`
    """

    if hex_string.startswith('#'):
        hex_string = hex_string.lstrip('#')

    hex_lenght = len(hex_string)
    red, green, blue = tuple(int(hex_string[i:i + hex_lenght // 3], 16)
                             for i in range(0, hex_lenght, hex_lenght // 3))

    return [red, green, blue]



def convert_color(color):
	color = color.replace('#', '')
	r = int(color[0:2], 16) // 16
	g = int(color[2:4], 16) // 16
	b = int(color[4:6], 16) // 16
	#c = [0x00, 0x00]
	#c[0] = r * 16 + g  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
	#c[1] = b * 16
	return [r,g,b]


def convert_color2(color):
	color = color.replace('#', '')
	r = int(color[0:2], 16) // 16
	g = int(color[2:4], 16) // 16
	b = int(color[4:6], 16) // 16
	
	#r = r *16
	#g = g * 16
	#b = b * 16
	
	c = [0x00, 0x00]
	c[0] = r * 16 + g  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
	c[1] = b * 16
	return [r,g]



for hex, rgb in (('#FFFFFF','255,255,255'),('#C0C0C0','192,192,192')):
	print(hex, rgb, hex_to_rgb(hex), convert_color(hex), convert_color2(hex))
