django_cyberpunk
================

<h4>private game database <a href="http://django-nonrel.org" target="_blank">django nonrel</a> web app for <a href="https://cloud.google.com/appengine/" target="_blank">Google App Engine</a>: Cyberpunk</h4>

<hr />
<br />
<p><b><i>Since I used <a href="https://djangoappengine.readthedocs.io/en/latest/" target="_blank">djangoappengine</a>, which is a 3rd party tweaked library of django to be compatible with <a href="https://cloud.google.com/appengine/" target="_blank">Google App Engine</a>, some features such as JOINS relationship within database are disabled. So I had to invent customized way to substitute aggregations and summations which Django originally provides.</i></b></p>

<p><b>** Major Design Update **</b><br />
Applied some of user requests and provided a gorgeous frame with jQuery UI,  <a href="http://packery.metafizzy.co" target="_blank">Packery.js</a> and <a href="http://draggabilly.desandro.com" target="_blank">Draggabilly.js</a>. Here is <a href="http://cyberpunktest.appspot.com" target="_blank"> What it looks like.</a><br />
Oh, I used <a href="http://www.theokamecke.com/functional_detail.php?cat_id=46" target="_blank">Theo Kamecke's Eiffel Dream</a> for the entrance image of the webpage because I thought that it matches the mood of database(the box part) of cyberpunk.</p>

<p><b>Description:</b></p>

<b>cyberpunk/admin.py:</b> admins can edit any attributes of any game character including bonus points and IP, which players can't modify. Admin can also lock a character to limit add/edit certain attributes.

<b>cyberpunk/models.py:</b> all necessary models are related to the character model via foreign key so that a character can have several items in the same category. (e.g. several weapons can be equipped while only one armor for each body part and only one vehicle can be equipped.) IP is editable only by admins via django admin site and contactpts(Contact Points) are automatically calculated based on a character's contact attributes by Character model method collect_contactpts used in views.py and admin.py

<b>cyberpunk/forms.py:</b> all models are using modelform for their new entries or changes. 

<b>cyberpunk/views.py:</b> I used some lists for vars to reduce duplicate of same structures. However, since Python assigns different memory places for a variable and the same variable in a list, I had to type some of the duplicates for the form variables for rendering to the template of method charedit. Any equipment that can be equipped and anything except Statistics, money, residence can be added/edited/deleted on the character page directly. Some features are limited to be able to be edited only by admins. When a user tries to edit those features, the system sends an edit request email to an admin instead. After admin locked a character, user cannot add/edit certain character attributes but request admin to do that by sending email with detailed information.


<b>templates/:</b> I used .djhtml for all the template pages for better highlighting on emacs.

<b>settings.py:</b> nothing much special from basic dependancies such as admin dependancies and django-nonrel dependancies.

<b>urls.py:</b> It has all url address redirection information according to the views.py methods.
 
 ***Last updated in February 17th, 2017***
