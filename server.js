const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

// Middleware para manejar datos JSON
app.use(express.json());

// Servir archivos estáticos (HTML, CSS, JS)
app.use(express.static('public'));

// Endpoint para obtener el contenido de un archivo
app.get('/archivos/:filename', (req, res) => {
    const filePath = path.join(__dirname, 'archivos', req.params.filename);
    res.sendFile(filePath);
});

// Endpoint para ejecutar un archivo de Python
app.post('/ejecutar', (req, res) => {
    const file = req.body.file; // Nombre del archivo enviado desde el frontend
    const filePath = path.join(__dirname, 'archivos', file); // Ruta completa del archivo

    // Ejecutar el archivo de Python
    exec(`python ${filePath}`, (error, stdout, stderr) => {
        if (error) {
            // Si hay un error, devolver el mensaje de error
            return res.json({ error: stderr });
        }
        // Si no hay errores, devolver la salida del archivo
        res.json({ output: stdout });
    });
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);
});
