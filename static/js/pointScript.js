
document.addEventListener('DOMContentLoaded', () => {
    
    const undoButton = document.getElementById("undo-button");
    const saveButton = document.getElementById("save-button");

    undoButton.addEventListener("click", goBack);
    saveButton.addEventListener("click", saveCoords);

    ajustarCanvas();
    loadCoords(drawSquare);
    window.onscroll = () =>{
        ajustarCanvas();
        drawSquare();
    } 

     // Ajustar el canvas si la ventana cambia de tamaño
     window.onresize = () =>{
        ajustarCanvas();
        drawSquare();
    } 

     updatePenguinCount()
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
    canvas.style.top = `${rect.top + window.scrollY}px`;
    canvas.style.left = `${rect.left + window.scrollX}px`;
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
        class: 0,
        x_center: x, 
        y_center: y,
        width: 30,
        height: 30,
        tile: tileName,
    });

    drawSquare()
    updatePenguinCount()
    saveCoords() 
}


function drawSquare(){
    let currentTile = document.getElementById("tile-name-input");
    // Obtener el canvas y su contexto
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    // Limpiar el canvas antes de dibujar
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    coordsList.forEach(point => {
        if (point.tile == currentTile.value) {
            // Calcular la esquina superior izquierda de la caja
            const x_start = point.x_center - point.width / 2;
            const y_start = point.y_center - point.height / 2;

            // Establecer el estilo de relleno
            ctx.strokeStyle = "#FF0000";
            ctx.lineWidth = 2;

            // Dibujar la caja
            ctx.strokeRect(x_start, y_start, point.width, point.height);

        }
    });
  
}

// Aquí solo rellenamos el campo oculto del formulario con las coordenadas
function saveCoords() {
    const coordsInput = document.getElementById('coords-input');
    coordsInput.value = JSON.stringify(coordsList);
}


function goBack(){
    coordsList.pop();
    drawSquare();
   
}




function loadCoords(callback) {
    const coordsListElement = document.getElementById('coords-list');
    const coordText = coordsListElement.textContent.trim();

    // Reemplazar ObjectId y comillas simples por comillas dobles
    const jsonText = coordText
        .replace(/ObjectId\(/g, '')
        .replace(/\)/g, '')
        .replace(/'/g, '"');

    // Parsear el texto como JSON
    const coordsArray = JSON.parse(jsonText);

    coordsArray.forEach(coord => {
        coordsList.push(coord);
    });

    console.log("Ya se han cargado las coordenadas desde el DOM", coordsList);
    if (callback) {
        callback();
    }
}

function updatePenguinCount() {
    console.log(coordsList.length)
    const penguinCount = document.getElementById("penguin-count");
    penguinCount.textContent = coordsList.length;
    
}