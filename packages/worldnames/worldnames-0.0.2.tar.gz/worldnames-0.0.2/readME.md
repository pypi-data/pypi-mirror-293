Random name generator.
Random email generator.
Random age generator. 

## Doel van het programma
Als developer wil je soms je database populeren met gebruikers om testen uit te voeren of een MVP te demonstreren of je hebt simpelweg
gewoon een random voornaam, achternaam, gender, email of leeftijd nodig. Met dit programma kan je MySQL of SQLite database populeren met gebruikers of de module gebruiken om een eigen populatie programma te maken.

# Installation manual

1. Clone the repository (**required**)

```commandline
git clone https://github.com/ayoub-abdessadak/worldnames.git
```

2. Create a python virtual environment (**optional**)
```commandline
python -m venv worldnames
```
3. Activate the python virtual environment (**optional**)
```commandline
source worldnames/bin/activate
```

4. Navigate to the repository and install the required packages (**required**)
```commandline
pip install -r requirments.txt
```
5. Run the population simulator 
```commandline
python populate.py
```

Or use the worldnames module to populate you're database:
```python
import worldnames

worldnames.full_name() # returns 'Ashanti Qjtkbyh' for example. Type is a string.

worldnames.first_name() # returns 'Teodor' for example. Type is a string.

worldnames.last_name() # returns 'Pmgnwzqls' for example. Type is a string.

worldnames.age() # returns 50 for example. Type is an int.

worldnames.gender() # returns male for example. Type is a string.

worldnames.email() # returns 'Ashanti.Qjtkbyh@gmail.com' for example. Type is a string.

worldnames.email('Ashanti', 'Qjtkby') # It is possible to pass a first_name and last_name to the email method.

worldnames.user() # Returns all the attributes above in a tuple, for example: ('Cuauhtémoc', 'Sfzn', 'Woman', 88, 'Cuauhtémoc.Sfzn@outlook.com'). Type is an tuple.
```
