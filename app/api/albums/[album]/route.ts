import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET(req: Request, { params }: { params: { album: string } }) {
  const db = getDb();
  const rows = db.prepare(`
    SELECT id, path, date_taken
    FROM photos
    WHERE event = ?
    ORDER BY date_taken ASC
  `).all(params.album);

  return NextResponse.json(rows);
}
