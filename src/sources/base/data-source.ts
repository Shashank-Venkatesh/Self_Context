export interface SyncResult {
  fetched: number;
  insertedOrUpdated: number;
  duplicatesSkipped: number;
  cursor: string | null;
}

export interface DataSource {
  readonly source: string;
  readonly provider: string;
  sync(): Promise<SyncResult>;
}
