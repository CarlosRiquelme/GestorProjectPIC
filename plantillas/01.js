var etiquetas = new Array();
var valores = new Array();
for (var gradoX=0; gradoX<=360; gradox+=30){
    radianX = gradoX*Math.PI/180;
    radianY = Math.cos(gradoX);
    etiquetas.push(radianX.toFixed(3));
    valores.push(radianY);
}

var Datos = {
    labels : etiquetas,
    datasets : [{
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "rgba(220,220,220,0.8)",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "fff",
        pointHighlighFill : "fff",
        pointHighliStroke : "rgba(220,220,220,1)",
        data : valores
      }]
}
var contexto = document.getElementById("canvas").getContext("2d");
window.Linea = new Chart(contexto).Line(Datos);
