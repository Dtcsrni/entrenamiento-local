(() => {
  'use strict';

  const DB_NAME = 'entrenamiento-progress';
  const DB_VERSION = 1;
  const PROGRESS_STORE = 'routineProgress';
  const SESSION_STORE = 'sessions';
  const FALLBACK_KEY = 'entrenamiento-progress-fallback-v1';
  const ROUTINES = {
    day1: { label: 'Día 1 · Espalda + Bíceps', totalExercises: 6, totalSeries: 20 },
    day2: { label: 'Día 2 · Pierna + Glúteo', totalExercises: 6, totalSeries: 20 },
    day3: { label: 'Día 3 · Pecho + Hombro + Tríceps', totalExercises: 7, totalSeries: 22 },
  };
  const LEGACY_KEYS = {
    day1: 'fitlovers-day1-series-v1',
    day2: 'fitlovers-day2-series-v1',
    day3: 'fitlovers-day3-series-v1',
  };

  let databasePromise;
  const writeQueues = new Map();

  const emit = (name, detail = {}) => {
    window.dispatchEvent(new CustomEvent(name, { detail }));
  };

  function openDatabase() {
    if (databasePromise) return databasePromise;
    if (!('indexedDB' in window)) return Promise.reject(new Error('IndexedDB no está disponible'));
    databasePromise = new Promise((resolve, reject) => {
      const request = window.indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(PROGRESS_STORE)) {
          const store = db.createObjectStore(PROGRESS_STORE, { keyPath: 'routineId' });
          store.createIndex('updatedAt', 'updatedAt');
        }
        if (!db.objectStoreNames.contains(SESSION_STORE)) {
          const store = db.createObjectStore(SESSION_STORE, { keyPath: 'sessionId' });
          store.createIndex('routineId', 'routineId');
          store.createIndex('status', 'status');
          store.createIndex('endedAt', 'endedAt');
        }
      };
      request.onsuccess = () => {
        const db = request.result;
        db.onversionchange = () => db.close();
        resolve(db);
      };
      request.onerror = () => {
        databasePromise = undefined;
        reject(request.error || new Error('No se pudo abrir IndexedDB'));
      };
      request.onblocked = () => {
        databasePromise = undefined;
        reject(new Error('IndexedDB está bloqueada por otra pestaña'));
      };
    });
    return databasePromise;
  }

  function transaction(db, stores, mode, operation) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(stores, mode);
      let result;
      try {
        result = operation(tx);
      } catch (error) {
        tx.abort();
        reject(error);
        return;
      }
      tx.oncomplete = () => resolve(result);
      tx.onerror = () => reject(tx.error || new Error('Transacción de almacenamiento fallida'));
      tx.onabort = () => reject(tx.error || new Error('Transacción de almacenamiento cancelada'));
    });
  }

  function enqueueWrite(routineId, operation) {
    const previous = writeQueues.get(routineId) || Promise.resolve();
    const next = previous.catch(() => {}).then(operation);
    writeQueues.set(routineId, next.finally(() => {
      if (writeQueues.get(routineId) === next) writeQueues.delete(routineId);
    }));
    return next;
  }

  function readFallback() {
    try {
      const value = JSON.parse(window.localStorage.getItem(FALLBACK_KEY) || '{}');
      return {
        progress: value.progress && typeof value.progress === 'object' ? value.progress : {},
        sessions: value.sessions && typeof value.sessions === 'object' ? value.sessions : {},
      };
    } catch (_) {
      return { progress: {}, sessions: {} };
    }
  }

  function writeFallback(record) {
    try {
      const fallback = readFallback();
      fallback.progress[record.routineId] = record;
      if (record.sessionId) {
        fallback.sessions[record.sessionId] = toSession(record);
      }
      window.localStorage.setItem(FALLBACK_KEY, JSON.stringify(fallback));
    } catch (error) {
      emit('training-storage-error', { error });
    }
  }

  function stateMetrics(state, routine) {
    const seriesKeys = Object.keys(state || {}).filter((key) => /^e\d+s\d+$/.test(key));
    const byExercise = new Map();
    seriesKeys.forEach((key) => {
      const exercise = key.match(/^e(\d+)s\d+$/)?.[1];
      if (!exercise) return;
      if (!byExercise.has(exercise)) byExercise.set(exercise, []);
      byExercise.get(exercise).push(state[key] === true);
    });
    const doneSeries = seriesKeys.reduce((sum, key) => sum + Number(state[key] === true), 0);
    const completedExercises = [...byExercise.values()].filter((series) => series.length > 0 && series.every(Boolean)).length;
    const timing = state && state.__timing && typeof state.__timing === 'object' ? state.__timing : {};
    const sessionStartedAt = Number.isFinite(Number(timing.sessionStartedAt)) ? Number(timing.sessionStartedAt) : 0;
    const sessionEndedAt = Number.isFinite(Number(timing.sessionEndedAt)) ? Number(timing.sessionEndedAt) : 0;
    return {
      totalExercises: routine.totalExercises,
      totalSeries: routine.totalSeries,
      doneSeries,
      completedExercises,
      sessionStartedAt,
      sessionEndedAt,
      sessionId: sessionStartedAt ? `${routine.id}:${sessionStartedAt}` : null,
    };
  }

  function normalizeSnapshot({ routineId, state, totalExercises, totalSeries }) {
    const base = ROUTINES[routineId];
    if (!base) throw new Error(`Rutina no reconocida: ${routineId}`);
    const routine = { ...base, id: routineId, totalExercises: totalExercises || base.totalExercises, totalSeries: totalSeries || base.totalSeries };
    const metrics = stateMetrics(state || {}, routine);
    return {
      routineId,
      label: routine.label,
      totalExercises: metrics.totalExercises,
      totalSeries: metrics.totalSeries,
      doneSeries: metrics.doneSeries,
      completedExercises: metrics.completedExercises,
      sessionStartedAt: metrics.sessionStartedAt,
      sessionEndedAt: metrics.sessionEndedAt,
      sessionId: metrics.sessionId,
      updatedAt: Date.now(),
    };
  }

  function toSession(record) {
    return {
      sessionId: record.sessionId,
      routineId: record.routineId,
      label: record.label,
      startedAt: record.sessionStartedAt,
      endedAt: record.sessionEndedAt || 0,
      status: record.sessionEndedAt ? 'completed' : 'active',
      completedSeries: record.doneSeries,
      completedExercises: record.completedExercises,
      totalSeries: record.totalSeries,
      updatedAt: record.updatedAt,
    };
  }

  async function capture(payload) {
    const record = normalizeSnapshot(payload);
    return enqueueWrite(record.routineId, async () => {
      try {
        const db = await openDatabase();
        await transaction(db, [PROGRESS_STORE, SESSION_STORE], 'readwrite', (tx) => {
          tx.objectStore(PROGRESS_STORE).put(record);
          if (record.sessionId) tx.objectStore(SESSION_STORE).put(toSession(record));
        });
        emit('training-progress-updated', { source: 'indexeddb', record });
        return { source: 'indexeddb', record };
      } catch (error) {
        writeFallback(record);
        emit('training-storage-error', { error, fallback: true });
        emit('training-progress-updated', { source: 'localstorage', record });
        return { source: 'localstorage', record };
      }
    });
  }

  function legacySnapshots() {
    return Object.entries(LEGACY_KEYS).flatMap(([routineId, key]) => {
      try {
        const state = JSON.parse(window.localStorage.getItem(key) || 'null');
        return state && typeof state === 'object' ? [{ routineId, state }] : [];
      } catch (_) {
        return [];
      }
    });
  }

  async function readDatabase() {
    try {
      const db = await openDatabase();
      const databaseData = await transaction(db, [PROGRESS_STORE, SESSION_STORE], 'readonly', (tx) => {
        const progressRequest = tx.objectStore(PROGRESS_STORE).getAll();
        const sessionsRequest = tx.objectStore(SESSION_STORE).getAll();
        return { progressRequest, sessionsRequest };
      }).then(({ progressRequest, sessionsRequest }) => ({
        progress: progressRequest.result || [],
        sessions: sessionsRequest.result || [],
      }));
      const fallback = readFallback();
      const progress = new Map();
      [...Object.values(fallback.progress), ...databaseData.progress].forEach((record) => {
        const current = progress.get(record.routineId);
        if (!current || (record.updatedAt || 0) >= (current.updatedAt || 0)) progress.set(record.routineId, record);
      });
      const sessions = new Map();
      [...Object.values(fallback.sessions), ...databaseData.sessions].forEach((session) => {
        const current = sessions.get(session.sessionId);
        if (!current || (session.updatedAt || 0) >= (current.updatedAt || 0)) sessions.set(session.sessionId, session);
      });
      return { progress: [...progress.values()], sessions: [...sessions.values()] };
    } catch (_) {
      const fallback = readFallback();
      return { progress: Object.values(fallback.progress), sessions: Object.values(fallback.sessions) };
    }
  }

  async function migrateLegacyProgress(data) {
    const known = new Set(data.progress.map((record) => record.routineId));
    const missing = legacySnapshots().filter(({ routineId }) => !known.has(routineId));
    if (!missing.length) return data;
    const migrated = await Promise.all(missing.map(({ routineId, state }) => capture({ routineId, state })));
    migrated.forEach(({ record }) => data.progress.push(record));
    migrated.forEach(({ record }) => {
      if (record.sessionId) data.sessions.push(toSession(record));
    });
    return data;
  }

  function dashboardFrom(data) {
    const progressByRoutine = new Map(data.progress.map((record) => [record.routineId, record]));
    const sessions = data.sessions.filter((session) => session.status === 'completed');
    const completedSeries = sessions.reduce((sum, session) => sum + session.completedSeries, 0);
    const activeSeries = data.progress.reduce((sum, record) => sum + (record.sessionEndedAt ? 0 : record.doneSeries), 0);
    const currentSeries = data.progress.reduce((sum, record) => sum + record.doneSeries, 0);
    const plannedSeries = Object.values(ROUTINES).reduce((sum, routine) => sum + routine.totalSeries, 0);
    const lastActivity = [...data.progress, ...data.sessions].reduce((latest, item) => Math.max(latest, item.updatedAt || item.endedAt || item.startedAt || 0), 0);
    return {
      plannedSeries,
      recordedSeries: completedSeries + activeSeries,
      currentSeries,
      currentPlanPercent: plannedSeries ? Math.min(100, Math.round((currentSeries / plannedSeries) * 100)) : 0,
      sessionsStarted: new Set(data.sessions.map((session) => session.sessionId)).size,
      sessionsCompleted: sessions.length,
      lastActivity,
      routines: Object.entries(ROUTINES).map(([routineId, routine]) => {
        const record = progressByRoutine.get(routineId);
        return {
          routineId,
          label: routine.label,
          totalExercises: routine.totalExercises,
          totalSeries: routine.totalSeries,
          doneSeries: record?.doneSeries || 0,
          completedExercises: record?.completedExercises || 0,
          percent: record ? Math.min(100, Math.round((record.doneSeries / routine.totalSeries) * 100)) : 0,
        };
      }),
    };
  }

  async function getDashboard() {
    const data = await migrateLegacyProgress(await readDatabase());
    return dashboardFrom(data);
  }

  async function requestPersistence() {
    if (!navigator.storage?.persist) return false;
    try {
      return await navigator.storage.persist();
    } catch (_) {
      return false;
    }
  }

  async function storageStatus() {
    const persistent = navigator.storage?.persisted ? await navigator.storage.persisted().catch(() => false) : false;
    return { indexedDB: 'indexedDB' in window, persistent };
  }

  window.TrainingProgressStore = Object.freeze({ capture, getDashboard, requestPersistence, storageStatus });
})();
