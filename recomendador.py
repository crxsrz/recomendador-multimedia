import csv
import heapq
import os
import random

# Carpeta donde vive este script  los CSV deben estar aqui tambien
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 
# 1. JERARQUIA DE GENEROS
# 
JERARQUIA = {
    "Accion": {
        "Shooter / FPS": ["FPS","Shooter","Arena Shooter","Hero Shooter","Boomer Shooter",
                          "Extraction Shooter","Looter Shooter","Third-Person Shooter",
                          "Top-Down Shooter","Twin Stick Shooter","Sniper","Bullet Hell","Shoot 'Em Up"],
        "Hack & Slash": ["Hack and Slash","Character Action Game","Spectacle fighter",
                         "Musou","Beat 'em up","Swordplay","Martial Arts","Ninja"],
        "Plataformas":  ["Platformer","2D Platformer","3D Platformer","Precision Platformer",
                         "Puzzle Platformer","Metroidvania","Runner","Parkour"],
        "Lucha":        ["Fighting","2D Fighter","3D Fighter","Wrestling","Boxing"],
        "Battle Royale":["Battle Royale","PvP","Competitive"],
        "Stealth":      ["Stealth","Assassin","Heist"],
    },
    "Aventura": {
        "Aventura Clasica":  ["Adventure","Action-Adventure","Exploration","Open World","Collectathon"],
        "Narrativa":         ["Story Rich","Narrative","Choices Matter","Multiple Endings",
                              "Cinematic","Well-Written","Lore-Rich","Drama","Episodic"],
        "Survival / Craft":  ["Survival","Open World Survival Craft","Crafting","Mining","Farming Sim"],
        "Horror":            ["Horror","Survival Horror","Psychological Horror","Gore",
                              "Lovecraftian","Zombie","Demons"],
        "Mundo Abierto":     ["Open World","Sandbox","Nature","Underwater","Space","Exploration"],
    },
    "Rol (RPG)": {
        "RPG Occidental": ["RPG","CRPG","Action RPG","Party-Based RPG","Dungeon Crawler","Loot"],
        "JRPG":           ["JRPG","Anime","Turn-Based Combat"],
        "Roguelike":      ["Roguelike","Roguelite","Action Roguelike","Traditional Roguelike",
                           "Roguelike Deckbuilder","Perma Death","Procedural Generation"],
        "Souls-like":     ["Souls-like","Difficult","Unforgiving"],
        "RPG por Turnos": ["Turn-Based Combat","Strategy RPG","Tactical RPG","Mystery Dungeon"],
    },
    "Estrategia": {
        "RTS":              ["RTS","Action RTS","Real-Time","Real Time Tactics","Real-Time with Pause"],
        "Por Turnos":       ["Turn-Based Strategy","Turn-Based Tactics","4X","Grand Strategy",
                             "Wargame","Hex Grid"],
        "Tower Defense":    ["Tower Defense"],
        "Construccion":     ["City Builder","Base Building","Colony Sim","Management",
                             "Economy","Resource Management","Automation","God Game"],
        "Cartas / Tablero": ["Card Game","Card Battler","Deckbuilding","Trading Card Game",
                             "Board Game","Tabletop","Dice","Mahjong"],
    },
    "Simulacion": {
        "Vida / Social":     ["Life Sim","Dating Sim","Romance","Creature Collector","Social Deduction"],
        "Vehiculos":         ["Automobile Sim","Driving","Flight","Jet","Space Sim",
                              "Naval","Submarine","Motorbike","Trains","Transportation"],
        "Trabajo / Gestion": ["Job Simulator","Hobby Sim","Farming Sim","Cooking",
                              "Shop Keeper","Time Management"],
        "Sandbox":           ["Sandbox","Building","Level Editor","Moddable","Voxel"],
        "Deportes":          ["Sports","Football (Soccer)","Football (American)","Basketball",
                              "Baseball","Hockey","Golf","Mini Golf","Skateboarding",
                              "Skating","Snowboarding","Motocross","Fishing","Hunting"],
    },
    "Puzzle / Casual": {
        "Puzzle":       ["Puzzle","Logic","Hidden Object","Escape Room","Mystery",
                         "Detective","Investigation","Word Game"],
        "Casual":       ["Casual","Relaxing","Cozy","Wholesome","Clicker","Idler",
                         "Cute","Family Friendly"],
        "Ritmo":        ["Rhythm","Music","Great Soundtrack","Rock Music","Soundtrack"],
        "Party":        ["Party Game","Party","Minigames","Trivia","Local Multiplayer",
                         "4 Player Local","Split Screen"],
    },
    "Indie / Arte": {
        "Visual Novel":   ["Visual Novel","Interactive Fiction","Text-Based","Conversation",
                           "Point & Click","Walking Simulator","Choose Your Own Adventure"],
        "Pixel / Retro":  ["Pixel Graphics","Retro","Classic","Old School","2D","Nostalgia"],
        "Arte / Estilo":  ["Hand-drawn","Cartoon","Cartoony","Colorful","Stylized",
                           "Minimalist","Anime","Comic Book","Psychedelic","Abstract"],
        "Indie General":  ["Indie","Singleplayer","Emotional","Atmospheric","Immersive","Addictive"],
    },
    "Multijugador": {
        "Cooperativo":  ["Co-op","Co-op Campaign","Online Co-Op","Local Co-Op","Team-Based"],
        "Competitivo":  ["PvP","eSports","Competitive","MOBA","Battle Royale"],
        "MMORPG":       ["MMORPG","Massively Multiplayer"],
        "Social":       ["Social Deduction","Party Game","Local Multiplayer"],
    },
    "Tematica": {
        "Ciencia Ficcion":   ["Sci-fi","Futuristic","Space","Cyberpunk","Dystopian",
                              "Robots","Mechs","Aliens","Transhumanism","Mars"],
        "Fantasia":          ["Fantasy","Dark Fantasy","Magic","Dragons","Mythology",
                              "Dungeons & Dragons","Medieval","Vampire","Supernatural","Gothic"],
        "Historia / Guerra": ["Historical","Military","War","World War I","World War II",
                              "Cold War","Alternate History","Rome","Vikings","Tanks","Wargame"],
        "Post-apocaliptico": ["Post-apocalyptic","Zombies","Survival","Dystopian"],
        "Western / Crimen":  ["Western","Crime","Heist","Noir","Detective","Conspiracy"],
        "Comedia / Satira":  ["Comedy","Dark Comedy","Dark Humor","Funny","Parody","Satire"],
    },
    #  PELICULAS 
    "Drama": {
        "Drama General":  ["Drama"],
        "Drama Historico":["History","Biography","War"],
        "Drama Criminal": ["Crime","Film-Noir"],
        "Romance":        ["Romance"],
    },
    "Accion / Aventura Cine": {
        "Accion":              ["Action"],
        "Aventura":            ["Adventure"],
        "Fantasia / Sci-Fi":   ["Fantasy","Sci-Fi"],
        "Thriller / Suspenso": ["Thriller","Mystery"],
    },
    "Terror / Sci-Fi Cine": {
        "Terror":       ["Horror"],
        "Ciencia Ficcion":["Sci-Fi"],
        "Sobrenatural": ["Fantasy"],
    },
    "Comedia Cine": {
        "Comedia":          ["Comedy"],
        "Musical / Musica": ["Musical","Music"],
        "Familiar":         ["Family","Animation"],
    },
    "Animacion / Familiar": {
        "Animacion":["Animation"],
        "Familia":  ["Family"],
    },
    "Otros Cine": {
        "Deporte": ["Sport"],
        "Western": ["Western"],
        "Musical": ["Musical","Music"],
        "Belico":  ["War"],
    },
}

GENEROS_JUEGOS    = ["Accion","Aventura","Rol (RPG)","Estrategia",
                     "Simulacion","Puzzle / Casual","Indie / Arte","Multijugador","Tematica"]
GENEROS_PELICULAS = ["Drama","Accion / Aventura Cine","Terror / Sci-Fi Cine",
                     "Comedia Cine","Animacion / Familiar","Otros Cine"]

# 
# 2. TITULOS ANCLA  100 titulos por categoria
#    El recomendador elige 5 al azar cada vez
# 
ANCLAS_JUEGOS_MAYOR = [
    #  FPS / Shooter 
    ("Counter-Strike 2",          ["FPS","Competitive","Multiplayer","Shooter","Team-Based"]),
    ("Left 4 Dead 2",             ["Zombies","Co-op","FPS","Horror","Multiplayer"]),
    ("Team Fortress 2",           ["FPS","Multiplayer","Funny","Team-Based","Shooter"]),
    ("Doom Eternal",              ["FPS","Action","Fast-Paced","Gore","Singleplayer"]),
    ("Half-Life 2",               ["FPS","Sci-fi","Story Rich","Singleplayer","Action"]),
    ("Titanfall 2",               ["FPS","Action","Sci-fi","Singleplayer","Multiplayer"]),
    ("Halo: The Master Chief Collection", ["FPS","Sci-fi","Co-op","Multiplayer","Action"]),
    ("Bioshock Infinite",         ["FPS","Story Rich","Sci-fi","Action","Singleplayer"]),
    ("Borderlands 2",             ["FPS","Co-op","Looter Shooter","RPG","Funny"]),
    ("Apex Legends",              ["Battle Royale","FPS","Competitive","Multiplayer","Free to Play"]),
    #  Accion / Aventura 
    ("Portal 2",                  ["Puzzle","Platformer","Sci-fi","Co-op","Funny"]),
    ("Portal",                    ["Puzzle","Platformer","Sci-fi","Singleplayer","Funny"]),
    ("The Witcher 3: Wild Hunt",  ["RPG","Open World","Story Rich","Fantasy","Action"]),
    ("Red Dead Redemption 2",     ["Open World","Western","Story Rich","Action","Adventure"]),
    ("Grand Theft Auto V",        ["Open World","Action","Crime","Multiplayer","Sandbox"]),
    ("Sekiro: Shadows Die Twice", ["Souls-like","Action","Difficult","Singleplayer","Ninja"]),
    ("Hollow Knight",             ["Metroidvania","Platformer","Difficult","Indie","Action"]),
    ("Hades",                     ["Action Roguelike","Roguelite","Dungeon Crawler","Indie","Action"]),
    ("Celeste",                   ["Precision Platformer","Platformer","Indie","Difficult","Story Rich"]),
    ("Ori and the Will of the Wisps", ["Platformer","Metroidvania","Colorful","Indie","Adventure"]),
    ("Cuphead",                   ["Difficult","Platformer","Hand-drawn","Action","Co-op"]),
    ("Disco Elysium",             ["RPG","Story Rich","Choices Matter","Mystery","Indie"]),
    ("Control",                   ["Action","Sci-fi","Mystery","Story Rich","Third Person"]),
    ("Death Stranding",           ["Action","Open World","Story Rich","Sci-fi","Cinematic"]),
    ("Batman: Arkham City",       ["Action","Superhero","Open World","Stealth","Adventure"]),
    #  RPG 
    ("FINAL FANTASY",             ["JRPG","RPG","Turn-Based Combat","Fantasy","Pixel Graphics"]),
    ("Elden Ring",                ["Souls-like","RPG","Open World","Fantasy","Difficult"]),
    ("Dark Souls III",            ["Souls-like","RPG","Action","Difficult","Fantasy"]),
    ("Divinity: Original Sin 2",  ["CRPG","RPG","Turn-Based","Co-op","Fantasy"]),
    ("Baldur's Gate 3",           ["CRPG","RPG","Turn-Based","Co-op","Fantasy"]),
    ("The Elder Scrolls V: Skyrim",["RPG","Open World","Fantasy","Moddable","Adventure"]),
    ("Mass Effect 2",             ["RPG","Sci-fi","Story Rich","Action","Choices Matter"]),
    ("Dragon Age: Origins",       ["RPG","Fantasy","Story Rich","CRPG","Party-Based RPG"]),
    ("Persona 5 Royal",           ["JRPG","RPG","Turn-Based Combat","Anime","Story Rich"]),
    ("Monster Hunter: World",     ["Action RPG","Co-op","Open World","Loot","Multiplayer"]),
    #  Estrategia 
    ("Civilization VI",           ["4X","Turn-Based Strategy","Strategy","Multiplayer","Historical"]),
    ("XCOM 2",                    ["Turn-Based Tactics","Strategy","Sci-fi","Difficult","Singleplayer"]),
    ("Starcraft II",              ["RTS","Competitive","Sci-fi","Multiplayer","eSports"]),
    ("Total War: Warhammer III",  ["Strategy","Turn-Based","RTS","Fantasy","Wargame"]),
    ("Age of Empires IV",         ["RTS","Historical","Multiplayer","Strategy","Singleplayer"]),
    ("Crusader Kings III",        ["Grand Strategy","Historical","Medieval","Simulation","Strategy"]),
    ("Into the Breach",           ["Turn-Based Tactics","Strategy","Sci-fi","Indie","Puzzle"]),
    ("Slay the Spire 2",          ["Roguelike","Card Game","Deckbuilding","Strategy","Indie"]),
    ("Hearthstone",               ["Card Game","Strategy","Fantasy","Multiplayer","Free to Play"]),
    ("Factorio",                  ["Automation","Base Building","Strategy","Management","Crafting"]),
    #  Simulacion / Construccion 
    ("Stardew Valley",            ["Farming Sim","Life Sim","Relaxing","RPG","Pixel Graphics"]),
    ("RimWorld",                  ["Colony Sim","Base Building","Survival","Strategy","Simulation"]),
    ("The Sims 4",                ["Life Sim","Simulation","Sandbox","Building","Casual"]),
    ("Cities: Skylines",          ["City Builder","Management","Simulation","Building","Strategy"]),
    ("Planet Zoo",                ["Management","Simulation","Building","Animals","Sandbox"]),
]

ANCLAS_JUEGOS_MENOR = [
    ("Counter-Strike 2",          ["FPS","Competitive","Multiplayer","Shooter","Team-Based"]),
    ("Minecraft",                 ["Sandbox","Survival","Building","Multiplayer","Crafting"]),
    ("Portal 2",                  ["Puzzle","Platformer","Sci-fi","Co-op","Funny"]),
    ("Portal",                    ["Puzzle","Platformer","Sci-fi","Singleplayer","Funny"]),
    ("Stardew Valley",            ["Farming Sim","Life Sim","Relaxing","RPG","Pixel Graphics"]),
    ("Terraria",                  ["Sandbox","Action","RPG","Crafting","Pixel Graphics"]),
    ("Garry's Mod",               ["Sandbox","Multiplayer","Physics","Funny","Moddable"]),
    ("Among Us",                  ["Social Deduction","Multiplayer","Casual","Party Game","Funny"]),
    ("Fall Guys",                 ["Party Game","Multiplayer","Casual","Battle Royale","Funny"]),
    ("Roblox",                    ["Sandbox","Multiplayer","Casual","Building","Free to Play"]),
    ("Fortnite",                  ["Battle Royale","Multiplayer","Shooter","Free to Play","Building"]),
    ("Apex Legends",              ["Battle Royale","FPS","Competitive","Multiplayer","Free to Play"]),
    ("Rocket League",             ["Sports","Competitive","Multiplayer","Vehicles","eSports"]),
    ("Hollow Knight",             ["Metroidvania","Platformer","Difficult","Indie","Action"]),
    ("Hades",                     ["Action Roguelike","Roguelite","Dungeon Crawler","Indie","Action"]),
    ("Celeste",                   ["Precision Platformer","Platformer","Indie","Difficult","Story Rich"]),
    ("Cuphead",                   ["Difficult","Platformer","Hand-drawn","Action","Co-op"]),
    ("Undertale",                 ["RPG","Indie","Story Rich","Pixel Graphics","Turn-Based Combat"]),
    ("Shovel Knight",             ["Platformer","Pixel Graphics","Action","Indie","Retro"]),
    ("Ori and the Will of the Wisps",["Platformer","Metroidvania","Colorful","Indie","Adventure"]),
    ("It Takes Two",              ["Co-op","Platformer","Adventure","Puzzle","Funny"]),
    ("Overcooked! 2",             ["Co-op","Casual","Funny","Party Game","Local Multiplayer"]),
    ("Human Fall Flat",           ["Puzzle","Co-op","Funny","Physics","Casual"]),
    ("Stray",                     ["Adventure","Indie","Sci-fi","Atmospheric","Singleplayer"]),
    ("Unpacking",                 ["Casual","Relaxing","Puzzle","Indie","Atmospheric"]),
    ("FINAL FANTASY",             ["JRPG","RPG","Turn-Based Combat","Fantasy","Pixel Graphics"]),
    ("Slay the Spire 2",          ["Roguelike","Card Game","Deckbuilding","Strategy","Indie"]),
    ("Cult of the Lamb",          ["Action Roguelike","Base Building","Cute","Dark Humor","Roguelite"]),
    ("Subnautica",                ["Survival","Underwater","Exploration","Open World"]),
    ("No Man's Sky",              ["Survival","Space","Open World","Exploration","Multiplayer"]),
    ("The Sims 4",                ["Life Sim","Simulation","Sandbox","Building","Casual"]),
    ("Civilization VI",           ["4X","Turn-Based Strategy","Strategy","Multiplayer","Historical"]),
    ("Age of Empires IV",         ["RTS","Historical","Multiplayer","Strategy","Singleplayer"]),
    ("Hearthstone",               ["Card Game","Strategy","Fantasy","Multiplayer","Free to Play"]),
    ("Dota 2",                    ["MOBA","Strategy","Multiplayer","Competitive","Free to Play"]),
    ("League of Legends",         ["MOBA","Strategy","Multiplayer","Competitive","Free to Play"]),
    ("Warframe",                  ["Action","Sci-fi","Co-op","Looter Shooter","Free to Play"]),
    ("Phasmophobia",              ["Horror","Co-op","Multiplayer","Investigation","Atmospheric"]),
    ("Lethal Company",            ["Horror","Co-op","Funny","Multiplayer","Atmospheric"]),
    ("Five Nights at Freddy's",   ["Horror","Survival","Strategy","Singleplayer","Atmospheric"]),
    ("Life is Strange",           ["Adventure","Choices Matter","Story Rich","Drama","Indie"]),
    ("Firewatch",                 ["Walking Simulator","Adventure","Story Rich","Mystery","Indie"]),
    ("Spiritfarer",               ["Indie","Relaxing","Emotional","Adventure","Management"]),
    ("Forza Horizon 5",           ["Racing","Open World","Driving","Multiplayer","Simulation"]),
    ("FIFA 23",                   ["Sports","Football (Soccer)","Multiplayer","Simulation","Competitive"]),
    ("NBA 2K23",                  ["Sports","Basketball","Simulation","Multiplayer","Competitive"]),
    ("Tony Hawk's Pro Skater 1+2",["Sports","Skateboarding","Action","Multiplayer","Remake"]),
    ("Factorio",                  ["Automation","Base Building","Strategy","Management","Crafting"]),
    ("RimWorld",                  ["Colony Sim","Base Building","Survival","Strategy","Simulation"]),
    ("Cities: Skylines",          ["City Builder","Management","Simulation","Building","Strategy"]),
]

ANCLAS_PELIS_MAYOR = [
    #  Drama 
    ("The Shawshank Redemption",  ["Drama"]),
    ("The Godfather",             ["Crime","Drama"]),
    ("The Godfather: Part II",    ["Crime","Drama"]),
    ("12 Angry Men",              ["Crime","Drama"]),
    ("Schindler's List",          ["Biography","Drama","History"]),
    ("Forrest Gump",              ["Drama","Romance"]),
    ("Fight Club",                ["Drama","Thriller"]),
    ("One Flew Over the Cuckoo's Nest", ["Drama"]),
    ("Goodfellas",                ["Crime","Drama","Biography"]),
    ("American Beauty",           ["Drama"]),
    ("A Beautiful Mind",          ["Biography","Drama"]),
    ("The Green Mile",            ["Crime","Drama","Fantasy"]),
    ("Parasite",                  ["Comedy","Drama","Thriller"]),
    ("Whiplash",                  ["Drama","Music"]),
    ("La La Land",                ["Drama","Music","Romance"]),
    ("Marriage Story",            ["Drama","Romance"]),
    ("Manchester by the Sea",     ["Drama"]),
    ("Moonlight",                 ["Drama"]),
    ("Brokeback Mountain",        ["Drama","Romance"]),
    ("Requiem for a Dream",       ["Drama","Thriller"]),
    #  Accion / Aventura 
    ("The Dark Knight",           ["Action","Crime","Drama"]),
    ("Inception",                 ["Action","Adventure","Sci-Fi"]),
    ("The Matrix",                ["Action","Sci-Fi"]),
    ("The Lord of the Rings: The Fellowship of the Ring", ["Action","Adventure","Fantasy"]),
    ("The Lord of the Rings: The Two Towers", ["Action","Adventure","Fantasy"]),
    ("The Lord of the Rings: The Return of the King", ["Action","Adventure","Fantasy"]),
    ("Star Wars: Episode IV - A New Hope", ["Action","Adventure","Fantasy"]),
    ("Star Wars: Episode V - The Empire Strikes Back", ["Action","Adventure","Fantasy"]),
    ("Mad Max: Fury Road",        ["Action","Adventure","Sci-Fi"]),
    ("John Wick",                 ["Action","Crime","Thriller"]),
    ("Mission: Impossible  Fallout", ["Action","Adventure","Thriller"]),
    ("Top Gun: Maverick",         ["Action","Drama"]),
    ("Avengers: Endgame",         ["Action","Adventure","Fantasy"]),
    ("Spider-Man: Into the Spider-Verse", ["Action","Adventure","Animation"]),
    ("The Dark Knight Rises",     ["Action","Crime","Drama"]),
    ("Batman Begins",             ["Action","Crime","Drama"]),
    ("Iron Man",                  ["Action","Adventure","Sci-Fi"]),
    ("Gladiator",                 ["Action","Adventure","Drama"]),
    ("Braveheart",                ["Action","Biography","Drama"]),
    ("300",                       ["Action","Drama","History"]),
    #  Ciencia Ficcion 
    ("Interstellar",              ["Adventure","Drama","Sci-Fi"]),
    ("Arrival",                   ["Drama","Mystery","Sci-Fi"]),
    ("Blade Runner 2049",         ["Drama","Mystery","Sci-Fi"]),
    ("2001: A Space Odyssey",     ["Mystery","Sci-Fi"]),
    ("Alien",                     ["Horror","Sci-Fi","Thriller"]),
    ("The Terminator",            ["Action","Sci-Fi"]),
    ("Terminator 2: Judgment Day",["Action","Sci-Fi"]),
    ("Ex Machina",                ["Drama","Mystery","Sci-Fi","Thriller"]),
    ("Gravity",                   ["Drama","Sci-Fi","Thriller"]),
    ("The Martian",               ["Adventure","Drama","Sci-Fi"]),
    #  Terror 
]

ANCLAS_PELIS_MENOR = [
    ("The Lion King",             ["Animation","Adventure","Drama","Family"]),
    ("Toy Story",                 ["Animation","Adventure","Comedy","Family"]),
    ("Finding Nemo",              ["Animation","Adventure","Comedy","Family"]),
    ("Up",                        ["Animation","Adventure","Comedy","Drama","Family"]),
    ("WALL-E",                    ["Animation","Adventure","Family","Romance","Sci-Fi"]),
    ("Inside Out",                ["Animation","Adventure","Comedy","Drama","Family"]),
    ("Coco",                      ["Animation","Adventure","Family","Fantasy","Music"]),
    ("Spirited Away",             ["Animation","Adventure","Family","Fantasy"]),
    ("Spider-Man: Into the Spider-Verse", ["Action","Adventure","Animation"]),
    ("Avengers: Endgame",         ["Action","Adventure","Fantasy"]),
    ("Iron Man",                  ["Action","Adventure","Sci-Fi"]),
    ("The Dark Knight",           ["Action","Crime","Drama"]),
    ("Batman Begins",             ["Action","Crime","Drama"]),
    ("Star Wars: Episode IV - A New Hope", ["Action","Adventure","Fantasy"]),
    ("Star Wars: Episode V - The Empire Strikes Back", ["Action","Adventure","Fantasy"]),
    ("The Lord of the Rings: The Fellowship of the Ring", ["Action","Adventure","Fantasy"]),
    ("The Lord of the Rings: The Return of the King", ["Action","Adventure","Fantasy"]),
    ("The Matrix",                ["Action","Sci-Fi"]),
    ("Inception",                 ["Action","Adventure","Sci-Fi"]),
    ("Interstellar",              ["Adventure","Drama","Sci-Fi"]),
    ("The Martian",               ["Adventure","Drama","Sci-Fi"]),
    ("Jurassic Park",             ["Adventure","Sci-Fi","Thriller"]),
    ("E.T. the Extra-Terrestrial",["Adventure","Family","Sci-Fi"]),
    ("Back to the Future",        ["Adventure","Comedy","Sci-Fi"]),
    ("Forrest Gump",              ["Drama","Romance"]),
    ("The Shawshank Redemption",  ["Drama"]),
    ("A Beautiful Mind",          ["Biography","Drama"]),
    ("The Truman Show",           ["Comedy","Drama","Sci-Fi"]),
    ("Knives Out",                ["Comedy","Crime","Drama","Mystery"]),
    ("The Grand Budapest Hotel",  ["Adventure","Comedy","Crime"]),
    ("Home Alone",                ["Comedy","Family"]),
    ("Mrs. Doubtfire",            ["Comedy","Drama","Family"]),
    ("Shrek",                     ["Animation","Adventure","Comedy","Family","Fantasy"]),
    ("Monsters, Inc.",            ["Animation","Adventure","Comedy","Family"]),
    ("A Bug's Life",              ["Animation","Adventure","Comedy","Family"]),
    ("Princess Mononoke",         ["Animation","Action","Adventure","Fantasy"]),
    ("Your Name",                 ["Animation","Drama","Fantasy","Romance"]),
    ("Braveheart",                ["Action","Biography","Drama"]),
    ("Gladiator",                 ["Action","Adventure","Drama"]),
    ("Top Gun: Maverick",         ["Action","Drama"]),
    ("Mission: Impossible  Fallout", ["Action","Adventure","Thriller"]),
    ("Mad Max: Fury Road",        ["Action","Adventure","Sci-Fi"]),
    ("Get Out",                   ["Horror","Mystery","Thriller"]),
    ("A Quiet Place",             ["Drama","Horror","Sci-Fi","Thriller"]),
    ("It",                        ["Horror"]),
    ("Saving Private Ryan",       ["Drama","History","War"]),
    ("Dunkirk",                   ["Action","Drama","History","Thriller","War"]),
    ("1917",                      ["Drama","History","War"]),
    ("Whiplash",                  ["Drama","Music"]),
    ("La La Land",                ["Drama","Music","Romance"]),
]

# 
# 3. ESTRUCTURAS DE DATOS PROPIAS
# 

#  3a. TABLA HASH PROPIA 
class TablaHash:
    """
    Tabla hash con encadenamiento (chaining).
    Permite busqueda O(1) promedio por nombre exacto o parcial.
    """
    def __init__(self, capacidad=2048):
        self.capacidad = capacidad
        self.tabla     = [[] for _ in range(capacidad)]
        self.total     = 0

    def _hash(self, clave: str) -> int:
        """Funcion hash djb2  buena distribucion para strings."""
        h = 5381
        for c in clave.lower():
            h = ((h << 5) + h) + ord(c)
        return h % self.capacidad

    def insertar(self, item) -> None:
        idx = self._hash(item.nombre)
        for par in self.tabla[idx]:
            if par[0] == item.nombre.lower():
                return                         # duplicado, no insertar
        self.tabla[idx].append((item.nombre.lower(), item))
        self.total += 1

    def buscar_exacto(self, nombre: str):
        """Devuelve el item con ese nombre exacto, o None."""
        idx = self._hash(nombre)
        for clave, item in self.tabla[idx]:
            if clave == nombre.lower():
                return item
        return None

    def buscar_parcial(self, termino: str) -> list:
        """Recorre todos los cubos y devuelve items cuyo nombre contiene el termino."""
        termino = termino.lower()
        resultados = []
        for cubo in self.tabla:
            for clave, item in cubo:
                if termino in clave:
                    resultados.append(item)
        return resultados

    def factor_carga(self) -> float:
        return self.total / self.capacidad


#  3b. ARBOL BINARIO DE BUSQUEDA (BST) 
class NodoBST:
    def __init__(self, item):
        self.item       = item
        self.izquierda  = None
        self.derecha    = None

class BST:
    """
    BST ordenado alfabeticamente por nombre.
    Permite busqueda O(log n) promedio, O(n) peor caso.
    """
    def __init__(self):
        self.raiz = None

    def insertar(self, item) -> None:
        self.raiz = self._insertar(self.raiz, item)

    def _insertar(self, nodo, item):
        if nodo is None:
            return NodoBST(item)
        if item.nombre.lower() < nodo.item.nombre.lower():
            nodo.izquierda = self._insertar(nodo.izquierda, item)
        elif item.nombre.lower() > nodo.item.nombre.lower():
            nodo.derecha   = self._insertar(nodo.derecha,   item)
        return nodo

    def buscar_prefijo(self, prefijo: str) -> list:
        """Devuelve todos los items cuyo nombre empieza con el prefijo."""
        prefijo = prefijo.lower()
        resultados = []
        self._buscar_prefijo(self.raiz, prefijo, resultados)
        return resultados

    def _buscar_prefijo(self, nodo, prefijo, resultados):
        if nodo is None:
            return
        nombre = nodo.item.nombre.lower()
        if nombre.startswith(prefijo):
            resultados.append(nodo.item)
            # Puede haber coincidencias en ambos lados
            self._buscar_prefijo(nodo.izquierda, prefijo, resultados)
            self._buscar_prefijo(nodo.derecha,   prefijo, resultados)
        elif prefijo < nombre:
            self._buscar_prefijo(nodo.izquierda, prefijo, resultados)
        else:
            self._buscar_prefijo(nodo.derecha,   prefijo, resultados)

    def inorden(self) -> list:
        """Devuelve todos los items ordenados alfabeticamente."""
        result = []
        self._inorden(self.raiz, result)
        return result

    def _inorden(self, nodo, result):
        if nodo is None: return
        self._inorden(nodo.izquierda, result)
        result.append(nodo.item)
        self._inorden(nodo.derecha,   result)


#  3c. GRAFO DE SIMILITUD 
class GrafoSimilitud:
    """
    Grafo no dirigido donde cada nodo es un titulo y
    las aristas conectan titulos que comparten generos.
    Representacion: lista de adyacencia con dict.
    """
    def __init__(self):
        self.adyacencia = {}   # nombre_lower  [(vecino_item, peso)]

    def agregar_nodo(self, item) -> None:
        key = item.nombre.lower()
        if key not in self.adyacencia:
            self.adyacencia[key] = []

    def agregar_arista(self, item_a, item_b, peso: float) -> None:
        a, b = item_a.nombre.lower(), item_b.nombre.lower()
        self.adyacencia[a].append((item_b, peso))
        self.adyacencia[b].append((item_a, peso))

    def vecinos_top(self, nombre: str, n: int = 5) -> list:
        """Devuelve los n vecinos mas similares (mayor peso) de un nodo."""
        key = nombre.lower()
        if key not in self.adyacencia:
            return []
        vecinos = self.adyacencia[key]
        vecinos_ord = sorted(vecinos, key=lambda x: (-x[1], -x[0].calificacion))
        return [item for item, _ in vecinos_ord[:n]]

    @staticmethod
    def similitud(a, b) -> float:
        """Jaccard sobre generos: |A  B| / |A  B|."""
        sa = set(g.lower() for g in a.generos_raw)
        sb = set(g.lower() for g in b.generos_raw)
        inter = len(sa & sb)
        union = len(sa | sb)
        return inter / union if union else 0.0

    @classmethod
    def construir(cls, items: list, umbral: float = 0.25):
        """
        Construye el grafo conectando pares con similitud >= umbral.
        Para 1000 items hace ~500k comparaciones  rapido en Python.
        """
        g = cls()
        for item in items:
            g.agregar_nodo(item)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                sim = cls.similitud(items[i], items[j])
                if sim >= umbral:
                    g.agregar_arista(items[i], items[j], sim)
        return g


#  3d. PILA DE HISTORIAL 
class PilaHistorial:
    """
    Pila (LIFO) para guardar el historial de busquedas de la sesion.
    Implementada sobre lista de Python sin usar collections.deque.
    """
    def __init__(self):
        self._datos = []

    def push(self, entrada: dict) -> None:
        self._datos.append(entrada)

    def pop(self):
        return self._datos.pop() if self._datos else None

    def peek(self):
        return self._datos[-1] if self._datos else None

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0

    def __len__(self) -> int:
        return len(self._datos)

    def todas(self) -> list:
        return list(reversed(self._datos))   # mas reciente primero


# 
# 4. CLASES DE DOMINIO
# 
class Contenido:
    def __init__(self, nombre, generos_raw, calificacion, es_adultos=False):
        self.nombre = nombre
        self.generos_raw = [g.strip() for g in
                            generos_raw.replace(';', ',').split(',') if g.strip()]
        self.calificacion = float(calificacion) if calificacion else 0.0
        self.es_adultos   = es_adultos

    def __lt__(self, other):
        return self.nombre < other.nombre

    def pertenece_a(self, principal, sub):
        tags = JERARQUIA.get(principal, {}).get(sub, [])
        return any(t.lower() in g.lower() or g.lower() in t.lower()
                   for t in tags for g in self.generos_raw)

    def puntaje_afinidad(self, gustados, no_gustados):
        """Score: +1 por cada tag que coincide con lo gustado, -1 con lo no gustado."""
        score = 0.0
        for tag in gustados:
            if any(tag.lower() in g.lower() or g.lower() in tag.lower()
                   for g in self.generos_raw):
                score += 1.0
        for tag in no_gustados:
            if any(tag.lower() in g.lower() or g.lower() in tag.lower()
                   for g in self.generos_raw):
                score -= 1.5
        return score

class Videojuego(Contenido):
    def __init__(self, nombre, generos_raw, calificacion, precio, steam_deck, reviews, owners, es_adultos=False):
        super().__init__(nombre, generos_raw, calificacion, es_adultos)
        self.precio     = precio
        self.steam_deck = steam_deck
        self.reviews    = reviews
        self.owners     = owners

class Pelicula(Contenido):
    def __init__(self, nombre, generos_raw, calificacion, duracion, sinopsis, es_adultos=False):
        super().__init__(nombre, generos_raw, calificacion, es_adultos)
        self.duracion = duracion
        self.sinopsis = sinopsis

# 
# 5. CARGA DE DATOS
# 
def cargar_base_datos():
    juegos, peliculas = [], []

    try:
        with open(os.path.join(BASE_DIR, 'steam_games_2026.csv'), encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 8: continue
                nombre      = row[1].strip()
                generos_raw = f"{row[3].strip()},{row[4].strip()}"
                try:    score = float(row[7]) / 10.0
                except: score = 7.0
                precio = row[5] if len(row) > 5 else "0.0"
                deck   = row[9] if len(row) > 9 else "Unknown"
                adult  = any(x in generos_raw.lower() for x in
                             ['sexual content','nudity','hentai','nsfw','adult','gambling'])
                reviews = row[8].strip() if len(row) > 8 else "0"
                owners  = row[10].strip() if len(row) > 10 else "?"
                juegos.append(Videojuego(nombre, generos_raw, score, precio, deck, reviews, owners, adult))
    except FileNotFoundError:
        print("ADVERTENCIA:  No se encontro steam_games_2026.csv")

    try:
        with open(os.path.join(BASE_DIR, 'imdb_top_1000.csv'), encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 7: continue
                nombre   = row[1].strip()
                duracion = row[4].strip()
                generos  = row[5].strip()
                try:    calif = float(row[6])
                except: continue
                sinopsis = row[7].strip() if len(row) > 7 else "Sin sinopsis."
                adult    = any(x in generos for x in ['Horror','Thriller'])
                peliculas.append(Pelicula(nombre, generos, calif, duracion, sinopsis, adult))
    except FileNotFoundError:
        print("ADVERTENCIA:  No se encontro imdb_top_1000.csv")

    return juegos, peliculas

# 
# 6. HELPERS UI
# 
def elegir(opciones, mensaje):
    print(f"\n{mensaje}")
    for i, op in enumerate(opciones, 1):
        print(f"  {i:2d}. {op}")
    while True:
        try:
            idx = int(input("\nIngresa numero: ")) - 1
            if 0 <= idx < len(opciones):
                return opciones[idx]
            print(f"  Opcion invalida. Ingresa un numero entre 1 y {len(opciones)}.")
        except ValueError:
            print(f"  Entrada invalida. Ingresa un numero entre 1 y {len(opciones)}.")

def mostrar_resultados(heap, top_n=5):
    if not heap:
        print("\nNo se encontraron resultados.")
        return
    print("\n" + "=" * 65)
    rank = 1
    while heap and rank <= top_n:
        _, item = heapq.heappop(heap)
        print(f"\n  #{rank}  {item.nombre}")
        print(f"   Calificacion: {item.calificacion:.1f}/10")
        if isinstance(item, Videojuego):
            precio_txt = "Gratis" if item.precio in ("0", "0.0", "0.00") else f"${item.precio}"
            print(f"   Precio: {precio_txt}  | Steam Deck: {item.steam_deck}")
            try:
                rev_txt = f"{int(item.reviews):,}".replace(",", ".")
            except:
                rev_txt = item.reviews
            print(f"   Resenas: {rev_txt}  | Propietarios est.: {item.owners}")
            print(f"   Tags: {', '.join(item.generos_raw[:8])}")
        else:
            print(f"   Duracion: {item.duracion}")
            print(f"   Sinopsis: {item.sinopsis[:160]}...")
        print("-" * 65)
        rank += 1

# 
# 7. BUSQUEDA POR NOMBRE
# 
def buscar_por_nombre(base, es_mayor, tabla_hash, bst):
    base_nombres = set(i.nombre.lower() for i in
                       (base if es_mayor else [i for i in base if not i.es_adultos]))

    termino = input("\nIngresa el nombre (o parte del nombre): ").strip()
    if not termino:
        print("Busqueda vacia."); return

    # Busqueda exacta O(1) con hash
    exacto = tabla_hash.buscar_exacto(termino)
    if exacto and exacto.nombre.lower() in base_nombres:
        print(f"\n>> Coincidencia exacta encontrada:")
        mostrar_resultados([(-exacto.calificacion, exacto)], top_n=1)
        return

    # Busqueda por prefijo con BST + parcial con hash
    por_prefijo = [i for i in bst.buscar_prefijo(termino)
                   if i.nombre.lower() in base_nombres]
    por_hash    = [i for i in tabla_hash.buscar_parcial(termino)
                   if i.nombre.lower() in base_nombres]
    vistos      = set(i.nombre for i in por_prefijo)
    resultados  = por_prefijo + [i for i in por_hash if i.nombre not in vistos]

    if not resultados:
        print(f"\nNo se encontro '{termino}' en la base de datos.")
        return

    top_n = min(20, len(resultados))
    heap = []
    for item in resultados:
        heapq.heappush(heap, (-item.calificacion, item))
    print(f"\n>> {len(resultados)} resultado(s) para '{termino}'  mostrando top {top_n}:")
    mostrar_resultados(heap, top_n=top_n)

# 
# 8. RECOMENDADOR POR GENEROS (menu jerarquico)
# 
def recomendar_por_genero(base, es_mayor, tipo):
    base_f  = base if es_mayor else [i for i in base if not i.es_adultos]
    raices  = GENEROS_JUEGOS if tipo == "1" else GENEROS_PELICULAS

    principal = elegir(raices, "-- GENERO PRINCIPAL")
    if not principal: return

    subs = list(JERARQUIA.get(principal, {}).keys())
    sub  = elegir(subs, f"-- SUBGENERO de '{principal}' ")
    if not sub: return

    heap = []
    for item in base_f:
        if item.pertenece_a(principal, sub):
            heapq.heappush(heap, (-item.calificacion, item))

    top_n = min(20, len(heap))
    print(f"\n=== TOP {top_n}  {principal.upper()} > {sub.upper()}")
    mostrar_resultados(heap, top_n=top_n)

# 
# 9. RECOMENDADOR POR PREFERENCIAS (anclas)
# 
def _calcular_heap(base_f, pesos_tags, tags_negativos, nombres_excluidos):
    """
    Construye el heap de recomendaciones usando pesos por tag.
    pesos_tags  : dict {tag: peso_acumulado}  (tags gustados/conocidos)
    tags_negativos: list de tags que no gustan
    """
    heap = []
    for item in base_f:
        if item.nombre.lower() in nombres_excluidos:
            continue

        score = 0.0
        # Sumar pesos de tags positivos
        for tag, peso in pesos_tags.items():
            if any(tag.lower() in g.lower() or g.lower() in tag.lower()
                   for g in item.generos_raw):
                score += peso
        # Penalizar tags negativos
        for tag in tags_negativos:
            if any(tag.lower() in g.lower() or g.lower() in tag.lower()
                   for g in item.generos_raw):
                score -= 2.0

        if score > 0:
            score_final = score * 2 + item.calificacion
            heapq.heappush(heap, (-score_final, item))
    return heap


def recomendar_por_preferencias(base, es_mayor, tipo):
    import random
    from collections import Counter

    base_f = base if es_mayor else [i for i in base if not i.es_adultos]
    anclas = (ANCLAS_JUEGOS_MAYOR if es_mayor else ANCLAS_JUEGOS_MENOR) if tipo == "1" \
             else (ANCLAS_PELIS_MAYOR if es_mayor else ANCLAS_PELIS_MENOR)

    tipo_txt   = "juego" if tipo == "1" else "pelicula"
    accion_txt = "jugado" if tipo == "1" else "visto"

    muestra = random.sample(anclas, min(5, len(anclas)))

    print(f"\n>> Se evaluaran 5 {tipo_txt}s famosos.")
    print("   Responde:")
    print("   s  = lo conozco y me gusto  (pedira intensidad del 1 al 5)")
    print("   n  = lo conozco y NO me gusto")
    print("   k  = lo conozco pero no lo he " + accion_txt)
    print("   ?  = no lo conozco\n")

    #  Mejora 1 & 2: intensidad + conteo de frecuencia de tags 
    # contador_positivo acumula peso por tag segun intensidad declarada
    contador_positivo = Counter()   # tag  peso total
    contador_negativo = []          # tags negativos (lista plana)
    contador_conocido = Counter()   # tag  peso leve (0.3 por aparicion)
    nombres_excluidos = set()

    for nombre_ancla, tags in muestra:
        while True:
            resp = input(f"  '{nombre_ancla}'  [s/n/k/?]: ").strip().lower()
            if resp in ("s", "n", "k", "?"):
                break
            print("   Respuesta invalida. Ingresa: s, n, k o ?")

        if resp == "s":
            nombres_excluidos.add(nombre_ancla.lower())
            # Pedir intensidad 1-5
            while True:
                try:
                    intensidad = int(input(f"     Cuanto te gusto '{nombre_ancla}'? (1=poco  5=mucho): "))
                    if 1 <= intensidad <= 5:
                        break
                    print("     Ingresa un numero entre 1 y 5")
                except ValueError:
                    print("     Ingresa un numero entre 1 y 5")
            # Cada tag gana peso = intensidad; si el tag ya aparecio antes
            # (frecuencia) el Counter lo acumula automaticamente
            for tag in tags:
                contador_positivo[tag] += intensidad

        elif resp == "n":
            nombres_excluidos.add(nombre_ancla.lower())
            contador_negativo.extend(tags)

        elif resp == "k":
            for tag in tags:
                contador_conocido[tag] += 0.3   # interes leve

        # "?"  ignorar

    if not contador_positivo and not contador_negativo and not contador_conocido:
        print("\n No diste ninguna respuesta util. Intenta de nuevo.")
        return

    # Unir pesos: positivos con su peso + conocidos con peso leve
    pesos_totales = Counter(contador_positivo)
    for tag, peso in contador_conocido.items():
        pesos_totales[tag] += peso

    # Mostrar perfil de gustos detectado
    if pesos_totales:
        top_tags = pesos_totales.most_common(5)
        print("\n>> Perfil de gustos detectado:")
        for tag, peso in top_tags:
            barras = "#" * int(peso) + "-" * max(0, 5 - int(peso))
            print(f"     {barras}  {tag}  (peso: {peso:.1f})")

    print("\n>> Calculando recomendaciones...")
    heap = _calcular_heap(base_f, pesos_totales, contador_negativo, nombres_excluidos)

    if not heap:
        print("\nNo se encontraron recomendaciones. Intenta explorar por genero.")
        return

    #  Mejora 3: ronda de refinamiento 
    # Mostrar top 5 y preguntar cual llama la atencion
    print(f"\n=== PRIMERA RONDA - TOP 5 RECOMENDACIONES ===")
    heap_copia = list(heap)
    mostrar_resultados(list(heap_copia), top_n=5)

    # Extraer top 5 reales del heap para refinamiento
    import heapq as _hq
    heap_temp = list(heap_copia)
    _hq.heapify(heap_temp)
    top5_items = []
    for _ in range(min(5, len(heap_temp))):
        _, it = _hq.heappop(heap_temp)
        top5_items.append(it)

    # Si 3 o mas resultados eran desconocidos, repetir con nuevas anclas
    print("\n>> De estos 5 resultados, cuantos conocias previamente?")
    while True:
        try:
            conocidos_rec = int(input("   Titulos que ya conocias (0-5): "))
            if 0 <= conocidos_rec <= 5:
                break
            print("   Ingresa un numero entre 0 y 5.")
        except ValueError:
            print("   Ingresa un numero entre 0 y 5.")

    if (5 - conocidos_rec) >= 3:
        print(f"\n>> {5 - conocidos_rec} de 5 recomendaciones eran desconocidas.")
        print("   Reiniciando con una nueva seleccion de titulos de referencia...")
        recomendar_por_preferencias(base, es_mayor, tipo)
        return

    # Refinamiento opcional
    print("\n>> Refinamiento opcional:")
    print("   Escribe parte del nombre del titulo que mas te llamo la atencion")
    print("   (o presiona Enter para omitir):")
    refinamiento = input("  >> ").strip()

    if not refinamiento:
        return

    candidato = None
    for it in top5_items:
        if refinamiento.lower() in it.nombre.lower():
            candidato = it
            break

    if not candidato:
        print("  No se encontro el titulo ingresado.")
        return

    pesos_refinados = Counter(pesos_totales)
    for tag in candidato.generos_raw:
        pesos_refinados[tag] += 3.0

    nombres_excluidos.add(candidato.nombre.lower())

    print(f"\n  >> Refinando basado en '{candidato.nombre}'...")
    heap2 = _calcular_heap(base_f, pesos_refinados, contador_negativo, nombres_excluidos)

    if not heap2:
        print("\nNo se encontraron mas recomendaciones refinadas.")
        return

    print(f"\n=== SEGUNDA RONDA - RECOMENDACIONES REFINADAS ===")
    mostrar_resultados(heap2, top_n=5)


# 
# 10. FILTRO DE PRECIO (juegos)
# 
def filtrar_por_precio(base_juegos):
    print("\nFiltro de precio:")
    print("  1. Solo gratuitos (Free to Play)")
    print("  2. Menos de $10")
    print("  3. Menos de $30")
    print("  4. Cualquier precio")
    def precio_float(j):
        try: return float(j.precio)
        except: return 999.0
    while True:
        op = input("Opcion (1-4): ").strip()
        if   op == "1": return [j for j in base_juegos if precio_float(j) == 0.0]
        elif op == "2": return [j for j in base_juegos if precio_float(j) < 10.0]
        elif op == "3": return [j for j in base_juegos if precio_float(j) < 30.0]
        elif op == "4": return base_juegos
        else: print("  Opcion invalida. Ingresa 1, 2, 3 o 4.")


# 
# 11. BUSQUEDA POR MULTIPLES GENEROS
# 
def buscar_multigenero(base, es_mayor, tipo):
    base_f  = base if es_mayor else [i for i in base if not i.es_adultos]
    raices  = GENEROS_JUEGOS if tipo == "1" else GENEROS_PELICULAS

    print("\n>> BUSQUEDA POR MULTIPLES GENEROS")
    print("   Selecciona hasta 3 generos. Solo apareceran titulos que pertenezcan a todos.")

    generos_elegidos = []
    for ronda in range(1, 4):
        print(f"\n-- Genero {ronda} de 3 (Enter para terminar)")
        principal = elegir(raices, "GENERO PRINCIPAL")
        if not principal: break
        subs = list(JERARQUIA.get(principal, {}).keys())
        sub  = elegir(subs, f"SUBGENERO de '{principal}'")
        if not sub: break
        generos_elegidos.append((principal, sub))
        if ronda < 3:
            mas = input("\nAgregar otro genero? (s/n): ").strip().lower()
            if mas != "s": break

    if not generos_elegidos:
        print("No se selecciono ningun genero."); return

    # Interseccion: el item debe pertenecer a TODOS los generos elegidos
    heap = []
    for item in base_f:
        if all(item.pertenece_a(p, s) for p, s in generos_elegidos):
            heapq.heappush(heap, (-item.calificacion, item))

    desc = " + ".join(f"{s}" for _, s in generos_elegidos)
    total = len(heap)
    if total == 0:
        print(f"\nNo hay titulos que combinen: {desc}")
        return

    top_n = min(20, total)
    print(f"\n=== TOP {top_n}  {desc.upper()}")
    mostrar_resultados(heap, top_n=top_n)


# 
# 12. COMPARADOR DE TITULOS
# 
def comparar_titulos(base, es_mayor, tabla_hash):
    base_nombres = set(i.nombre.lower() for i in
                       (base if es_mayor else [i for i in base if not i.es_adultos]))

    print("\n>> COMPARADOR DE TITULOS")
    t1 = input("  Nombre del primer titulo: ").strip()
    t2 = input("  Nombre del segundo titulo: ").strip()

    item1 = tabla_hash.buscar_exacto(t1)
    item2 = tabla_hash.buscar_exacto(t2)

    # Si no es exacto, buscar parcial
    if not item1:
        res = tabla_hash.buscar_parcial(t1)
        res = [r for r in res if r.nombre.lower() in base_nombres]
        item1 = res[0] if res else None
    if not item2:
        res = tabla_hash.buscar_parcial(t2)
        res = [r for r in res if r.nombre.lower() in base_nombres]
        item2 = res[0] if res else None

    if not item1:
        print(f"  No se encontro '{t1}'"); return
    if not item2:
        print(f"  No se encontro '{t2}'"); return

    g1 = set(g.lower() for g in item1.generos_raw)
    g2 = set(g.lower() for g in item2.generos_raw)
    comunes   = g1 & g2
    solo_en_1 = g1 - g2
    solo_en_2 = g2 - g1
    sim = len(comunes) / len(g1 | g2) if (g1 | g2) else 0

    print("\n" + "=" * 65)
    print(f"  Comparacion: {item1.nombre}  vs  {item2.nombre}")
    print("=" * 65)
    print(f"   Calificacion   : {item1.calificacion:.1f}/10  vs  {item2.calificacion:.1f}/10")

    if isinstance(item1, Videojuego) and isinstance(item2, Videojuego):
        print(f"   Precio         : ${item1.precio}  vs  ${item2.precio}")
        print(f"   Steam Deck     : {item1.steam_deck}  vs  {item2.steam_deck}")
    elif isinstance(item1, Pelicula) and isinstance(item2, Pelicula):
        print(f"   Duracion       : {item1.duracion}  vs  {item2.duracion}")

    print(f"\n  Generos en comun ({len(comunes)}):")
    print(f"     {', '.join(sorted(comunes)[:8]) if comunes else 'Ninguno'}")
    print(f"\n  Exclusivo de '{item1.nombre[:25]}' ({len(solo_en_1)}):")
    print(f"     {', '.join(sorted(solo_en_1)[:6]) if solo_en_1 else ''}")
    print(f"\n  Exclusivo de '{item2.nombre[:25]}' ({len(solo_en_2)}):")
    print(f"     {', '.join(sorted(solo_en_2)[:6]) if solo_en_2 else ''}")
    print(f"\n  Similitud Jaccard: {sim:.0%}")
    print("=" * 65)


# 
# 13. SIMILARES (grafo)
# 
def buscar_similares(base, es_mayor, tabla_hash, grafo):
    base_nombres = set(i.nombre.lower() for i in
                       (base if es_mayor else [i for i in base if not i.es_adultos]))
    termino = input("\nIngresa el titulo del que deseas ver similares: ").strip()
    item = tabla_hash.buscar_exacto(termino)
    if not item:
        res = tabla_hash.buscar_parcial(termino)
        res = [r for r in res if r.nombre.lower() in base_nombres]
        item = res[0] if res else None
    if not item:
        print(f"  No se encontro '{termino}'"); return

    similares = [v for v in grafo.vecinos_top(item.nombre, n=10)
                 if v.nombre.lower() in base_nombres]

    if not similares:
        print(f"\n No se encontraron titulos similares a '{item.nombre}'.")
        return

    print(f"\n>> TITULOS SIMILARES A '{item.nombre.upper()}'")
    heap = [(-v.calificacion, v) for v in similares]
    heapq.heapify(heap)
    mostrar_resultados(heap, top_n=min(5, len(similares)))


# 
# 14. HISTORIAL DE SESION
# 
def mostrar_historial(historial):
    if historial.esta_vacia():
        print("\n No hay busquedas en el historial todavia.")
        return
    print("\nHISTORIAL DE SESION (mas reciente primero)")
    print("=" * 65)
    for i, entrada in enumerate(historial.todas(), 1):
        print(f"\n  #{i}  {entrada['contexto']}")
        for titulo in entrada['resultados']:
            print(f"        {titulo}")
    print("=" * 65)


# 
# 15. FLUJO PRINCIPAL
# 
def iniciar_recomendador():
    print("=========================================")
    print("  RECOMENDADOR MULTIMEDIA - ESTRUCTURAS DE DATOS")
    print("=========================================\n")

    juegos, peliculas = cargar_base_datos()
    print(f">> Cargados: {len(juegos)} juegos | {len(peliculas)} peliculas")

    #  Construir estructuras de datos 
    print(">> Construyendo estructuras de datos...")
    hash_juegos   = TablaHash(); bst_juegos   = BST()
    hash_pelis    = TablaHash(); bst_pelis    = BST()
    for j in juegos:
        hash_juegos.insertar(j); bst_juegos.insertar(j)
    for p in peliculas:
        hash_pelis.insertar(p);  bst_pelis.insertar(p)

    print(">> Construyendo grafo de similitud (esto puede tomar unos segundos)...")
    grafo_juegos = GrafoSimilitud.construir(juegos,   umbral=0.25)
    grafo_pelis  = GrafoSimilitud.construir(peliculas, umbral=0.20)
    print(f"   - Juegos: {sum(len(v) for v in grafo_juegos.adyacencia.values())//2} conexiones")
    print(f"   - Peliculas: {sum(len(v) for v in grafo_pelis.adyacencia.values())//2} conexiones")

    historial = PilaHistorial()

    #  Edad 
    try:    edad = int(input("\nIngresa tu edad: "))
    except: edad = 17
    es_mayor = edad >= 18
    print(">> Modo seguro activado (menor de edad)" if not es_mayor else ">> Acceso completo habilitado")

    #  Loop principal 
    while True:
        print("\n" + "" * 43)
        print("Que deseas hacer?")
        print("  1. Videojuegos")
        print("  2. Peliculas")
        print("  0. Salir")
        tipo = input("Opcion: ").strip()

        if tipo == "0":
            break
        if tipo not in ("1", "2"):
            print("  Opcion invalida. Ingresa 1, 2 o 0."); continue

        base       = juegos     if tipo == "1" else peliculas
        tabla_hash = hash_juegos if tipo == "1" else hash_pelis
        bst        = bst_juegos  if tipo == "1" else bst_pelis
        grafo      = grafo_juegos if tipo == "1" else grafo_pelis
        tipo_txt   = "Videojuegos" if tipo == "1" else "Peliculas"

        # Filtro de precio solo para juegos
        base_filtrada = base
        if tipo == "1":
            base_f_edad = base if es_mayor else [i for i in base if not i.es_adultos]
            while True:
                aplicar_precio = input("\nFiltrar por precio? (s/n): ").strip().lower()
                if aplicar_precio in ("s", "n"):
                    break
                print("  Respuesta invalida. Ingresa s o n.")
            if aplicar_precio == "s":
                base_filtrada = filtrar_por_precio(base_f_edad)
                print(f"  >> {len(base_filtrada)} juegos en ese rango de precio.")

        print(f"\nComo deseas explorar {tipo_txt}?")
        print("  1. Buscar por nombre")
        print("  2. Explorar por genero")
        print("  3. Multiples generos")
        print("  4. Recomendacion personalizada")
        modo = input("Opcion (1-4): ").strip()

        if   modo == "1": buscar_por_nombre(base_filtrada, es_mayor, tabla_hash, bst)
        elif modo == "2": recomendar_por_genero(base_filtrada, es_mayor, tipo)
        elif modo == "3": buscar_multigenero(base_filtrada, es_mayor, tipo)
        elif modo == "4": recomendar_por_preferencias(base_filtrada, es_mayor, tipo)
        else:             print("  Opcion invalida. Ingresa un numero entre 1 y 4.")

    # Resumen al salir
    if not historial.esta_vacia():
        print(f"\n>> Realizaste {len(historial)} busqueda(s) en esta sesion.")
        ver = input("Ver resumen de busquedas antes de salir? (s/n): ").strip().lower()
        if ver == "s":
            mostrar_historial(historial)

    print("\nGracias por usar el Recomendador Multimedia. Hasta luego.\n")

if __name__ == "__main__":
    iniciar_recomendador()