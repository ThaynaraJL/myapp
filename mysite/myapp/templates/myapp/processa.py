
{% if pontos %}
		
	{% for p in pontos %}
		<h3>pontos:{{ p }}</h3>
		
	{% endfor %}
{%else %}
	<h3>Não passou a variavel - pontos</h3>
{% endif %}

{% if criar_poligono %}
	poligono:{{criar_poligono}}
{%else %}
	<h3>Não passou a variavel - criar_poligono</h3>
{% endif %}
