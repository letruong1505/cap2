import { DatabaseSync } from 'node:sqlite';
import fs from 'node:fs';
import crypto from 'node:crypto';

// Giả lập giao diện D1 bằng SQLite trong bộ nhớ để test nghiệp vụ.
export function fakeD1() {
  const sql = new DatabaseSync(':memory:');
  sql.exec(fs.readFileSync(new URL('../schema.sql', import.meta.url), 'utf8'));
  const wrap = (q, args = []) => ({
    bind: (...a) => wrap(q, a),
    first: async () => sql.prepare(q).get(...args) ?? null,
    run: async () => { const r = sql.prepare(q).run(...args); return { meta: { changes: Number(r.changes) } }; },
    all: async () => ({ results: sql.prepare(q).all(...args) }),
  });
  return { prepare: (q) => wrap(q), raw: sql };
}

export function testEnv() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('ed25519');
  return {
    env: { SIGNING_KEY_PEM: privateKey.export({ type: 'pkcs8', format: 'pem' }), SEPAY_API_KEY: 'sepay-secret', ADMIN_TOKEN: 'admin-secret' },
    publicKey,
  };
}
