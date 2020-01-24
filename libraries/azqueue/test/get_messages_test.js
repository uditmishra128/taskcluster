const helper = require('./helper');
const { Schema } = require('taskcluster-lib-postgres');
const AZQueue = require('taskcluster-lib-azqueue');
const testing = require('taskcluster-lib-testing');
const path = require('path');
const assert = require('assert').strict;
const _ = require('lodash');

helper.dbSuite(path.basename(__filename), function() {
  let db;

  teardown(async function() {
    if (db) {
      try {
        await db.close();
      } finally {
        db = null;
      }
    }
  });

  const schema = Schema.fromDbDirectory(path.join(__dirname, 'db'));
  const serviceName = 'test-azqueue';

  test('get from empty queue', async function() {
    db = await helper.withDb({ schema, serviceName });
    const queue = new AZQueue({ db });

    const result = await queue.getMessages('foo', {visibilityTimeout: 10, numberOfMessages: 1});

    assert.deepEqual(result, []);
  });

  test('get from one-item queue', async function() {
    db = await helper.withDb({ schema, serviceName });
    const queue = new AZQueue({ db });

    await queue.putMessage('foo', 'bar-1', { visibilityTimeout: 0, messageTTL: 100 });
    const result = await queue.getMessages('foo', {visibilityTimeout: 10, numberOfMessages: 2});

    assert.deepEqual(result.map(({messageText}) => messageText), ['bar-1']);
  });

  test('get from multi-item queue', async function() {
    db = await helper.withDb({ schema, serviceName });
    const queue = new AZQueue({ db });

    // sleeps are long enough that the timestamps for these messages are different
    await queue.putMessage('foo', 'bar-1', { visibilityTimeout: 0, messageTTL: 100 });
    await testing.sleep(5);
    await queue.putMessage('foo', 'bar-2', { visibilityTimeout: 0, messageTTL: 100 });
    await testing.sleep(5);
    await queue.putMessage('foo', 'bar-3', { visibilityTimeout: 0, messageTTL: 100 });
    const result = await queue.getMessages('foo', {visibilityTimeout: 10, numberOfMessages: 2});

    // note that the messages returned are not in order; we want to get 1 and 2, but it
    // doesn't matter which order
    assert.deepEqual(result.map(({messageText}) => messageText).sort(), ['bar-1', 'bar-2']);
  });

  test('get skips invisible items', async function() {
    db = await helper.withDb({ schema, serviceName });
    const queue = new AZQueue({ db });

    await queue.putMessage('foo', 'bar-1', { visibilityTimeout: 10, messageTTL: 100 });
    await queue.putMessage('foo', 'bar-2', { visibilityTimeout: 0, messageTTL: 100 });
    await queue.putMessage('foo', 'bar-3', { visibilityTimeout: 10, messageTTL: 100 });
    const result = await queue.getMessages('foo', {visibilityTimeout: 10, numberOfMessages: 2});
    assert.deepEqual(result.map(({messageText}) => messageText).sort(), ['bar-2']);
  });

  test('get skips expired items', async function() {
    db = await helper.withDb({ schema, serviceName });
    const queue = new AZQueue({ db });

    await queue.putMessage('foo', 'bar-1', { visibilityTimeout: 0, messageTTL: 1 });
    await queue.putMessage('foo', 'bar-2', { visibilityTimeout: 0, messageTTL: 100 });
    await queue.putMessage('foo', 'bar-3', { visibilityTimeout: 0, messageTTL: 1 });

    // note that the TTL is in seconds, so we must wait..
    await testing.sleep(1100);

    const result = await queue.getMessages('foo', {visibilityTimeout: 10, numberOfMessages: 2});
    assert.deepEqual(result.map(({messageText}) => messageText).sort(), ['bar-2']);
  });

  test('multiple parallel gets', async function() {
    db = await helper.withDb({ schema, serviceName });
    const queue = new AZQueue({ db });

    for (let i = 0; i < 150; i++) {
      await queue.putMessage('q', `foo-${i}`, { visibilityTimeout: 0, messageTTL: 100 });
    }

    const got = [];
    await Promise.all(_.range(40).map(async () => {
      const result = await queue.getMessages('q', {visibilityTimeout: 10, numberOfMessages: 5});
      result.forEach(({messageText}) => got.push(messageText));
    }));

    // note that *crucially* this does not include any duplicates
    assert.deepEqual(got.sort(), _.range(150).map(i => `foo-${i}`).sort());
  });
});
