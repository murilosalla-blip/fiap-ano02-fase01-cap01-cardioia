// Inicio uma instância local, mantendo os arquivos de execução fora do Git.
const fs = require('fs');
const path = require('path');
const {spawn} = require('child_process');
const root = path.resolve(__dirname,'../..');
const source = path.join(root,'src/fase3/node-red');
const nodeRedPackage = require.resolve('node-red/package.json',{paths:[source]});
const installedModules = path.dirname(path.dirname(nodeRedPackage));
const {build} = require(path.join(source,'gerar_fluxo'));
const port = Number(process.env.CARDIOIA_PORT || 1880);
if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('Porta local inválida.');
const runtime = path.join(root,'.tools/runtime/fase3',port === 1880 ? 'node-red' : `node-red-${port}`);
fs.mkdirSync(runtime,{recursive:true});
const modules = path.join(runtime,'node_modules');
if (!fs.existsSync(modules)) fs.symlinkSync(installedModules,modules,process.platform === 'win32' ? 'junction' : 'dir');
fs.writeFileSync(path.join(runtime,'flows.json'),JSON.stringify(build({
  root:process.env.CARDIOIA_TOPIC_ROOT,
  device:process.env.CARDIOIA_DEVICE_ID
}),null,2)+'\n');
const cli = path.join(path.dirname(nodeRedPackage),'red.js');
if (process.argv.includes('--com-consumidor') && process.env.CARDIOIA_TOPIC_ROOT) throw new Error('Uso o consumidor integrado apenas no tópico principal.');
const child = spawn(process.execPath,[cli,'--userDir',runtime,'--settings',path.join(root,'config/fase3/node-red/settings.js')],{stdio:'inherit',windowsHide:true,cwd:source,env:{...process.env,CARDIOIA_RUNTIME_DIR:runtime}});
let consumer;
if (process.argv.includes('--com-consumidor')) {
  const log = fs.openSync(path.join(runtime,'consumidor.log'),'a');
  const localModules = path.join(root,'.tools/python-mqtt');
  const pythonPath = [localModules,process.env.PYTHONPATH].filter(Boolean).join(path.delimiter);
  consumer = spawn(process.env.CARDIOIA_PYTHON || 'python',['-u',path.join(root,'src/fase3/python/consumidor_mqtt.py')],
    {env:{...process.env,PYTHONPATH:pythonPath},stdio:['ignore',log,log],windowsHide:true});
  fs.closeSync(log);
  console.log('Inicio também o consumidor. Registro seus eventos em .tools/runtime/fase3/node-red/consumidor.log.');
  consumer.on('error',error=>console.error('Não consegui iniciar o consumidor: '+error.message));
  consumer.on('exit',code=>{if(code)console.error('O consumidor encerrou com erro. Confiro o arquivo consumidor.log.');});
}
console.log('Painel: http://127.0.0.1:'+(process.env.CARDIOIA_PORT || 1880)+'/dashboard/monitoramento');
console.log('Mantenho esta janela aberta. Para encerrar, pressiono Ctrl+C.');
process.on('SIGINT',()=>{child.kill('SIGINT');if(consumer)consumer.kill('SIGINT');});
process.on('SIGTERM',()=>{child.kill('SIGTERM');if(consumer)consumer.kill('SIGTERM');});
child.on('error',error=>{console.error(error.message);process.exitCode=1;});
child.on('exit',code=>{if(consumer)consumer.kill('SIGTERM');process.exitCode=code || 0;});
