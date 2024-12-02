
document.addEventListener('DOMContentLoaded', () => {
  
    const undoButton = document.getElementById("undo-button");
    const saveButton = document.getElementById("save-button");
    const deleteButton = document.getElementById("delete-button");
    const drawButton = document.getElementById("draw-button");

    drawButton.addEventListener("click", saveCoords);
    undoButton.addEventListener("click", goBack);
    saveButton.addEventListener("click", saveCoords);

    loadCoords()
     // Ajustar el canvas al cargar la página
     window.onload = ajustarCanvas;

     // Ajustar el canvas si la ventana cambia de tamaño
     window.onresize = ajustarCanvas;
});

var coordsList = [];

function ajustarCanvas() {
    const img = document.getElementById("imagen");
    const canvas = document.getElementById("canvas");

    // Ajustar las dimensiones del canvas al tamaño real de la imagen
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;

    // Asegurar el tamaño visual del canvas
    canvas.style.width = `${img.offsetWidth}px`;
    canvas.style.height = `${img.offsetHeight}px`;

    // Posicionar el canvas sobre la imagen
    const rect = img.getBoundingClientRect();
    canvas.style.top = `${rect.top}px`;
    canvas.style.left = `${rect.left}px`;
}

function obtenerCoordenadas(event) {
    // Obtener las coordenadas relativas a la imagen
    const x = event.offsetX;
    const y = event.offsetY;


    console.log(`Coordenadas: X=${x}, Y=${y}`);
    coordsList.push({ x: x, y: y });

    drawSquare()
}


function drawSquare(){
    // Obtener el canvas y su contexto
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    // Limpiar el canvas antes de dibujar
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dibujar un cuadrado en cada punto de coordsList
    coordsList.forEach(point => {
        ctx.fillStyle = "#FF0000";
        ctx.fillRect(point.x, point.y, 10, 10); // Dibuja un cuadrado de 10x10 píxeles
    });
  

}

// Aquí solo rellenamos el campo oculto del formulario con las coordenadas
function saveCoords(event) {
    event.preventDefault();
    const coordsInput = document.getElementById('coords-input');
    coordsInput.value = JSON.stringify(coordsList);
    document.getElementById('coords-form').submit();
}


function goBack(){
    coordsList.pop();
    drawSquare();
}

function loadCoords() {
    fetch('/static/data/coords.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const { x, y } = item;
                    coordsList.push({ x: parseFloat(x), y: parseFloat(y) });
            });
            console.log(coordsList); 
        })
        .catch(error => console.error('Error al cargar el archivo JSON:', error));
}