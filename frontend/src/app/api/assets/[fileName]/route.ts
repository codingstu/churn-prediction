import { promises as fs } from "node:fs";
import path from "node:path";

import { notFound } from "next/navigation";

const FIGURES_DIR = path.resolve(process.cwd(), "..", "outputs", "figures");

export async function GET(_: Request, context: { params: Promise<{ fileName: string }> }) {
  const { fileName } = await context.params;

  if (!fileName.endsWith(".png") || fileName.includes("..") || fileName.includes("/")) {
    notFound();
  }

  const filePath = path.join(FIGURES_DIR, fileName);

  try {
    const buffer = await fs.readFile(filePath);
    return new Response(buffer, {
      headers: {
        "Content-Type": "image/png",
        "Cache-Control": "no-store",
      },
    });
  } catch {
    notFound();
  }
}
