---
layout: default
title: Bio
permalink: /
---

<div class="bio">
  <img class="profile-photo" src="{{ site.photo | relative_url }}" alt="Photo of {{ site.title }}">

  <div class="bio-text">
    <h1>{{ site.title }}</h1>
    <p class="institute"><a href="{{ site.institute.url }}">{{ site.institute.name }}</a></p>

    <p>{{ site.bio }}</p>

    <ul class="links">
      {% for link in site.links %}
      <li><a href="{{ link.url }}">{{ link.label }}</a></li>
      {% endfor %}
    </ul>
  </div>
</div>
