import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { TaskStore, type TaskStatus } from './tasks.ts';

const STATUSES: TaskStatus[] = ['todo', 'doing', 'done'];
const MAX_BODY_BYTES = 16_384;

class RequestError extends Error {
  readonly status: number;
  constructor(message: string, status = 400) {
    super(message);
    this.status = status;
  }
}

function send(res: ServerResponse, status: number, body?: unknown): void {
  res.writeHead(status, {
    'content-type': 'application/json',
    'access-control-allow-origin': '*',
    'access-control-allow-methods': 'GET,POST,PATCH,DELETE,OPTIONS',
    'access-control-allow-headers': 'content-type',
  });
  res.end(body === undefined ? undefined : JSON.stringify(body));
}

async function readJson(req: IncomingMessage): Promise<Record<string, unknown>> {
  let raw = '';
  let bytes = 0;
  for await (const chunk of req) {
    bytes += chunk.length;
    if (bytes > MAX_BODY_BYTES) throw new RequestError('body too large', 413);
    raw += chunk;
  }
  let value: unknown;
  try { value = JSON.parse(raw); }
  catch (err) {
    if (err instanceof SyntaxError) throw new RequestError('invalid JSON');
    throw err;
  }
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new RequestError('JSON body must be an object');
  }
  return value;
}

export function createApp(store = new TaskStore()) {
  async function handle(req: IncomingMessage, res: ServerResponse) {
    const url = new URL(req.url ?? '/', 'http://localhost');
    const match = url.pathname.match(/^\/tasks\/(\d+)$/);

    if (req.method === 'OPTIONS') return send(res, 204);
    if (req.method === 'GET' && url.pathname === '/health') return send(res, 200, { ok: true });
    if (req.method === 'GET' && url.pathname === '/tasks') return send(res, 200, store.list());

    if (req.method === 'POST' && url.pathname === '/tasks') {
      const body = await readJson(req);
      if (typeof body.title !== 'string' || !body.title.trim()) {
        throw new RequestError('title is required and must be a non-empty string');
      }
      return send(res, 201, store.create(body.title));
    }

    if (req.method === 'PATCH' && match) {
      const { status } = await readJson(req);
      const taskStatus = STATUSES.find(value => value === status);
      if (!taskStatus) {
        return send(res, 400, { error: 'invalid status' });
      }
      const task = store.setStatus(Number(match[1]), taskStatus);
      return task ? send(res, 200, task) : send(res, 404, { error: 'not found' });
    }

    if (req.method === 'DELETE' && match) {
      return send(res, store.remove(Number(match[1])) ? 204 : 404);
    }

    send(res, 404, { error: 'not found' });
  }
  return createServer((req, res) => {
    void handle(req, res).catch(err => {
      if (err instanceof RequestError) return send(res, err.status, { error: err.message });
      console.error('Request failed:', err);
      send(res, 500, { error: 'internal server error' });
    });
  });
}
