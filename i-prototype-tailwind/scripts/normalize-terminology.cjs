#!/usr/bin/env node
/**
 * 🔄 Script de Normalisation Terminologique - Phase 2 Catégorie D
 * Selon prompt ultra-précis : Respecter terminologie métier existante
 * 
 * "Capteurs" → "Sondes" (terminologie backend)
 */

const fs = require('fs');
const path = require('path');

const terminologyMap = {
  // Respecter la terminologie backend CHNeoWave
  'Capteur': 'Sonde',
  'capteur': 'sonde',
  'Capteurs': 'Sondes', 
  'capteurs': 'sondes',
  'CAPTEUR': 'SONDE',
  'CAPTEURS': 'SONDES',
  
  // Termes techniques spécifiques
  'sensor': 'sonde', // Conserver en français
  'Sensor': 'Sonde',
  'sensors': 'sondes',
  'Sensors': 'Sondes',
  
  // Interfaces et types (garder cohérence)
  'SensorData': 'SondeData',
  'SensorStatus': 'SondeStatus',
  'SensorConfig': 'SondeConfig',
  'sensorId': 'sondeId',
  'sensor_id': 'sonde_id',
  
  // Messages utilisateur
  'État des Capteurs': 'État des Sondes',
  'Configuration Capteur': 'Configuration Sonde',
  'Sélection Capteur': 'Sélection Sonde'
};

const excludePatterns = [
  /node_modules/,
  /\.git/,
  /dist/,
  /build/,
  /coverage/,
  /\.min\./,
  /package-lock\.json/,
  /yarn\.lock/
];

const includeExtensions = ['.ts', '.tsx', '.js', '.jsx', '.json', '.md'];

function shouldProcessFile(filePath) {
  // Exclure certains patterns
  if (excludePatterns.some(pattern => pattern.test(filePath))) {
    return false;
  }
  
  // Inclure seulement certaines extensions
  const ext = path.extname(filePath);
  return includeExtensions.includes(ext);
}

function normalizeFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    let normalizedContent = content;
    let hasChanges = false;
    
    // Appliquer les remplacements de terminologie
    Object.entries(terminologyMap).forEach(([oldTerm, newTerm]) => {
      const regex = new RegExp(`\\b${oldTerm}\\b`, 'g');
      if (regex.test(normalizedContent)) {
        normalizedContent = normalizedContent.replace(regex, newTerm);
        hasChanges = true;
      }
    });
    
    // Écrire le fichier seulement si des changements ont été faits
    if (hasChanges) {
      fs.writeFileSync(filePath, normalizedContent, 'utf8');
      console.log(`✅ Normalisé: ${filePath}`);
      return 1;
    }
    
    return 0;
  } catch (error) {
    console.error(`❌ Erreur traitement ${filePath}:`, error.message);
    return 0;
  }
}

function processDirectory(dirPath) {
  let filesProcessed = 0;
  
  try {
    const items = fs.readdirSync(dirPath);
    
    for (const item of items) {
      const fullPath = path.join(dirPath, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        // Récursion dans les sous-dossiers
        filesProcessed += processDirectory(fullPath);
      } else if (stat.isFile() && shouldProcessFile(fullPath)) {
        filesProcessed += normalizeFile(fullPath);
      }
    }
  } catch (error) {
    console.error(`❌ Erreur lecture dossier ${dirPath}:`, error.message);
  }
  
  return filesProcessed;
}

function main() {
  console.log('🔄 Normalisation Terminologique CHNeoWave - Phase 2 Catégorie D');
  console.log('📋 Règle: Respecter terminologie métier backend');
  console.log('');
  
  const startTime = Date.now();
  const srcPath = path.join(__dirname, '../src');
  
  if (!fs.existsSync(srcPath)) {
    console.error('❌ Dossier src/ non trouvé');
    process.exit(1);
  }
  
  console.log(`📁 Traitement du dossier: ${srcPath}`);
  console.log('');
  
  const filesProcessed = processDirectory(srcPath);
  const duration = Date.now() - startTime;
  
  console.log('');
  console.log('📊 Résumé de la normalisation:');
  console.log(`   • Fichiers modifiés: ${filesProcessed}`);
  console.log(`   • Durée: ${duration}ms`);
  console.log('');
  
  if (filesProcessed > 0) {
    console.log('✅ Normalisation terminologique terminée avec succès');
    console.log('🎯 Terminologie unifiée selon les standards backend CHNeoWave');
  } else {
    console.log('ℹ️  Aucune modification nécessaire - terminologie déjà normalisée');
  }
}

if (require.main === module) {
  main();
}

module.exports = { normalizeFile, processDirectory, terminologyMap };
