L=['signup.html','login.html','home.html','admin.html','book_tickets.html','logout.html', 'profile.html','create_venue.html','show_venue.html','update_venue.html','delete_venue.html','create_shows.html','show_shows.html','update_shows.html','delete_shows.html']

for x in L:
    y=x
    y=['a.html','b.html']
    to_write=["{% extends 'base.html' %}\n",
          '{% block title %}',y[0],'{% endblock %}\n',
          ' {% block content %}\n\n',
          '{% endblock %}']
    # f = open(x, "w")
