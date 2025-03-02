
ATOM_SYMBOLS = ["","H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Uub","Uut","Uuq","Uup","Uuh","Uus","Uuo"]
ATOM_NAMES = ["","Hydrogen","Helium","Lithium","Beryllium","Boron","Carbon","Nitrogen","Oxygen","Fluorine","Neon","Sodium","Magnesium","Aluminium","Silicon","Phosphorus","Sulfur","Chlorine","Argon","Potassium","Calcium","Scandium","Titanium","Vanadium","Chromium","Manganese","Iron","Cobalt","Nickel","Copper","Zinc","Gallium","Germanium","Arsenic","Selenium","Bromine","Krypton","Rubidium","Strontium","Yttrium","Zirconium","Niobium","Molybdenum","Technetium","Ruthenium","Rhodium","Palladium","Silver","Cadmium","Indium","Tin","Antimony","Tellurium","Iodine","Xenon","Caesium","Barium","Lanthanum","Cerium","Praseodymium","Neodymium","Promethium","Samarium","Europium","Gadolinium","Terbium","Dysprosium","Holmium","Erbium","Thulium","Ytterbium","Lutetium","Hafnium","Tantalum","Tungsten","Rhenium","Osmium","Iridium","Platinum","Gold","Mercury","Thallium","Lead","Bismuth","Polonium","Astatine","Radon","Francium","Radium","Actinium","Thorium","Protactinium","Uranium","Neptunium","Plutonium","Americium","Curium","Berkelium","Californium","Einsteinium","Fermium","Mendelevium","Nobelium","Lawrencium","Rutherfordium","Dubnium","Seaborgium","Bohrium","Hassium","Meitnerium","Darmstadtium","Roentgenium","Copernicium","Nihonium","Flerovium","Moscovium","Livermorium","Tennessine","Oganesson"]
SUBSHELL_NAMES = ["1s","2s","2p","3s","3p","4s","3d","4p","5s","4d","5p","6s","4f","5d","6p","7s","5f","6d","7p"]
SUBSHELL_SIZE = [2,2,6,2,6,2,10,6,2,10,6,2,14,10,6,2,14,10,6]

class Atom:
    def __init__(self, arg):
        if isinstance(arg, int):
            self.z = arg
        elif isinstance(arg, str):
            if arg.capitalize() in ATOM_SYMBOLS:
                self.z = ATOM_SYMBOLS.index(arg.capitalize())
            elif arg.capitalize() in ATOM_NAMES:
                self.z = ATOM_NAMES.index(arg.capitalize())
            
    
    def __str__(self) -> str:
        return "Atom(" + self.symb + ")"
    
    def __repr__(self) -> str:
        return 'Atom("' + self.symb + '")'
    
    def get_symb(self) -> str:
        return ATOM_SYMBOLS[self.z]
    
    def get_name(self) -> str:
        return ATOM_NAMES[self.z]
    
    def get_elec_config(self) -> str:
        i = 0
        j = 0
        S = ""
        for k in range(self.z):
            if j >= SUBSHELL_SIZE[i]:
                S += SUBSHELL_NAMES[i] + ''.join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[int(n)] for n in str(SUBSHELL_SIZE[i])])
                i += 1
                j = 0
            j += 1
        S += SUBSHELL_NAMES[i] + ''.join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[int(n)] for n in str(j)])
        return S

    
    symb = property(get_symb)
    name = property(get_name)
    elec_config = property(get_elec_config)
