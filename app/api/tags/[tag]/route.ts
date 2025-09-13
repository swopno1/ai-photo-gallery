import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET(req: Request, { params }: { params: { tag: string } }) {
  const db = getDb();
  const rows = db.prepare(`
    SELECT id, path, date_taken
    FROM photos
    WHERE tags LIKE ?
    ORDER BY date_taken ASC
  `).all(`%${params.tag}%`);

  return NextResponse.json(rows);
}
