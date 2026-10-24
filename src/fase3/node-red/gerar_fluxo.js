// Gero o export importável a partir dos arquivos que mantenho no projeto.
const fs = require('fs');
const path = require('path');
const {ROOT, DEVICE} = require('./monitor');
function build({root = ROOT, device = DEVICE} = {}) {
  const tab = 'ca-flow', broker = 'ca-broker';
  const nodes = [{id:tab,type:'tab',label:'CardioIA · Monitoramento IoT',disabled:false,
    info:'Recebo telemetria simulada por MQTT, valido o contrato e separo histórico de condição atual. O consumidor Python permanece responsável pela persistência e pelo ACK.'}];
  for (const [i,kind] of ['telemetry','status','ack'].entries()) nodes.push({
    id:'ca-'+kind,type:'mqtt in',z:tab,name:{telemetry:'Leituras do ESP32',status:'Estado do dispositivo',ack:'Confirmações de gravação'}[kind],
    topic:`${root}/devices/${device}/${kind}`,qos:'1',datatype:'utf8',broker,nl:false,rap:true,rh:0,inputs:0,x:190,y:100+i*65,wires:[['ca-process']]});
  nodes.push({id:broker,type:'mqtt-broker',name:'HiveMQ · demonstração pública',broker:'broker.hivemq.com',port:'1883',clientid:'',autoConnect:true,usetls:false,protocolVersion:'4',keepalive:'30',cleansession:true,autoUnsubscribe:true});
  nodes.push({id:'ca-link',type:'status',z:tab,name:'Conexão com o broker',scope:['ca-telemetry','ca-status','ca-ack'],x:200,y:295,wires:[['ca-process']]});
  nodes.push({id:'ca-clock',type:'inject',z:tab,name:'Conferir atualização a cada segundo',props:[{p:'tick',v:'true',vt:'bool'}],repeat:'1',once:true,onceDelay:.2,x:230,y:355,wires:[['ca-process']]});
  nodes.push({id:'ca-process',type:'function',z:tab,name:'Validar, deduplicar e avaliar atualidade',outputs:1,timeout:0,noerr:0,initialize:'',finalize:'',libs:[],
    func:`const monitor = global.get('cardioia');
const state = flow.get('cardioiaState') || monitor.createState();
if (msg.status) {
  state.broker = msg.status.fill === 'green' ? 'connected' : 'disconnected';
  if (state.broker !== 'connected') state.liveAt = null;
}
else if (!msg.tick) monitor.ingest(state, msg, Date.now(), global.get('cardioiaConfig'));
const view = monitor.snapshot(state);
view.testMode = global.get('cardioiaConfig').root !== monitor.ROOT;
flow.set('cardioiaState', state);
flow.set('cardioiaView', view);
return {payload:view};`,x:590,y:200,wires:[['ca-screen']]});
  nodes.push({id:'ca-screen',type:'ui-template',z:tab,group:'ca-group',page:'',ui:'',name:'CardioIA · painel de monitoramento',order:1,width:12,height:0,head:'',format:fs.readFileSync(path.join(__dirname,'painel.vue'),'utf8'),storeOutMessages:true,passthru:false,resendOnRefresh:true,templateScope:'local',className:'cardioia-root',x:970,y:200,wires:[[]]});
  nodes.push({id:'ca-base',type:'ui-base',name:'CardioIA',path:'/dashboard',appIcon:'favorite',includeClientData:true,acceptsClientConfig:[],showPathInSidebar:false,showPageTitle:false,navigationStyle:'none',titleBarStyle:'hidden',showReconnectNotification:true,notificationDisplayTime:4,showDisconnectNotification:true,allowInstall:false});
  nodes.push({id:'ca-page',type:'ui-page',name:'Monitoramento',ui:'ca-base',path:'/monitoramento',icon:'monitor_heart',layout:'grid',theme:'ca-theme',breakpoints:[{name:'Default',px:0,cols:3},{name:'Tablet',px:576,cols:6},{name:'Desktop',px:1024,cols:12}],order:1,className:'',visible:true,disabled:false});
  nodes.push({id:'ca-group',type:'ui-group',name:'Monitoramento IoT',page:'ca-page',width:12,height:1,order:1,showTitle:false,className:'cardioia-container',visible:true,disabled:false,groupType:'default'});
  nodes.push({id:'ca-theme',type:'ui-theme',name:'CardioIA · claro',colors:{surface:'#f4f6f8',primary:'#26877b',bgPage:'#f4f6f8',groupBg:'#f4f6f8',groupOutline:'#f4f6f8'},sizes:{density:'default',pagePadding:'12px',groupGap:'0px',groupBorderRadius:'0px',widgetGap:'0px'}});
  nodes.push({id:'ca-state-http',type:'http in',z:tab,name:'Estado do painel · consulta local',url:'/cardioia/api/state',method:'get',upload:false,swaggerDoc:'',x:260,y:465,wires:[['ca-state-json']]});
  nodes.push({id:'ca-state-json',type:'function',z:tab,name:'Consultar estado sem alterar leituras',func:"msg.payload=flow.get('cardioiaView') || {}; msg.headers={'Content-Type':'application/json','Cache-Control':'no-store'}; return msg;",outputs:1,libs:[],x:620,y:465,wires:[['ca-state-response']]});
  nodes.push({id:'ca-state-response',type:'http response',z:tab,name:'Resposta JSON',statusCode:'',headers:{},x:960,y:465,wires:[]});
  return nodes;
}
if (require.main === module) {
  fs.writeFileSync(path.join(__dirname,'flows.json'),JSON.stringify(build(),null,2)+'\n');
  console.log('Gerei flows.json para importar no Node-RED.');
}
module.exports = {build};
