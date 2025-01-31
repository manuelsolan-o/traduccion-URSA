import dash

import dash_bootstrap_components as dbc
import ursa.ghsl as ghsl
import ursa.utils.geometry as ug

from components.text import figureWithDescription, figureWithDescription_translation
from components.text import mapComponent
from components.page import new_page_layout
from dash import html, dcc, callback, Input, Output
from pathlib import Path
from shapely.geometry import shape
from zipfile import ZipFile

translations = {
    "WELCOME_TEXT_PART1": {
        "es": "En esta pestaña encontrarás información acerca del crecimiento histórico de la ciudad. A partir de datos del proyecto ",
        "en": "In this tab, you will find information about the historical growth of the city. Based on data from the project",
        "pt": "Nesta aba, você encontrará informações sobre o crescimento histórico da cidade. Com base em dados do projeto",
    },
    "WELCOME_TEXT_PART2": {
        "es": "(GHSL) se muestra el cambio en el área urbanizada, la superficie construida y la población en la zona metropolitana de tu elección.",
        "en": "(GHSL) shows the change in the urbanized area, the built-up surface, and the population in the metropolitan area of your choice.",
        "pt": "(GHSL) mostra a mudança na área urbanizada, a superfície construída e a população na área metropolitana de sua escolha.",
    },
    "MAP_INTRO_TEXT_PART1": {
        "es": "Los cuatro mapas que se presentan a continuación contienen información agregada de las características urbanas de la región.",
        "en": "The four maps presented below contain aggregated information on the urban characteristics of the region.",
        "pt": "Os quatro mapas apresentados a seguir contêm informações agregadas sobre as características urbanas da região.",
    },
    "MAP_INTRO_TEXT_PART2": {
        "es": "Los límites de la región de análisis se delinean con un contorno de color azul.",
        "en": "The boundaries of the analysis region are outlined with a blue contour.",
        "pt": "Os limites da região de análise são delineados com um contorno azul.",
    },
    "MAP_INTRO_TEXT_PART3": {
        "es": "La región delineada en un color marrón identifica el área urbana principal.",
        "en": "The region outlined in brown identifies the main urban area.",
        "pt": "A região delineada em marrom identifica a área urbana principal.",
    },
    "MAP_INTRO_TEXT_PART4": {
        "es": "El área urbana principal se define porque cada pixel (100x100 metros) posee una densidad de al menos 300 habitantes por kilómetro cuadrado al año 2020.",
        "en": "The main urban area is defined because each pixel (100x100 meters) has a density of at least 300 inhabitants per square kilometer as of the year 2020.",
        "pt": "A área urbana principal é definida porque cada pixel (100x100 metros) possui uma densidade de pelo menos 300 habitantes por quilômetro quadrado no ano de 2020.",
    },
    "MAP_INTRO_TEXT_PART5": {
        "es": "Las regiones delineadas con un color amarillo corresponden a la urbanización periférica; se trata de zonas sin contigüidad al área urbana principal, pero que tienen una densidad de al menos 300 habitantes por kilómetro cuadrado al año 2020. Accede a más información acerca de cada mapa haciendo clic en el botón correspondiente en la interfaz de usuario.",
        "en": "The regions outlined in yellow correspond to peripheral urbanization; these are areas without contiguity to the main urban area, but which have a density of at least 300 inhabitants per square kilometer as of the year 2020. Access more information about each map by clicking on the corresponding button in the user interface.",
        "pt": "As regiões delineadas em amarelo correspondem à urbanização periférica; são áreas sem contiguidade à área urbana principal, mas que têm uma densidade de pelo menos 300 habitantes por quilômetro quadrado no ano de 2020. Acesse mais informações sobre cada mapa clicando no botão correspondente na interface do usuário.",
    },
    
    # MAP_HIST_BUILTUP_INTRO_TEXT,
    
    "MAP_HIST_BUILTUP_EXPANDED_TEXT_PART1": {
        "es": "Las celdas de la cartografía son de 100x100 metros. Una celda se considera como construida (built-up) cuando al menos el 20% de su superficie está cubierta por algún tipo de construcción. De acuerdo con la definición del ",
        "en": "The mapping cells are 100x100 meters. A cell is considered built-up when at least 20% of its surface is covered by some type of construction. According to the definition of ",
        "pt": "As células do mapeamento são de 100x100 metros. Uma célula é considerada construída (built-up) quando pelo menos 20% de sua superfície é coberta por algum tipo de construção. De acordo com a definição do ",
    },
    "MAP_HIST_BUILTUP_EXPANDED_TEXT_PART2": {
        "es": ", una construcción es cualquier tipo de estructura techada erigida sobre suelo para cualquier uso. Este mapa muestra el año en que cada celda se considera construida por primera vez en las imágenes de satélite.",
        "en": ", a construction is any type of roofed structure erected on the ground for any use. This map shows the year when each cell is considered built for the first time in satellite images.",
        "pt": ", uma construção é qualquer tipo de estrutura coberta erguida no solo para qualquer uso. Este mapa mostra o ano em que cada célula é considerada construída pela primeira vez nas imagens de satélite.",
    },
    
    # Muchos
    
    "LINE_GRAPH_TEXT_2_PART1": {
        "es": "A partir de las imágenes de satélite y de la información del",
        "en": "Based on satellite images and information from the",
        "pt": "Com base em imagens de satélite e informações do"
    },
    "LINE_GRAPH_TEXT_2_PART2": {
        "es": ", el gráfico de lineas muestra el cambio en la superficie del área construida dentro de la zona de interés del año 1975 al 2020. El área en color marrón corresponde a los kilómetros cuadrados por año de la superficie urbanizada en el cluster urbano principal de la ciudad. El área en color amarillo corresponde a la superficie urbanizada de las zonas periféricas sin contigüidad con la zona urbanizada central. El lector o lectora puede apreciar el crecimiento de la superficie urbanizada por año, distinguiendo en que medida se debe a crecimiento en la periferia versus en la zona central.",
        "en": ", the line graph shows the change in the built-up area within the area of interest from 1975 to 2020. The brown area corresponds to the square kilometers per year of the urbanized surface in the main urban cluster of the city. The yellow area corresponds to the urbanized surface of the peripheral areas without contiguity with the central urbanized zone. The reader can appreciate the growth of the urbanized surface per year, distinguishing to what extent it is due to growth in the periphery versus the central area.",
        "pt": ", o gráfico de linha mostra a mudança na área construída dentro da área de interesse de 1975 a 2020. A área marrom corresponde aos quilômetros quadrados por ano da superfície urbanizada no aglomerado urbano principal da cidade. A área amarela corresponde à superfície urbanizada das áreas periféricas sem contiguidade com a zona urbanizada central. O leitor pode apreciar o crescimento da superfície urbanizada por ano, distinguindo em que medida se deve ao crescimento na periferia versus na zona central."
    },
    
    "LINE_GRAPH_TEXT_3": {
        "es": " calcula estimados de población para las zonas metropolitanas de todo el mundo. Estos estimados se reportan en una cuadrícula, en este caso de 100x100 metros. El gráfico de líneas muestra el cambio en número de población de acuerdo con estos estimados, solamente para las celdas clasificadas como urbanizadas. Los estimados de población fueron elaborados con datos del 2010, extrapolados el 2020. Estaremos actualizando la herramienta conforme GHS publica nuevos estimados de población basados en las proyecciones de los censos levantados en 2020. El lector o lectora puede apreciar el cambio poblacional por año y por tipo de urbanización: central o periférica.",
        "en": " calculates population estimates for metropolitan areas around the world. These estimates are reported in a grid, in this case, 100x100 meters. The line graph shows the change in population number according to these estimates, only for cells classified as urbanized. The population estimates were made with data from 2010, extrapolated to 2020. We will be updating the tool as GHS publishes new population estimates based on the projections of the censuses conducted in 2020. The reader can appreciate the population change per year and by type of urbanization: central or peripheral.",
        "pt": " calcula estimativas populacionais para áreas metropolitanas ao redor do mundo. Essas estimativas são reportadas em uma grade, neste caso, de 100x100 metros. O gráfico de linha mostra a mudança no número da população de acordo com essas estimativas, apenas para células classificadas como urbanizadas. As estimativas populacionais foram feitas com dados de 2010, extrapoladas para 2020. Estaremos atualizando a ferramenta conforme o GHS publica novas estimativas populacionais baseadas nas projeções dos censos realizados em 2020. O leitor pode apreciar a mudança populacional por ano e por tipo de urbanização: central ou periférica."
    },
    
    
    # Mapas
    
    "map-title-1": {
        "es": "Año en el que aparece la construcción",
        "en": "Year of construction appearance",
        "pt": "Ano de aparição da construção"
    },
    "map-title-2": {
        "es": "Año en el que se considera celda urbana",
        "en": "Year when the cell is considered urban",
        "pt": "Ano em que a célula é considerada urbana"
    },
    "map-title-3": {
        "es": "Fracción de construcción 2020",
        "en": "Construction fraction 2020",
        "pt": "Fração de construção 2020"
    },
    "map-title-4": {
        "es": "Habitantes por celda",
        "en": "Inhabitants per cell",
        "pt": "Habitantes por célula"
    },
    
    # Lines
    
    "LINE_GRAPH_TEXT_1": {
        "es": "Este primer gráfico de líneas muestra el cambio en la superficie urbanizada dentro de la zona de interés del año 1975 al 2020. El cambio se desglosa en dos categorías: la superficie urbana dentro del cluster urbano principal y la superficie urbana en la periferia (desconectada y sin contigüidad con la mancha urbana). El recuadro con un contorno azul en los mapas delimita la zona de análisis en la región metropolitana, a partir del cual se derivan ambas categorías de la urbanización. La línea en color marrón en el gráfico corresponde a la superficie urbana del centro urbano principal, misma que se identifica en los mapas como el recuadro con un contorno en color marrón. La línea amarilla del gráfico representa el cambio por año en la superficie urbana en la periferia de la ciudad, cuya representación en el mapa se puede identificar como un recuadro con un color amarillo.",
        "en": "This first line graph shows the change in urbanized surface within the area of interest from 1975 to 2020. The change is broken down into two categories: the urban surface within the main urban cluster and the urban surface in the periphery (disconnected and not contiguous with the urban sprawl). The box with a blue outline on the maps delimits the area of analysis in the metropolitan region, from which both categories of urbanization are derived. The brown line on the graph corresponds to the urban surface of the main urban center, which is identified on the maps as the box with a brown outline. The yellow line on the graph represents the year-on-year change in urban surface in the city's periphery, which can be identified on the map as a box in yellow.",
        "pt": "Este primeiro gráfico de linha mostra a mudança na superfície urbanizada dentro da área de interesse de 1975 a 2020. A mudança é dividida em duas categorias: a superfície urbana dentro do aglomerado urbano principal e a superfície urbana na periferia (desconectada e sem contiguidade com a expansão urbana). A caixa com um contorno azul nos mapas delimita a área de análise na região metropolitana, a partir da qual são derivadas ambas as categorias de urbanização. A linha marrom no gráfico corresponde à superfície urbana do centro urbano principal, que é identificada nos mapas como a caixa com um contorno em marrom. A linha amarela no gráfico representa a mudança anual na superfície urbana na periferia da cidade, que pode ser identificada no mapa como uma caixa em amarelo."
    },
    
    "sub1": {
        "es": "Superficie del Área Urbana por Tipo de Urbanización (1975-2020)",
        "en": "Urban Area Surface by Type of Urbanization (1975-2020)",
        "pt": "Superfície da Área Urbana por Tipo de Urbanização (1975-2020)"
    },
    
    "LINE_GRAPH_TEXT_4": {
        "es": "El proceso de urbanización y crecimiento urbano va dejando huecos conforme la ciudad se expande territorialmente. Los mapas presentados anteriormente mostraron la proporción de suelo construido en cada celda e identificaban las celdas urbanizadas. Este gráfico de líneas compara ambos elementos y su cambio en el tiempo. Las fracciones se presentan para toda la zona metropolitana y también desglosadas por tipo de urbanización, central y en la periferia.",
        "en": "The process of urbanization and urban growth leaves gaps as the city expands territorially. The maps presented earlier showed the proportion of built-up land in each cell and identified the urbanized cells. This line graph compares both elements and their change over time. The fractions are presented for the entire metropolitan area and also broken down by type of urbanization, central and peripheral.",
        "pt": "O processo de urbanização e crescimento urbano deixa lacunas à medida que a cidade se expande territorialmente. Os mapas apresentados anteriormente mostraram a proporção de solo construído em cada célula e identificaram as células urbanizadas. Este gráfico de linha compara ambos os elementos e sua mudança ao longo do tempo. As frações são apresentadas para toda a área metropolitana e também detalhadas por tipo de urbanização, central e periférica."
    },
    
    "sub4": {
        "es": "Densidad de Construcción por Tipo de Urbanización (1975-2020)",
        "en": "Construction Density by Type of Urbanization (1975-2020)",
        "pt": "Densidade de Construção por Tipo de Urbanização (1975-2020)"
    },
    
    "LINE_GRAPH_TEXT_5": {
        "es": "Finalmente, contando con las áreas de superficie construida y urbana y la población por año, es posible calcular la evolución de la densidad poblacional a través del tiempo. En este caso, se presenta la densidad de población, representada como número de personas por superficie urbanizada en kilómetros cuadrados.",
        "en": "Finally, with the areas of built-up and urban surface and the population per year, it is possible to calculate the evolution of population density over time. In this case, the population density is presented, represented as the number of people per urbanized surface in square kilometers.",
        "pt": "Finalmente, com as áreas de superfície construída e urbana e a população por ano, é possível calcular a evolução da densidade populacional ao longo do tempo. Neste caso, apresenta-se a densidade populacional, representada como o número de pessoas por superfície urbanizada em quilômetros quadrados."
    },
    
    "sub5": {
        "es": "Densidad de Población por Tipo de Urbanización (1975-2020)",
        "en": "Population Density by Type of Urbanization (1975-2020)",
        "pt": "Densidade Populacional por Tipo de Urbanização (1975-2020)"
    },
    
    "LINE_GRAPH_TEXT_6": {
        "es": "El gráfico de líneas muestra la densidad poblacional, pero en este caso calculada como el número de personas sobre la superficie construida en kilómetros cuadrados. Se puede apreciar la evolución y cambio en la densidad poblacional del año 1975 al 2020. La densidad por superficie construida—y no urbanizada—es un indicador útil para medir el aprovechamiento de la infrainstructura en la ciudad: a mayor densidad, hay un uso más intensivo de la misma infraestructura.",
        "en": "The line graph shows the population density, but in this case calculated as the number of people over the built-up surface in square kilometers. The evolution and change in population density from 1975 to 2020 can be observed. The density per built-up surface—not urbanized—is a useful indicator to measure the use of infrastructure in the city: the higher the density, the more intensive the use of the same infrastructure.",
        "pt": "O gráfico de linha mostra a densidade populacional, mas neste caso calculada como o número de pessoas sobre a superfície construída em quilômetros quadrados. Pode-se observar a evolução e mudança na densidade populacional de 1975 a 2020. A densidade por superfície construída—e não urbanizada—é um indicador útil para medir o aproveitamento da infraestrutura na cidade: quanto maior a densidade, mais intensivo é o uso da mesma infraestrutura."
    },
    
    "sub6": {
        "es": "Densidad de Población (por Superficie de Construcción) por Tipo de Urbanización (1975-2020)",
        "en": "Population Density (by Construction Surface) by Type of Urbanization (1975-2020)",
        "pt": "Densidade Populacional (por Superfície de Construção) por Tipo de Urbanização (1975-2020)"
    },
    
    # titulos
    "sub7": {
        "es": "Año en el que aparece la construcción",
        "en": "Year of Construction Appearance",
        "pt": "Ano de Aparecimento da Construção"
    },
    
    "MAP_HIST_URBAN_EXPANDED_TEXT": {
        "es": "En contraste con el suelo construido, una celda de 1000x1000 metros se considera urbana cuando su densidad de población excede los 300 habitantes por kilómetro cuadrado. El segundo mapa representa el año en que cada celda se consideró como urbana por primera vez a partir del histórico de imágenes de satélite registradas.",
        "en": "In contrast to built-up land, a 1000x1000 meter cell is considered urban when its population density exceeds 300 inhabitants per square kilometer. The second map represents the year when each cell was first considered urban based on the historical satellite images recorded.",
        "pt": "Em contraste com o solo construído, uma célula de 1000x1000 metros é considerada urbana quando sua densidade populacional excede 300 habitantes por quilômetro quadrado. O segundo mapa representa o ano em que cada célula foi considerada urbana pela primeira vez com base no histórico de imagens de satélite registradas.",
    },
    
    "sub8": {
        "es": "Año en el que se considera celda urbana",
        "en": "Year When the Cell is Considered Urban",
        "pt": "Ano em que a Célula é Considerada Urbana"
    },
    "sub9": {
        "es": "Fracción de construcción 2020",
        "en": "Construction Fraction 2020",
        "pt": "Fração de Construção 2020"
    },
    
    "MAP_BUILT_F_EXPANDED_TEXT": {
        "es": "La escala de colores de azul a amarillo del mapa representa la fracción de construcción de cada celda de 100x100 metros para el año 2020. Esta fracción es 0 para una celda sin construcción (en color azul) y 1 para una celda completamente cubierta por construcción (en color amarillo).",
        "en": "The map's color scale from blue to yellow represents the construction fraction of each 100x100 meter cell for the year 2020. This fraction is 0 for a cell with no construction (in blue) and 1 for a cell completely covered by construction (in yellow).",
        "pt": "A escala de cores do mapa de azul a amarelo representa a fração de construção de cada célula de 100x100 metros para o ano de 2020. Esta fração é 0 para uma célula sem construção (em azul) e 1 para uma célula completamente coberta por construção (em amarelo).",
    },
    
    "sub10": {
        "es": "Habitantes por celda",
        "en": "Inhabitants per Cell",
        "pt": "Habitantes por Célula"
    },
    
    "MAP_POP_EXPANDED_TEXT": {
        "es": "Este mapa muestra el número de habitantes en cada celda de 100x100 metros al año 2020.",
        "en": "This map shows the number of inhabitants in each 100x100 meter cell in the year 2020.",
        "pt": "Este mapa mostra o número de habitantes em cada célula de 100x100 metros no ano de 2020.",
    },
    
    "btn-download-rasters": {
        "es": "Descargar a disco",
        "en": "Download to Disk",
        "pt": "Baixar para o Disco"
    },
    "download-raster-instructions": {
        "es": "Descarga los archivos Raster localmente en tu carpeta de Descargas.",
        "en": "Download the Raster files locally to your Downloads folder.",
        "pt": "Baixe os arquivos Raster localmente na sua pasta de Downloads."
    },

    
    "charts-generation-error": {
        "es": "Algunas gráficas no pudieron ser generadas. Considere cambiar la bounding box de análisis.",
        "en": "Some charts could not be generated. Consider changing the bounding box for analysis.",
        "pt": "Alguns gráficos não puderam ser gerados. Considere mudar a caixa de delimitação para análise."
    }
    
}

dash.register_page(__name__, title="URSA")

WELCOME_TEXT = [
    (
        html.Div(id='WELCOME_TEXT_PART1')
    ),
    html.A("Global Human Settlement Layer", href="https://ghsl.jrc.ec.europa.eu/"),
    (
        html.Div(id='WELCOME_TEXT_PART2')
    ),
]

MAP_INTRO_TEXT = [
    (
        html.Div(id='MAP_INTRO_TEXT_PART1')
    ),
    html.Ul(
        [
            html.Li(
                id='MAP_INTRO_TEXT_PART2'
            ),
            html.Li(
                id='MAP_INTRO_TEXT_PART3'
            ),
            html.Li(
                id='MAP_INTRO_TEXT_PART4'
            ),
            html.Li(
                id='MAP_INTRO_TEXT_PART5'
            ),
        ]
    ),
]

MAP_HIST_BUILTUP_INTRO_TEXT = "Evolución temporal de la construcción."

MAP_HIST_BUILTUP_EXPANDED_TEXT = html.Div(
    [
        html.Span(id="MAP_HIST_BUILTUP_EXPANDED_TEXT_PART1"),
        html.Acronym("GHSL", title="Global Human Settlement Layer"),
        html.Span(id="MAP_HIST_BUILTUP_EXPANDED_TEXT_PART2"),
    ]
)

MAP_HIST_URBAN_INTRO_TEXT = "Evolución temporal de la urbanización. "

MAP_HIST_URBAN_EXPANDED_TEXT = (
    "En contraste con el suelo construido, una celda de 1000x1000 metros se "
    "considera urbana cuando su densidad de población excede los 300 "
    "habitantes por kilómetro cuadrado. El segundo mapa "
    "representa el año en que cada celda se consideró como urbana por "
    "primera vez a partir del histórico de imágenes de satélite registradas."
)

MAP_BUILT_F_INTRO_TEXT = "Fracción de construcción. "

MAP_BUILT_F_EXPANDED_TEXT = (
    "La escala de colores de azul a amarillo del mapa "
    "representa la fracción de construcción de cada celda de 100x100 metros "
    "para el año 2020. Esta fracción es 0 para una celda sin construcción "
    "(en color azul) y 1 para una celda completamente cubierta por "
    "construcción (en color amarillo)."
)

MAP_POP_INTRO_TEXT = "Número de habitantes. "

MAP_POP_EXPANDED_TEXT = (
    "Este mapa muestra el número de habitantes en cada celda de 100x100 "
    "metros al año 2020."
)

LINE_GRAPH_TEXT_1 = """Este primer gráfico de líneas muestra el cambio en la
    superficie urbanizada dentro de la zona de interés del año 1975 al 2020.
    El cambio se desglosa en dos categorías:
    la superficie urbana dentro del cluster urbano principal y
    la superficie urbana en la periferia (desconectada y sin contigüidad
    con la mancha urbana).
    El recuadro con un contorno azul en los mapas delimita la zona de
    análisis en la región metropolitana, a partir del cual se derivan
    ambas categorías de la urbanización.
    La línea en color marrón en el gráfico corresponde a la superficie
    urbana del centro urbano principal,
    misma que se identifica en los mapas como el recuadro con un contorno
    en color marrón.
    La línea amarilla del gráfico representa el cambio por año en la
    superficie urbana en la periferia de la ciudad,
    cuya representación en el mapa se puede identificar como un recuadro
    con un color amarillo."""

LINE_GRAPH_TEXT_2 = html.Div(
    [
        html.Span(id="LINE_GRAPH_TEXT_2_PART1"),
        html.Acronym("GHSL", title="Global Human Settlement Layer"),
        html.Span(id="LINE_GRAPH_TEXT_2_PART2"),
    ],
)

LINE_GRAPH_TEXT_3 = html.Div(
    [
        html.Acronym("GHSL", title="Global Human Settlement Layer"),
        
        html.Span(id="LINE_GRAPH_TEXT_3"),
    ]
)

LINE_GRAPH_TEXT_4 = """El proceso de urbanización y crecimiento urbano va
dejando huecos conforme la ciudad se expande territorialmente. Los mapas
presentados anteriormente mostraron la proporción de suelo construido en
cada celda e identificaban las celdas urbanizadas. Este gráfico de líneas
compara ambos elementos y su cambio en el tiempo. Las fracciones se presentan para toda la zona metropolitana y también desglosadas por tipo de urbanización, central y en la periferia."""

LINE_GRAPH_TEXT_5 = """Finalmente, contando con las áreas de superficie construida y urbana y la población por año, es posible calcular la evolución de la densidad poblacional a través del tiempo. En este caso, se presenta la densidad de población, representada como número de personas por superficie urbanizada en kilométros cuadrados."""

LINE_GRAPH_TEXT_6 = """El gráfico de líneas muestra la densidad poblacional,
pero en este caso calculada como el número de personas sobre la superficie
construida en kilómetros cuadrados. Se puede apreciar la evolución y cambio
en la densidad poblacional del año 1975 al 2020. La densidad por superficie
construida—y no urbanizada—es un indicador útil para medir el aprovechamiento
de la infrainstructura en la ciudad: a mayor densidad, hay un uso más intensivo
de la misma infraestructura. """


maps = html.Div(
    [
        html.Div(
            [
                html.H4(id="map-title-1"),  
                mapComponent(title="", id="growth-map-1")  
            ],
            style={"margin-bottom": "20px"}  
        ),
        html.Div(
            [
                html.H4(id="map-title-2"),  
                mapComponent(title="", id="growth-map-2")  
            ],
            style={"margin-bottom": "20px"} 
        ),
        html.Div(
            [
                html.H4(id="map-title-3"),  
                mapComponent(title="", id="growth-map-3") 
            ],
            style={"margin-bottom": "20px"}  
        ),
        html.Div(
            [
                html.H4(id="map-title-4"),  
                mapComponent(title="", id="growth-map-4")  
            ],
            style={"margin-bottom": "20px"}  
        )

    ],
    style={"height": "90vh", "overflow": "scroll"},
)

lines = html.Div(
    [
        figureWithDescription_translation(
        dcc.Graph(id="growth-lines-1"),
        "LINE_GRAPH_TEXT_1",  # ID descripción
        "sub1"  # ID título
        ),
        
        figureWithDescription(
            dcc.Graph(id="growth-lines-2"),
            LINE_GRAPH_TEXT_2,
            "Superficie del Área Construida por Tipo de Urbanización (1975-2020)",
        ),
        
        figureWithDescription(
            dcc.Graph(id="growth-lines-3"),
            LINE_GRAPH_TEXT_3,
            "Población Total del Área Urbana por Tipo de Urbanización (1975-2020)",
        ),
        figureWithDescription_translation(
        dcc.Graph(id="growth-lines-4"),
        "LINE_GRAPH_TEXT_4",  # ID descripción
        "sub4"  # ID título
        ),
        
        figureWithDescription_translation(
        dcc.Graph(id="growth-lines-5"),
        "LINE_GRAPH_TEXT_5",  # ID descripción
        "sub5"  # ID título
        ),
        figureWithDescription_translation(
        dcc.Graph(id="growth-lines-6"),
        "LINE_GRAPH_TEXT_6",  # ID descripción
        "sub6"  # ID título
        ),
    ],
    style={"height": "82vh", "overflow": "scroll"},
)


welcomeAlert = dbc.Card(dbc.CardBody(WELCOME_TEXT), class_name="main-info")
mapIntroAlert = dbc.Card(dbc.CardBody(MAP_INTRO_TEXT), class_name="supp-info")
constructionYearMapInfoAlert = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="sub7"),
            MAP_HIST_BUILTUP_EXPANDED_TEXT,
        ]
    ),
    class_name="supp-info",
)
urbanCellYearMapInfoAlert = dbc.Card(
    dbc.CardBody(
        [
            html.H4(id="sub8"),
            html.Span(id = "MAP_HIST_URBAN_EXPANDED_TEXT"),
        ]
    ),
    class_name="supp-info",
)
contstructionFractionMapInfoAlert = dbc.Card(
    dbc.CardBody([html.H4(id="sub9"), 
                  
                  html.Span(id = "MAP_BUILT_F_EXPANDED_TEXT")]),
    class_name="supp-info",
)
inhabitantsFractionMapInfoAlert = dbc.Card(
    dbc.CardBody([html.H4(id = "sub10"), 
                  html.Span(id = "MAP_POP_EXPANDED_TEXT")]),
    class_name="supp-info",
)


download_button = html.Div(
    [
        dbc.Button(id="btn-download-rasters", color="light"),
        dcc.Download(id="download-rasters-zip"),
        html.Span(
            "?",
            id="tooltip-target01",
            style={
                "textAlign": "center",
                "color": "white",
                "height": 25,
                "width": 25,
                "background-color": "#bbb",
                "border-radius": "50%",
                "display": "inline-block",
            },
        ),
        dbc.Tooltip(
            html.Span(id = "download-raster-instructions"),
            target="tooltip-target01",
        ),
    ]
)


tabs = [
    dbc.Tab(
        lines,
        label = "Gráficas",
        id="tab-plots",
        tab_id="tabPlots",
    ),
    dbc.Tab(
        html.Div(
            [
                welcomeAlert,
                mapIntroAlert,
                constructionYearMapInfoAlert,
                urbanCellYearMapInfoAlert,
                contstructionFractionMapInfoAlert,
                inhabitantsFractionMapInfoAlert,
            ]
        ),
        label= "Info",
        id="tab-info",
        tab_id="tabInfo",
    ),
    dbc.Tab(
        html.Div([download_button]),

        label= "Descargables",
        id="tab-download",
        tab_id="tabDownload",
    ),
]

# Traduccion

language_buttons = dbc.ButtonGroup(
    [
        dbc.Button("Español", id="btn-lang-es", n_clicks=0),
        dbc.Button("English", id="btn-lang-en", n_clicks=0),
        dbc.Button("Portuguese", id="btn-lang-pt", n_clicks=0),
    ],
    style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1"},
)

layout = new_page_layout(
    maps,
    tabs,
    stores=[dcc.Location(id="growth-location")],
    alerts=[
        dbc.Alert(
           html.Span(id="charts-generation-error"),
            id="growth-alert",
            is_open=False,
            dismissable=True,
            color="warning",
        )
    ],
)
# ---

layout = html.Div(
    [language_buttons, layout],
    style={"position": "relative"}
)

@callback(
    [Output(key, 'children') for key in translations.keys()],
    [Input('btn-lang-es', 'n_clicks'),
     Input('btn-lang-en', 'n_clicks'),
     Input('btn-lang-pt', 'n_clicks')]
)
def update_translated_content(btn_lang_es, btn_lang_en, btn_lang_pt):
    ctx = dash.callback_context

    if not ctx.triggered:
        language = 'es'  # Predeterminado
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        language = 'es' if button_id == 'btn-lang-es' else 'en' if button_id == 'btn-lang-en' else 'pt'

    return [translations[key][language] for key in translations.keys()]

# ---


@callback(
    Output("download-rasters-zip", "data"),
    Input("btn-download-rasters", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    rasters: list[str] = [
        "GHS_BUILT_S_100.tif",
        #'GHS_LAND_100.tif',
        "GHS_POP_100.tif",
        "GHS_SMOD_1000.tif",
        #'dou.tif',
        #'protected.tif',
        #'slope.tif'
    ]

    zip_file_name: str = f"hist-growth-rasters.zip"

    def write_archive(bytes_io):
        with ZipFile(bytes_io, mode="w") as zip_object:
            for raster_file_name in rasters:
                zip_object.write(raster_file_name, raster_file_name)

    return dcc.send_bytes(write_archive, zip_file_name)


@callback(
    Output("growth-lines-1", "figure"),
    Output("growth-lines-2", "figure"),
    Output("growth-lines-3", "figure"),
    Output("growth-lines-4", "figure"),
    Output("growth-lines-5", "figure"),
    Output("growth-lines-6", "figure"),
    Output("growth-map-1", "figure"),
    Output("growth-map-2", "figure"),
    Output("growth-map-3", "figure"),
    Output("growth-map-4", "figure"),
    Output("growth-alert", "is_open"),
    Output("growth-location", "pathname"),
    Input("global-store-hash", "data"),
    Input("global-store-bbox-latlon", "data"),
    Input("global-store-uc-latlon", "data"),
)
def generate_lines(id_hash, bbox_latlon, uc_latlon):
    error_triggered = False

    if id_hash is None:
        return [dash.no_update] * 11 + ["/"]

    path_cache = Path(f"./data/cache/{str(id_hash)}")

    bbox_latlon = shape(bbox_latlon)
    bbox_mollweide = ug.reproject_geometry(bbox_latlon, "ESRI:54009").envelope

    uc_latlon = shape(uc_latlon)
    uc_mollweide = ug.reproject_geometry(uc_latlon, "ESRI:54009")

    centroid_mollweide = uc_mollweide.centroid

    smod, built, pop = ghsl.load_plot_datasets(bbox_mollweide, path_cache, clip=True)

    growth_df = ghsl.get_urb_growth_df(
        smod=smod,
        built=built,
        pop=pop,
        centroid_mollweide=centroid_mollweide,
        path_cache=path_cache,
    )

    line_plot_params = [
        dict(
            y_cols=["urban_cluster_main", "urban_cluster_other"],
            title="Área urbana",
            ylabel="Área (km²)",
            var_type="extensive",
        ),
        dict(
            y_cols=["built_cluster_main", "built_cluster_other"],
            title="Área construida",
            ylabel="Área (km²)",
            var_type="extensive",
        ),
        dict(
            y_cols=["pop_cluster_main", "pop_cluster_other"],
            title="Población",
            ylabel="Población",
            var_type="extensive",
        ),
        dict(
            y_cols=[
                "built_density_cluster_main",
                "built_density_cluster_other",
                "built_density_cluster_all",
            ],
            title="Densidad de construcción",
            ylabel="Fracción de área construida",
            var_type="intensive",
        ),
        dict(
            y_cols=[
                "pop_density_cluster_main",
                "pop_density_cluster_other",
                "pop_density_cluster_all",
            ],
            title="Densidad de población",
            ylabel="Personas por km²",
            var_type="intensive",
        ),
        dict(
            y_cols=[
                "pop_b_density_cluster_main",
                "pop_b_density_cluster_other",
                "pop_b_density_cluster_all",
            ],
            title="Densidad de población (construcción)",
            ylabel="Personas por km² de construcción",
            var_type="intensive",
        ),
    ]

    plots = []
    for params in line_plot_params:
        try:
            lines = ghsl.plot_growth(growth_df, **params)
            plots.append(lines)
        except Exception:
            plots.append(dash.no_update)
            error_triggered = True

    map1 = ghsl.plot_built_agg_img(smod, built, bbox_mollweide, centroid_mollweide)
    map2 = ghsl.plot_smod_clusters(smod, bbox_latlon)
    map3 = ghsl.plot_built_year_img(
        smod, built, bbox_latlon, bbox_mollweide, centroid_mollweide
    )
    map4 = ghsl.plot_pop_year_img(smod, pop, bbox_mollweide, centroid_mollweide)

    plots.append(map1)
    plots.append(map2)
    plots.append(map3)
    plots.append(map4)

    return plots + [error_triggered, dash.no_update]