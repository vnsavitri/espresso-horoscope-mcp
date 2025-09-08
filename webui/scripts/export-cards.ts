#!/usr/bin/env tsx

import { chromium, Browser, Page } from '@playwright/test';
import { promises as fs } from 'fs';
import path from 'path';

interface CardData {
  shot_id: string;
  emoji: string;
  title: string;
  mantra: string;
  snapshot: {
    ratio: string;
    time: string;
    peak: string;
    temp: string;
    channel: string;
  };
  advice: string[];
  flavour_line: string;
}

interface ExportOptions {
  format?: 'portrait' | 'og';
  outputDir?: string;
  quality?: number;
}

async function fetchCards(): Promise<CardData[]> {
  try {
    const response = await fetch('http://127.0.0.1:8000/cards.json');
    if (!response.ok) {
      throw new Error(`Failed to fetch cards: ${response.status} ${response.statusText}`);
    }
    const data = await response.json();
    
    // Handle the actual API response structure
    if (data.readings && Array.isArray(data.readings)) {
      return data.readings.map((reading: any) => ({
        shot_id: reading.shot_id,
        emoji: reading.card.emoji,
        title: reading.card.title,
        mantra: reading.card.mantra,
        snapshot: {
          ratio: `${reading.card.snapshot.brew_ratio.toFixed(2)}:1`,
          time: `${reading.card.snapshot.shot_time.toFixed(0)}s`,
          peak: `${reading.card.snapshot.peak_pressure.toFixed(1)} bar`,
          temp: `${reading.card.snapshot.temp_avg.toFixed(1)}°C`,
          channel: reading.card.snapshot.channeling.toFixed(2)
        },
        advice: reading.card.advice,
        flavour_line: reading.card.flavour_line
      }));
    }
    
    // Fallback for direct array format
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('❌ Error fetching cards:', error);
    throw error;
  }
}

async function exportCard(
  browser: Browser,
  cardIndex: number,
  options: ExportOptions
): Promise<void> {
  const { format = 'portrait', outputDir = 'share', quality = 90 } = options;
  
  const viewport = format === 'og' 
    ? { width: 1200, height: 630 }
    : { width: 768, height: 1024 };
  
  const filename = format === 'og' 
    ? `card_${cardIndex}_og`
    : `card_${cardIndex}`;
  
  const url = format === 'og'
    ? `http://localhost:3000/share/${cardIndex}?format=og`
    : `http://localhost:3000/share/${cardIndex}`;

  console.log(`📸 Exporting card ${cardIndex} (${format})...`);
  
  const page = await browser.newPage();
  
  try {
    // Set viewport
    await page.setViewportSize(viewport);
    
    // Navigate to the share page
    await page.goto(url, { waitUntil: 'networkidle' });
    
    // Wait for the card to load (look for the card content)
    await page.waitForSelector('[data-testid="share-card"], .text-center', { timeout: 10000 });
    
    // Wait a bit more for any animations or loading to complete
    await page.waitForTimeout(1000);
    
    // Ensure output directory exists
    await fs.mkdir(outputDir, { recursive: true });
    
    // Take screenshot as PNG
    const pngPath = path.join(outputDir, `${filename}.png`);
    await page.screenshot({ 
      path: pngPath,
      fullPage: false,
      clip: { x: 0, y: 0, width: viewport.width, height: viewport.height }
    });
    
    // Take screenshot as JPG with quality
    const jpgPath = path.join(outputDir, `${filename}.jpg`);
    await page.screenshot({ 
      path: jpgPath,
      type: 'jpeg',
      quality,
      fullPage: false,
      clip: { x: 0, y: 0, width: viewport.width, height: viewport.height }
    });
    
    console.log(`✅ Exported: ${pngPath} and ${jpgPath}`);
    
  } catch (error) {
    console.error(`❌ Error exporting card ${cardIndex}:`, error);
  } finally {
    await page.close();
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  // Help option
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🎨 Espresso Horoscope Card Exporter

Usage:
  npm run export:images [options]

Options:
  --format=portrait    Export in portrait format (768×1024) [default]
  --format=og          Export in OG format (1200×630)
  --help, -h           Show this help message

Examples:
  npm run export:images                    # Export all cards in portrait format
  npm run export:images -- --format=og     # Export all cards in OG format

Requirements:
  - FastAPI server running on http://127.0.0.1:8000
  - Next.js server running on http://localhost:3000
  - Cards available at /cards.json endpoint
`);
    return;
  }
  
  const formatArg = args.find(arg => arg.startsWith('--format='));
  const format = formatArg?.split('=')[1] as 'portrait' | 'og' | undefined;
  
  if (format && !['portrait', 'og'].includes(format)) {
    console.error('❌ Invalid format. Use --format=portrait or --format=og');
    console.error('💡 Run with --help for usage information');
    process.exit(1);
  }
  
  const options: ExportOptions = {
    format: format || 'portrait',
    outputDir: 'share',
    quality: 90
  };
  
  console.log(`🚀 Starting card export (${options.format} format)...`);
  console.log(`📁 Output directory: ${options.outputDir}`);
  console.log(`🎨 Viewport: ${options.format === 'og' ? '1200×630' : '768×1024'}`);
  
  try {
    // Fetch cards to get count
    const cards = await fetchCards();
    console.log(`📊 Found ${cards.length} cards to export`);
    
    if (cards.length === 0) {
      console.log('⚠️  No cards found. Make sure the FastAPI server is running and has data.');
      return;
    }
    
    // Launch browser
    const browser = await chromium.launch({ headless: true });
    
    try {
      // Export each card
      for (let i = 0; i < cards.length; i++) {
        await exportCard(browser, i, options);
      }
      
      console.log(`🎉 Successfully exported ${cards.length} cards!`);
      console.log(`📁 Check the ${options.outputDir}/ directory for your images.`);
      
    } finally {
      await browser.close();
    }
    
  } catch (error) {
    console.error('❌ Export failed:', error);
    process.exit(1);
  }
}

// Run the script
if (require.main === module) {
  main().catch(console.error);
}
