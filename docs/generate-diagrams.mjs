#!/usr/bin/env node
/**
 * Extract Mermaid diagrams from markdown files and generate SVG images.
 * 
 * Usage: node generate-diagrams.mjs
 * 
 * Requires: @mermaid-js/mermaid-cli (mmdc) - installed in markdown2pdf-webapp
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, unlinkSync } from 'fs';
import { join, basename } from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const DOCS_DIR = __dirname;
const WEBAPP_DIR = join(DOCS_DIR, '..', 'markdown2pdf-webapp');
const DIAGRAMS_DIR = join(DOCS_DIR, 'diagrams');
const MERMAID_SOURCES_DIR = join(DIAGRAMS_DIR, 'sources');

// Ensure output directories exist
if (!existsSync(DIAGRAMS_DIR)) {
  mkdirSync(DIAGRAMS_DIR, { recursive: true });
}
if (!existsSync(MERMAID_SOURCES_DIR)) {
  mkdirSync(MERMAID_SOURCES_DIR, { recursive: true });
}

/**
 * Extract all mermaid code blocks from a markdown file
 * @param {string} filePath - Path to the markdown file
 * @returns {Array<{index: number, code: string}>} - Array of mermaid diagrams
 */
function extractMermaidBlocks(filePath) {
  const content = readFileSync(filePath, 'utf-8');
  const mermaidRegex = /```mermaid\n([\s\S]*?)```/g;
  const blocks = [];
  let match;
  let index = 0;

  while ((match = mermaidRegex.exec(content)) !== null) {
    blocks.push({
      index: index++,
      code: match[1].trim()
    });
  }

  return blocks;
}

/**
 * Generate a descriptive name from the diagram content
 * @param {string} code - Mermaid diagram code
 * @param {number} index - Index of the diagram in the file
 * @returns {string} - A descriptive name
 */
function getDiagramName(code, index) {
  // Try to extract the diagram type
  const firstLine = code.split('\n')[0].trim();
  const typeMatch = firstLine.match(/^(flowchart|sequenceDiagram|graph|classDiagram|stateDiagram|erDiagram|gantt|pie)/i);
  const type = typeMatch ? typeMatch[1].toLowerCase() : 'diagram';
  
  return `${type}-${index + 1}`;
}

/**
 * Process a single markdown file
 * @param {string} mdFile - Markdown filename
 */
function processMarkdownFile(mdFile) {
  const filePath = join(DOCS_DIR, mdFile);
  const baseName = basename(mdFile, '.md');
  const blocks = extractMermaidBlocks(filePath);

  if (blocks.length === 0) {
    console.log(`  No mermaid diagrams found in ${mdFile}`);
    return;
  }

  console.log(`  Found ${blocks.length} diagram(s) in ${mdFile}`);

  blocks.forEach((block, idx) => {
    const diagramName = getDiagramName(block.code, block.index);
    const outputName = `${baseName}-${diagramName}`;
    const mmdPath = join(MERMAID_SOURCES_DIR, `${outputName}.mmd`);
    const svgPath = join(DIAGRAMS_DIR, `${outputName}.svg`);

    // Write the .mmd source file
    writeFileSync(mmdPath, block.code);
    console.log(`    Created source: ${outputName}.mmd`);

    // Generate SVG using mmdc (run from webapp dir where mermaid-cli is installed)
    try {
      execSync(`npx mmdc -i "${mmdPath}" -o "${svgPath}" -b transparent`, {
        stdio: 'pipe',
        cwd: WEBAPP_DIR
      });
      console.log(`    Generated SVG:  ${outputName}.svg`);
    } catch (error) {
      console.error(`    Error generating ${outputName}.svg:`, error.message);
    }
  });
}

// Main execution
console.log('Generating Mermaid diagrams...\n');

// Clean up old PNG files
const existingPngs = readdirSync(DIAGRAMS_DIR).filter(f => f.endsWith('.png'));
if (existingPngs.length > 0) {
  console.log('Cleaning up old PNG files...');
  existingPngs.forEach(png => {
    unlinkSync(join(DIAGRAMS_DIR, png));
    console.log(`  Deleted: ${png}`);
  });
  console.log('');
}

// Find all markdown files in docs directory
const mdFiles = readdirSync(DOCS_DIR).filter(f => f.endsWith('.md'));

mdFiles.forEach(processMarkdownFile);

console.log('\nDone! Diagrams saved to docs/diagrams/');

