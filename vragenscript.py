# Alle benodigde libraries importeren na ze gedownload te hebben
import sympy as smp
import random as rt

# Symbolen definen van ten voren. Deze zijn globaal. String waardes van x zijn niet het symbool en iterables met de waarde x zorgen voor een crash
x = smp.Symbol('x', real=True)

# Hier komen alle functies die integreer vragen maken en ze doorgeven aan de checker
''' Machtsregel vragen:
∫ax^b dx = a/b * x^(b + 1) + c
'''
def machtsregel_vragen(difficulty='Beginner'): # Beginner wordt standaard gedefined indien er iets fout gaat
  if difficulty == 'Beginner':
    highest_waarde = 10 # Hoogste random waarde, is inclusive. Geldt voor elke functie
    highest_macht = 5   # Hoogste macht waarde, is inclusive. Geldt voor elke functie
    kans = 6            # De kans dat je een breuk krijgt. Geldt voor elke functie met een breuk optie

  elif difficulty == 'Medium':
    highest_waarde = 30
    highest_macht = 15
    kans = 4

  elif difficulty == 'Hard':
    highest_waarde = 100
    highest_macht = 30
    kans = 2

  else:
    highest_waarde = 10
    highest_macht = 5
    kans = 6

  noemer = rt.randint(1, highest_waarde)                                     # De noemer en/of coëfficiënt. De teller is er alleen als je een breuk krijgt. Deze is willekeurig
  macht = rt.randint(1, highest_macht)                                       # De macht waarde, deze is willekeurig
  breuk_of_normaal = rt.choice(['Breuk'] * (10 - kans) + ['Normaal'] * kans) # Kijkt of je een breuk hebt of niet

  if breuk_of_normaal == 'Breuk':                                            # Is er een breuk, dan zit er een breuk in je gegeven functie
    teller = rt.randint(1, highest_waarde)                                   # Bij een breuk hoort een teller
    return smp.Rational(noemer, teller)*x**macht

  return noemer*x**macht
''' Machtsregel vragen '''
#------------------------------#
''' Logaritmische vragen:
∫ log(ax^b, g) dx = ∫ ln(ax^b) / ln(g) dx = (xln(ax^b) - bx) / ln(g)
'''
def log_vragen(difficulty='Beginner'):
  if difficulty == 'Beginner':
    highest_coëfficiënt = 10
    highest_grondtal = 12  # Logaritme hebben grondtallen, dus vandaar
    highest_macht = 5
    kans = 6

  elif difficulty == 'Medium':
    highest_coëfficiënt = 30
    highest_grondtal = 25
    highest_macht = 15
    kans = 4

  elif difficulty == 'Hard':
    highest_coëfficiënt = 100
    highest_grondtal = 60
    highest_macht = 30
    kans = 2

  else:
    highest_waarde = 10
    highest_macht = 5
    kans = 6

  coëfficiënt = rt.randint(1, highest_coëfficiënt)
  macht = rt.randint(1, highest_macht)
  log_of_ln = rt.choice(['Log'] * (10 - kans) + ['Ln'] * kans)

#if log_of_ln == 'Ln':                           # Bij code geldt dat het natuurlijke logaritme ln(x) = log(x), dus dat moet handmatig gecheckt worden. Hiervoor ben ik te lui dus geen ln
#return smp.log(coëfficiënt*x**macht, e)

  grondtal = rt.randint(1, highest_grondtal)
  return smp.log(coëfficiënt*x**macht, grondtal)
''' Logaritmische vragen '''
#------------------------------#
''' Natuurlijk getal e vragen '''
def e_vragen(difficulty='Beginner'):
  if difficulty == 'Beginner':
    highest_waarde = 10
    highest_macht = 5
    kans = 6

  elif difficulty == 'Medium':
    highest_waarde = 30
    highest_macht = 15
    kans = 4

  elif difficulty == 'Hard':
    highest_waarde = 100
    highest_macht = 30
    kans = 2

  else:
    highest_waarde = 10
    highest_macht = 5
    kans = 6

  noemer = rt.randint(1, highest_waarde)
  teller = rt.randint(1, highest_waarde)
  macht = rt.randint(1, highest_macht)
  breuk_of_normaal = rt.choice(['Breuk'] * (10 - kans) + ['Normaal'] * kans)
  if breuk_of_normaal == 'Breuk':
    return smp.Rational(noemer, teller)*smp.exp(x*macht)

  return noemer*smp.exp(x*macht)

''' Natuurlijk getal e vragen '''
#------------------------------#
''' Meerdereterm vragen
Alle voorgaande vragen, maar dan willekeurig
'''
def meerderetermen_vragen(difficulty='Beginner'):
  if difficulty == 'Beginner':
    highest_aantal = 2

  elif difficulty == 'Medium':
    highest_aantal = 5

  elif difficulty == 'Hard':
    highest_aantal = 8

  else:
    highest_aantal = 2

  waarde = 0
  aantal = 0

  while aantal < highest_aantal:
    aantal += 1
    keuzes = [machtsregel_vragen(difficulty), e_vragen(difficulty), log_vragen(difficulty)]
    waarde += rt.choice(keuzes)

  return waarde
''' Meerdereterm vragen '''
    waarde += rt.choice(keuzes)

  return waarde
''' Meerdereterm vragen '''

# Hier komt een functie die een keuze maakt op basis van database informatie. De informatie zal een array zijn met alle foutsoorten die de leerling heeft en daarmee wordt een kans genomen
def keuze(informatie, difficulty):
  opties = [machtsregel_vragen(difficulty), e_vragen(difficulty), log_vragen(difficulty), meerderetermen_vragen(difficulty)]
  kans = [functie * opties[ind] for ind, functie in enumerate(informatie)]

  return rt.choice(kans)

# Hier komt een functie die het antwoord nakijkt op basis van de eerder gekozen functie
API_request = ''
#gekozen_functie = keuze(API_request, 'Beginner') # Dit wordt naar de PHP gestuurt en ook gecheckt door de code hier

def check(gekozen, antwoord):
  try:
    juist = smp.integrate(gekozen) # Berekent de juiste integraal
    constante = True
    leerling_antwoord = ''.join(value if not value.isalpha() or value not in 'abdefghijklmnopqrstuvwyz' else 'c' for value in leerling.lower()) # Zorgt voor de juiste constante

    if 'c' not in leerling_antwoord: # Kijkt of er een constante is
      constante = False

    leerling_smp = smp.sympify(leerling_antwoord.replace('^', '**')) # Zet het om naar een sympy vergelijking. Hieronder wordt de juiste variabele toegediend en de constante weggehaald
    leerling = smp.simplify(leerling_smp - smp.Symbol('c')).subs('x', x) # Zat hier een goed uur op vast. Antwoord van een leerling maakt de x een str en niet de pre-defined x variabele

    if leerling != juist:  # Eerste waarde is om te kijken of je de vraag goed hebt, 2e of er een constante is
      return False, constante

    return True, constante

  except Exception as exc:
    print(f'Er is iets fout gegaan, vraag wordt fout gerekend en niks wordt geüpdate')
    return False, None, True # Hier is een derde waarde voor als er een foutmelding is. Om die reden is de 2e onbekent want er kan niet gekeken worden voor een constante
