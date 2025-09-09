import { NextRequest, NextResponse } from "next/server";
import fs from "node:fs/promises";
import path from "node:path";
import sharp from "sharp";

type Payload = {
  sign: string;  // e.g. "gemini"
  signLabel: string;
  title: string;
  subtitle: string;
  metrics: {
    ratio: string;
    time: string;
    pressure: string;
    temp: string;
    rdt: string;
  };
  bullets: string[];
  message: string;
  meta: string;
  footer: string;
  format?: "png" | "svg";
};

export async function POST(request: NextRequest) {
  try {
    const data: Payload = await request.json();
    
    // Load the SVG template
    const templatePath = path.join(process.cwd(), "public/templates/card-template.svg");
    let svg = await fs.readFile(templatePath, "utf-8");
    
    // Load the sign SVG
    const signPath = path.join(process.cwd(), `public/signs/sign-${data.sign}.svg`);
    const signSvg = await fs.readFile(signPath, "utf-8");
    
    // Inject the sign SVG into the template
    svg = svg.replace(
      /<g id="signIconSlot"[^>]*>[\s\S]*?<\/g>/,
      `<g id="signIconSlot" transform="translate(319.74, 130)">${signSvg}</g>`
    );

    // helper to set text by id with inline styles
    const setText = (id: string, text: string) => {
      svg = svg.replace(
        new RegExp(`(<text[^>]*id="${id}"[^>]*>)([\\s\\S]*?)(</text>)`),
        `$1${text}$3`
      );
    };

    setText("signLabel", data.signLabel || data.sign.toUpperCase());
    setText("title", data.title);
    setText("subtitle", data.subtitle);
    setText("statRatio", data.metrics.ratio);
    setText("statTime", data.metrics.time);
    setText("statPressure", data.metrics.pressure);
    setText("statTemp", data.metrics.temp);
    setText("statEY", data.metrics.rdt);

    // Handle bullets (multiline text)
    const bulletsText = data.bullets.map(bullet => `• ${bullet}`).join('\n');
    setText("bullets", bulletsText);

    setText("narrative", data.message);
    setText("meta", data.meta);
    setText("footer", data.footer);

    // Return SVG if requested
    if (data.format === "svg") {
      return new NextResponse(svg, { headers: { "Content-Type": "image/svg+xml" } });
    }

    try {
      // Use Sharp with better configuration for text rendering
      const png = await sharp(Buffer.from(svg))
        .png({ 
          quality: 100,
          compressionLevel: 6,
          adaptiveFiltering: false,
          force: true
        })
        .toBuffer();
      
      return new NextResponse(png, { 
        headers: { 
          "Content-Type": "image/png",
          "Cache-Control": "public, max-age=3600"
        } 
      });
    } catch (error) {
      console.error("Error generating PNG:", error);
      return new NextResponse("Error generating image", { status: 500 });
    }
  } catch (error) {
    console.error("Error processing request:", error);
    return new NextResponse("Error processing request", { status: 500 });
  }
}