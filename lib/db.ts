// import Database from "better-sqlite3";
// import path from "path";

// const DB_PATH = path.join(process.cwd(), "photos.db");

// export type Photo = {
//   id: number;
//   filename: string;
//   filepath: string;
//   date_taken: string;
//   gps: string | null;
//   faces: string | null;
//   tags: string | null;
// };

// export const getPhotos = (filters?: { tags?: string; face?: string }) => {
//   const db = new Database(DB_PATH, { readonly: true });

//   let sql = "SELECT * FROM photos WHERE is_duplicate=0";
//   const params: any[] = [];

//   if (filters?.tags) {
//     sql += " AND tags LIKE ?";
//     params.push(`%${filters.tags}%`);
//   }

//   if (filters?.face) {
//     sql += " AND faces LIKE ?";
//     params.push(`%${filters.face}%`);
//   }

//   const rows: Photo[] = db.prepare(sql).all(...params);
//   db.close();
//   return rows;
// };

import Database from "better-sqlite3";
import path from "path";

// Point this to where your SQLite DB is stored
const dbPath = path.join(process.cwd(), "python_pipeline", "photos.db");

let db: Database.Database;

export function getDb() {
  if (!db) {
    db = new Database(dbPath, { fileMustExist: true });
  }
  return db;
}
