#!/usr/bin/env node

const testPayload = {
  sign: "aries",
  signLabel: "ARIES",
  title: "Celestial Perfection",
  subtitle: "Cosmic equilibrium found.",
  metrics: {
    ratio: "2.10:1",
    time: "28s",
    pressure: "8.4 bar",
    temp: "91.8 °C",
    rdt: "0.00"
  },
  bullets: [
    "Excellent shot parameters!",
    "Maintain current grid setting",
    "Keep consistent puck preparation"
  ],
  message: "Your Aries energy transcends through this peaceful supernova, creating cosmic harmony in every drop.",
  meta: "seed: b99addb6 • rule: sweet_spot • severity: perfect",
  footer: "Espresso Horoscope",
  format: "svg"
};

async function testAPI() {
  try {
    console.log("🧪 Testing card API...");
    
    const response = await fetch("http://localhost:3000/api/card", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(testPayload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const buffer = await response.arrayBuffer();
    console.log(`✅ Success! Generated ${buffer.byteLength} bytes`);
    console.log(`📊 Content-Type: ${response.headers.get("content-type")}`);
    
    // Save test image
    const fs = require('fs');
    const filename = testPayload.format === 'svg' ? 'test-card.svg' : 'test-card.png';
    fs.writeFileSync(filename, Buffer.from(buffer));
    console.log(`💾 Saved test image as ${filename}`);
    
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

testAPI();
