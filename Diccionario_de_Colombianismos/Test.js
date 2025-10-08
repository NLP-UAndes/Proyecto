import DictionaryRepository from './DictionaryRepository.js';
import * as fs from 'fs'; // Módulo de Node.js para escribir archivos

// Alfabeto español, incluyendo la Ñ
const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÑ'.split('');
const DICTIONARY_ID = "642af684da699a2968ef1d19";

// -----------------------------------------------------------
// FUNCIÓN DE EXTRACCIÓN
// -----------------------------------------------------------
function extractEntryData(entry) {
    const lema = entry.lemmaSign;
    let definicion = 'Definición no encontrada.';
    let ejemplo = 'Ejemplo no encontrado.';
    
    // Normalizar la 'acepcion'
    const acepciones = Array.isArray(entry.acepcion) 
        ? entry.acepcion 
        : (entry.acepcion ? [entry.acepcion] : []);

    // Extraer solo la primera acepción
    if (acepciones.length > 0) {
        const primeraAcepcion = acepciones[0];
        
        // 1. EXTRACCIÓN DE LA DEFINICIÓN (Solución final para la API)
        if (primeraAcepcion.definicion) {
            let defData = primeraAcepcion.definicion;

            // Prioridad 1: Estructura de objeto con propiedad 'definicion'
            if (defData && defData.definicion) { 
                definicion = defData.definicion;
            }
            // Prioridad 2: Es un array con un objeto que tiene 'texto'
            else if (Array.isArray(defData) && defData.length > 0 && defData[0].texto) {
                definicion = defData[0].texto;
            } 
            // Prioridad 3: Es un objeto directo con la propiedad 'texto'
            else if (defData && defData.texto) {
                definicion = defData.texto;
            } 
            // Prioridad 4: Es una cadena directa
            else if (typeof defData === 'string') {
                definicion = defData;
            }
        }

        // 2. EXTRACCIÓN DEL EJEMPLO
        if (primeraAcepcion.ejemplo) {
            // Ejemplo encontrado en 'ejemplo.ejemplo'
            if (primeraAcepcion.ejemplo.ejemplo) {
                ejemplo = primeraAcepcion.ejemplo.ejemplo;
            } else if (typeof primeraAcepcion.ejemplo === 'string') {
                ejemplo = primeraAcepcion.ejemplo;
            }
        }
    }
    
    return `\n**PALABRA:** ${lema}\n**SIGNIFICADO:** ${definicion}\n**EJEMPLO:** ${ejemplo}\n------------------------------\n`;
}

// -----------------------------------------------------------
// FUNCIÓN PARA GUARDAR EN DISCO (Node.js)
// -----------------------------------------------------------
function saveTextFile(content, filename) {
    try {
        // Escribe el contenido en el disco. El archivo se guardará en la misma carpeta donde ejecutas el script.
        fs.writeFileSync(filename, content, 'utf8');
        console.log(`\nArchivo '${filename}' guardado con éxito en el disco.`);
    } catch (err) {
        console.error("Error al guardar el archivo:", err);
    }
}


// -----------------------------------------------------------
// FUNCIÓN PRINCIPAL
// -----------------------------------------------------------
async function init() {
    const repo = new DictionaryRepository();
    
    let outputText = "--- Diccionario de Colombianismos (DICOL) - Extracción Completa ---\n";

    console.log("Iniciando carga y acumulación de datos...");
    
    for (const letter of ALPHABET) {
        const header = `\n==============================================\n| ENTRADAS QUE EMPIEZAN CON: ${letter} |\n==============================================\n`;
        outputText += header;
        console.log(`Cargando entradas con: ${letter}`);

        try {
            // Llama a la API para obtener las entradas de la letra actual
            const entries = await repo.fetchDictionaryEntries(DICTIONARY_ID, letter, 'api');
            
            if (entries.length === 0) {
                outputText += `\nNo se encontraron entradas para la letra ${letter}.\n`;
                continue;
            }

            // Procesa y añade el texto a la variable outputText
            entries.forEach(entry => {
                outputText += extractEntryData(entry);
            });
            
        } catch (error) {
            const errorMsg = `Error al cargar entradas para la letra ${letter}: ${error.message || error}\n`;
            outputText += errorMsg;
            console.error(errorMsg);
        }
    }
    
    // PASO FINAL: Guardar en el disco
    const filename = "diccionario_colombianismos.txt";
    saveTextFile(outputText, filename);
    
    console.log("\nProceso de extracción de diccionario completado.");
}

init();