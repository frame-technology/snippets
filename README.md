#Snippets


##Original README

Folks who worked at Google may miss snippets at their current employers. Help is at hand.

Every week, the system emails out a reminder email. Users can reply to it with what they did that week. Users can follow other users via the web, as well as following tags, and assigning tags to themselves. All content matching the tags they follow will be mailed to them in a digest every Monday afternoon. In addition, archives for each user and the most recent data for each tag are visible on the web.

It was hard to make this totally portable. You'll probably want to fork and change the application name and hardcoded email addresses, creating your own application on app engine with authentication restricted to your custom domain. I would love patches to core functionality, though.

Little attention has been paid to making this particularly scalable, but it should work for any small or medium company.

---

###Changes by Harper Reed

* Moved to python2.7
* added bootstrap
* separated out logic into different handlers
* moved to micro framework

####Note: remember to add the app engine app to the google apps domain!!


####TODO

* make email template based.

---

###Changes by Frank Harris

* Added support for email aliases (frank@domain.com --> frank.harris@domain.com)
* Moved the organization avatar to settings
* Added support for custom filters/tags
* Added last submitted snippet to reminder email
* Added a final reminder email
* Added an email for people that forgot to submit snippets
* General usability improvements and clean-up
* Moved to Mandrill for sending emails
