// Centralizo as regras do painel e as testo sem depender da interface.
const path = require('path');
const Ajv = require(require.resolve('ajv/dist/2020', {
  paths: [__dirname, path.resolve(__dirname, '../../../fase3/node-red')]
}));
const schema = require('../../../config/fase3/contratos/telemetria.schema.json');
const validate = new Ajv({strict: false}).compile(schema);
const DEVICE = 'cardioia-esp32-01';
const ROOT = 'cardioia/aura/fase3/478054573982428161/v1';
const STALE_MS = 15000;
const HISTORY = 120;
const rules = {pulse: {enter: 120, exit: 108}, temperature: {enter: 30, exit: 28}};

function createState() {
  return {session: null, retired: [], lastSequence: 0, last: null, lastAt: null,
    liveAt: null, live: null, status: null, broker: 'connecting', ack: null,
    history: [], events: [], rejected: 0, duplicates: 0,
    rules: {pulse: {active: false, count: 0}, temperature: {active: false, count: 0}}};
}
function event(s, now, kind, text) {
  s.events.unshift({at: now, kind, text});
  s.events = s.events.slice(0, 12);
}
function reject(s, reason) { s.rejected++; return {accepted: false, reason}; }
function applyRule(s, key, value, now) {
  const r = s.rules[key], limit = rules[key];
  if (value === null) {r.count = 0; return;}
  const transition = r.active ? value <= limit.exit : value > limit.enter;
  r.count = transition ? r.count + 1 : 0;
  if (r.count >= 2) {
    r.active = !r.active; r.count = 0;
    event(s, now, r.active ? 'alert' : 'resolved',
      (key === 'pulse' ? 'Pulsos simulados' : 'Temperatura ambiente') +
      (r.active ? ': limite didático ultrapassado.' : ': retorno à faixa definida.'));
  }
}
function ingest(s, message, now = Date.now(), config = {}) {
  const root = config.root || ROOT, device = config.device || DEVICE;
  const prefix = `${root}/devices/${device}/`;
  if (!message.topic || !message.topic.startsWith(prefix)) return reject(s, 'topico');
  let data;
  try {
    const raw = Buffer.isBuffer(message.payload) ? message.payload.toString('utf8') : message.payload;
    if (typeof raw === 'string' && Buffer.byteLength(raw) > 2048) return reject(s, 'tamanho');
    data = typeof raw === 'string' ? JSON.parse(raw) : raw;
  } catch (_) { return reject(s, 'json'); }
  if (!data || typeof data !== 'object' || Array.isArray(data) || data.device_id !== device) return reject(s, 'dispositivo');
  const kind = message.topic.slice(prefix.length);
  if (kind === 'status') {
    if (!/^[a-f0-9]{16}$/.test(data.session_id) || data.simulated !== true ||
        !['online', 'offline_simulated', 'offline_unexpected', 'broker_fault_test'].includes(data.state)) return reject(s, 'status');
    if (!s.session || s.session === data.session_id) {
      s.status = {state: data.state, session: data.session_id};
      if (data.state !== 'online') {
        s.liveAt = null;
        s.rules.pulse.count = 0; s.rules.temperature.count = 0;
      }
    }
    return {accepted: true};
  }
  if (kind === 'ack') {
    if (message.retain || data.schema_version !== 1 || data.status !== 'stored' ||
        !Number.isInteger(data.sequence) || data.sequence < 1 || data.sequence > 4294967295 ||
        data.session_id !== s.session || data.sequence > s.lastSequence) return reject(s, 'ack');
    if (!s.ack || data.sequence > s.ack.sequence) s.ack = {sequence: data.sequence, at: now};
    return {accepted: true};
  }
  if (kind !== 'telemetry' || message.retain || !validate(data) || data.transport !== 'mqtt') return reject(s, 'contrato');
  if (data.sent_uptime_ms - data.collected_uptime_ms !== data.age_ms || data.age_ms < 0 ||
      data.replay !== (data.age_ms > 10000) || !Number.isFinite(data.heart_rate_bpm) ||
      Math.abs(data.heart_rate_bpm - data.pulse_count * 60000 / data.window_ms) > .011) return reject(s, 'coerencia');
  if (s.retired.includes(data.session_id)) return reject(s, 'sessao_antiga');
  if (s.session !== data.session_id) {
    if (s.session) s.retired = [...s.retired, s.session].slice(-16);
    s.session = data.session_id; s.lastSequence = 0; s.history = [];
    s.liveAt = null; s.live = null; s.ack = null;
    s.rules = {pulse: {active: false, count: 0}, temperature: {active: false, count: 0}};
    if (s.status?.session !== s.session) s.status = null;
    event(s, now, 'info', 'Iniciei o acompanhamento de uma nova sessão.');
  }
  if (data.sequence <= s.lastSequence) {s.duplicates++; return {accepted: false, reason: 'repetida_ou_antiga'};}
  s.lastSequence = data.sequence; s.lastAt = now; s.last = data;
  const live = data.age_ms <= 10000 && data.backlog_samples === 1;
  s.history.push({sequence: data.sequence, bpm: data.heart_rate_bpm,
    temperature: data.temperature_c, replay: !live, receivedAt: now, ageMs: data.age_ms});
  s.history = s.history.slice(-HISTORY);
  if (live) {
    // Confiro janelas consecutivas no relógio do dispositivo. Não confundo
    // lentidão do simulador com uma janela perdida ou desconexão explícita.
    const previous = s.live;
    if (s.liveAt === null || !previous || data.sequence !== previous.sequence + 1 ||
        data.collected_uptime_ms - previous.collected_uptime_ms > Math.max(previous.window_ms, data.window_ms) * 1.5) {
      s.rules.pulse.count = 0; s.rules.temperature.count = 0;
    }
    s.liveAt = now; s.live = data;
    applyRule(s, 'pulse', data.heart_rate_bpm, now);
    applyRule(s, 'temperature', data.dht_valid ? data.temperature_c : null, now);
  } else {
    s.rules.pulse.count = 0; s.rules.temperature.count = 0;
  }
  return {accepted: true, live};
}
function snapshot(s, now = Date.now()) {
  const status = s.status?.state;
  const blocked = status && status !== 'online';
  const fresh = s.liveAt !== null && now - s.liveAt <= STALE_MS && !blocked && s.broker === 'connected';
  const recovering = !blocked && s.last && now - s.lastAt <= STALE_MS && (s.last.replay || s.last.backlog_samples > 1);
  let mode = !s.last ? 'waiting' : fresh && !recovering ? 'live' : recovering ? 'recovering' : 'stale';
  if (blocked || s.broker !== 'connected') mode = s.last ? 'offline' : 'waiting';
  const current = mode === 'live' ? s.live : null;
  const tempKnown = !!current?.dht_valid;
  const alerts = [];
  if (current && s.rules.pulse.active) alerts.push('Pulsos acima do limite didático');
  if (tempKnown && s.rules.temperature.active) alerts.push('Temperatura ambiente acima do limite didático');
  const pending = Object.values(s.rules).some(r => r.count > 0);
  const connection = s.broker !== 'connected' ? 'broker_offline' : blocked ? 'device_offline' : status === 'online' ? 'online' : 'unknown';
  return {mode, connection, broker: s.broker, status: status || 'unknown', session: s.session,
    current, tempKnown, alerts, pending, history: s.history, events: s.events,
    last: s.last, lastSequence: s.lastSequence, ack: s.ack,
    ageSeconds: s.lastAt === null ? null : Math.max(0, Math.floor((now - s.lastAt) / 1000)),
    liveAgeSeconds: s.liveAt === null ? null : Math.max(0, Math.floor((now - s.liveAt) / 1000)),
    rejected: s.rejected, duplicates: s.duplicates,
    totalInChart: s.history.length,
    rules: {pulseEnter: 120, pulseExit: 108, tempEnter: 30, tempExit: 28, consecutive: 2},
    generatedAt: now};
}
module.exports = {createState, ingest, snapshot, STALE_MS, HISTORY, ROOT, DEVICE};
