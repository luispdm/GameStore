# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def create_games(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("Users", "Profile")
    Category = apps.get_model("Store", "Category")
    Game = apps.get_model("Store", "Game")

    Game.objects.create(name="WSD2015 - NoOp",
                        description="This simple game does nothing, it simply tests the messaging functionality. ",
                        url="http://webcourse.cs.hut.fi/example_game.html",
                        price=0,
                        _category=Category.objects.get(name='Test'),
                        popularity=0,
                        logo="/static/images/no-image-available.jpg",
                        _developer=Profile.objects.get(user=User.objects.get(username='dev97')))

    Game.objects.create(name="Tic-Tac-Toe",
                        description="Try to beat the computer at the oldest game in the world",
                        url="/static/tris.html",
                        price=10,
                        _category=Category.objects.get(name='Puzzle'),
                        popularity=0,
                        logo="http://www.giochi.com/wp-content/uploads/2013/08/390x323xflipped-tac-toe.jpg.pagespeed.ic.I1vpYw7EaD.jpg",
                        _developer=User.objects.get(username='dev96').profile)

    Game.objects.create(name="GTA V",
                        description="Grand Theft Auto is an action-adventure video game series created by David Jones and Mike Dailly;[3] the later titles of which were created by brothers Dan and Sam Houser, Leslie Benzies and Aaron Garbut. It is primarily developed by Rockstar North (formerly DMA Design), and published by Rockstar Games. The name of the series references the term used in the US for motor vehicle theft. Most games in the series are set in fictional locales modelled on American cities, usually either Liberty City, Vice City, or San Andreas, which are stand-ins for New York City, Miami, and the state of California, respectively. The first game encompassed three fictional cities, while subsequent titles tend to emphasise a single city and its outlying areas. Gameplay focuses on an open world where the player can choose missions to progress an overall story, as well as engaging in side activities, all consisting of action-adventure, driving, third-person shooting, occasional role-playing, stealth, and racing elements. The series also has elements of the earlier beat 'em up games from the 16-bit era. The series has gained controversy for its adult nature and violent themes. The series focuses around many different protagonists who attempt to rise through the ranks of the criminal underworld, although their motives for doing so vary in each game. The antagonists are commonly characters who have betrayed the protagonist or his organisation, or characters who have the most impact impeding the protagonist's progress. The series contains satire and humour.[4] British video game developer DMA Design began the series in 1997. as of 2014, it has eleven stand-alone games and four expansion packs. The third chronological title, Grand Theft Auto III, was widely acclaimed, as it brought the series to a 3D setting and more immersive experience, and is considered a landmark title that has subsequently influenced many other open world action games and led to the label \"Grand Theft Auto clone\" on similar games. Subsequent titles would follow and build upon the concept established in Grand Theft Auto III. Film and music veterans have voiced characters, including Ray Liotta, Burt Reynolds, Dennis Hopper, Samuel L. Jackson, Debbie Harry, Phil Collins, Axl Rose, and Peter Fonda.[5] The series has been critically acclaimed and commercially successful, having shipped more than 220 million units, as of September 2015.[6] The Telegraph ranked the GTA series among Britain's most successful exports.[4]",
                        url="http://www.rockstargames.com/grandtheftauto/",
                        price=50,
                        _category=Category.objects.get(name='Adventure'),
                        popularity=10,
                        logo="http://cdn2.knowyourmobile.com/sites/knowyourmobilecom/files/styles/gallery_wide/public/0/67/GTAV-GTA5-Michael-Sweatshop-1280-2277432.jpg?itok=nKEHENTW",
                        _developer=User.objects.get(username='dev96').profile)

    Game.objects.create(name="Gran Turismo 6",
                        description="Gran Turismo 6 is a racing video game developed by Polyphony Digital and published by Sony Computer Entertainment for the PlayStation 3 video game console. It is the sixth major release and twelfth game overall in the Gran Turismo video game series. It was released worldwide on December 6, 2013,[1] and was popular with critics, won awards, and topped charts in countries around the world. New features included the addition of more cars and tracks, improvements to the car customisation options, and partnerships with the Goodwood Festival of Speed, The Ayrton Senna Institute, the FIA and NASA.",
                        url="https://en.wikipedia.org/wiki/Gran_Turismo_6",
                        price=40,
                        _category=Category.objects.get(name='Racing'),
                        popularity=5,
                        logo="https://upload.wikimedia.org/wikipedia/en/f/fc/GranTurismo6.jpg",
                        _developer=User.objects.get(username='dev97').profile)


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_populate_sample_games'),
        ('Users', '0004_populate_sample_users'),
    ]

    operations = [
        migrations.RunPython(create_games),
    ]
