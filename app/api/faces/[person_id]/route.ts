import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET(req: Request, { params }: { params: { person_id: string } }) {
  const db = getDb();
  const rows = db.prepare(`
    SELECT id, path, date_taken
    FROM photos
    WHERE face_cluster = ?
    ORDER BY date_taken ASC
  `).all(params.person_id);

  return NextResponse.json(rows);
}
