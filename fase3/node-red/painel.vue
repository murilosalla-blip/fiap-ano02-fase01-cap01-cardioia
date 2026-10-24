<template>
  <main class="cardioia" v-if="v">
    <header class="ca-header">
      <div><div class="ca-eyebrow">GRUPO AURA <span> / </span> FASE 03</div><h1>Cardio<span>IA</span></h1><p>Do sensor à informação, em tempo real.</p></div>
      <div class="ca-header-right"><span class="ca-pill" :class="v.broker === 'connected' ? 'live' : 'offline'"><i></i>{{ v.broker === 'connected' ? 'Broker MQTT conectado' : 'Broker MQTT desconectado' }}</span><small>{{v.testMode ? 'Ensaio controlado · publicador Python' : 'ESP32 · monitoramento simulado'}}</small></div>
    </header>

    <section class="ca-notice" :class="noticeClass" aria-live="polite">
      <span class="ca-notice-icon">{{ v.alerts.length ? '!' : '↗' }}</span>
      <div><strong>{{ noticeTitle }}</strong><p>{{ noticeText }}</p></div>
    </section>

    <section class="ca-metrics">
      <article :class="{'ca-values-stale':displayStale}"><span>BATIMENTOS SIMULADOS</span><strong>{{ display ? format(display.heart_rate_bpm) : '—' }}<small>BPM</small></strong><p>{{ v.current ? (v.current.pulse_count ? v.current.pulse_count + ' pulsos na última janela' : 'Sem acionamentos na janela') : display ? 'Último valor recebido · sem atualização' : 'Aguardando uma leitura' }}</p></article>
      <article><span>ÚLTIMA LEITURA RECEBIDA</span><strong>{{ v.lastSequence ? '#' + v.lastSequence : '—' }}</strong><p>{{ v.ageSeconds === null ? 'Nenhuma leitura nesta sessão' : 'Recebida há ' + v.ageSeconds + ' s' }}</p></article>
      <article><span>ÚLTIMA CONFIRMAÇÃO</span><strong>{{ v.ack ? '#' + v.ack.sequence : '—' }}</strong><p>{{ v.ack ? 'Gravação confirmada pelo consumidor' : 'Aguardando confirmação de gravação' }}</p></article>
      <article><span>PERDAS INFORMADAS</span><strong :class="{'ca-loss':v.last?.dropped_total > 0}">{{ v.last ? v.last.dropped_total : '—' }}</strong><p>{{ v.last ? 'Fila no último envio: ' + v.last.backlog_samples : 'Aguardando informação do dispositivo' }}</p></article>
    </section>

    <section class="ca-main-grid">
      <article class="ca-card ca-chart-card">
        <div class="ca-card-heading"><div><span class="ca-eyebrow">EVOLUÇÃO DA SESSÃO</span><h2>Batimentos ao longo das leituras</h2></div><span class="ca-tag">{{ v.totalInChart }} / 120 leituras</span></div>
        <div class="ca-legend"><span><i class="ca-dot orange"></i> Pulsos simulados</span><span><i class="ca-dot blue"></i> Leitura recuperada</span><span class="ca-rule-label">Limite didático: &gt; 120 BPM</span></div>
        <div class="ca-chart-wrap">
          <svg viewBox="0 0 760 270" role="img" aria-label="Gráfico de batimentos simulados por sequência, com limite didático de 120 BPM">
            <g v-for="level in [0,1,2,3,4]" :key="level"><line x1="48" x2="740" :y1="230-level*48" :y2="230-level*48" stroke="#e5eaf0"/><text x="37" :y="234-level*48" text-anchor="end" class="ca-axis">{{ Math.round(maxBpm*level/4) }}</text></g>
            <line x1="48" x2="740" :y1="y(120)" :y2="y(120)" stroke="#c96464" stroke-dasharray="6 6"/>
            <polyline v-if="v.history.length" :points="points" fill="none" stroke="#e7954a" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
            <circle v-for="(p,i) in v.history" :key="p.sequence" :cx="x(i)" :cy="y(p.bpm)" :r="v.history.length < 30 ? 4 : 2.5" :fill="p.replay ? '#538ac8' : '#e7954a'"><title>Leitura {{p.sequence}} · {{format(p.bpm)}} BPM · {{p.replay ? 'recuperada' : 'atual no recebimento'}}</title></circle>
            <text x="48" y="254" class="ca-axis">{{v.history.length ? '#' + v.history[0].sequence : 'Aguardando dados'}}</text><text x="740" y="254" text-anchor="end" class="ca-axis">{{v.history.length ? '#' + v.history[v.history.length-1].sequence : ''}}</text>
            <text v-if="!v.history.length" x="394" y="126" text-anchor="middle" class="ca-chart-empty">As leituras aparecerão aqui</text>
          </svg>
        </div>
        <p v-if="noPulses" class="ca-zero-note">Registrei {{v.history.length}} leituras com 0 BPM. Acione e solte o botão verde do Wokwi para registrar pulsos.</p>
        <p class="ca-footnote">Eixo horizontal: sequência de coleta. Passe o mouse sobre os pontos para consultar cada leitura.</p>
      </article>

      <article class="ca-card ca-gauge-card" :class="{'ca-values-stale':displayStale}">
        <div class="ca-card-heading"><div><span class="ca-eyebrow">SENSOR DHT22</span><h2>Temperatura ambiente</h2></div></div>
        <svg viewBox="0 0 300 190" role="img" :aria-label="displayTempKnown ? (displayStale ? 'Última temperatura recebida: ' : 'Temperatura ambiente atual: ') + format(display.temperature_c) + ' graus Celsius' : 'Temperatura indisponível'">
          <path d="M 40 145 A 110 110 0 0 1 260 145" fill="none" stroke="#e9eef0" stroke-width="17" stroke-linecap="round"/>
          <path v-if="displayTempKnown" d="M 40 145 A 110 110 0 0 1 260 145" fill="none" :stroke="displayStale ? '#9baab5' : display.temperature_c > 30 ? '#c35957' : '#26877b'" stroke-width="17" stroke-linecap="round" :stroke-dasharray="gaugeLength + ' 346'"/>
          <text x="150" y="126" text-anchor="middle" class="ca-gauge-value">{{displayTempKnown ? format(display.temperature_c) : '—'}}</text><text x="150" y="152" text-anchor="middle" class="ca-gauge-unit">°C</text>
          <text x="35" y="181" class="ca-axis">−40</text><text x="267" y="181" text-anchor="end" class="ca-axis">80</text>
        </svg>
        <div class="ca-sensor-status"><i class="ca-dot" :class="displayTempKnown && !displayStale ? 'green' : 'gray'"></i>{{displayTempKnown ? (displayStale ? 'Último valor recebido · sem atualização' : 'Leitura atual válida') : 'Temperatura indisponível'}}</div>
        <div class="ca-gauge-meta"><span>Umidade <b>{{displayTempKnown ? format(display.humidity_pct) + '%' : '—'}}</b></span><span>Alerta didático <b>&gt; 30 °C</b></span></div>
        <p class="ca-footnote">Temperatura do ambiente simulado, sem interpretação de temperatura corporal.</p>
      </article>
    </section>

    <section class="ca-bottom-grid">
      <article class="ca-card"><div class="ca-card-heading"><div><span class="ca-eyebrow">DADOS RECEBIDOS</span><h2>Últimas leituras</h2></div></div><div class="ca-table-scroll"><table><thead><tr><th>Leitura</th><th>BPM</th><th>Ambiente</th><th>Idade no envio</th><th>Recebimento</th></tr></thead><tbody><tr v-for="p in recent" :key="p.sequence"><td>#{{p.sequence}}</td><td>{{format(p.bpm)}}</td><td>{{p.temperature === null ? '—' : format(p.temperature) + ' °C'}}</td><td>{{Math.round(p.ageMs / 1000)}} s</td><td><span class="ca-row-type" :class="p.replay ? 'recovered' : 'live'">{{p.replay ? 'Recuperada' : 'Atual na chegada'}}</span></td></tr><tr v-if="!recent.length"><td colspan="5" class="ca-empty">Ainda não recebi leituras.</td></tr></tbody></table></div></article>
      <article class="ca-card"><div class="ca-card-heading"><div><span class="ca-eyebrow">ACOMPANHAMENTO</span><h2>Eventos do monitoramento</h2></div></div><ol class="ca-events"><li v-for="(e,i) in v.events" :key="i"><i class="ca-dot" :class="e.kind === 'alert' ? 'red' : 'green'"></i><div><p>{{e.text}}</p><time>{{time(e.at)}}</time></div></li><li v-if="!v.events.length" class="ca-empty">Os eventos aparecerão com as primeiras leituras.</li></ol><div class="ca-policy"><b>Como os alertas funcionam</b><p>Confirmo a entrada e a saída em duas leituras atuais consecutivas. Retorno à faixa definida: até 108 BPM e até 28 °C. Dados recuperados não disparam alertas atuais.</p></div></article>
    </section>
    <footer><span>CardioIA · Grupo Aura</span><span>Demonstração acadêmica · sinais simulados · sem avaliação clínica</span></footer>
  </main>
</template>
<script>
export default {
  computed: {
    v(){return this.msg?.payload || null},
    display(){return this.v.current || this.v.last || null},
    displayTempKnown(){return !!this.display?.dht_valid},
    displayStale(){return !!this.display && this.v.mode !== 'live'},
    noPulses(){return this.v.history.length > 0 && this.v.history.every(p=>p.bpm === 0)},
    modeLabel(){return {waiting:'Aguardando dados',live:'Recebendo dados atuais',recovering:'Recuperando histórico',stale:'Aguardando próxima leitura',offline:'Conexão interrompida'}[this.v.mode]},
    maxBpm(){return Math.max(180,Math.ceil(Math.max(0,...this.v.history.map(p=>p.bpm))/60)*60)},
    points(){return this.v.history.map((p,i)=>this.x(i)+','+this.y(p.bpm)).join(' ')},
    recent(){return this.v.history.slice(-7).reverse()},
    gaugeLength(){return Math.max(0,Math.min(1,(this.display.temperature_c+40)/120))*346},
    noticeClass(){return this.v.mode !== 'live' ? 'muted' : this.v.alerts.length ? 'danger' : !this.v.tempKnown || this.v.pending ? 'warning' : 'good'},
    noticeTitle(){return this.v.mode !== 'live' ? (this.v.mode === 'stale' && this.v.connection === 'online' ? 'Dispositivo conectado · aguardando próxima leitura' : this.modeLabel) : this.v.alerts.length ? this.v.alerts.join(' · ') : !this.v.tempKnown ? 'Temperatura atual indisponível' : this.v.pending ? 'Conferindo mudança nos valores' : 'Acompanhando os limites definidos'},
    noticeText(){return this.v.mode === 'recovering' ? 'Recebo leituras acumuladas no histórico. Aguardo dados atuais para avaliar os alertas.' : this.v.mode !== 'live' ? 'Mantenho o último valor recebido em cinza, com indicação de falta de atualização. Os alertas atuais aguardam uma nova leitura válida.' : this.v.alerts.length ? 'A condição foi confirmada em duas leituras consecutivas. Os limites são exclusivos desta simulação.' : !this.v.tempKnown ? 'O sensor não forneceu temperatura válida nesta leitura. O valor ausente é exibido como traço.' : 'Atualizo o acompanhamento a cada leitura. A confirmação em duas janelas evita oscilações nos alertas.'}
  },
  methods:{format(n){return Number(n).toLocaleString('pt-BR',{maximumFractionDigits:1})},x(i){return 48+i*692/Math.max(1,this.v.history.length-1)},y(n){return 230-n*192/this.maxBpm},time(n){return new Date(n).toLocaleTimeString('pt-BR')}}
}
</script>
<style>
.ca-values-stale strong{color:#798998}.ca-values-stale .ca-gauge-value{fill:#798998}.ca-zero-note{font-size:11px;color:#63798a;background:#f1f5f8;border-radius:7px;padding:9px 12px;line-height:1.6;margin:10px 0 0}

.cardioia{font-family:Inter,Segoe UI,sans-serif;color:#243649;max-width:1460px;margin:0 auto;padding:12px 8px 20px}.ca-header{display:flex;justify-content:space-between;align-items:center;margin:8px 0 26px;gap:20px}.ca-eyebrow{font-size:10px;letter-spacing:1.6px;font-weight:700;color:#7b8794}.ca-eyebrow span{margin:0 9px;color:#c4cbd1}.ca-header h1{font-size:42px;line-height:1.1;letter-spacing:-1.8px;margin:9px 0 8px;font-weight:750}.ca-header h1 span{color:#26877b}.ca-header p{color:#7b8794;font-size:13px;margin:0}.ca-header-right{display:flex;flex-direction:column;align-items:flex-end;gap:10px}.ca-header-right small{font-size:11px;color:#82909c}.ca-pill{font-size:11px;font-weight:650;border-radius:30px;padding:9px 13px;background:#e8edf1;color:#657585;display:flex;gap:8px;align-items:center}.ca-pill i{height:6px;width:6px;border-radius:50%;background:currentColor}.ca-pill.live{background:#e3f2eb;color:#25745e}.ca-pill.recovering{background:#e8f0fa;color:#4b76aa}.ca-notice{display:flex;gap:14px;padding:17px 20px;border:1px solid #dfe8e7;border-radius:12px;margin-bottom:22px;background:#edf5f2}.ca-notice-icon{width:30px;height:30px;flex-shrink:0;background:#dcece4;color:#286c57;border-radius:50%;text-align:center;line-height:30px;font-weight:700}.ca-notice strong{font-size:13px}.ca-notice p{font-size:11px;color:#637b72;margin:5px 0 0;line-height:1.6}.ca-notice.muted{background:#edf1f6;border-color:#dde4ec}.ca-notice.muted p{color:#718095}.ca-notice.danger{background:#fff0ed;border-color:#f4d4ce}.ca-notice.danger strong{color:#a14842}.ca-notice.danger .ca-notice-icon{background:#f6d6d0;color:#a14842}.ca-notice.warning{background:#fff7e7;border-color:#eadcbb}.ca-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:22px}.ca-metrics article,.ca-card{background:white;border:1px solid #e4e9ed;border-radius:14px;box-shadow:0 2px 5px #233a4810}.ca-metrics article{padding:20px}.ca-metrics article>span{font-size:9px;letter-spacing:1px;color:#85909e;font-weight:700}.ca-metrics strong{display:block;font-size:30px;font-weight:650;line-height:1.4;margin:10px 0 6px}.ca-metrics strong small{font-size:12px;color:#8b97a3;font-weight:500;margin-left:7px}.ca-metrics p{font-size:10px;color:#81909d;margin:0}.ca-loss{color:#b25b4c}.ca-main-grid{display:grid;grid-template-columns:minmax(0,2fr) minmax(260px,1fr);gap:20px;margin-bottom:20px}.ca-card{padding:22px;min-width:0}.ca-card-heading{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:18px}.ca-card h2{font-size:15px;margin:7px 0 0;font-weight:650}.ca-tag{font-size:9px;color:#788697;white-space:nowrap;background:#f4f6f8;padding:6px 9px;border-radius:6px}.ca-legend{display:flex;gap:16px;flex-wrap:wrap;font-size:10px;color:#8290a0;align-items:center}.ca-legend span{display:flex;gap:6px;align-items:center}.ca-dot{display:inline-block;width:7px;height:7px;border-radius:50%;flex-shrink:0;background:#7d8e9f}.ca-dot.orange{background:#e7954a}.ca-dot.blue{background:#538ac8}.ca-dot.green{background:#26877b}.ca-dot.gray{background:#9ba4ac}.ca-dot.red{background:#c35957}.ca-rule-label{margin-left:auto}.ca-chart-wrap{margin:12px -2px 0}.ca-chart-wrap svg{width:100%;display:block;overflow:visible}.ca-axis{font:10px Segoe UI,sans-serif;fill:#8b98a6}.ca-chart-empty{font:13px Segoe UI,sans-serif;fill:#a3afbb}.ca-footnote{font-size:10px;color:#8b97a4;line-height:1.7;margin:10px 0 0}.ca-gauge-card svg{width:100%;max-width:320px;display:block;margin:-4px auto 0}.ca-gauge-value{font:bold 40px Segoe UI,sans-serif;fill:#243649}.ca-gauge-unit{font:13px Segoe UI,sans-serif;fill:#8997a5}.ca-sensor-status{display:flex;align-items:center;justify-content:center;gap:7px;font-size:10px;color:#788a96;margin:0 0 18px}.ca-gauge-meta{display:flex;justify-content:space-between;gap:10px;border-top:1px solid #edf0f3;padding-top:15px;font-size:10px;color:#85929d}.ca-gauge-meta b{display:block;margin-top:6px;color:#405866;font-size:12px;font-weight:600}.ca-bottom-grid{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(260px,1fr);gap:20px}.ca-table-scroll{overflow-x:auto}table{width:100%;border-collapse:collapse;white-space:nowrap}th{text-align:left;font-size:9px;font-weight:600;letter-spacing:.4px;color:#92a0ab;border-bottom:1px solid #edf0f4;padding:0 8px 12px}td{font-size:11px;padding:12px 8px;border-bottom:1px solid #f0f3f6;color:#506374}tbody tr:last-child td{border-bottom:0}.ca-row-type{font-size:9px;padding:4px 7px;border-radius:5px;background:#eef6f1;color:#488674}.ca-row-type.recovered{background:#eaf0f9;color:#5f83af}.ca-events{list-style:none;padding:0;margin:0;max-height:215px;overflow:auto}.ca-events li{display:flex;gap:10px;padding:9px 0}.ca-events i{margin-top:5px}.ca-events p{font-size:11px;color:#5e7080;margin:0;line-height:1.6}.ca-events time{font-size:9px;color:#9aa5b0}.ca-policy{margin-top:15px;padding:13px;background:#f6f8fa;border-radius:8px}.ca-policy b{font-size:10px;font-weight:650;color:#64778a}.ca-policy p{font-size:10px;color:#83909d;line-height:1.7;margin:6px 0 0}.ca-empty{font-size:11px;color:#97a4b1;padding:25px 8px}.cardioia footer{display:flex;justify-content:space-between;gap:15px;padding:22px 4px 0;font-size:9px;color:#96a2ae}.nrdb-ui-group{box-shadow:none!important}.nrdb-ui-template{overflow:visible!important}@media(max-width:900px){.ca-metrics{grid-template-columns:repeat(2,1fr)}.ca-main-grid,.ca-bottom-grid{grid-template-columns:1fr}.ca-gauge-card svg{max-width:280px}}@media(max-width:500px){.ca-header{align-items:flex-start}.ca-header h1{font-size:34px}.ca-header-right small{display:none}.ca-pill{font-size:9px;padding:8px}.ca-metrics{gap:10px}.ca-metrics article,.ca-card{padding:15px}.ca-metrics article>span{font-size:8px}.ca-rule-label{margin-left:0}.cardioia footer{flex-direction:column}.ca-eyebrow{font-size:8px}}
</style>
