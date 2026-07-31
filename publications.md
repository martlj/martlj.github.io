---
layout: default
title: Scientific Outputs
permalink: /publications/
---

# Scientific Outputs

Below are my 5 most-cited publications, updated automatically from ORCID
and Semantic Scholar.

{% if site.data.publications.last_updated %}
<p class="meta">Last updated: {{ site.data.publications.last_updated }}</p>
{% endif %}

<ol class="publications">
  {% for pub in site.data.publications.items %}
  <li>
    <span class="pub-title">
      {% if pub.link and pub.link != "#" %}
        <a href="{{ pub.link }}">{{ pub.title }}</a>
      {% else %}
        {{ pub.title }}
      {% endif %}
    </span>
    <span class="pub-meta">{{ pub.authors }}{% if pub.year %} · {{ pub.year }}{% endif %}{% if pub.citations %} · {{ pub.citations }} citations{% endif %}</span>
  </li>
  {% endfor %}
</ol>

{% assign orcid_id = site.orcid.id | replace: "https://orcid.org/", "" | replace: "http://orcid.org/", "" | remove: "/" %}
{% if orcid_id %}
<p><a href="https://orcid.org/{{ orcid_id }}">View my full publication list on ORCID &rarr;</a></p>
{% endif %}
