<template>

<head_text class="frontTo"> 
  <h1 class="frontTo">Quiénes somos</h1>
  <big_img class="frontTo">
    <p>Por medio de esta página podrá saber aquellas zonas que están en peligro de inundación, y qué acciones llevar a cabo según el área en el que se encuentre. Entre éstas se encuentran los recorridos de evacuación y puntos de encuentro cercanos a su localidad.
    <br>
    También podrá redactar una denuncia en caso de encontrar basurales o alcantarillas tapadas.
  </p>
  </big_img>

  <h3>Inundación de La Plata 2013</h3>
  <big_img class="frontTo">
      <p>La inundación en La Plata de 2013 ocurrió el 2 de abril de 2013, con un registro de precipitaciones en la región con más de 400 mm acumulados en cuatro horas. Las ciudades de Ensenada y Berisso y los barrios platenses de Los Hornos, Villa Elvira y Tolosa fueron los más afectados junto al casco céntrico de la ciudad.</p>

  <h4>Plan de Gestión Integrada de Riesgos de Desastres</h4>
  <p> La Universidad Nacional de La Plata junto con la Universidad Tecnológica Nacional propusieron un Plan de Gestión Integrada de Riesgos de Desastres (GRID), y crearon la colección Emergencia Hídrica dentro del Servicio de Difusión de la Creación Intelectual, el repositorio institucional de la UNLP, para reunir trabajos (artículos, informes técnicos, libros y otros) que contribuyan al desarrollo del plan y sirvan como base de datos para futuros trabajos en el área.</p>
  </big_img>
  
</head_text>

<content>
  
	<br>
	<line_cards class="frontTo">
		<card_box class="frontTo">
			<card class="frontTo"><router-link to="/puntos_y_recorridos"><h3>Puntos y recorridos</h3>
       <img class="imagen_tarjeta" src="../assets/punto_recorrido.png" alt="mapa_punto_recorrido">
       <p>Puntos de encuentro en caso de inundaciones y recorridos de evacuación para llegar a éstos.</p>
      </router-link></card>
      <card class="frontTo"><router-link :to="{name:'zonas_inundables', params: {page: 1}}"><h3>Zonas inundables</h3>
      <img class="imagen_tarjeta" src="../assets/zona.png" alt="mapa_punto_recorrido">
      <p> Informate sobre las zonas de la ciudad que están en riesgo de inundacion. </p>
      </router-link></card>
      <card class="frontTo"><router-link :to="{ name: 'denuncia', params: { page: 1 } }"><h3>Realizar denuncias</h3>
       <img class="imagen_tarjeta" src="../assets/denuncia.png" alt="mapa_punto_recorrido">
       <p> Prevení inundaciones al realizar denuncias sobre lugares peligrosos de tu ciudad.</p>
      </router-link></card>
		</card_box>
	</line_cards>
</content>
<br>

  
</template>


