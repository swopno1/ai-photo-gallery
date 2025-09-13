import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET() {
  const db = getDb();
  const rows = db.prepare(`
    SELECT event as name, COUNT(*) as count, MIN(path) as cover
    FROM photos
    GROUP BY event
    ORDER BY date_taken DESC
  `).all();

  return NextResponse.json(rows);
}
