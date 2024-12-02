

document.addEventListener('DOMContentLoaded', () => {
    
    const undoButton = document.getElementById("undo-button");
    const saveButton = document.getElementById("save-button");
    const deleteButton = document.getElementById("delete-button");
    const drawButton = document.getElementById("draw-button");

    drawButton.addEventListener("click", saveCoords);
    undoButton.addEventListener("click", goBack);
    saveButton.addEventListener("click", saveCoords);

    loadCoords()
     

     // Ajustar el canvas si la ventana cambia de tamaño
     window.onresize = ajustarCanvas;

     // Ajustar el canvas al cargar la página
     window.onload = ajustarCanvas;
});

var coordsList = [];

function ajustarCanvas() {
    const img = document.getElementById("tile");
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
    canvas.style.position = "absolute";
}

function obtenerCoordenadas(event) {
    const imgElement = document.getElementById("tile");
    let srcArray = imgElement.src.split('/');
    let fileName = srcArray[srcArray.length - 1];
    let tileName = fileName.split('.')[0];

    console.log("Nombre del tile: " + tileName);
    // Obtener las coordenadas relativas a la imagen
    const x = event.offsetX;
    const y = event.offsetY;


    console.log(`Coordenadas: X=${x}, Y=${y}`);
    coordsList.push({ 
        tile: tileName,
        x: x, 
        y: y 
    });

    drawSquare()
}


function drawSquare(){

    let currentTile = document.getElementById("tile-name-input");
  

    // Obtener el canvas y su contexto
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    // Limpiar el canvas antes de dibujar
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dibujar un cuadrado en cada punto de coordsList
    coordsList.forEach(point => {
        if (point.tile == currentTile.value) {
            ctx.fillStyle = "#FF0000";
            ctx.fillRect(point.x - 2.5, point.y - 2.5, 5, 5); 
        }
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
                const { x, y, tile } = item;
                    coordsList.push({ x: parseFloat(x), y: parseFloat(y), tile: tile });
            });
            console.log(coordsList); 
        })
        .catch(error => console.error('Error al cargar el archivo JSON:', error));
}