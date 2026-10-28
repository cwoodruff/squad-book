import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import type { AddressInfo } from 'node:net';
import { createApp } from '../src/app.ts';

const server = createApp();
let base = '';
before(() => new Promise<void>((resolve) => server.listen(0, () => {
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  resolve();
})));
after(() => { server.close(); });

const json = (method: string, body?: unknown) =>
  ({ method, headers: { 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });

test('health check', async () => {
  assert.deepEqual(await (await fetch(`${base}/health`)).json(), { ok: true });
});

test('creates and lists tasks', async () => {
  const created = await fetch(`${base}/tasks`, json('POST', { title: 'Read chapter 1' }));
  assert.equal(created.status, 201);
  assert.equal((await created.json()).status, 'todo');
  const list = await (await fetch(`${base}/tasks`)).json();
  assert.ok(list.some((t: { title: string }) => t.title === 'Read chapter 1'));
});

test('rejects empty titles', async () => {
  assert.equal((await fetch(`${base}/tasks`, json('POST', { title: '  ' }))).status, 400);
});

test('rejects malformed, non-object, and oversized input', async () => {
  for (const body of ['{', 'null', '[]', '"title"']) {
    const res = await fetch(`${base}/tasks`, {
      method: 'POST', headers: { 'content-type': 'application/json' }, body,
    });
    assert.equal(res.status, 400);
    assert.equal(typeof (await res.json()).error, 'string');
  }
  for (const title of [12, {}, null]) {
    assert.equal((await fetch(`${base}/tasks`, json('POST', { title }))).status, 400);
  }
  const large = await fetch(`${base}/tasks`, json('POST', { title: 'x'.repeat(20_000) }));
  assert.equal(large.status, 413);
});

test('updates status, validates input, and 404s on unknown ids', async () => {
  const task = await (await fetch(`${base}/tasks`, json('POST', { title: 'x' }))).json();
  const updated = await fetch(`${base}/tasks/${task.id}`, json('PATCH', { status: 'done' }));
  assert.equal((await updated.json()).status, 'done');
  assert.equal((await fetch(`${base}/tasks/999`, json('PATCH', { status: 'done' }))).status, 404);
  assert.equal((await fetch(`${base}/tasks/${task.id}`, json('PATCH', { status: 'nope' }))).status, 400);
});

test('deletes tasks', async () => {
  const task = await (await fetch(`${base}/tasks`, json('POST', { title: 'temp' }))).json();
  assert.equal((await fetch(`${base}/tasks/${task.id}`, { method: 'DELETE' })).status, 204);
  assert.equal((await fetch(`${base}/tasks/${task.id}`, { method: 'DELETE' })).status, 404);
});
