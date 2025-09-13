import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const SETTINGS_PATH = path.join(process.cwd(), "settings.json");

export async function GET() {
  try {
    const data = fs.existsSync(SETTINGS_PATH)
      ? JSON.parse(fs.readFileSync(SETTINGS_PATH, "utf-8"))
      : {};
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({}, { status: 500 });
  }
}

export async function POST(req: Request) {
  const body = await req.json();
  fs.writeFileSync(SETTINGS_PATH, JSON.stringify(body, null, 2));
  return NextResponse.json({ ok: true });
}
