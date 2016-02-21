# GameStore

**NOTE: the software has a pure educational purpose**

## Team
**Armano Giovanni** (Giova805)

**di Girolamo Luigi** (luispdm)

**Geniola Alberto** (albertogeniola)

## Description
We developed an online Game Store for _JavaScript_ games.
According to the Django framework, the website follows the **MVC** pattern.

There are two kind of users: developers and players. A player can purchase games from the Store and play those he owns, while a developer can upload games, manage his inventory and see sales statistics. The payment service was provided by the **Aalto University** and is a mockup one.

When somebody tries to register, he needs to activate his account by clicking on a link that provides an unique activation token (UUID4). The e-mail actually is not sent (because we did not have an e-mail server), so the registration is practically impossible; but the DB is prefilled with 100 users.

The website also provides a per-game leaderboard.
If a guest does not want to register to our website, he can login with his Facebook account.

The software was deployed on the Heroku Platform (PAAS) at the address: _http://fast-badlands-87500.herokuapp.com/_

JetBrains PyCharm used to developed it through the Git version control provided by the university.

Language used: **HTML5, CSS (with bootstrap), Django framework on Python 3.5.**

## Models
The DB schema can be found in the _Model.mdj_ (or exported as _model.svg_) inside the folder _docs_.

## Views

### Profile related
_register user, login, logout, list purchased games, buy/play/search game_

### Developer related
_add/edit/delete game from own inventory, sales statistics, list games of own inventory_

### SavedGame related
_save game state, load game state_

### PlayedMatch related
_list high scores, record player score_

### Additional features related
_save game, load game, resolution setting, 3rdparty login, 3rd party sharing, own JavaScript game, RESTful API, responsive design,_

## Minimum functional requirements

#### Register as a player and developer 

**Done, we use the permission mechanism so in the future we can enable and/or developer independently.**

#### As a developer:

**add games to their inventory, see list of game sales**

Done, a developer can add a new game with a description, logo, category and price to his inventory and he has a feedback of sales thanks to a chart and diagram
#### As a player:

**buy games, play games, see game high scores and record their score to it**

Done, we implemented a simple cart in order to allow the user to buy multiple games at the same time. thanks to the leaderborad he can see his score compare to the ones of other player when is playing or on the Leaderboard page (control to prevent double purchase are performed).

#### Authentication

**Login, logout and register (both as player or developer). Use _Django auth_**

Done, we use _Django auth_. We implemented some other checks so that an user who's already logged in cannot login again. Plus the login, logout and register, we give the chance to the user to reset the password (when he's performing the login) or change it(in the account page).

The activation process has been implemented by generating a token (**UUID4**) saved into the DB at registration time. At that time user's active flag (Django's standard) is set to false, and that is set to true when he perform the activation (we use the console in order to get the token because we haven't a mail server).

#### Basic player functionalities

**Buy games, payment is handled by a mockup payment service (http://payments.webcourse.niksula.hut.fi/) :**

Done, we redirect the user on the payment website after he confirm the order that his shown in the cart.

**Play games. See also game/service interaction**

Done, users can play games, save, load and submit scores. Also we implemented the setting message protocol.

**Security restrictions, e.g. player is only allowed to play the games they’ve purchased.**

Done, an user can play only at the games that he had purchased. By our implementation a developer can't play. This is not an architectural restriction; from our prespective was better to keep the roles separeted.

**Also consider how your players will find games (are they in a category, is there a search functionality?)**

Done, we developed a page in which we show the game list. This list is paginated (each of 10 games).  The user can sort it (by popularity, price, name or category) or filter it by gategory and/or name. This has been implemented using a RESTful service (ajax). The reason why we did this is that the gamelist may be very long and it is better to load selective data, when requested by the user.

#### Basic developer functionalities

Done, developers may add games into the system. However we check that there is no other game with the same name/url, in order to prevent ambiguities. The _URL_ has to be absolute.
Basic game inventory and sales statistics (how many of the developers' games have been bought and when)

Done. To do that, we needed to save redundant data on the date of orders in order to facilitate aggregation features. We make full usage of aggregation/group-by ORM feature, without using db-specific SQL, so any DB supported by the ORM can be used. On the client side, we used javascript library called chart.js, that takes care of graph drawings. We also used ajax requests to filter data and to update the graphs.

**Security restrictions, e.g. developers are only allowed to modify/add/etc. their own games, developer can only add games to their own inventory, etc.**

Done, we checked developer can only deal with his own games. From our perspective a developer should not be able to play games, and he needs a separate account. So we perform this kind of checks as well. If the developer cancels the game, every record related to that game is deleted as well, causing a cascade reaction. This may be unsafe in case of orders and statistics (retroactive reactions are possible), however there was no requirement for that feature, so we decided to go for this way.

#### Game/service interaction

When player has finished playing a game (or presses submit score), the game sends a postMessage to the parent window containing the current score. This score must be recorded to the player's scores and to the global high score list for that game. See section on Game Developer Information for details.

Done. Contextually to the classic messages to be handled we also provide support for the settings message. Messages to be sent to the service are processed by ajax so the user experience is preserved.
Messages from service to the game must be implemented as well

Done, used postMessage as requested.
	
#### Quality of Work

**Quality of code (structure of the application, comments).**

We've put much effort to provide a project structure that meets the stanrdards. Django and Python were frameworks completely new for us, so we do not have much experience to say our code is perfect. However we've put as much effort we could in order to meet the requirements.
	
**Purposeful use of framework (Don't-Repeat-Yourself principle, Model-View-Template separation of concerns)**

We followed the tips we were given during the lectures. For instance we tried to use ModelForm instead of Forms when possible and at the same time we provided custom to_json_dict() functions to the models in order to quickly present "safe" data to the user.

**User experience (styling, interaction)**

We took inspiration from Steam when possible and we ensured the look-and-feel of the entire application was ok. Also we checked the website is easily accessible by non experts (provided images, buttons and intuitive functions). We also made sure the website is accessible via handled/mobile touch devices.
	
#### Meaningful testing

We applied both manual and automated tests to ensure all the features work correctly. Tests have been run with Selenium (chrome and firefox) for the frontend and unittest for models basic checks. We also validated each webpage against HTML5 W3C validator.

#### Non-functional requirements
	
**Overall documentation, demo, teamwork, and project management as seen from the history of your GitLab project (and possible other sources that you submit in your final report)**

We have been taking track of the project structure, expecially for models by using STAR-UML software. This also allowed us to produce cool _HTML5_ documentation pages and a class diagram documentation. The rest of the documentation work has been done inline with the code. We've been meeting regularly on week base to define the structure of the project and we performed late-coding. Late coding was performed almost all together in parallalel as reflected by the commit hystory. We tried to follow the new project plan in order to separate duties and during late coding we helped one-another in order to balance the workload of each one.
	
## More Features

We implemented chart support alongside statistics. Also we took care of some default django auth "problems", like the possibility to login again with a different user if already logged in. We used the user_passes_test middlaware to check wether a user can access some views.

We also implemented custom migrations in order to populate the DB.
When needed we made use of transaction so our DB status is always consistent.

#### Save/load and resolution feature

**The service supports saving and loading for games with the simple message protocol described in Game Developer Information**

Done, both save/load and resolution support. At the moment we always accept the resolution provided by the game, with constraints with maximum/minimum window bounds.

#### 3rd party login (0-100 points)

**Allow OpenID, Gmail or Facebook login to your system. This is the only feature where you are supposed to use third party Django apps in your service.**

We used the python-social-auth plugin, that enables multiple providers. We focused only on facebook login but simple modifications are needed in order to support multiple providers. This required us to develop a custom pipeline step in order to assign a profile to the social user upon first login.

#### RESTful API

Design and Implement some _RESTful API_ to the service
E.g. showing available games, high scores, showing sales for game developers (remember authentication)

We provided restful api for listing and searching games into our system. This API is public, so there was no authentication required. This service is even used internally by some our templates/views. 

The api provided supports versioning alongside a simple hierarchy for categories/games. Other than that, we implemented search functionality via the same API.

#### Own game

**Develop a simple game in JavaScript that communicates with the service (at least high score, save, load)**

Done! The game is working well!

#### Mobile Friendly

Attention is paid to usability on both traditional computers and mobile devices (smart phones/tablets)
We used bootstrap framework and paid attention to the grid system in order to provide responsivness. We tested the website on Full HD desktops, 13inches notebooks, 10 inches tablet and 4 inches smartphones. On every device we had a good user experience.		

#### Social media sharing

**Enable sharing games in some social media site (Facebook, Twitter, Google+, etc.)**

We focused on metadata as requested and for this feature weused the classic facebook API. We refused to use the same access_token of the social-auth: we wanted to separate permissions requested by the app to facebook framework. Doing that, the social app only needs 'email' permission.