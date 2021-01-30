import folium
import pandas
#toimportmarkerdata
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
#todisplayelevation
elev = list(data["ELEV"])
name = list(data["NAME"])

#colour gradient
def color_producer(elevation):
    if elevation<1000:
        return "green"
    elif 1000<= elevation <3000:
        return"orange"
    else:
        return "red"

#CHANGINGFONTSandaddinghyperlink
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

#tocreatebasemap
map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles = "Stamen Terrain")

fgv = folium.FeatureGroup(name = "Volcanoes")
#opacitygradientformarkers
def fc(elevation):
    if elevation<500:
        return 0.2
    elif 500 <= elevation <1000:
        return 0.4
    elif 1000<= elevation <1500:
        return 0.6
    elif 1500 <= elevation < 2000:
        return 0.8
    elif 2000 <= elevation < 2500:
        return 1
    elif 2500 <= elevation < 3000:
        return 1.2
    else:
        return 1.5


#toaddmultiplemarkers/ziphelps to iterate through 2 columns
for lt,ln, el, name in zip(lat, lon, elev, name):
#toaddfonts
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
#toaddmarkeronmap
    fgv.add_child(folium.vector_layers.CircleMarker(location=[lt, ln], radius=8, popup=folium.Popup(iframe),
                               fill_color=color_producer(el), fill=True, color = 'black', fill_opacity=fc(el)))

fgp = folium.FeatureGroup(name="Population")

#bordersofcountries
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x :{'fillColor':'yellow' if x['properties']['POP2005']<10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))


map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())

map.save("Map1_html_popup_advanced.html")