import DictionaryRepository from './DictionaryRepository.js';
import * as fs from 'fs'; // Módulo de Node.js para escribir archivos

// Alfabeto español, incluyendo la Ñ
const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÑ'.split('');
const DICTIONARY_ID = "642af684da699a2968ef1d19";

function primeraAcepcionExtract(acepcion){
    let definicion = 'Definición no encontrada.';
    let ejemplo = 'Ejemplo no encontrado.';

    if (!acepcion) {
        return { definicion, ejemplo };
    }

    // 1. EXTRACCIÓN DE LA DEFINICIÓN
    // La definición puede ser un string, un objeto con 'texto', un objeto con 'definicion', o un array.
    if (acepcion.definicion) {
        let defData = acepcion.definicion;

        if (typeof defData === 'string') {
            definicion = defData;
        } else if (defData.texto) {
            definicion = defData.texto;
        } else if (defData.definicion) {
            // A veces la definición está anidada: { definicion: { definicion: "texto" } }
            if (typeof defData.definicion === 'string') {
                definicion = defData.definicion;
            } else if (defData.definicion.definicion) {
                definicion = defData.definicion.definicion;
            }
        } else if (Array.isArray(defData) && defData.length > 0 && defData[0].texto) {
            definicion = defData[0].texto;
        }
    }

    // 2. EXTRACCIÓN DEL EJEMPLO
    // El ejemplo puede ser un string, un objeto con 'ejemplo', o un array.
    if (acepcion.ejemplo) {
        let ejData = acepcion.ejemplo;

        if (typeof ejData === 'string') {
            ejemplo = ejData;
        } else if (ejData.ejemplo) {
            // Puede ser un objeto { ejemplo: "texto" } o un array [{ ejemplo: "texto" }]
            if (typeof ejData.ejemplo === 'string') {
                ejemplo = ejData.ejemplo;
            } else if (Array.isArray(ejData.ejemplo) && ejData.ejemplo.length > 0) {
                ejemplo = ejData.ejemplo[0];
            }
        } else if (Array.isArray(ejData) && ejData.length > 0) {
            // Puede ser un array de strings o de objetos
            if (typeof ejData[0] === 'string') {
                ejemplo = ejData[0];
            } else if (ejData[0].ejemplo) {
                ejemplo = ejData[0].ejemplo;
            }
        }
    }

    return { definicion, ejemplo };
}

// -----------------------------------------------------------
// FUNCIÓN PARA GUARDAR ENTRY COMO JSON (Individual)
// -----------------------------------------------------------
function saveEntryAsJson(entry) {
    if (!entry || !entry.lemmaSign) {
        console.error("No se puede guardar el entry: objeto inválido.");
        return;
    }
    // Crea un nombre de archivo seguro a partir del lema
    const safeLemma = entry.lemmaSign.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const filename = `entry_${safeLemma}.json`;
    try {
        // Convierte el objeto a un string JSON formateado
        const jsonContent = JSON.stringify(entry, null, 2);
        fs.writeFileSync(filename, jsonContent, 'utf8');
        console.log(`Entry para '${entry.lemmaSign}' guardado en ${filename}`);
    } catch (err) {
        console.error(`Error al guardar el JSON del entry '${entry.lemmaSign}':`, err);
    }
}

// -----------------------------------------------------------
// FUNCIÓN DE EXTRACCIÓN (REFACTORIZADA)
// -----------------------------------------------------------
function extractEntryData(entry) {
    // Si la entrada no tiene lema, no podemos procesarla.
    if (!entry || !entry.lemmaSign) {
        return ''; 
    }

    const lema = entry.lemmaSign;

    // CASO 1: 'acepcion' es un array, indica múltiples definiciones distintas.
    if (Array.isArray(entry.acepcion)) {
        let output = '';
        // Iteramos sobre cada acepción para crear un registro por cada una.
        for (const acepcion of entry.acepcion) {
            const { definicion, ejemplo } = primeraAcepcionExtract(acepcion);

            const finalDefinicion = (typeof definicion === 'string') ? definicion : JSON.stringify(definicion);
            const finalEjemplo = (typeof ejemplo === 'string') ? ejemplo : JSON.stringify(ejemplo);

            output += `\n**PALABRA:** ${lema}\n**SIGNIFICADO:** ${finalDefinicion.trim()}\n**EJEMPLO:** ${finalEjemplo.trim()}\n------------------------------\n`;
        }
        return output;
    }

    // CASO 2: 'SubEntrada' es un array, indica múltiples definiciones distintas.
    if (Array.isArray(entry.SubEntrada)) {
        let output = '';
        // Iteramos sobre cada SubEntrada para crear un registro por cada una.
        for (const sub of entry.SubEntrada) {
            if (sub.acepcion) {
                // Tomamos la primera acepción de esta SubEntrada.
                const acepcion = Array.isArray(sub.acepcion) ? sub.acepcion[0] : sub.acepcion;
                const { definicion, ejemplo } = primeraAcepcionExtract(acepcion);

                const finalDefinicion = (typeof definicion === 'string') ? definicion : JSON.stringify(definicion);
                const finalEjemplo = (typeof ejemplo === 'string') ? ejemplo : JSON.stringify(ejemplo);

                output += `\n**PALABRA:** ${lema}\n**SIGNIFICADO:** ${finalDefinicion.trim()}\n**EJEMPLO:** ${finalEjemplo.trim()}\n------------------------------\n`;
            }
        }
        return output;
    }

    // CASO GENERAL: Se busca una única definición principal (cuando no hay arrays).
    let primeraAcepcion = null;

    // Búsqueda de la acepción principal.
    if (entry.acepcion) { // 'acepcion' es un objeto único
        primeraAcepcion = entry.acepcion;
    } else if (entry.SubEntrada && entry.SubEntrada.acepcion) { // 'SubEntrada' es un objeto único.
        primeraAcepcion = Array.isArray(entry.SubEntrada.acepcion) ? entry.SubEntrada.acepcion[0] : entry.SubEntrada.acepcion;
    }

    // Si no encontramos ninguna acepción, no hay nada que mostrar.
    if (!primeraAcepcion) {
        return '';
    }

    // --- Extracción y formato para la acepción única encontrada ---
    const { definicion, ejemplo } = primeraAcepcionExtract(primeraAcepcion);
    
    // Limpieza final de los textos extraídos
    const finalDefinicion = (typeof definicion === 'string') ? definicion : JSON.stringify(definicion);
    const finalEjemplo = (typeof ejemplo === 'string') ? ejemplo : JSON.stringify(ejemplo);

    return `\n**PALABRA:** ${lema}\n**SIGNIFICADO:** ${finalDefinicion.trim()}\n**EJEMPLO:** ${finalEjemplo.trim()}\n------------------------------\n`;
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
// FUNCIÓN PARA GUARDAR TODAS LAS ENTRADAS EN UN SOLO JSON
// -----------------------------------------------------------
function saveAllEntriesAsJson(entries, filename) {
    try {
        const jsonContent = JSON.stringify(entries, null, 2);
        fs.writeFileSync(filename, jsonContent, 'utf8');
        console.log(`\nTodas las entradas guardadas con éxito en '${filename}'.`);
    } catch (err) {
        console.error("Error al guardar el archivo JSON completo:", err);
    }
}

// -----------------------------------------------------------
// FUNCIÓN PRINCIPAL
// -----------------------------------------------------------
async function init() {
    const repo = new DictionaryRepository();
    
    let outputText = "--- Diccionario de Colombianismos (DICOL) - Extracción Completa ---\n";
    let allEntries = []; // Array para acumular todas las entradas

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
            
            // Acumula las entradas en el array general
            allEntries.push(...entries);

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
    
    // PASO FINAL: Guardar los archivos en el disco
    const textFilename = "diccionario_colombianismos.txt";
    saveTextFile(outputText, textFilename);

    // const jsonFilename = "diccionario_colombianismos_completo.json";
    // saveAllEntriesAsJson(allEntries, jsonFilename);
    
    console.log("\nProceso de extracción de diccionario completado.");
}

init();